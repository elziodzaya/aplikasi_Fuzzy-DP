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
# HERO HEADER 
# ==========================================================
st.markdown("""
<style>
/* Poster poster-like hero */
.hero {
    text-align: center;
    padding: 40px 20px 22px;
    background: #0b1a2b;
    color: white;
}
.hero-title {
    font-size: 72px;
    line-height: 1.05;
    font-weight: 900;
    margin: 0;
    letter-spacing: 1px;
}
.hero-subtitle {
    font-size: 28px;
    color: #e6f0fb;
    margin-top: 10px;
}
.hero-subtitle-muted {
    color: #a8c0e8;
}
.hero-divider {
    height: 2px;
    background: #1e2d4a;
    width: 60%;
    margin: 18px auto;
    border-radius: 4px;
}
.hero-meta {
    font-size: 16px;
    color: #dfeaf8;
    margin-top: 8px;
}
.hero-desc {
    font-size: 16px;
    color: #cbd5e1;
    max-width: 900px;
    margin: 14px auto 0;
}
.btn-enter {
    background-color: #2b6cb0;
    color: white;
    padding: 16px 38px;
    font-size: 20px;
    border-radius: 999px;
    border: none;
    text-decoration: none;
    display: inline-block;
    box-shadow: 0 6px 0 rgba(0,0,0,0.25);
}
.btn-enter:hover {
    background-color: #2463a8;
}
@media (max-width: 1200px) {
    .hero-title { font-size: 66px; }
}
@media (max-width: 900px) {
    .hero-title { font-size: 54px; }
}
@media (max-width: 600px) {
    .hero-title { font-size: 42px; }
}
</style>
""", unsafe_allow_html=True)

# Konten poster
st.markdown('<div class="hero">', unsafe_allow_html=True)
st.markdown('<div class="hero-title">DYNAMIC SYSTEM MODEL TO IMPROVE THE RATIO AND EFFICIENCY IN THE SUPPLY CHAIN MANAGEMENT (SCM) DISTRIBUTION OF THE CEMENT INDUSTRY</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-subtitle">AT BANTEN PROVINCE, INDONESIA</div>', unsafe_allow_html=True)

st.markdown('<div class="hero-subtitle-muted" style="font-weight:600; margin-top:6px;">YUDI MAULANA</div>', unsafe_allow_html=True)

st.markdown("""
<div class="hero-meta" style="margin-top:6px;">
  A thesis submitted in fulfilment of the requirement for the award of the
  <b>Doctor of Philosophy in Mechanical Engineering</b>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero-meta">
  <b>FACULTY OF MECHANICAL AND MANUFACTURING ENGINEERING</b><br/>
  <b>UNIVERSITI TUN HUSSEIN ONN MALAYSIA</b><br/>
  January 2025
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero-cta" style="margin-top:20px;">
  <a class="btn-enter" href="#simulate" aria-label="Enter Simulation Application">
    Enter Simulation Application
  </a>
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

st.divider()

