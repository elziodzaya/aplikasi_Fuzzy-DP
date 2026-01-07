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
# CUSTOM CSS (MATCH IMAGE 1)
# =============================
st.markdown(
    """
    <style>
    body {
        background-color: #0b1c2d;
    }

    .block-container {
        padding-top: 40px;
    }

    .title {
        text-align: center;
        font-size: 26px;
        font-weight: 700;
        color: #ffffff;
        line-height: 1.4;
        margin-bottom: 15px;
    }

    .subtitle {
        text-align: center;
        font-size: 14px;
        color: #cbd5e1;
        margin-bottom: 25px;
    }

    .author {
        text-align: center;
        font-size: 18px;
        font-weight: 600;
        color: #ffffff;
        margin: 20px 0;
    }

    .section {
        text-align: center;
        font-size: 14px;
        color: #e2e8f0;
        margin-bottom: 6px;
    }

    .button-area {
        display: flex;
        justify-content: center;
        margin: 30px 0 40px 0;
    }

    .declaration {
        background-color: #0f2a44;
        padding: 22px;
        border-radius: 12px;
        color: #e5e7eb;
        font-size: 13px;
        margin-top: 30px;
    }

    .declaration-title {
        text-align: center;
        font-weight: 600;
        color: #ffffff;
        margin-bottom: 12px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# =============================
# MAIN TITLE
# =============================
st.markdown(
    """
    <div class="title">
    DYNAMIC SYSTEM MODEL TO IMPROVE THE RATIO AND EFFICIENCY IN THE SUPPLY CHAIN
    MANAGEMENT (SCM) DISTRIBUTION OF THE CEMENT INDUSTRY
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

# =============================
# AUTHOR
# =============================
st.markdown(
    """
    <div class="author">
    YUDI MAULANA
    </div>
    """,
    unsafe_allow_html=True
)

# =============================
# THESIS INFO
# =============================
st.markdown(
    """
    <div class="section">
    A thesis submitted in fulfilment of the requirement for the award of the
    </div>
    <div class="section">
    <b>Doctor of Philosophy in Mechanical Engineering</b>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="section">
    Faculty of Mechanical and Manufacturing Engineering
    </div>
    <div class="section">
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
st.markdown("<div class='button-area'>", unsafe_allow_html=True)
if st.button("🚀 Enter Simulation Application"):
    st.session_state["page"] = "simulation"
st.markdown("</div>", unsafe_allow_html=True)

# =============================
# STUDENT DECLARATION
# =============================
st.markdown(
    """
    <div class="declaration">
        <div class="declaration-title">STUDENT DECLARATION</div>
        <p>
        “I hereby declare that the work in this thesis is my own except for quotations
        and summaries which have been duly acknowledged.”
        </p>
        <p>
        <b>Student:</b> Yudi Maulana<br>
        <b>Date:</b> 22 January 2025
        </p>
        <p>
        <b>Supervisor:</b> Prof. Ir. Ts. Dr. Bukhari Bin Manshoor<br>
        <b>Supervisor:</b> Ir. Dr.-Eng. Mairiza Zainuddin
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

