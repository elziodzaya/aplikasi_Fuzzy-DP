import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import f_oneway

from modules.export_excel import export_multi_sheet
from modules.export_pdf import export_summary_pdf
from modules.kpi_metrics import (
    calculate_kpis,
    validation_summary
)
from modules.kpi_visuals import show_kpi_metrics, plot_inventory_profile

# ==========================================================
# CONFIG
# ==========================================================
st.set_page_config(
    page_title="Validasi",
    layout="wide"
)

st.title("📊 Analisis dan Validasi")
st.markdown("""
Halaman ini menyajikan **analisis hasil sistem fuzzy dan dynamic programming (DP)**  
serta menyediakan **laporan akhir dalam format Excel dan PDF**, lengkap dengan **validasi statistik**.
""")

# ==========================================================
# LOAD DATA DARI SESSION STATE
# ==========================================================
st.header("📥 Memuat Data Hasil Simulasi")

if "fuzzy_result" not in st.session_state or "dp_result" not in st.session_state:
    st.warning("⚠️ Data fuzzy atau DP belum tersedia. Silakan jalankan halaman 1 dan 2 terlebih dahulu.")
    st.stop()

df_fuzzy = st.session_state["fuzzy_result"]
df_dp = st.session_state["dp_result"]

st.success("✅ Data fuzzy dan DP berhasil dimuat")

# ==========================================================
# KPI DASHBOARD
# ==========================================================
st.header("📊 KPI Kinerja Sistem")

kpi = calculate_kpis(
    df_policy=df_dp,
    demand=df_dp["Demand"].values,
    import_cost=df_dp["Import_Cost"].sum() / df_dp["Impor_Optimal"].sum(),
    holding_cost=df_dp["Holding_Cost"].sum() / df_dp["Stok_Akhir"].sum(),
    max_stock=df_dp["Stok_Akhir"].max()
)

show_kpi_metrics(kpi)
plot_inventory_profile(df_dp)

# ==========================================================
# VALIDASI FUZZY + DIEBOLD–MARIANO
# ==========================================================
st.header("📊 Validasi Prediksi Fuzzy & DM Test")

df_validation = validation_summary(
    actual=df_dp["Demand"].values,
    fuzzy=df_fuzzy["Prediksi_Impor_Fuzzy"].values,
    baseline=df_dp["Impor_Optimal"].values
)

st.dataframe(df_validation, use_container_width=True)

# ==========================================================
# UJI ANOVA Fuzzy vs DP vs Actual
# ==========================================================
st.header("📊 Uji ANOVA Prediksi Fuzzy vs DP vs Demand Aktual")

anova_stat, anova_p = f_oneway(
    df_fuzzy["Prediksi_Impor_Fuzzy"].values,
    df_dp["Impor_Optimal"].values,
    df_dp["Demand"].values
)

st.markdown(f"""
- **F-statistic:** {anova_stat:.4f}  
- **p-value:** {anova_p:.4f}  
- **Signifikan pada α=0.05:** {'Ya' if anova_p < 0.05 else 'Tidak'}
""")
# ==========================================================
# RINGKASAN HASIL
# ==========================================================
st.header("📌 Ringkasan Hasil")

total_fuzzy_import = df_fuzzy["Prediksi_Impor_Fuzzy"].sum()
total_dp_import = df_dp["Impor_Optimal"].sum()
total_cost = df_dp["Total_Cost"].sum()

col1, col2, col3 = st.columns(3)
col1.metric("Total Impor (Fuzzy)", f"{int(total_fuzzy_import):,}")
col2.metric("Total Impor (DP)", f"{int(total_dp_import):,}")
col3.metric("Total Biaya Sistem", f"{int(total_cost):,}")

# ==========================================================
# ANALISIS BULANAN
# ==========================================================
st.header("📋 Analisis Bulanan")

df_analysis = pd.DataFrame({
    "Bulan": df_fuzzy["Month"].astype(str),
    "Demand": df_dp["Demand"],
    "Stok Awal": df_dp["Stok_Awal"],
    "Impor (Fuzzy)": df_fuzzy["Prediksi_Impor_Fuzzy"],
    "Impor Optimal (DP)": df_dp["Impor_Optimal"],
    "Stok Akhir": df_dp["Stok_Akhir"],
    "Biaya Total": df_dp["Total_Cost"]
})

