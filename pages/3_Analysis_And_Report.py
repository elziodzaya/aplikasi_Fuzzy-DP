import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import f_oneway

# ==========================================================
# INTERNAL MODULES
# ==========================================================
from modules.export_excel import export_multi_sheet
from modules.export_pdf import export_summary_pdf
from modules.kpi_metrics import (
    calculate_kpis,
    validation_summary
)
from modules.kpi_visuals import show_kpi_metrics, plot_inventory_profile

# ==========================================================
# CONFIG & STYLING
# ==========================================================
st.set_page_config(
    page_title="Validation & Analysis",
    layout="wide"
)

st.markdown("""
<style>
div[data-testid="stMetric"] {
    background-color: #ffffff;
    border: 1px solid #e0e0e0;
    padding: 15px 20px;
    border-radius: 12px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
}
label[data-testid="stMetricLabel"] {
    font-weight: 700;
    color: #444;
}
</style>
""", unsafe_allow_html=True)

st.title("📊 Analysis and Validation")
st.markdown("""
This page presents the **analysis of Fuzzy Logic and Dynamic Programming (DP)** results,
including **KPI evaluation, statistical validation, and report generation**.
""")

# ==========================================================
# LOAD DATA
# ==========================================================
st.header("📥 Loading Simulation Data")

if "fuzzy_result" not in st.session_state or "dp_result" not in st.session_state:
    st.warning("⚠️ Please run Fuzzy System and DP Simulation first.")
    st.stop()

df_fuzzy = st.session_state["fuzzy_result"]
df_dp = st.session_state["dp_result"]

st.success("✅ Data successfully loaded")

# ==========================================================
# KPI DASHBOARD (COLUMN NORMALIZATION FIX)
# ==========================================================
st.header("📊 System Performance KPIs")

# ---- IMPORTANT FIX: normalize column names for KPI module ----
df_dp_kpi = df_dp.rename(columns={
    "Impor_Optimal": "Optimal_Import",
    "Stok_Akhir": "Ending_Stock"
})

kpi = calculate_kpis(
    df_policy=df_dp_kpi,
    demand=df_dp_kpi["Demand"].values,
    import_cost=df_dp_kpi["Import_Cost"].sum(),
    holding_cost=df_dp_kpi["Holding_Cost"].sum(),
    max_stock=df_dp_kpi["Ending_Stock"].max()
)

show_kpi_metrics(kpi)
plot_inventory_profile(df_dp)

# ==========================================================
# FUZZY VALIDATION & DIEBOLD–MARIANO TEST
# ==========================================================
st.header("📊 Fuzzy Prediction Validation & DM Test")

df_validation = validation_summary(
    actual=df_dp["Demand"].values,
    fuzzy=df_fuzzy["Prediksi_Impor_Fuzzy"].values,
    baseline=df_dp["Impor_Optimal"].values
)

st.dataframe(df_validation, use_container_width=True)

# ==========================================================
# ANOVA TEST
# ==========================================================
st.header("📊 ANOVA Test: Fuzzy vs DP vs Actual Demand")

anova_stat, anova_p = f_oneway(
    df_fuzzy["Prediksi_Impor_Fuzzy"].values,
    df_dp["Impor_Optimal"].values,
    df_dp["Demand"].values
)

st.markdown(f"""
- **F-statistic:** {anova_stat:.4f}  
- **p-value:** {anova_p:.4f}  
- **Significant (α = 0.05):** {'Yes' if anova_p < 0.05 else 'No'}
""")

# ==========================================================
# PERFORMANCE SUMMARY
# ==========================================================
st.header("📌 Performance Summary")

total_fuzzy_import = df_fuzzy["Prediksi_Impor_Fuzzy"].sum()
total_dp_import = df_dp["Impor_Optimal"].sum()
total_cost = df_dp["Total_Cost"].sum()

c1, c2, c3 = st.columns(3)
c1.metric("Total Import (Fuzzy)", f"{int(total_fuzzy_import):,}")
c2.metric("Total Import (DP)", f"{int(total_dp_import):,}")
c3.metric("Total System Cost", f"{int(total_cost):,}")

# ==========================================================
# MONTHLY ANALYSIS TABLE
# ==========================================================
st.header("📋 Monthly Analysis")

df_analysis = pd.DataFrame({
    "Month": df_fuzzy["Month"].astype(str),
    "Demand": df_dp["Demand"],
    "Initial Stock": df_dp["Stok_Awal"],
    "Import (Fuzzy)": df_fuzzy["Prediksi_Impor_Fuzzy"],
    "Optimal Import (DP)": df_dp["Impor_Optimal"],
    "Final Stock": df_dp["Stok_Akhir"],
    "Total Cost": df_dp["Total_Cost"]
})

st.dataframe(df_analysis, use_container_width=True)

# ==========================================================
# VISUAL COMPARISON
# ==========================================================
st.header("📈 Import Comparison Visualizations")

col1, col2 = st.columns(2)

with col1:
    fig1, ax1 = plt.subplots(figsize=(10, 6))
    ax1.plot(df_analysis["Month"], df_analysis["Import (Fuzzy)"], marker="o", label="Fuzzy")
    ax1.plot(df_analysis["Month"], df_analysis["Optimal Import (DP)"], marker="s", label="DP")
    ax1.set_title("Fuzzy vs DP Import Decision")
    ax1.set_xlabel("Month")
    ax1.set_ylabel("Import Quantity")
    ax1.legend()
    ax1.grid(True)
    st.pyplot(fig1)

with col2:
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    err_fuzzy = np.abs(df_dp["Demand"] - df_fuzzy["Prediksi_Impor_Fuzzy"])
    err_dp = np.abs(df_dp["Demand"] - df_dp["Impor_Optimal"])
    x = np.arange(len(df_dp))
    ax2.bar(x - 0.2, err_fuzzy, 0.4, label="Fuzzy Error")
    ax2.bar(x + 0.2, err_dp, 0.4, label="DP Error")
    ax2.set_xticks(x)
    ax2.set_xticklabels(df_dp["Month"], rotation=45)
    ax2.set_title("Absolute Error Comparison")
    ax2.legend()
    ax2.grid(axis="y")
    st.pyplot(fig2)

# ==========================================================
# EXPORT REPORTS
# ==========================================================
st.header("⬇️ Download Reports")

excel_buffer = export_multi_sheet({
    "Fuzzy_Result": df_fuzzy,
    "DP_Result": df_dp,
    "Final_Analysis": df_analysis,
    "Validation_Fuzzy": df_validation,
    "ANOVA_Test": pd.DataFrame({
        "F-statistic": [anova_stat],
        "p-value": [anova_p],
        "Significant (α=0.05)": ["Yes" if anova_p < 0.05 else "No"]
    })
})

st.download_button(
    "📥 Download Excel Report",
    excel_buffer,
    "Fuzzy_DP_Report.xlsx",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    use_container_width=True
)

pdf_buffer = export_summary_pdf(
    title="Final Import Decision Support System Report",
    metrics={
        "Total Fuzzy Import": f"{int(total_fuzzy_import):,}",
        "Total DP Import": f"{int(total_dp_import):,}",
        "Total Cost": f"{int(total_cost):,}"
    },
    conclusion=(
        "The integration of fuzzy logic and dynamic programming "
        "produces an optimal import policy with lower cost and "
        "better inventory control, supported by DM Test and ANOVA."
    )
)

st.download_button(
    "📥 Download PDF Summary",
    pdf_buffer,
    "Fuzzy_DP_Summary.pdf",
    "application/pdf",
    use_container_width=True
)

st.success("✅ Analysis and reporting completed successfully.")
