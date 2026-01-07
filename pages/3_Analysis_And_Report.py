import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import f_oneway

# Import your internal modules
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

# CSS for Card-style KPI Metrics
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
This page presents the **analysis of Fuzzy System and Dynamic Programming (DP) results**, 
and provides **final reports in Excel and PDF formats**, complete with **statistical validation**.
""")

# ==========================================================
# LOAD DATA FROM SESSION STATE
# ==========================================================
st.header("📥 Loading Simulation Data")

if "fuzzy_result" not in st.session_state or "dp_result" not in st.session_state:
    st.warning("⚠️ Fuzzy or DP data is not available. Please run Page 1 and 2 first.")
    st.stop()

df_fuzzy = st.session_state["fuzzy_result"]
df_dp = st.session_state["dp_result"]

st.success("✅ Fuzzy and DP data successfully loaded")

# ==========================================================
# KPI DASHBOARD
# ==========================================================
st.header("📊 System Performance KPIs")

kpi = calculate_kpis(
    df_policy=df_dp,
    demand=df_dp["Demand"].values,
    import_cost=df_dp["Import_Cost"].sum() / df_dp["Impor_Optimal"].sum(),
    holding_cost=df_dp["Holding_Cost"].sum() / df_dp["Stok_Akhir"].sum(),
    max_stock=df_dp["Stok_Akhir"].max()
)

# Displaying KPI using your original function (Cards styled via CSS)
show_kpi_metrics(kpi)
plot_inventory_profile(df_dp)

# ==========================================================
# FUZZY VALIDATION + DM TEST
# ==========================================================
st.header("📊 Fuzzy Prediction Validation & DM Test")

df_validation = validation_summary(
    actual=df_dp["Demand"].values,
    fuzzy=df_fuzzy["Prediksi_Impor_Fuzzy"].values,
    baseline=df_dp["Impor_Optimal"].values
)

st.dataframe(df_validation, use_container_width=True)

# ==========================================================
# ANOVA TEST: Fuzzy vs DP vs Actual
# ==========================================================
st.header("📊 ANOVA Test: Fuzzy Prediction vs DP vs Actual Demand")

anova_stat, anova_p = f_oneway(
    df_fuzzy["Prediksi_Impor_Fuzzy"].values,
    df_dp["Impor_Optimal"].values,
    df_dp["Demand"].values
)

st.markdown(f"""
- **F-statistic:** {anova_stat:.4f}  
- **p-value:** {anova_p:.4f}  
- **Significant at α=0.05:** {'Yes' if anova_p < 0.05 else 'No'}
""")

# ==========================================================
# PERFORMANCE SUMMARY
# ==========================================================
st.header("📌 Performance Summary")

total_fuzzy_import = df_fuzzy["Prediksi_Impor_Fuzzy"].sum()
total_dp_import = df_dp["Impor_Optimal"].sum()
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
# IMPORT COMPARISON VISUALIZATION
# ==========================================================
st.header("📈 Import Comparison Visualizations")

col_fig1, col_fig2 = st.columns(2)

with col_fig1:
    fig1, ax1 = plt.subplots(figsize=(10, 6))
    ax1.plot(df_analysis["Month"], df_analysis["Import (Fuzzy)"], marker="o", label="Fuzzy Import")
    ax1.plot(df_analysis["Month"], df_analysis["Optimal Import (DP)"], marker="s", label="DP Import")
    ax1.set_xlabel("Month")
    ax1.set_ylabel("Import Quantity")
    ax1.set_title("Fuzzy vs Dynamic Programming Comparison")
    ax1.legend()
    ax1.grid(True)
    st.pyplot(fig1)

with col_fig2:
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    errors_fuzzy = np.abs(df_dp["Demand"] - df_fuzzy["Prediksi_Impor_Fuzzy"])
    errors_dp = np.abs(df_dp["Demand"] - df_dp["Impor_Optimal"])
    x = np.arange(len(df_dp))
    ax2.bar(x - 0.2, errors_fuzzy, 0.4, label="Fuzzy Error", color='skyblue')
    ax2.bar(x + 0.2, errors_dp, 0.4, label="DP Error", color='salmon')
    ax2.set_xticks(x)
    ax2.set_xticklabels(df_dp["Month"], rotation=45)
    ax2.set_title("Absolute Error Comparison")
    ax2.legend()
    ax2.grid(True, axis='y')
    st.pyplot(fig2)

# ==========================================================
# DOWNLOAD REPORTS
# ==========================================================
st.header("⬇️ Download Reports")

# Restoring the original multi-sheet structure in English
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
    label="📥 Download Excel Report (Multi-Sheet)",
    data=excel_buffer,
    file_name="Fuzzy_DP_Report.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
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
        "effectively generates an optimal annual import policy "
        "with minimum costs and improved stock control. "
        "Statistical tests (DM test & ANOVA) highlight the performance differences."
    )
)

st.download_button(
    label="📥 Download PDF Summary Report",
    data=pdf_buffer,
    file_name="Fuzzy_DP_Summary.pdf",
    mime="application/pdf",
    use_container_width=True
)

st.success("✅ Analysis and reporting complete.")
