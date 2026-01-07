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
# GLOBAL CSS
# ======================================================
st.markdown(
    """
    <style>
    body {
        background: linear-gradient(180deg, #081826 0%, #0b2239 100%);
        color: #e5e7eb;
    }

    .block-container {
        padding-top: 40px;
        max-width: 900px;
    }

    /* HERO CARD */
    .hero {
        background: linear-gradient(180deg, #102a43, #0b2239);
        border-left: 6px solid #3b82f6;
        padding: 36px 32px 26px 32px;
        border-radius: 16px;
        box-shadow: 0 12px 35px rgba(0,0,0,0.45);
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

    .author {
        text-align: center;
        font-size: 18px;
        font-weight: 600;
        margin: 26px 0 30px 0;
        color: #f8fafc;
    }

    .info {
        background: #0f2a44;
        padding: 24px;
        border-radius: 14px;
        text-align: center;
        font-size: 14px;
        color: #e2e8f0;
        box-shadow: 0 8px 24px rgba(0,0,0,0.35);
        margin-bottom: 22px;
    }

    .declaration {
        background: #081a2c;
        padding: 24px;
        border-radius: 14px;
        font-size: 13px;
        color: #e5e7eb;
        box-shadow: 0 8px 24px rgba(0,0,0,0.4);
        margin-bottom: 10px;
    }

    .declaration-title {
        text-align: center;
        font-weight: 600;
        margin-bottom: 14px;
        color: #ffffff;
    }

    /* BUTTON POSITION */
    .hero-btn-anchor {
        height: 0;
    }

    .hero-btn {
        display: flex;
        justify-content: center;
        margin-top: -5px;
        margin-bottom: 5px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ======================================================
# HERO CONTENT (HTML RENDERED SAFELY)
# ======================================================
st.markdown(
    """
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
            January 2025
        </div>

        <div class="declaration">
            <div class="declaration-title">STUDENT DECLARATION</div>
            “I hereby declare that the work in this thesis is my own except for quotations
            and summaries which have been duly acknowledged.”<br><br>

            <b>Student:</b> Yudi Maulana<br>
            <b>Date:</b> 22 January 2025<br><br>

            <b>Supervisor:</b> Prof. Ir. Ts. Dr. Bukhari Bin Manshoor<br>
            <b>Supervisor:</b> Ir. Dr.-Eng. Mairiza Zainuddin
        </div>

        <div class="hero-btn-anchor"></div>
    </div>
    """,
    unsafe_allow_html=True
)

# ======================================================
# STREAMLIT BUTTON (INTERACTIVE)
# ======================================================
st.markdown("<div class='hero-btn'>", unsafe_allow_html=True)

if st.button("🚀 Enter Simulation Application"):
    st.switch_page("pages/1_Fuzzy_System.py")

st.markdown("</div>", unsafe_allow_html=True)
