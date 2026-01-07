import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from modules.fuzzy_system import build_fuzzy_system, predict_import
from modules.data_loader import load_anylogic_data
from modules.visualization import plot_mf, plot_fuzzy_surface
from io import BytesIO

# =========================================================
# CONFIGURATION
# =========================================================
st.set_page_config(page_title="Fuzzy Import System", layout="wide")
st.title("📊 Import Requirement Forecasting Using a Fuzzy System")

# =========================================================
# BUILD FUZZY SYSTEM
# =========================================================
system, md, ps, pc, pi = build_fuzzy_system()

# =========================================================
# MEMBERSHIP FUNCTIONS (WITH TOGGLE BUTTON)
# =========================================================
st.subheader("📐 Membership Functions")

if 'show_mf' not in st.session_state:
    st.session_state.show_mf = False

if st.button("📐 Show"):
    st.session_state.show_mf = not st.session_state.show_mf

if st.session_state.show_mf:
    col1, col2 = st.columns(2)

    with col1:
        st.pyplot(
            plot_mf(
                md.universe,
                {k: md[k].mf for k in md.terms},
                "Market Demand"
            )
        )
        st.pyplot(
            plot_mf(
                ps.universe,
                {k: ps[k].mf for k in ps.terms},
                "Product Stock"
            )
        )

    with col2:
        st.pyplot(
            plot_mf(
                pc.universe,
                {k: pc[k].mf for k in pc.terms},
                "Production Capacity"
            )
        )
        st.pyplot(
            plot_mf(
                pi.universe,
                {k: pi[k].mf for k in pi.terms},
                "Product Import"
            )
        )

# =========================================================
# FUZZY SURFACE (3D VISUALIZATION)
# =========================================================
st.subheader("🧩 Fuzzy Surface (3D Visualization)")

if 'show_surface' not in st.session_state:
    st.session_state.show_surface = False

if st.button("🧩 Show"):
    st.session_state.show_surface = not st.session_state.show_surface

if st.session_state.show_surface:
    md_range = np.linspace(md.universe.min(), md.universe.max(), 30)
    ps_range = np.linspace(ps.universe.min(), ps.universe.max(), 30)

    fig_surface = plot_fuzzy_surface(
        system,
        md_range,
        ps_range,
        pc_fixed=100
    )

    st.pyplot(fig_surface)

# =========================================================
# DATA UPLOAD
# =========================================================
st.subheader("📂 Upload AnyLogic Data")
uploaded_file = st.file_uploader(
    "Upload CSV or Excel File",
    type=["csv", "xlsx"]
)

if uploaded_file:
    df = load_anylogic_data(uploaded_file)

    # ===== MONTHLY TIME SERIES HANDLING =====
    df['Month'] = pd.to_datetime(df['Month']).dt.to_period('M')

    # ===== STANDARDIZE COLUMN NAMES =====
    df = df.rename(columns={
        'Demand': 'Market_Demand',
        'Stock': 'Product_Stock',
        'Production': 'Production_Capacity'
    })

    st.success("✅ Data Successfully Uploaded")
    st.dataframe(df)

    # =====================================================
    # FUZZY PREDICTION
    # =====================================================
    if st.button("🔍 Run Fuzzy Prediction"):
        predictions = []

        for _, row in df.iterrows():
            pred = predict_import(
                system,
                row['Market_Demand'],
                row['Product_Stock'],
                row['Production_Capacity']
            )
            predictions.append(pred)

        df['Fuzzy_Import_Prediction'] = predictions

        st.session_state["fuzzy_result"] = df.copy()

        st.success("✅ Prediction Results Saved to Session")
        st.dataframe(df)

        # =================================================
        # RESULTS
        # =================================================
        st.subheader("📈 Import Prediction Results (Fuzzy System)")
        st.dataframe(df)

        # =================================================
        # TIME SERIES PLOT
        # =================================================
        st.subheader("📉 Time Series of Import Prediction")

        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(
            df['Month'].astype(str),
            df['Fuzzy_Import_Prediction'],
            marker='o'
        )
        ax.set_xlabel("Month")
        ax.set_ylabel("Import Volume")
        ax.set_title("Time Series of Fuzzy Import Prediction")
        ax.grid(True)
        plt.xticks(rotation=45)

        st.pyplot(fig)

        # =================================================
        # DOWNLOAD EXCEL
        # =================================================
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(
                writer,
                index=False,
                sheet_name='Fuzzy_Results'
            )

        output.seek(0)

        st.download_button(
            label="⬇️ Download Results (Excel)",
            data=output,
            file_name="fuzzy_import_predictions.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
