import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import f_oneway

# Import modul internal Anda
from modules.export_excel import export_multi_sheet
from modules.export_pdf import export_summary_pdf
from modules.kpi_metrics import (
    calculate_kpis,
    validation_summary
)
from modules.kpi_visuals import show_kpi_metrics, plot_inventory_profile

# ==========================================================
# 1. CONFIG & ADVANCED STYLING (Kunci Tampilan Card)
# ==========================================================
st.set_page_config(
    page_title="Validasi & Analisis",
    page_icon="📊",
    layout="wide"
)

# CSS ini akan memaksa fungsi show_kpi_metrics() Anda tampil bergaya Card
st.markdown("""
    <style>
    /* Mengubah container metric menjadi Card */
    div[data-testid="stMetric"] {
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        padding: 15px 20px;
        border-radius: 12px;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
        transition: transform 0.2s;
    }
    div[data-testid="stMetric"]:hover {
        transform: translateY(-5px);
        border-color: #2e7d32;
    }
    /* Mempercantik label dan nilai */
    label[data-testid="stMetricLabel"] {
        font-weight: 700;
        color: #444;
        font-size: 16px;
    }
    div[data-testid="stMetricValue"] {
        font-size: 24px;
        color: #1f77b4;
    }
    /* Meratakan kolom agar lebih rapi */
    [data-testid="column"] {
        padding: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# ==========================================================
# 2. HEADER
# ==========================================================
st.title("📊 Analisis dan Validasi")
st.markdown("Dashboard hasil integrasi sistem **Fuzzy Logic** dan **Dynamic Programming**.")

# ==========================================================
# 3. LOAD DATA DARI SESSION STATE
# ==========================================================
if "fuzzy_result" not in st.session_state or "dp_result" not in st.session_state:
    st.warning("⚠️ Data fuzzy atau DP belum tersedia. Silakan jalankan halaman sebelumnya.")
    st.stop()

df_fuzzy = st.session_state["fuzzy_result"]
df_dp = st.session_state["dp_result"]

# ==========================================================
# 4. KPI DASHBOARD (Tampilan Card Otomatis)
# ==========================================================
st.header("📊 KPI Kinerja Sistem")

# Kalkulasi KPI sesuai fungsi asli Anda
kpi = calculate_kpis(
    df_policy=df_dp,
    demand=df_dp["Demand"].values,
    import_cost=df_dp["Import_Cost"].sum() / df_dp["Impor_Optimal"].sum(),
    holding_cost=df_dp["Holding_Cost"].sum() / df_dp["Stok_Akhir"].sum(),
    max_stock=df_dp["Stok_Akhir"].max()
)

# Menampilkan KPI menggunakan fungsi asli Anda
# CSS di atas akan otomatis membungkus output fungsi ini menjadi Card
show_kpi_metrics(kpi)

# Menampilkan grafik profil inventori
st.markdown("---")
plot_inventory_profile(df_dp)

# ==========================================================
# 5. VALIDASI & STATISTIK (DIBUAT BERKOLOM)
# ==========================================================
st.divider()
col_val, col_anova = st.columns([2, 1])

with col_val:
    st.subheader("🔍 Validasi Prediksi & DM Test")
    df_validation = validation_summary(
        actual=df_dp["Demand"].values,
        fuzzy=df_fuzzy["Prediksi_Impor_Fuzzy"].values,
        baseline=df_dp["Impor_Optimal"].values
    )
    st.dataframe(df_validation, use_container_width=True)

with col_anova:
    st.subheader("🔬 Uji ANOVA")
    anova_stat, anova_p = f_oneway(
        df_fuzzy["Prediksi_Impor_Fuzzy"].values,
        df_dp["Impor_Optimal"].values,
        df_dp["Demand"].values
    )
    
    is_significant = anova_p < 0.05
    st.info(f"**F-Stat:** `{anova_stat:.4f}`")
    if is_significant:
        st.error(f"**P-Value:** `{anova_p:.4f}`\n\n(Signifikan)")
    else:
        st.success(f"**P-Value:** `{anova_p:.4f}`\n\n(Tidak Signifikan)")

# ==========================================================
# 6. ANALISIS BULANAN & VISUALISASI
# ==========================================================
st.divider()
tab1, tab2 = st.tabs(["📋 Data Bulanan", "📈 Grafik Perbandingan"])

with tab1:
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

with tab2:
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(df_analysis["Bulan"], df_analysis["Impor (Fuzzy)"], marker="o", label="Fuzzy")
    ax.plot(df_analysis["Bulan"], df_analysis["Impor (DP)"], marker="s", label="DP Optimal")
    ax.set_title("Fuzzy vs Dynamic Programming")
    ax.legend()
    st.pyplot(fig)

# ==========================================================
# 7. DOWNLOAD LAPORAN
# ==========================================================
st.divider()
st.subheader("⬇️ Unduh Laporan")
c1, c2, _ = st.columns([1, 1, 2])

with c1:
    excel_buf = export_multi_sheet({"Analysis": df_analysis, "Validation": df_validation})
    st.download_button("📂 Download Excel", data=excel_buf, file_name="Laporan.xlsx", use_container_width=True)

with c2:
    pdf_buf = export_summary_pdf(title="Laporan Akhir", metrics={"Total Cost": df_dp["Total_Cost"].sum()}, conclusion="Selesai.")
    st.download_button("📄 Download PDF", data=pdf_buf, file_name="Laporan.pdf", use_container_width=True)
