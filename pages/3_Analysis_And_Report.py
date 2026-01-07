import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import f_oneway

# Import modul internal Anda
from modules.export_excel import export_multi_sheet
from modules.export_pdf import export_summary_pdf
from modules.kpi_metrics import calculate_kpis, validation_summary
from modules.kpi_visuals import show_kpi_metrics, plot_inventory_profile

# ==========================================================
# CONFIG & STYLING
# ==========================================================
st.set_page_config(
    page_title="Analisis & Validasi",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS untuk efek Card
st.markdown("""
    <style>
    .stMetric {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border: 1px solid #f0f2f6;
    }
    div[data-testid="stExpander"] {
        border: none;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_html=True)

# ==========================================================
# HEADER SECTION
# ==========================================================
col_title, col_logo = st.columns([4, 1])
with col_title:
    st.title("📊 Analisis dan Validasi")
    st.caption("Dashboard Evaluasi Sistem Fuzzy Logic & Dynamic Programming")

# ==========================================================
# LOAD DATA
# ==========================================================
if "fuzzy_result" not in st.session_state or "dp_result" not in st.session_state:
    st.error("🚨 **Data Tidak Ditemukan!** Silakan jalankan simulasi di halaman sebelumnya.")
    st.stop()

df_fuzzy = st.session_state["fuzzy_result"]
df_dp = st.session_state["dp_result"]

# ==========================================================
# KPI METRICS (CARD VIEW)
# ==========================================================
st.subheader("📌 Ringkasan Eksekutif")
total_fuzzy_import = df_fuzzy["Prediksi_Impor_Fuzzy"].sum()
total_dp_import = df_dp["Impor_Optimal"].sum()
total_cost = df_dp["Total_Cost"].sum()

m1, m2, m3 = st.columns(3)
with m1:
    st.metric("Total Impor (Fuzzy)", f"{int(total_fuzzy_import):,}", help="Akumulasi prediksi impor dari sistem Fuzzy")
with m2:
    st.metric("Total Impor (DP)", f"{int(total_dp_import):,}", delta=f"{int(total_dp_import - total_fuzzy_import):,}", delta_color="inverse")
with m3:
    st.metric("Total Biaya Sistem", f"Rp {int(total_cost):,}", help="Total biaya operasional (Import + Holding)")

st.divider()

# ==========================================================
# VISUALISASI UTAMA
# ==========================================================
c1, c2 = st.columns(2)

with c1:
    st.subheader("📈 Profil Inventori")
    # Menggunakan fungsi bawaan Anda
    plot_inventory_profile(df_dp)

with c2:
    st.subheader("📈 Perbandingan Impor")
    fig, ax = plt.subplots()
    ax.plot(df_fuzzy["Month"].astype(str), df_fuzzy["Prediksi_Impor_Fuzzy"], marker="o", ls='--', label="Fuzzy", color='#1f77b4')
    ax.plot(df_dp["Month"], df_dp["Impor_Optimal"], marker="s", label="DP (Optimal)", color='#ff7f0e')
    ax.set_ylabel("Jumlah Unit")
    ax.legend()
    st.pyplot(fig)

# ==========================================================
# VALIDASI STATISTIK
# ==========================================================
st.subheader("🧪 Uji Validasi & Statistik")
tab1, tab2, tab3 = st.tabs(["📊 Tabel Validasi", "📉 Analisis Error", "🔬 Uji ANOVA"])

with tab1:
    df_validation = validation_summary(
        actual=df_dp["Demand"].values,
        fuzzy=df_fuzzy["Prediksi_Impor_Fuzzy"].values,
        baseline=df_dp["Impor_Optimal"].values
    )
    st.dataframe(df_validation, use_container_width=True)

with tab2:
    errors_fuzzy = np.abs(df_dp["Demand"] - df_fuzzy["Prediksi_Impor_Fuzzy"])
    errors_dp = np.abs(df_dp["Demand"] - df_dp["Impor_Optimal"])
    
    fig3, ax3 = plt.subplots(figsize=(10, 4))
    x = np.arange(len(df_dp))
    ax3.bar(x - 0.2, errors_fuzzy, 0.4, label="Error Fuzzy", color='#a6cee3')
    ax3.bar(x + 0.2, errors_dp, 0.4, label="Error DP", color='#fb9a99')
    ax3.set_xticks(x)
    ax3.set_xticklabels(df_dp["Month"], rotation=45)
    ax3.legend()
    st.pyplot(fig3)

with tab3:
    anova_stat, anova_p = f_oneway(
        df_fuzzy["Prediksi_Impor_Fuzzy"].values,
        df_dp["Impor_Optimal"].values,
        df_dp["Demand"].values
    )
    
    col_a, col_b = st.columns(2)
    col_a.info(f"**F-Statistic:** {anova_stat:.4f}")
    
    status = "Signifikan" if anova_p < 0.05 else "Tidak Signifikan"
    color = "green" if anova_p >= 0.05 else "red" # P > 0.05 berarti tidak ada perbedaan nyata (bagus)
    
    col_b.markdown(f"""
    **P-Value:** {anova_p:.4f}  
    **Hasil:** <span style='color:{color}; font-weight:bold;'>{status}</span> (α=0.05)
    """, unsafe_allow_html=True)

# ==========================================================
# DATA DETAIL & EXPORT
# ==========================================================
with st.expander("📄 Lihat Detail Data Bulanan"):
    df_analysis = pd.DataFrame({
        "Bulan": df_fuzzy["Month"].astype(str),
        "Demand": df_dp["Demand"],
        "Stok Awal": df_dp["Stok_Awal"],
        "Impor (Fuzzy)": df_fuzzy["Prediksi_Impor_Fuzzy"],
        "Impor (DP)": df_dp["Impor_Optimal"],
        "Stok Akhir": df_dp["Stok_Akhir"],
        "Biaya Total": df_dp["Total_Cost"]
    })
    st.dataframe(df_analysis, use_container_width=True)

st.subheader("⬇️ Unduh Laporan")
d1, d2, _ = st.columns([1, 1, 2])

# Logika ekspor tetap sama seperti kode Anda
with d1:
    excel_buffer = export_multi_sheet({"Final_Analysis": df_analysis, "Validation": df_validation})
    st.download_button("📂 Simpan ke Excel", data=excel_buffer, file_name="Laporan.xlsx", use_container_width=True)

with d2:
    pdf_buffer = export_summary_pdf(title="Laporan Akhir", metrics={"Cost": total_cost}, conclusion="Optimal.")
    st.download_button("📄 Simpan ke PDF", data=pdf_buffer, file_name="Laporan.pdf", use_container_width=True)
