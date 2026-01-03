import streamlit as st

# ==========================================================
# PAGE CONFIG
# ==========================================================
st.set_page_config(
    page_title="Decision Support System Impor Semen",
    page_icon="🏭",
    layout="wide"
)

# ==========================================================
# HEADER
# ==========================================================
st.title("🏭 Decision Support System Kebutuhan Impor Semen")
st.subheader("Integrasi AnyLogic – Fuzzy Logic – Dynamic Programming")

st.markdown("""
Sistem ini dikembangkan sebagai **platform pendukung keputusan**  
untuk memprediksi dan mengoptimalkan **kebutuhan impor semen** berbasis:

- 🔁 **Simulasi sistem dinamis (AnyLogic)**
- 🧠 **Sistem Fuzzy (Mamdani)**
- 📐 **Dynamic Programming deterministik (finite horizon)**
""")

st.divider()

# ==========================================================
# ALUR SISTEM
# ==========================================================
st.header("🔄 Alur Sistem Pendukung Keputusan")

st.markdown("""
1️⃣ **Simulasi AnyLogic**  
Menghasilkan data:
- Permintaan pasar
- Produksi
- Stok

2️⃣ **Sistem Fuzzy (Bulanan)**  
Memprediksi **kebutuhan impor ideal** berdasarkan kondisi operasional.

3️⃣ **Dynamic Programming (Tahunan)**  
Menghasilkan **kebijakan impor optimal 12 bulan**  
dengan mempertimbangkan biaya dan hasil fuzzy.

4️⃣ **Analisis & Laporan**  
Visualisasi, evaluasi kebijakan, dan laporan siap unduh.
""")

# ==========================================================
# NAVIGATION BUTTONS
# ==========================================================
st.header("🚀 Mulai Sistem")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 🧠 Sistem Fuzzy")
    st.markdown("""
    - Upload hasil simulasi AnyLogic  
    - Visualisasi fungsi keanggotaan  
    - Prediksi impor bulanan
    """)
    if st.button("➡️ Masuk Halaman Fuzzy"):
        st.switch_page("pages/1_Fuzzy_System.py")

with col2:
    st.markdown("### 📐 Dynamic Programming")
    st.markdown("""
    - Optimasi impor 12 bulan  
    - Minimasi biaya total  
    - Kebijakan stok & impor
    """)
    if st.button("➡️ Masuk Halaman DP"):
        st.switch_page("pages/2_DP.py")

with col3:
    st.markdown("### 📊 Analisis & Laporan")
    st.markdown("""
    - Evaluasi hasil fuzzy & DP  
    - Visualisasi kebijakan  
    - Unduh Excel & PDF
    """)
    if st.button("➡️ Masuk Halaman Laporan"):
        st.switch_page("pages/3_Analysis_and_Report.py")

st.divider()

# ==========================================================
# FOOTER
# ==========================================================
st.markdown("""
---
📌 **NOTE**  
Pendekatan ini merepresentasikan **Dynamic Programming deterministik finite horizon**  
dengan **Sistem Fuzzy Mamdani** sebagai mekanisme estimasi kebutuhan awal.

""")

st.info("💡 Gunakan sidebar untuk navigasi cepat antar halaman.")
