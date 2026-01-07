import streamlit as st

# ======================================================
# PAGE CONFIG
# ======================================================
st.set_page_config(
    page_title="Cement SCM Simulation",
    page_icon="🏭",
    layout="centered"
)

# ======================================================
# GLOBAL STYLE (AMAN)
# ======================================================
st.markdown("""
<style>
body {
    background-color: #0b2239;
    color: #e5e7eb;
}

.block-container {
    max-width: 900px;
    padding-top: 50px;
}

.card {
    background: linear-gradient(180deg, #102a43, #0b2239);
    border-left: 6px solid #3b82f6;
    padding: 36px;
    border-radius: 16px;
    box-shadow: 0 15px 40px rgba(0,0,0,0.45);
}

.title {
    text-align: center;
    font-size: 30px;
    font-weight: 800;
    line-height: 1.4;
    color: white;
}

.subtitle {
    text-align: center;
    margin-top: 12px;
    font-size: 15px;
    color: #cbd5e1;
}

.author {
    text-align: center;
    margin: 26px 0;
    font-size: 18px;
    font-weight: 600;
}

.section {
    background-color: #0f2a44;
    padding: 22px;
    border-radius: 14px;
    margin-bottom: 20px;
    font-size: 14px;
    text-align: center;
}

.declaration {
    background-color: #081a2c;
    padding: 22px;
    border-radius: 14px;
    font-size: 13px;
}

.declaration h4 {
    text-align: center;
    margin-bottom: 12px;
}
</style>
""", unsafe_allow_html=True)

# ======================================================
# MAIN CARD
# ======================================================
st.markdown("""
<div class="card">
    <div class="title">
        DYNAMIC SYSTEM MODEL TO IMPROVE THE RATIO AND EFFICIENCY IN THE SUPPLY CHAIN
        MANAGEMENT (SCM) DISTRIBUTION OF THE CEMENT INDUSTRY
    </div>

    <div class="subtitle">
        AT BANTEN PROVINCE, INDONESIA
    </div>

    <div class="author">
        YUDI MAULANA
    </div>

    <div class="section">
        A thesis submitted in fulfilment of the requirement for the award of the<br><br>
        <b>Doctor of Philosophy in Mechanical Engineering</b><br><br>
        Faculty of Mechanical and Manufacturing Engineering<br>
        Universiti Tun Hussein Onn Malaysia<br><br>
        January 2025
    </div>

    <div class="declaration">
        <h4>STUDENT DECLARATION</h4>
        “I hereby declare that the work in this thesis is my own except for quotations
        and summaries which have been duly acknowledged.”<br><br>

        <b>Student:</b> Yudi Maulana<br>
        <b>Date:</b> 22 January 2025<br><br>

        <b>Supervisor:</b> Prof. Ir. Ts. Dr. Bukhari Bin Manshoor<br>
        <b>Supervisor:</b> Ir. Dr.-Eng. Mairiza Zainuddin
    </div>
</div>
""", unsafe_allow_html=True)

# ======================================================
# BUTTON (STREAMLIT NATIF & STABIL)
# ======================================================
st.markdown("<br>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("🚀 Enter Simulation Application", use_container_width=True):
        st.switch_page("pages/1_Fuzzy_System.py")
