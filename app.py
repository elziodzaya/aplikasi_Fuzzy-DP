import streamlit as st

# ==========================================================
# PAGE CONFIG
# ==========================================================
st.set_page_config(
    page_title="Decision Support System Kebutuhan Impor Semen",
    page_icon="🏭",
    layout="wide"
)

# ==========================================================
# HERO HEADER – Versi B dengan tombol utama besar
# ==========================================================
# Tambahkan CSS inline untuk hero dengan tombol utama besar
st.markdown("""
<style>
/* Hero section styling (versi B) */
.hero {
    text-align: center;
    padding: 40px 20px 10px;
}

.hero-title {
    font-size: 72px;
    line-height: 1.05;
    font-weight: 900;
}
.hero-subtitle {
    font-size: 28px;
    color: #555;
    margin-top: 6px;
}
.hero-desc {
    font-size: 16px;
    color: #555;
    max-width: 900px;
    margin: 14px auto 0;
}
.hero-cta {
    margin-top: 26px;
}
@media (max-width: 1200px) {
    .hero-title { font-size: 64px; }
}
@media (max-width: 768px) {
    .hero-title { font-size: 42px; }
}
.btn-enter {
    background-color: #2b6cb0;
    color: white;
    padding: 18px 38px;
    font-size: 20px;
    border-radius: 12px;
    border: none;
    text-decoration: none;
    display: inline-block;
    box-shadow: 0 6px 0 rgba(0,0,0,0.15);
}
.btn-enter:hover {
    background-color: #2762a3;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="hero">', unsafe_allow_html=True)
st.markdown('<div class="hero-title">🏭 Decision Support System Kebutuhan Impor Semen</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-subtitle">Integrasi AnyLogic – Fuzzy Logic – Dynamic Programming</div>', unsafe_allow_html=True)

st.markdown("""
<div class="hero-desc">
 Sistem ini dirancang sebagai platform pendukung keputusan untuk memprediksi dan mengoptimalkan kebutuhan impor semen berbasis:
</div>
""", unsafe_allow_html=True)

st.markdown("""
- 🔁 Simulasi sistem dinamis (AnyLogic)
- 🧠 Sistem Fuzzy (Mamdani)
- 📐 Dynamic Programming deterministik (finite horizon)
""", unsafe_allow_html=True)

# Tombol utama besar "Enter Simulation Application"
st.markdown("""
<div class="hero-cta" style="text-align:center;">
  <a class="btn-enter" href="#enter-simulation" aria-label="Enter Simulation Application">
    Enter Simulation Application
  </a>
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

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
Menghasilkan **kebijakan impor optimal 12 bulan** dengan mempertimbangkan biaya dan hasil fuzzy.

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
        st.experimental_rerun()  # Sesuaikan dengan navigasi halaman jika ada

with col2:
    st.markdown("### 📐 Dynamic Programming")
    st.markdown("""
    - Optimasi impor 12 bulan  
    - Minimasi biaya total  
    - Kebijakan stok & impor
    """)
    if st.button("➡️ Masuk Halaman DP"):
        st.experimental_rerun()

with col3:
    st.markdown("### 📊 Analisis & Laporan")
    st.markdown("""
    - Evaluasi hasil fuzzy & DP  
    - Visualisasi kebijakan  
    - Unduh Excel & PDF
    """)
    if st.button("➡️ Masuk Halaman Laporan"):
        st.experimental_rerun()

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

st.info("💡 Gunakan navigasi untuk berpindah antar halaman.")
