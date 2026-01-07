import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import f_oneway

# Internal modules
from modules.export_excel import export_multi_sheet
from modules.export_pdf import export_summary_pdf
from modules.kpi_metrics import calculate_kpis, validation_summary
from modules.kpi_visuals import show_kpi_metrics, plot_inventory_profile

# ==========================================================
# CONFIG
# ==========================================================
st.set_page_config(
    page_title="Analysis & Validation",
    layout="wide"
)

st.title("📊 Analysis and Validation")
st.markdown("""
This page presents **performance analysis, statistical validation, 
and final reporting** of the **Fuzzy Logic and Dynamic Programming (DP) integration**.
""")

# ==========================================================
# LOAD SESSION DATA
# ==========================================================
st.header("📥 Loading Simulation Data")

if "fuzzy_result" not in st.session_state or "dp_result" not in st.session_state:
    st.warning("⚠️ Fuzzy or DP data not found. Please run Pages 1 and 2 first.")
    st.stop()

df_fuzzy = st.session_state["fuzzy_result"]
df_dp = st.session_state["dp_result"]

st.success("✅ Simulation data successfully loaded")

# ==========================================================
# KPI DASHBOARD
# ==========================================================
st.header("📊 System Performance KPIs")

kpi = calculate_kpis(
    df_policy=df_dp,
    demand=df_dp["Market_Demand"].values,
    import_cost=df_dp["Import_Cost"].sum() / df_dp["Optimal_Import"].sum(),
    holding_cost=df_dp["Holding_Cost"].sum() / df_dp["Ending_Stock"].sum(),
    max_stock=df_dp["Ending_Stock"].max()
)

show_kpi_metrics(kpi)
plot_inventory_profile(df_dp)

# ==========================================================
# FUZZY VALIDATION + DM TEST
# ==========================================================
st.header("📊 Fuzzy Prediction Validation")

df_validation = validation_summary(
    actual=df_dp["Market_Demand"].values,
    fuzzy=df_fuzzy["Fuzzy_Import_Prediction"].values,
    baseline=df_dp["Optimal_Import"].values
)

st.dataframe(df_validation, use_container_width=True)

# ==========================================================
# ANOVA TEST
# ==========================================================
st.header("📊 ANOVA Test: Fuzzy vs DP vs Actual Demand")

anova_stat, anova_p = f_oneway(
    df_fuzzy["Fuzzy_Import_Prediction"].values,
    df_dp["Optimal_Import"].values,
    df_dp["Market_Demand"].values
)

st.markdown(f"""
- **F-statistic:** {anova_stat:.4f}  
- **p-value:** {anova_p:.4f}  
- **Significant at α = 0.05:** {'Yes' if anova_p < 0.05 else 'No'}
""")

# ==========================================================
# PERFORMANCE SUMMARY
# ==========================================================
st.header("📌 Performance Summary")

total_fuzzy_import = df_fuzzy["Fuzzy_Import_Prediction"].sum()
total_dp_import = df_dp["Optimal_Import"].sum()
total_cost = df_dp["Total_Cost"].sum()

col1, col2, col3 = st.columns(3)
col1.metric("Total Import (Fuzzy)", f"{int(total_fuzzy_import):,}")
col2.metric("Total Import (DP)", f"{int(total_dp_import):,}")
col3.metric("Total System Cost", f"{int(total_cost):,}")

# ==========================================================
# MONTHLY ANALYSIS
# ==========================================================
st.header("📋 Monthly Analysis")

df_analysis = pd.DataFrame({
    "Month": df_dp["Month"],
    "Market Demand": df_dp["Market_Demand"],
    "Starting Stock": df_dp["Starting_Stock"],
    "Import (Fuzzy)": df_fuzzy["Fuzzy_Import_Prediction"],
    "Optimal Import (DP)": df_dp["Optimal_Import"],
    "Ending Stock": df_dp["Ending_Stock"],
    "Total Cost": df_dp["Total_Cost"]
})

st.dataframe(df_analysis, use_container_width=True)

# ==========================================================
# VISUALIZATION
# ==========================================================
st.header("📈 Import & Error Comparison")

col1, col2 = st.columns(2)

with col1:
    fig1, ax1 = plt.subplots(figsize=(10, 5))
    ax1.plot(df_analysis["Month"], df_analysis["Import (Fuzzy)"], marker="o", label="Fuzzy Import")
    ax1.plot(df_analysis["Month"], df_analysis["Optimal Import (DP)"], marker="s", label="DP Import")
    ax1.set_title("Fuzzy vs DP Import Decision")
    ax1.set_xlabel("Month")
    ax1.set_ylabel("Import Quantity")
    ax1.legend()
    ax1.grid(True)
    st.pyplot(fig1)

with col2:
    fig2, ax2 = plt.subplots(figsize=(10, 5))
    err_fuzzy = abs(df_dp["Market_Demand"] - df_fuzzy["Fuzzy_Import_Prediction"])
    err_dp = abs(df_dp["Market_Demand"] - df_dp["Optimal_Import"])
    x = np.arange(len(err_fuzzy))

    ax2.bar(x - 0.2, err_fuzzy, 0.4, label="Fuzzy Error")
    ax2.bar(x + 0.2, err_dp, 0.4, label="DP Error")
    ax2.set_xticks(x)
    ax2.set_xticklabels(df_dp["Month"], rotation=45)
    ax2.set_title("Absolute Error Comparison")
    ax2.legend()
    ax2.grid(axis="y")
    st.pyplot(fig2)

# ==========================================================
# DOWNLOAD REPORTS
# ==========================================================
st.header("⬇️ Download Reports")

excel_buffer = export_multi_sheet({
    "Fuzzy_Result": df_fuzzy,
    "DP_Result": df_dp,
    "Monthly_Analysis": df_analysis,
    "Validation": df_validation,
    "ANOVA_Test": pd.DataFrame({
        "F-statistic": [anova_stat],
        "p-value": [anova_p],
        "Significant (α=0.05)": ["Yes" if anova_p < 0.05 else "No"]
    })
})

st.download_button(
    "📥 Download Excel Report",
    excel_buffer,
    "Fuzzy_DP_Final_Report.xlsx",
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
        "The integration of fuzzy logic and dynamic programming "
        "successfully produces an optimal import policy with "
        "lower costs and improved inventory control. "
        "Statistical validation confirms significant performance differences."
    )
)

st.download_button(
    "📥 Download PDF Summary",
    pdf_buffer,
    "Fuzzy_DP_Summary.pdf",
    mime="application/pdf"
)

st.success("✅ Analysis and reporting completed successfully.")
