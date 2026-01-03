import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from modules.dp_model import dp_deterministic_horizon

# =========================================================
# CONFIG
# =========================================================
st.set_page_config(
    page_title="Dynamic Programming - Optimasi Impor",
    layout="wide"
)

st.title("⚙️ Optimasi Impor Menggunakan Dynamic Programming")
st.markdown("""
Halaman ini melakukan **optimasi keputusan impor** menggunakan  
**Dynamic Programming (DP)** dengan **hasil Fuzzy sebagai pembatas aksi**.
""")

# =========================================================
# UPLOAD DATA HASIL FUZZY
# =========================================================
st.subheader("📂 Upload Data Hasil Fuzzy")

uploaded_file = st.file_uploader(
    "Upload file Excel hasil prediksi Fuzzy",
    type=["xlsx"]
)

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    required_cols = [
        "Market_Demand",
        "Product_Stock",
        "Prediksi_Impor_Fuzzy"
    ]

    if not all(col in df.columns for col in required_cols):
        st.error(
            "❌ File tidak valid. Pastikan berasal dari halaman Fuzzy dan "
            "memiliki kolom: Market_Demand, Product_Stock, Prediksi_Impor_Fuzzy"
        )
        st.stop()

    st.success("✅ Data Fuzzy berhasil dimuat")
    st.dataframe(df)

    # =====================================================
    # PARAMETER DP
    # =====================================================
    st.subheader("🎛️ Parameter Dynamic Programming")

    col1, col2, col3 = st.columns(3)

    with col1:
        holding_cost = st.number_input(
            "Holding Cost / unit",
            min_value=0.0,
            value=2.0
        )

    with col2:
        import_cost = st.number_input(
            "Import Cost / unit",
            min_value=0.0,
            value=5.0
        )

    with col3:
        max_stock = st.number_input(
            "Kapasitas Gudang Maksimum",
            min_value=1,
            value=500
        )

    initial_stock = st.number_input(
        "Stok Awal",
        min_value=0,
        value=int(df["Product_Stock"].iloc[0])
    )

    # =====================================================
    # RUN DP
    # =====================================================
    if st.button("⚙️ Jalankan Optimasi DP"):
        demand = df["Market_Demand"].values
        fuzzy_import = df["Prediksi_Impor_Fuzzy"].values

        results_dp, total_cost = dp_deterministic_horizon(
            demand=demand,
            fuzzy_import=fuzzy_import,
            holding_cost=holding_cost,
            import_cost=import_cost,
            max_stock=int(max_stock),
            initial_stock=int(initial_stock)
        )

        # =================================================
        # HITUNG BIAYA PER PERIODE
        # =================================================
        results_dp["Import_Cost"] = (
            results_dp["Impor_Optimal"] * import_cost
        )
        results_dp["Holding_Cost"] = (
            results_dp["Stok_Akhir"] * holding_cost
        )

        results_dp["Total_Cost"] = (
            results_dp["Import_Cost"] +
            results_dp["Holding_Cost"]
        )

        # simpan ke session
        st.session_state["dp_result"] = results_dp.copy()
        st.session_state["dp_total_cost"] = total_cost

        st.success("✅ Hasil DP dan Total Cost disimpan ke session")

        # =================================================
        # HASIL DP
        # =================================================
        st.subheader("📊 Hasil Optimasi Dynamic Programming")
        st.dataframe(results_dp)

        st.metric(
            label="💰 Total Biaya Minimum (Kumulatif)",
            value=f"{results_dp['Total_Cost'].sum():,.2f}"
        )

        # =================================================
        # GRAFIK PERBANDINGAN
        # =================================================
        st.subheader("📈 Perbandingan Impor Fuzzy vs Impor Optimal (DP)")

        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(
            results_dp["Month"],
            results_dp["Impor_Fuzzy"],
            marker="o",
            label="Impor Fuzzy"
        )
        ax.plot(
            results_dp["Month"],
            results_dp["Impor_Optimal"],
            marker="s",
            label="Impor Optimal (DP)"
        )

        ax.set_xlabel("Month")
        ax.set_ylabel("Jumlah Impor")
        ax.set_title("Perbandingan Keputusan Impor")
        ax.legend()
        ax.grid(True)

        st.pyplot(fig)

        # =================================================
        # DOWNLOAD HASIL
        # =================================================
        st.subheader("⬇️ Download Hasil Optimasi")

        output = pd.ExcelWriter(
            "hasil_dp.xlsx",
            engine="openpyxl"
        )

        results_dp.to_excel(
            output,
            index=False,
            sheet_name="Hasil_DP"
        )

        output.close()

        with open("hasil_dp.xlsx", "rb") as f:
            st.download_button(
                label="⬇️ Download Hasil DP (Excel)",
                data=f,
                file_name="hasil_dp.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
