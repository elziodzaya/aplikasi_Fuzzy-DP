import streamlit as st

# =============================
# PAGE CONFIG
# =============================
st.set_page_config(
    page_title="Cement Supply Chain Simulation",
    page_icon="🏭",
    layout="centered"
)

# =============================
# CUSTOM CSS
# =============================
st.markdown(
    """
    <style>
    body {
        background-color: #0b1c2d;
    }
    .main {
        background: linear-gradient(180deg, #0b1c2d 0%, #102a43 100%);
        padding: 30px;
        border-radius: 12px;
    }
    .title {
        text-align: center;
        font-size: 26px;
        font-weight: 700;
        color: white;
        margin-bottom: 10px;
    }
    .subtitle {
        text-align: center;
        font-size: 15px;
        color: #cbd5e1;
        margin-bottom: 20px;
    }
    .author {
        text-align: center;
        font-size: 18px;
        font-weight: 600;
        color: white;
        margin: 15px 0;
    }
    .section {
        text-align: center;
        font-size: 14px;
        color: #e2e8f0;
        margin-top: 10px;
    }
    .button-container {
        display: flex;
        justify-content: center;
        margin-top: 25px;
        margin-bottom: 30px;
    }
    .declaration-box {
        background-color: #0f2a44;
        padding: 20px;
        border-radius: 10px;
        margin-top: 30px;
        color: #e5e7eb;
        font-size: 13px;
    }
    .declaration-title {
        text-align: center;
        font-weight: 600;
        margin-bottom: 10px;
        color: white;
    }
    .footer {
        font-size: 12px;
        margin-top: 15px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# =============================
# MAIN CONTENT
# =============================
st.markdown("<div class='main'>", unsafe_allow_html=True)

st.markdown(
    """
    <div class="title">
    DYNAMIC SYSTEM MODEL TO IMPROVE THE RATIO AND EFFICIENCY IN THE SUPPLY CHAIN MANAGEMENT (SCM) DISTRIBUTION OF THE CEMENT INDUSTRY
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="subtitle">
    AT BANTEN PROVINCE, INDONESIA
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="author">
    YUDI MAULANA
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="section">
    A thesis submitted in fulfilment of the requirement for the award of the<br>
    <b>Doctor of Philosophy in Mechanical Engineering</b>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="section">
    Faculty of Mechanical and Manufacturing Engineering<br>
    Universiti Tun Hussein Onn Malaysia
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="section">
    January 2025
    </div>
    """,
    unsafe_allow_html=True
)

# =============================
# BUTTON
# =============================
st.markdown("<div class='button-container'>", unsafe_allow_html=True)
if st.button("🚀 Enter Simulation Application"):
    st.session_state["page"] = "simulation"
st.markdown("</div>", unsafe_allow_html=True)

# =============================
# STUDENT DECLARATION
# =============================
st.markdown(
    """
    <div class="declaration-box">
        <div class="declaration-title">STUDENT DECLARATION</div>
        <p>
        “I hereby declare that the work in this thesis is my own except for quotations and summaries which have been duly acknowledged.”
        </p>
        <div class="footer">
        <b>Student:</b> Yudi Maulana<br>
        <b>Date:</b> 22 January 2025<br><br>
        <b>Supervisor:</b> Prof. Ir. Ts. Dr. Bukhari Bin Manshoor<br>
        <b>Supervisor:</b> Ir. Dr.-Eng. Mairiza Zainuddin
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("</div>", unsafe_allow_html=True)

