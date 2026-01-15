import streamlit as st

# =============================
# PAGE CONFIG
# =============================
st.set_page_config(
    page_title="Cement SCM Simulation",
    page_icon="🏭",
    layout="centered"
)

# =============================
# CSS STYLE
# =============================
st.markdown("""
<style>
body {
    background: linear-gradient(180deg, #081826 0%, #0b2239 100%);
    color: #e5e7eb;
}

/* main width */
.block-container {
    padding-top: 40px;
    max-width: 900px;
}

/* HERO CARD */
.hero {
    background: linear-gradient(180deg, #102a43, #0b2239);
    border-left: 6px solid #3b82f6;
    padding: 36px 32px;
    border-radius: 16px;
    box-shadow: 0 12px 35px rgba(0,0,0,0.45);
    margin-bottom: 30px;
}

/* TITLE */
.hero-title {
    text-align: center;
    font-size: 28px;
    font-weight: 800;
    line-height: 1.45;
    color: #ffffff;
    letter-spacing: 0.4px;
}

.hero-subtitle {
    text-align: center;
    font-size: 15px;
    color: #cbd5e1;
    margin-top: 14px;
}

/* AUTHOR */
.author {
    text-align: center;
    font-size: 18px;
    font-weight: 600;
    margin: 25px 0 30px 0;
    color: #f8fafc;
}

/* UNIVERSITY CARD */
.uni-card {
    background: #0f2a44;
    padding: 26px 20px 32px 20px;
    border-radius: 14px;
    text-align: center;
    color: #e2e8f0;
    box-shadow: 0 10px 28px rgba(0,0,0,0.35);
}

.uni-degree {
    font-weight: 700;
    font-size: 15px;
    color: #ffffff;
    margin-bottom: 16px;
}

.uni-text {
    font-size: 14px;
    line-height: 1.6;
}

/* DECLARATION */
.declaration {
    background: #081a2c;
    padding: 26px;
    border-radius: 14px;
    font-size: 13px;
    color: #e5e7eb;
    box-shadow: 0 8px 24px rgba(0,0,0,0.4);
    margin-top: 35px;
}

.declaration-title {
    text-align: center;
    font-weight: 600;
    margin-bottom: 14px;
    color: #ffffff;
}

/* BUTTON */
.btn-wrap {
    display: flex;
    justify-content: center;
    margin: 45px 0;
}
</style>
""", unsafe_allow_html=True)

# =============================
# HERO SECTION
# =============================
st.markdown("""
<div class="hero">
    <div class="hero-title">
        DYNAMIC SYSTEM MODEL TO IMPROVE THE RATIO AND EFFICIENCY IN THE SUPPLY CHAIN
        MANAGEMENT (SCM) DISTRIBUTION OF THE CEMENT INDUSTRY
    </div>

    <div class="hero-subtitle">
        AT BANTEN PROVINCE, INDONESIA
    </div>

    <div class="author">
        YUDI MAULANA
    </div>
</div>
""", unsafe_allow_html=True)

# =============================
# UNIVERSITY CARD + LOGO
# =============================
st.markdown("""
<div class="uni-card">
    <div class="uni-degree">
        Doctor of Philosophy in Mechanical Engineering
    </div>
    <div class="uni-text">
        Faculty of Mechanical and Manufacturing Engineering<br>
        Universiti Tun Hussein Onn Malaysia
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<div style='text-align:center; margin-top:-22px;'>", unsafe_allow_html=True)
st.image("assets/LOGO-UTM.png", width=110)
st.markdown("</div>", unsafe_allow_html=True)

st.markdown("""
<div style="text-align:center; margin-top:10px; color:#cbd5e1;">
    January 2026
</div>
""", unsafe_allow_html=True)

# =============================
# STUDENT DECLARATION
# =============================
st.markdown("""
<div class="declaration">
    <div class="declaration-title">STUDENT DECLARATION</div>
    “I hereby declare that the work in this thesis is my own except for quotations
    and summaries which have been duly acknowledged.”<br><br>

    <b>Student:</b> Yudi Maulana<br>
    <b>Date:</b> 22 January 2026<br><br>

    <b>Supervisor:</b> Prof. Ir. Ts. Dr. Bukhari Bin Manshoor<br>
    <b>Supervisor:</b> Ir. Dr.-Eng. Mairiza Zainuddin
</div>
""", unsafe_allow_html=True)

# =============================
# RUN SIMULATION BUTTON
# =============================
st.markdown("<div class='btn-wrap'>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("🚀 Run Simulation", use_container_width=True):
        st.switch_page("pages/1_Fuzzy_System.py")

st.markdown("</div>", unsafe_allow_html=True)
