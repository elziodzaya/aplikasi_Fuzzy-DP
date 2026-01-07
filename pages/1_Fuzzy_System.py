import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from modules.fuzzy_system import build_fuzzy_system, predict_import
from modules.data_loader import load_anylogic_data
from modules.visualization import plot_mf, plot_fuzzy_surface
from io import BytesIO

# =========================================================
# CONFIG
# =========================================================
st.set_page_config(page_title="Fuzzy Import System", layout="wide")
st.title("📊 Prediksi Kebutuhan Impor Dengan Sistem Fuzzy")

# =========================================================
# BUILD FUZZY SYSTEM
# =========================================================
system, md, ps, pc, pi = build_fuzzy_system()

# =========================================================
# MEMBERSHIP FUNCTION (DENGAN TOMBOL)
# =========================================================
st.subheader("📐 Membership Function")

if 'show_mf' not in st.session_state:
    st.session_state.show_mf = False

if st.button("📐 Show "):
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
# FUZZY SURFACE (DENGAN TOMBOL)
# =========================================================
st.subheader("🧩 Surface Fuzzy (3D)")

if 'show_surface' not in st.session_state:
    st.session_state.show_surface = False

if st.button("🧩 Show "):
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
# UPLOAD DATA
# =========================================================
st.subheader("📂 Upload Data AnyLogic")
uploaded_file = st.file_uploader(
    "Upload file CSV / Excel",
    type=["csv", "xlsx"]
)

if uploaded_file:
    df = load_anylogic_data(uploaded_file)

    # ===== KONTROL BULAN (TIME SERIES BULANAN) =====
    df['Month'] = pd.to_datetime(df['Month']).dt.to_period('M')

    # ===== STANDARISASI NAMA KOLOM =====
    df = df.rename(columns={
        'Demand': 'Market_Demand',
        'Stock': 'Product_Stock',
        'Production': 'Production_Capacity'
    })

    st.success("✅ Data Uploaded")
    st.dataframe(df)

    # =====================================================
    # FUZZY PREDICTION
    # =====================================================
    if st.button("🔍 Fuzzy Prediction"):
        predictions = []

        for _, row in df.iterrows():
            pred = predict_import(
                system,
                row['Market_Demand'],
                row['Product_Stock'],
                row['Production_Capacity']
            )
            predictions.append(pred)

        df['Prediksi_Impor_Fuzzy'] = predictions

        st.session_state["fuzzy_result"] = df.copy()

        st.success("✅ Saved Result into session")
        st.dataframe(df)
        # =================================================
        # HASIL
        # =================================================
        st.subheader("📈 Import Prediction Result (Fuzzy)")
        st.dataframe(df)

        # =================================================
        # TIME SERIES PLOT
        # =================================================
        st.subheader("📉 Plot Time Series Import Prediction")

        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(
            df['Month'].astype(str),
            df['Prediksi_Impor_Fuzzy'],
            marker='o'
        )
        ax.set_xlabel("Bulan")
        ax.set_ylabel("Jumlah Impor")
        ax.set_title("Time Series Import Prediction")
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
                sheet_name='Hasil_Fuzzy'
            )

        output.seek(0)

        st.download_button(
            label="⬇️ Download Result (Excel)",
            data=output,
            file_name="fuzzy_predictions.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

