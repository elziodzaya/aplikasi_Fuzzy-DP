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
# HERO HEADER - Centered poster with improved typography  
# ==========================================================  
st.markdown("""  
<style>  
/* Poster poster-like hero - center aligned with refined typography */  
:root {  
    --bg: #0b1a2b;  
    --fg: #ffffff;  
    --muted: #dbe7ff;  
    --subtle: #aabded;  
    --btn: #2b6cb0;  
}  
* { box-sizing: border-box; }  

.hero-wrapper {  
    text-align: center;  
    padding: 48px 20px 28px;  
    background: var(--bg);  
    color: var(--fg);  
}  

.hero-title {  
    font-family: "Inter", system-ui, -apple-system, "Segoe UI", Roboto, Arial;  
    font-size: 64px;  
    line-height: 1.08;  
    font-weight: 900;  
    letter-spacing: 0.5px;  
    margin: 0 auto;  
    max-width: 1100px;  
}  

.hero-subtitle {  
    font-family: "Inter", system-ui, -apple-system, "Segoe UI", Roboto, Arial;  
    font-size: 26px;  
    color: var(--muted);  
    margin-top: 12px;  
}  

.hero-subtitle-muted {  
    color: #cbd8ff;  
    font-weight: 600;  
    margin-top: 8px;  
}  

.hero-meta,  
.hero-meta strong {  
    font-family: "Inter", system-ui, -apple-system, "Segoe UI", Roboto, Arial;  
    color: #e8f0ff;  
}  
.hero-desc {  
    font-family: "Inter", system-ui, -apple-system, "Segoe UI", Roboto, Arial;  
    font-size: 15.5px;  
    color: #d6e4f9;  
    max-width: 900px;  
    margin: 12px auto 0;  
    line-height: 1.6;  
}  

.btn-enter {  
    background-color: #2b6cb0;  
    color: white;  
    padding: 14px 34px;  
    font-size: 18px;  
    border-radius: 999px;  
    border: none;  
    text-decoration: none;  
    display: inline-block;  
    margin-top: 18px;  
    box-shadow: 0 6px 0 rgba(0,0,0,0.25);  
    font-weight: 700;  
}  
.btn-enter:hover {  
    background-color: #2463a8;  
}  
.hero-divider {  
    height: 2px;  
    background: #1e2d4a;  
    width: 60%;  
    margin: 18px auto;  
    border-radius: 4px;  
}  
@media (max-width: 1200px) {  
    .hero-title { font-size: 56px; }  
}  
@media (max-width: 900px) {  
    .hero-title { font-size: 48px; }  
    .hero-subtitle { font-size: 22px; }  
}  
@media (max-width: 600px) {  
    .hero-title { font-size: 38px; }  
    .hero-subtitle { font-size: 20px; }  
}  
</style>  
""", unsafe_allow_html=True)  

# Konten poster - centered  
st.markdown('<div class="hero-wrapper">', unsafe_allow_html=True)  
st.markdown('<div class="hero-title">DYNAMIC SYSTEM MODEL TO IMPROVE THE RATIO AND EFFICIENCY IN THE SUPPLY CHAIN MANAGEMENT (SCM) DISTRIBUTION OF THE CEMENT INDUSTRY</div>', unsafe_allow_html=True)  
st.markdown('<div class="hero-subtitle">AT BANTEN PROVINCE, INDONESIA</div>', unsafe_allow_html=True)  
st.markdown('<div class="hero-subtitle-muted" style="margin-top:6px;">YUDI MAULANA</div>', unsafe_allow_html=True)

st.markdown("""
<div class="hero-meta" style="margin-top:6px;">
  A thesis submitted in fulfilment of the requirement for the award of the
  <b>Doctor of Philosophy in Mechanical Engineering</b>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero-meta" style="margin-top:6px;">
  <b>FACULTY OF MECHANICAL AND MANUFACTURING ENGINEERING</b><br/>
  <b>UNIVERSITI TUN HUSSEIN ONN MALAYSIA</b><br/>
  January 2025
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero-cta" style="margin-top:20px; text-align:center;">
  <a class="btn-enter" href="#simulate" aria-label="Enter Simulation Application">
    Enter Simulation Application
  </a>
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

st.divider()