st.dataframe(df_analysis, use_container_width=True)

# ==========================================================
# VISUALISASI PERBANDINGAN IMPOR
# ==========================================================
st.header("📈 Visualisasi Perbandingan Impor")

fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(df_analysis["Bulan"], df_analysis["Impor (Fuzzy)"], marker="o", label="Impor Fuzzy")
ax.plot(df_analysis["Bulan"], df_analysis["Impor Optimal (DP)"], marker="s", label="Impor DP")
ax.set_xlabel("Bulan")
ax.set_ylabel("Jumlah Impor")
ax.set_title("Perbandingan Impor Fuzzy vs Dynamic Programming")
ax.legend()
ax.grid(True)
st.pyplot(fig)


# ==========================================================
# GRAFIK PREDIKSI VS AKTUAL
# ==========================================================
st.header("📈 Prediksi Fuzzy vs Demand Aktual")

fig2, ax2 = plt.subplots(figsize=(10,5))
ax2.plot(df_dp["Month"], df_dp["Demand"], marker='o', label="Demand Aktual")
ax2.plot(df_fuzzy["Month"].astype(str), df_fuzzy["Prediksi_Impor_Fuzzy"], marker='x', label="Prediksi Fuzzy")

ax2.set_title("Prediksi Fuzzy vs Demand Aktual")
ax2.set_xlabel("Bulan")
ax2.set_ylabel("Jumlah Impor")
ax2.legend()
ax2.grid(True)
st.pyplot(fig2)

# ==========================================================
# GRAFIK PERBANDINGAN ERROR
# ==========================================================
st.header("📊 Perbandingan Error Fuzzy vs DP")

errors_fuzzy = np.abs(df_dp["Demand"] - df_fuzzy["Prediksi_Impor_Fuzzy"])
errors_dp = np.abs(df_dp["Demand"] - df_dp["Impor_Optimal"])

fig3, ax3 = plt.subplots(figsize=(10,5))
x = np.arange(len(df_dp))
width = 0.35
ax3.bar(x - width/2, errors_fuzzy, width, label="Error Fuzzy")
ax3.bar(x + width/2, errors_dp, width, label="Error DP")
ax3.set_xticks(x)
ax3.set_xticklabels(df_dp["Month"], rotation=45)
ax3.set_ylabel("Error Absolut")
ax3.set_title("Perbandingan Error Fuzzy vs DP")
ax3.legend()
ax3.grid(True)
st.pyplot(fig3)


# ==========================================================
# DOWNLOAD LAPORAN
# ==========================================================
st.header("⬇️ Unduh Laporan")

excel_buffer = export_multi_sheet({
    "Fuzzy_Result": df_fuzzy,
    "DP_Result": df_dp,
    "Final_Analysis": df_analysis,
    "Validation_Fuzzy": df_validation,
    "ANOVA_Test": pd.DataFrame({
        "F-statistic": [anova_stat],
        "p-value": [anova_p],
        "Signifikan (α=0.05)": ["Ya" if anova_p < 0.05 else "Tidak"]
    })
})

st.download_button(
    label="📥 Download Laporan Excel",
    data=excel_buffer,
    file_name="Laporan_Fuzzy_DP.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

pdf_buffer = export_summary_pdf(
    title="Laporan Akhir Sistem Pendukung Keputusan Impor",
    metrics={
        "Total Impor Fuzzy": f"{int(total_fuzzy_import):,}",
        "Total Impor DP": f"{int(total_dp_import):,}",
        "Total Biaya": f"{int(total_cost):,}"
    },
    conclusion=(
        "Integrasi sistem fuzzy dan dynamic programming "
        "mampu menghasilkan kebijakan impor tahunan yang optimal "
        "dengan biaya minimum dan pengendalian stok yang lebih baik. "
        "Uji statistik (DM test & ANOVA) menunjukkan perbedaan performa antara Fuzzy, DP, dan Demand Aktual."
    )
)

st.download_button(
    label="📥 Download Laporan PDF",
    data=pdf_buffer,
    file_name="Laporan_Fuzzy_DP.pdf",
    mime="application/pdf"
)

st.success("✅ Halaman analisis dan pelaporan selesai")

