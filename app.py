import streamlit as st
import base64

# =============================
# PAGE CONFIG
# =============================
st.set_page_config(
    page_title="Cement SCM Simulation",
    page_icon="🏭",
    layout="centered"
)

# =============================
# LOAD LOGO (BASE64)
# =============================
def img_to_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

uthm_logo_base64 = img_to_base64("assets/LOGO-UTM.png")

# =============================
# CSS STYLE
# =============================
st.markdown(f"""
<style>
body {{
    background: linear-gradient(180deg, #081826 0%, #0b2239 100%);
    color: #e5e7eb;
}}

.block-container {{
    padding-top: 40px;
    max-width: 900px;
}}

/* HERO */
.hero {{
    background: linear-gradient(180deg, #102a43, #0b2239);
    border-left: 6px solid #3b82f6;
    padding: 36px 32px 40px 32px;
    border-radius: 16px;
    box-shadow: 0 12px 35px rgba(0,0,0,0.45);
    margin-bottom: 28px;
}}

.hero-title {{
    text-align: center;
    font-size: 28px;
    font-weight: 800;
    line-height: 1.45;
    color: #ffffff;
}}

.hero-subtitle {{
    text-align: center;
    font-size: 15px;
    color: #cbd5e1;
    margin-top: 14px;
}}

.author {{
    text-align: center;
    font-size: 18px;
    font-weight: 600;
    margin-top: 22px;
    color: #f8fafc;
}}

/* UNIVERSITY CARD (WATERMARK) */
.uni-card {{
    background:
        linear-gradient(rgba(15,42,68,0.94), rgba(15,42,68,0.94)),
        url("data:image/png;base64,{uthm_logo_base64}");
    background-repeat: no-repeat;
    background-position: center;
    background-size: 200px;
    padding: 36px 24px;
    border-radius: 14px;
    text-align: center;
    color: #e2e8f0;
    box-shadow: 0 10px 28px rgba(0,0,0,0.35);
}}

.uni-degree {{
    font-weight: 700;
    font-size: 15px;
    color: #ffffff;
    margin-bottom: 14px;
}}

.uni-text {{
    font-size: 14px;
    line-height: 1.6;
}}

/* DECLARATION */
.declaration {{
    background: #081a2c;
    padding: 26px;
    border-radius: 14px;
    font-size: 13px;
    color: #e5e7eb;
    box-shadow: 0 8px 24px rgba(0,0,0,0.4);
    margin-top: 36px;
}}

.declaration-title {{
    text-align: center;
    font-weight: 600;
    margin-bottom: 14px;
    color: #ffffff;
}}

/* BUTTON */
.btn-wrap {{
    display: flex;
    justify-content: center;
    margin: 42px 0;
}}
</style>
""", unsafe_allow_html=True)

# =============================
# HERO + UNIVERSITY CARD
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

    <div style="margin-top:30px;">
        <div class="uni-card">
            <div class="uni-degree">
                Doctor of Philosophy in Mechanical Engineering
            </div>
            <div class="uni-text">
                Faculty of Mechanical and Manufacturing Engineering<br>
                Universiti Tun Hussein Onn Malaysia
            </div>
        </div>
    </div>

</div>
""", unsafe_allow_html=True)

# =============================
# YEAR
# =============================
st.markdown(
    "<div style='text-align:center; margin-top:10px; color:#cbd5e1;'>January 2026</div>",
    unsafe_allow_html=True
)

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

