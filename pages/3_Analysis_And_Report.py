import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from modules.kpi_metrics import (
    validation_summary,
    calculate_kpis
)

# =========================================================
# PAGE CONFIGURATION
# =========================================================
st.set_page_config(
    page_title="Analysis & Report",
    layout="wide"
)

st.title("📊 Analysis & Performance Evaluation")

st.markdown("""
This page provides **performance evaluation**, **KPI analysis**, and
**statistical validation** for:
- Fuzzy Import Prediction
- Dynamic Programming Optimization
""")

# =========================================================
# LOAD DP RESULTS
# =========================================================
if "dp_result" not in st.session_state:
    st.warning("⚠️ Please run the Dynamic Programming page first.")
    st.stop()

df = st.session_state["dp_result"].copy()

# =========================================================
# DATA VALIDATION (HARD CHECK)
# =========================================================
required_cols = [
    "Month",
    "Demand",
    "Fuzzy_Import",
    "Optimal_Import",
    "Ending_Stock",
    "Holding_Cost",
    "Import_Cost",
    "Total_Cost"
]

missing_cols = [c for c in required_cols if c not in df.columns]

if missing_cols:
    st.error("❌ Missing required columns:")
    st.write(missing_cols)
    st.stop()

# =========================================================
# PREVIEW DATA
# =========================================================
st.subheader("📄 Final Optimization Dataset")
st.dataframe(df, use_container_width=True)

# =========================================================
# KPI – DYNAMIC PROGRAMMING
# =========================================================
st.subheader("📌 Key Performance Indicators (DP Policy)")

kpi = calculate_kpis(
    df_policy=df,
    demand=df["Demand"].values,
    import_cost=df["Import_Cost"].mean(),
    holding_cost=df["Holding_Cost"].mean(),
    max_stock=df["Ending_Stock"].max()
)

kpi_df = pd.DataFrame.from_dict(kpi, orient="index", columns=["Value"])
st.dataframe(kpi_df, use_container_width=True)

# =========================================================
# ERROR METRICS & STATISTICAL VALIDATION
# =========================================================
st.subheader("📐 Prediction Accuracy & Statistical Test")

validation_df = validation_summary(
    actual=df["Demand"].values,
    fuzzy=df["Fuzzy_Import"].values,
    baseline=df["Optimal_Import"].values
)

st.dataframe(validation_df, use_container_width=True)

# =========================================================
# COST ANALYSIS
# =========================================================
st.subheader("💰 Cost Breakdown Over Time")

fig, ax = plt.subplots(figsize=(10, 4))

ax.plot(df["Month"], df["Holding_Cost"], label="Holding Cost", marker="o")
ax.plot(df["Month"], df["Import_Cost"], label="Import Cost", marker="s")
ax.plot(df["Month"], df["Total_Cost"], label="Total Cost", linewidth=2)

ax.set_xlabel("Month")
ax.set_ylabel("Cost")
ax.set_title("Cost Components Over Time")
ax.legend()
ax.grid(True)

st.pyplot(fig)

# =========================================================
# INVENTORY LEVEL ANALYSIS
# =========================================================
st.subheader("📦 Inventory Level Analysis")

fig2, ax2 = plt.subplots(figsize=(10, 4))

ax2.plot(
    df["Month"],
    df["Ending_Stock"],
    marker="o",
    label="Ending Stock"
)

ax2.axhline(
    y=df["Ending_Stock"].mean(),
    linestyle="--",
    label="Average Stock"
)

ax2.set_xlabel("Month")
ax2.set_ylabel("Stock Level")
ax2.set_title("Ending Inventory Level Over Time")
ax2.legend()
ax2.grid(True)

st.pyplot(fig2)

# =========================================================
# SUMMARY METRICS
# =========================================================
st.subheader("📊 Summary Metrics")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Total Cost",
        f"{df['Total_Cost'].sum():,.2f}"
    )

with col2:
    st.metric(
        "Average Inventory",
        f"{df['Ending_Stock'].mean():,.2f}"
    )

with col3:
    st.metric(
        "Service Level",
        f"{(df['Ending_Stock'] > 0).mean() * 100:.2f}%"
    )
