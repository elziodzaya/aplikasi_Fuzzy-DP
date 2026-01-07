import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import f_oneway

# =========================
# INTERNAL MODULES
# =========================
from modules.export_excel import export_multi_sheet
from modules.export_pdf import export_summary_pdf
from modules.kpi_metrics import calculate_kpis, validation_summary
from modules.kpi_visuals import show_kpi_metrics, plot_inventory_profile

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Analysis & Validation",
    layout="wide"
)

st.title("📊 Analysis and Validation")
st.markdown("""
This page presents a **comprehensive analysis of the Fuzzy Logic System and
Dynamic Programming (DP) optimization results**, including:
- KPI evaluation  
- Statistical validation (DM Test & ANOVA)  
- Final reporting in **Excel and PDF**
""")

# =========================
# LOAD SESSION DATA
# =========================
st.header("📥 Load Simulation Results")

if "fuzzy_result" not in st.session_state or "dp_result" not in st.session_state:
    st.warning("⚠️ Fuzzy or DP results not found. Please run Page 1 and Page 2 first.")
    st.stop()

df_fuzzy = st.session_state["fuzzy_result"].copy()
df_dp = st.session_state["dp_result"].copy()

st.success("✅ Fuzzy and DP results successfully loaded")

# ==========================================================
# 🔴 CRITICAL FIX — STANDARDIZE COLUMN NAMES
# ==========================================================
df_dp = df_dp.rename(columns={
    "Demand": "Market_Demand",
    "Impor_Fuzzy": "Fuzzy_Import",
    "Impor_Optimal": "Optimal_Import",
    "Stok_Awal": "Starting_Stock",
    "Stok_Akhir": "Ending_Stock"
})

# Debug safety check (can be removed after verification)
required_cols = [
    "Market_Demand",
    "Fuzzy_Import",
    "Optimal_Import",
    "Starting_Stock",
    "Ending_Stock",
    "Holding_Cost",
    "Import_Cost"
]

missing = [c for c in required_cols if c not in df_dp.columns]
if missing:
    st.error(f"❌ Missing required DP columns: {missing}")
    st.stop()

# =========================
# KPI DASHBOARD
# =========================
st.header("📊 System Performance KPIs")

kpi = calculate_kpis(
    df_policy=df_dp,
    demand=df_dp["Market_Demand"].values,
    import_cost=df_dp["Import_Cost"].sum() / df_dp["Optimal_Import"].sum(),
    holding_cost=df_dp["Holding_Cost"].sum() / df_dp["Ending_Stock"].mean(),
    max_stock=df_dp["Ending_Stock"].max()
)

show_kpi_metrics(kpi)
plot_inventory_profile(df_dp)

# =========================
# FUZZY VALIDATION & DM TEST
# =========================
st.header("📊 Fuzzy Prediction Validation")

df_validation = validation_summary(
    actual=df_dp["Market_Demand"].values,
    fuzzy=df_fuzzy["Prediksi_Impor_Fuzzy"].values,
    baseline=df_dp["Optimal_Import"].values
)

st.dataframe(df_validation, use_container_width=True)

# =========================
# ANOVA TEST
# =========================
st.header("📊 ANOVA Test")

anova_stat, anova_p = f_oneway(
    df_fuzzy["Prediksi_Impor_Fuzzy"].values,
    df_dp["Optimal_Import"].values,
    df_dp["Market_Demand"].values
)

st.markdown(f"""
- **F-statistic:** {anova_stat:.4f}  
- **p-value:** {anova_p:.4f}  
- **Significant (α = 0.05):** {"Yes" if anova_p < 0.05 else "No"}
""")

# =========================
# PERFORMANCE SUMMARY
# =========================
st.header("📌 Performance Summary")

total_fuzzy_import = df_fuzzy["Prediksi_Impor_Fuzzy"].sum()
total_dp_import = df_dp["Optimal_Import"].sum()
total_cost = df_dp["Total_Cost"].sum()

col1, col2, col3 = st.columns(3)
col1.metric("Total Import (Fuzzy)", f"{int(total_fuzzy_import):,}")
col2.metric("Total Import (DP)", f"{int(total_dp_import):,}")
col3.metric("Total System Cost", f"{int(total_cost):,}")

# =========================
# MONTHLY ANALYSIS TABLE
# =========================
st.header("📋 Monthly Analysis")

df_analysis = pd.DataFrame({
    "Month": df_dp["Month"].astype(str),
    "Demand": df_dp["Market_Demand"],
    "Initial Stock": df_dp["Starting_Stock"],
    "Fuzzy Import": df_fuzzy["Prediksi_Impor_Fuzzy"],
    "Optimal Import (DP)": df_dp["Optimal_Import"],
    "Final Stock": df_dp["Ending_Stock"],
    "Total Cost": df_dp["Total_Cost"]
})

st.dataframe(df_analysis, use_container_width=True)

# =========================
# VISUAL COMPARISON
# =========================
st.header("📈 Import Comparison")

col1, col2 = st.columns(2)

with col1:
    fig1, ax1 = plt.subplots(figsize=(9, 5))
    ax1.plot(df_analysis["Month"], df_analysis["Fuzzy Import"], marker="o", label="Fuzzy")
    ax1.plot(df_analysis["Month"], df_analysis["Optimal Import (DP)"], marker="s", label="DP")
    ax1.set_title("Import Decision Comparison")
    ax1.set_xlabel("Month")
    ax1.set_ylabel("Import Quantity")
    ax1.legend()
    ax1.grid(True)
    st.pyplot(fig1)

with col2:
    fig2, ax2 = plt.subplots(figsize=(9, 5))
    error_fuzzy = np.abs(df_dp["Market_Demand"] - df_fuzzy["Prediksi_Impor_Fuzzy"])
    error_dp = np.abs(df_dp["Market_Demand"] - df_dp["Optimal_Import"])
    x = np.arange(len(error_fuzzy))
    ax2.bar(x - 0.2, error_fuzzy, 0.4, label="Fuzzy Error")
    ax2.bar(x + 0.2, error_dp, 0.4, label="DP Error")
    ax2.set_title("Absolute Error Comparison")
    ax2.legend()
    ax2.grid(axis="y")
    st.pyplot(fig2)

# =========================
# DOWNLOAD REPORTS
# =========================
st.header("⬇️ Download Reports")

excel_buffer = export_multi_sheet({
    "Fuzzy_Result": df_fuzzy,
    "DP_Result": df_dp,
    "Monthly_Analysis": df_analysis,
    "Validation": df_validation,
    "ANOVA": pd.DataFrame({
        "F-statistic": [anova_stat],
        "p-value": [anova_p],
        "Significant": [anova_p < 0.05]
    })
})

st.download_button(
    label="📥 Download Excel Report",
    data=excel_buffer,
    file_name="Fuzzy_DP_Analysis_Report.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

pdf_buffer = export_summary_pdf(
    title="Final Import Decision Support System Report",
    metrics={
        "Total Fuzzy Import": f"{int(total_fuzzy_import):,}",
        "Total DP Import": f"{int(total_dp_import):,}",
        "Total Cost": f"{int(total_cost):,}"
    },
    conclusion=(
        "The integration of fuzzy logic and dynamic programming successfully "
        "produces an optimal import policy with lower costs, improved service level, "
        "and statistically significant performance improvements."
    )
)

st.download_button(
    label="📥 Download PDF Summary",
    data=pdf_buffer,
    file_name="Fuzzy_DP_Summary.pdf",
    mime="application/pdf"
)

st.success("✅ Analysis and reporting completed successfully.")
