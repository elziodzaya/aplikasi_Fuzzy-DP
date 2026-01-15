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

/* HERO TITLE CARD */
.hero {
    background: linear-gradient(180deg, #102a43, #0b2239);
    border-left: 6px solid #3b82f6;
    padding: 36px 32px;
    border-radius: 16px;
    box-shadow: 0 12px 35px rgba(0,0,0,0.45);
    margin-bottom: 30px;
}

.hero-title {
    text-align: center;
    font-size: 30px;
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

/* author */
.author {
    text-align: center;
    font-size: 18px;
    font-weight: 600;
    margin: 25px 0 30px 0;
    color: #f8fafc;
}

/* info card */
.info {
    background: #0f2a44;
    padding: 26px;
    border-radius: 14px;
    text-align: center;
    font-size: 14px;
    color: #e2e8f0;
    box-shadow: 0 10px 28px rgba(0,0,0,0.35);
}


/* button */
.btn-wrap {
    display: flex;
    justify-content: center;
    margin: 45px 0;
}

/* divider */
.divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, #334155, transparent);
    margin: 35px 0;
}

/* declaration */
.declaration {
    background: #081a2c;
    padding: 26px;
    border-radius: 14px;
    font-size: 13px;
    color: #e5e7eb;
    box-shadow: 0 8px 24px rgba(0,0,0,0.4);
}

.declaration-title {
    text-align: center;
    font-weight: 600;
    margin-bottom: 14px;
    color: #ffffff;
}
</style>
""", unsafe_allow_html=True)

# =============================
# HERO TITLE (VISIBLE & STRONG)
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
    <div class="info">
        A thesis submitted in fulfilment of the requirement for the award of the<br><br>
        <b>Doctor of Philosophy in Mechanical Engineering</b><br><br>
        Faculty of Mechanical and Manufacturing Engineering<br>
        Universiti Tun Hussein Onn Malaysia<br><br>
        January 2026
    </div>
    st.markdown("<div style='text-align:center; margin-top:-20px;'>", unsafe_allow_html=True)
        st.image(
            "assets/uthm_logo.png",
            width=110
        )
    <div class="declaration">
        <div class="declaration-title">STUDENT DECLARATION</div>
            “I hereby declare that the work in this thesis is my own except for quotations
            and summaries which have been duly acknowledged.”<br><br>
            <b>Student:</b> Yudi Maulana<br>
            <b>Date:</b> 22 January 2026<br><br>
            <b>Supervisor:</b> Prof. Ir. Ts. Dr. Bukhari Bin Manshoor<br>
            <b>Supervisor:</b> Ir. Dr.-Eng. Mairiza Zainuddin<br>
        </div>
    </div>
    
</div>
""", unsafe_allow_html=True)
# =============================
# ENTER APPLICATION BUTTON
# =============================
st.markdown("<br>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("🚀 Run Simulation ", use_container_width=True):
        st.switch_page("pages/1_Fuzzy_System.py")







