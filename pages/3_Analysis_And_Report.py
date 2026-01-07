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
# 1. CONFIG & STYLING
# ==========================================================
st.set_page_config(
    page_title="Analisis & Validasi",
    page_icon="📊",
    layout="wide"
)

# Custom CSS untuk membuat tampilan "Card" pada Metric
st.markdown("""
    <style>
    /* Mengatur style kartu untuk metric */
    div[data-testid="stMetric"] {
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        padding: 15px 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
    }
    /* Memberikan warna khusus pada label metric */
    label[data-testid="stMetricLabel"] {
        font-weight: bold;
        color: #555;
    }
    /* Mempercantik header tab */
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# ==========================================================
# 2. HEADER
# ==========================================================
st.title("📊 Analisis dan Validasi")
st.markdown("""
Halaman ini menyajikan **analisis hasil sistem fuzzy dan dynamic programming (DP)**, 
visualisasi perbandingan, serta validasi statistik untuk mendukung pengambilan keputusan.
""")
st.divider()

# ==========================================================
# 3. LOAD DATA
# ==========================================================
if "fuzzy_result" not in st.session_state or "dp_result" not in st.session_state:
    st.error("🚨 **Data Tidak Ditemukan!** Silakan jalankan simulasi di halaman 1 (Fuzzy) dan halaman 2 (DP) terlebih dahulu.")
    st.stop()

df_fuzzy = st.session_state["fuzzy_result"]
df_dp = st.session_state["dp_result"]

# ==========================================================
# 4. KPI DASHBOARD (CARD SECTION)
# ==========================================================
st.subheader("📌 Key Performance Indicators (KPI)")

# Hitung data untuk KPI
total_fuzzy_import = df_fuzzy["Prediksi_Impor_Fuzzy"].sum()
total_dp_import = df_dp["Impor_Optimal"].sum()
total_cost = df_dp["Total_Cost"].sum()
avg_demand = df_dp["Demand"].mean()

# Tampilkan dalam 4 kolom kartu
k1, k2, k3, k4 = st.columns(4)

with k1:
    st.metric("Total Impor (Fuzzy)", f"{int(total_fuzzy_import):,}")
with k2:
    st.metric("Total Impor (DP)", f"{int(total_dp_import):,}", 
              delta=f"{int(total_dp_import - total_fuzzy_import):,} diff")
with k3:
    st.metric("Total Biaya Sistem", f"Rp {int(total_cost):,}")
with k4:
    st.metric("Rata-rata Demand", f"{int(avg_demand):,}")

st.markdown("<br>", unsafe_allow_html=True)

# ==========================================================
# 5. VISUALISASI UTAMA
# ==========================================================
col_graph1, col_graph2 = st.columns(2)

with col_graph1:
    st.subheader("📈 Profil Inventori")
    # Memanggil fungsi plot dari modul kpi_visuals
    plot_inventory_profile(df_dp)

with col_graph2:
    st.subheader("📈 Perbandingan Impor")
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(df_fuzzy["Month"].astype(str), df_fuzzy["Prediksi_Impor_Fuzzy"], 
            marker="o", label="Impor Fuzzy", color="#1f77b4", linewidth=2)
    ax.plot(df_dp["Month"], df_dp["Impor_Optimal"], 
            marker="s", label="Impor DP", color="#ff7f0e", linewidth=2)
    ax.set_xlabel("Bulan")
    ax.set_ylabel("Jumlah Unit")
    ax.legend()
    ax.grid(True, alpha=0.3)
    st.pyplot(fig)

# ==========================================================
# 6. ANALISIS DETAIL & STATISTIK (TABS)
# ==========================================================
st.divider()
st.subheader("🧪 Detail Analisis & Validasi")

tab_data, tab_stat, tab_error = st.tabs(["📄 Tabel Analisis", "🔬 Uji Statistik", "📊 Analisis Error"])

with tab_data:
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

with tab_stat:
    col_a, col_b = st.columns([1, 2])
    
    # Hitung ANOVA
    anova_stat, anova_p = f_oneway(
        df_fuzzy["Prediksi_Impor_Fuzzy"].values,
        df_dp["Impor_Optimal"].values,
        df_dp["Demand"].values
    )
    
    with col_a:
        st.write("**Hasil Uji ANOVA**")
        st.write(f"- F-Statistic: `{anova_stat:.4f}`")
        st.write(f"- P-Value: `{anova_p:.4f}`")
        if anova_p < 0.05:
            st.error("Signifikan (Ada perbedaan nyata)")
        else:
            st.success("Tidak Signifikan (Data selaras)")
            
    with col_b:
        st.write("**DM Test & Summary**")
        df_validation = validation_summary(
            actual=df_dp["Demand"].values,
            fuzzy=df_fuzzy["Prediksi_Impor_Fuzzy"].values,
            baseline=df_dp["Impor_Optimal"].values
        )
        st.dataframe(df_validation, use_container_width=True)

with tab_error:
    st.write("**Perbandingan Error Absolut (Fuzzy vs DP)**")
    errors_fuzzy = np.abs(df_dp["Demand"] - df_fuzzy["Prediksi_Impor_Fuzzy"])
    errors_dp = np.abs(df_dp["Demand"] - df_dp["Impor_Optimal"])
    
    fig_err, ax_err = plt.subplots(figsize=(10, 4))
    x = np.arange(len(df_dp))
    ax_err.bar(x - 0.2, errors_fuzzy, 0.4, label="Error Fuzzy", color='#a6cee3')
    ax_err.bar(x + 0.2, errors_dp, 0.4, label="Error DP", color='#fb9a99')
    ax_err.set_xticks(x)
    ax_err.set_xticklabels(df_dp["Month"], rotation=45)
    ax_err.legend()
    st.pyplot(fig_err)

# ==========================================================
# 7. DOWNLOAD LAPORAN
# ==========================================================
st.divider()
st.subheader("⬇️ Unduh Laporan Resmi")

d1, d2, _ = st.columns([1, 1, 2])

with d1:
    excel_buffer = export_multi_sheet({
        "Fuzzy_Result": df_fuzzy,
        "DP_Result": df_dp,
        "Final_Analysis": df_analysis,
        "Validation": df_validation
    })
    st.download_button(
        label="📥 Download Excel",
        data=excel_buffer,
        file_name="Laporan_Fuzzy_DP.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True
    )

with d2:
    pdf_buffer = export_summary_pdf(
        title="Laporan Akhir Sistem Pendukung Keputusan",
        metrics={
            "Total Impor Fuzzy": f"{int(total_fuzzy_import):,}",
            "Total Impor DP": f"{int(total_dp_import):,}",
            "Total Biaya": f"Rp {int(total_cost):,}"
        },
        conclusion="Sistem berhasil mengoptimalkan stok dan biaya impor."
    )
    st.download_button(
        label="📥 Download PDF",
        data=pdf_buffer,
        file_name="Laporan_Fuzzy_DP.pdf",
        mime="application/pdf",
        use_container_width=True
    )

st.success("✅ Dashboard siap digunakan.")
