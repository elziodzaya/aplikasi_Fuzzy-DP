import streamlit as st
import base64
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Cement SCM Simulation",
    page_icon="🏭",
    layout="centered"
)

# =============================
# LOAD LOGO BASE64
# =============================
def img_to_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

logo = img_to_base64("assets/LOGO-UTM.png")

# =============================
# FULL HTML (ANTI RUSAK)
# =============================
html_code = f"""
<!DOCTYPE html>
<html>
<head>
<style>
body {{
    margin: 0;
    background: linear-gradient(180deg, #081826, #0b2239);
    font-family: Arial, sans-serif;
    color: #e5e7eb;
}}

.container {{
    max-width: 900px;
    margin: 40px auto;
}}

.hero {{
    background: linear-gradient(180deg, #102a43, #0b2239);
    border-left: 6px solid #3b82f6;
    padding: 36px;
    border-radius: 16px;
    box-shadow: 0 12px 35px rgba(0,0,0,0.45);
}}

.hero-title {{
    text-align: center;
    font-size: 28px;
    font-weight: 800;
    color: #ffffff;
    line-height: 1.45;
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
}}

.uni-card {{
    margin-top: 30px;
    background:
        linear-gradient(rgba(15,42,68,0.94), rgba(15,42,68,0.94)),
        url("data:image/png;base64,{logo}");
    background-repeat: no-repeat;
    background-position: center;
    background-size: 200px;
    padding: 36px;
    border-radius: 14px;
    text-align: center;
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

.year {{
    text-align: center;
    margin-top: 12px;
    color: #cbd5e1;
}}

.declaration {{
    margin-top: 36px;
    background: #081a2c;
    padding: 26px;
    border-radius: 14px;
    font-size: 13px;
    box-shadow: 0 8px 24px rgba(0,0,0,0.4);
}}

.declaration-title {{
    text-align: center;
    font-weight: 600;
    margin-bottom: 14px;
    color: #ffffff;
}}
</style>
</head>

<body>
<div class="container">

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

    <div class="year">January 2026</div>

    <div class="declaration">
        <div class="declaration-title">STUDENT DECLARATION</div>
        “I hereby declare that the work in this thesis is my own except for quotations
        and summaries which have been duly acknowledged.”<br><br>

        <b>Student:</b> Yudi Maulana<br>
        <b>Date:</b> 22 January 2026<br><br>

        <b>Supervisor:</b> Prof. Ir. Ts. Dr. Bukhari Bin Manshoor<br>
        <b>Supervisor:</b> Ir. Dr.-Eng. Mairiza Zainuddin
    </div>

</div>
</body>
</html>
"""

components.html(html_code, height=1000)

# =============================
# BUTTON (STREAMLIT NATIVE)
# =============================
col1, col2, col3 = st.columns([1,2,1])
with col2:
    if st.button("🚀 Run Simulation", use_container_width=True):
        st.switch_page("pages/1_Fuzzy_System.py")

