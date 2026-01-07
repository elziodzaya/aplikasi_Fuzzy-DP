import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from modules.dp_model import dp_deterministic_horizon

# =========================================================
# CONFIGURATION
# =========================================================
st.set_page_config(
    page_title="Dynamic Programming - Import Optimization",
    layout="wide"
)

st.title("⚙️ Import Optimization Using Dynamic Programming")
st.markdown("""
This page performs import decision optimization using a Dynamic Programming (DP) approach,
with fuzzy prediction results used as action constraints.
""")

# =========================================================
# UPLOAD FUZZY RESULTS
# =========================================================
st.subheader("📂 Upload Fuzzy Prediction Results")

uploaded_file = st.file_uploader(
    "Upload Fuzzy Prediction Result File (Excel)",
    type=["xlsx"]
)

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    # =====================================================
    # REQUIRED COLUMNS FROM FUZZY PAGE
    # =====================================================
    required_cols = [
        "Market_Demand",
        "Product_Stock",
        "Fuzzy_Import_Prediction"
    ]

    if not all(col in df.columns for col in required_cols):
        st.error(
            f"❌ Invalid file format.\n\n"
            f"Required columns:\n{required_cols}\n\n"
            f"Detected columns:\n{df.columns.tolist()}"
        )
        st.stop()

    st.success("✅ Fuzzy prediction data successfully loaded")
    st.dataframe(df)

    # =====================================================
    # DYNAMIC PROGRAMMING PARAMETERS
    # =====================================================
    st.subheader("🎛️ Dynamic Programming Parameters")

    col1, col2, col3 = st.columns(3)

    with col1:
        holding_cost = st.number_input(
            "Holding Cost per Unit",
            min_value=0.0,
            value=2.0
        )

    with col2:
        import_cost = st.number_input(
            "Import Cost per Unit",
            min_value=0.0,
            value=5.0
        )

    with col3:
        max_stock = st.number_input(
            "Maximum Warehouse Capacity",
            min_value=1,
            value=500
        )

    initial_stock = st.number_input(
        "Initial Stock Level",
        min_value=0,
        value=int(df["Product_Stock"].iloc[0])
    )

    # =====================================================
    # RUN DYNAMIC PROGRAMMING
    # =====================================================
    if st.button("⚙️ Run Dynamic Programming Optimization"):

        demand = df["Market_Demand"].values
        fuzzy_import = df["Fuzzy_Import_Prediction"].values

        results_dp, total_cost = dp_deterministic_horizon(
            demand=demand,
            fuzzy_import=fuzzy_import,
            holding_cost=holding_cost,
            import_cost=import_cost,
            max_stock=int(max_stock),
            initial_stock=int(initial_stock)
        )

        # =====================================================
        # 🔍 DETECT & STANDARDIZE COLUMN NAMES (CRITICAL FIX)
        # =====================================================
        possible_opt_cols = [
            "Optimal_Import",
            "Optimal_Import_DP",
            "optimal_import",
            "Import",
            "Import_Quantity",
            "Decision"
        ]

        opt_col = None
        for c in possible_opt_cols:
            if c in results_dp.columns:
                opt_col = c
                break

        if opt_col is None:
            st.error(
                "❌ Dynamic Programming output does not contain an optimal import column.\n\n"
                f"Available columns:\n{results_dp.columns.tolist()}"
            )
            st.stop()

        # rename to standard
        results_dp = results_dp.rename(columns={opt_col: "Optimal_Import"})

        # =================================================
        # COST CALCULATION PER PERIOD
        # =================================================
        results_dp["Import_Cost"] = (
            results_dp["Optimal_Import"] * import_cost
        )

        results_dp["Holding_Cost"] = (
            results_dp["Ending_stock"] * holding_cost
        )

        results_dp["Total_Cost"] = (
            results_dp["Import_Cost"] +
            results_dp["Holding_Cost"]
        )

        # =================================================
        # SAVE RESULTS TO SESSION
        # =================================================
        st.session_state["dp_result"] = results_dp.copy()
        st.session_state["dp_total_cost"] = results_dp["Total_Cost"].sum()

        st.success("✅ Dynamic Programming results successfully computed")

        # =================================================
        # DP RESULTS
        # =================================================
        st.subheader("📊 Dynamic Programming Optimization Results")
        st.dataframe(results_dp)

        st.metric(
            label="💰 Minimum Total Cost (Cumulative)",
            value=f"{results_dp['Total_Cost'].sum():,.2f}"
        )

        # =================================================
        # COMPARISON PLOT
        # =================================================
        st.subheader("📈 Comparison: Fuzzy Import vs Optimal Import (DP)")

        fig, ax = plt.subplots(figsize=(10, 4))

        ax.plot(
            results_dp.index,
            fuzzy_import,
            marker="o",
            label="Fuzzy Import"
        )

        ax.plot(
            results_dp.index,
            results_dp["Optimal_Import"],
            marker="s",
            label="Optimal Import (DP)"
        )

        ax.set_xlabel("Period")
        ax.set_ylabel("Import Quantity")
        ax.set_title("Comparison of Import Decisions")
        ax.legend()
        ax.grid(True)

        st.pyplot(fig)

        # =================================================
        # DOWNLOAD RESULTS
        # =================================================
        st.subheader("⬇️ Download Results")

        output_file = "dp_optimization_results.xlsx"

        with pd.ExcelWriter(output_file, engine="openpyxl") as writer:
            results_dp.to_excel(
                writer,
                index=False,
                sheet_name="DP_Results"
            )

        with open(output_file, "rb") as f:
            st.download_button(
                label="⬇️ Download Results (Excel)",
                data=f,
                file_name=output_file,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
