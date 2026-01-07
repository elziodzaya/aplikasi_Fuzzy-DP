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
# GLOBAL STYLE
# =============================
st.markdown("""
<style>
body {
    background: radial-gradient(circle at top, #102a43 0%, #081826 60%);
    color: #e5e7eb;
}

/* container */
.block-container {
    padding-top: 60px;
    max-width: 850px;
}

/* title */
.main-title {
    text-align: center;
    font-size: 30px;
    font-weight: 700;
    line-height: 1.45;
    color: #ffffff;
    margin-bottom: 18px;
}

/* subtitle */
.sub-title {
    text-align: center;
    font-size: 15px;
    color: #cbd5e1;
    margin-bottom: 28px;
}

/* author */
.author {
    text-align: center;
    font-size: 18px;
    font-weight: 600;
    letter-spacing: 1px;
    color: #f8fafc;
    margin-bottom: 32px;
}

/* info card */
.info-card {
    background: linear-gradient(180deg, #0f2a44, #0b2239);
    padding: 28px;
    border-radius: 14px;
    text-align: center;
    font-size: 14px;
    color: #e2e8f0;
    box-shadow: 0 10px 30px rgba(0,0,0,0.35);
}

/* button */
.button-wrap {
    display: flex;
    justify-content: center;
    margin: 45px 0;
}

/* declaration */
.declaration {
    margin-top: 40px;
    background: linear-gradient(180deg, #0b2239, #081a2c);
    padding: 26px;
    border-radius: 14px;
    font-size: 13px;
    color: #e5e7eb;
    box-shadow: 0 8px 25px rgba(0,0,0,0.4);
}

.declaration-title {
    text-align: center;
    font-weight: 600;
    margin-bottom: 14px;
    letter-spacing: 0.5px;
    color: #ffffff;
}

/* subtle divider */
.divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, #334155, transparent);
    margin: 35px 0;
}
</style>
""", unsafe_allow_html=True)

# =============================
# TITLE
# =============================
st.markdown("""
<div class="main-title">
DYNAMIC SYSTEM MODEL TO IMPROVE THE RATIO AND EFFICIENCY IN THE SUPPLY CHAIN
MANAGEMENT (SCM) DISTRIBUTION OF THE CEMENT INDUSTRY
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="sub-title">
AT BANTEN PROVINCE, INDONESIA
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="author">
YUDI MAULANA
</div>
""", unsafe_allow_html=True)

# =============================
# INFO CARD
# =============================
st.markdown("""
<div class="info-card">
A thesis submitted in fulfilment of the requirement for the award of the<br><br>
<b>Doctor of Philosophy in Mechanical Engineering</b><br><br>
Faculty of Mechanical and Manufacturing Engineering<br>
Universiti Tun Hussein Onn Malaysia<br><br>
January 2025
</div>
""", unsafe_allow_html=True)

# =============================
# BUTTON
# =============================
st.markdown("<div class='button-wrap'>", unsafe_allow_html=True)
if st.button("🚀 Enter Simulation Application"):
    st.session_state["page"] = "simulation"
st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

# =============================
# DECLARATION
# =============================
st.markdown("""
<div class="declaration">
<div class="declaration-title">STUDENT DECLARATION</div>

“I hereby declare that the work in this thesis is my own except for quotations
and summaries which have been duly acknowledged.”<br><br>

<b>Student:</b> Yudi Maulana<br>
<b>Date:</b> 22 January 2025<br><br>

<b>Supervisor:</b> Prof. Ir. Ts. Dr. Bukhari Bin Manshoor<br>
<b>Supervisor:</b> Ir. Dr.-Eng. Mairiza Zainuddin
</div>
""", unsafe_allow_html=True)

