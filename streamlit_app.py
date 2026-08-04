import streamlit as st
import pandas as pd
import joblib
import base64
import time

st.set_page_config(
    page_title="FleetSense AI",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
#MainMenu{visibility:hidden;}
footer{visibility:hidden;}
header{visibility:hidden;}
[data-testid="stSidebar"]{display:none;}
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_resources():
    model = joblib.load("model.joblib")
    scaler = joblib.load("scaler.joblib")
    return model, scaler

model, scaler = load_resources()

def get_base64(file):
    with open(file,"rb") as f:
        return base64.b64encode(f.read()).decode()

bg = get_base64("background.jpg")

st.markdown(f"""
<style>

.stApp{{
background:
linear-gradient(rgba(0,0,0,.55),rgba(0,0,0,.55)),
url("data:image/jpeg;base64,{bg}");
background-size:cover;
background-position:center;
background-repeat:no-repeat;
background-attachment:fixed;
}}

.block-container{{
max-width:700px;
margin:auto;
padding-top:80px;
}}

.container{{
background:rgba(0,0,0,.65);
backdrop-filter:blur(18px);
padding:40px;
border-radius:20px;
box-shadow:0 10px 40px rgba(0,0,0,.5);
}}

.title{{
text-align:center;
font-size:40px;
font-weight:bold;
color:#FFD54F;
margin-bottom:25px;
}}

label{{
color:white!important;
font-weight:bold!important;
font-size:36px!important;
}}

.stTextInput input{{
    background:#2f2f2f!important;
    color:grey!important;
    border:1px solid #9e9e9e!important;
    border-radius:12px!important;
    font-size:18px!important;
}}

.stTextInput input::placeholder{{
    color:grey!important;
    opacity:1!important;
}}

.stButton>button{{
background:linear-gradient(90deg,#ff512f,#dd2476);
color:white;
}}

.bottom{{
text-align:center;
color:white;
}}

.stNumberInput label{{
    color:white!important;
    font-size:30px!important;
    font-weight:bold!important;
}}

</style>
""", unsafe_allow_html=True)


st.markdown("""
<div class="title">
Vehicle Engine Prediction
</div>
""",unsafe_allow_html=True)
## Decimal Numeric Inputs

engine_temp = st.number_input(
    "Engine Temperature (°C)",
    min_value=0.0,
    max_value=150.0,
    value=0.0,
    step=0.1,
    format="%.2f"
)

coolant_temp = st.number_input(
    "Coolant Temperature (°C)",
    min_value=0.0,
    max_value=150.0,
    value=0.0,
    step=0.1,
    format="%.2f"
)

engine_load = st.number_input(
    "Engine Load (%)",
    min_value=0.0,
    max_value=150.0,
    value=0.0,
    step=0.1,
    format="%.2f"
)

vehicle_speed = st.number_input(
    "Vehicle Speed (km/h)",
    min_value=0.0,
    max_value=150.0,
    value=0.0,
    step=0.1,
    format="%.2f"
)

st.write("")

predict = st.button("Predict Engine Status")

st.markdown("""
<div class="bottom">
AI Powered Vehicle Telemetry Monitoring System
</div>
""", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)
if predict:

    try:

        data = pd.DataFrame({
            "engine_temp_c":[float(engine_temp)],
            "coolant_temp_c":[float(coolant_temp)],
            "engine_load_percent":[float(engine_load)],
            "vehicle_speed_kph":[float(vehicle_speed)]
        })

        with st.spinner("Analyzing Vehicle Data..."):
            time.sleep(2)
        data_scaled = scaler.transform(data)
        prediction = model.predict(data_scaled)[0]

        st.markdown("<br>", unsafe_allow_html=True)

        if prediction == "No Engine Failure":

            st.success("✅ No Engine Failure")

        else:

            st.error("⚠ Engine Failure")

        st.markdown("""
        <div style="
        background:rgba(255,255,255,.10);
        padding:18px;
        border-radius:12px;
        margin-top:15px;
        color:white;
        ">
        <h4 style="color:#FFD54F;">Input Summary</h4>
        </div>
        """, unsafe_allow_html=True)

        summary = pd.DataFrame({
            "Parameter":[
                "Engine Temperature",
                "Coolant Temperature",
                "Engine Load",
                "Vehicle Speed"
            ],
            "Value":[
                f"{engine_temp} °C",
                f"{coolant_temp} °C",
                f"{engine_load} %",
                f"{vehicle_speed} km/h"
            ]
        })

        st.table(summary)

    except ValueError:

        st.warning("Please enter valid numeric values.")
st.markdown("""
<style>

.stSuccess{
background:rgba(34,197,94,.15)!important;
border-radius:12px!important;
border:1px solid #22c55e!important;
}

.stError{
background:rgba(239,68,68,.15)!important;
border-radius:12px!important;
border:1px solid #ef4444!important;
}

.stWarning{
background:rgba(245,158,11,.15)!important;
border-radius:12px!important;
border:1px solid #f59e0b!important;
}

table{
background:rgba(255,255,255,.08)!important;
border-radius:12px!important;
overflow:hidden;
}

thead tr th{
background:#FFD54F!important;
color:black!important;
font-size:16px!important;
}

tbody tr td{
background:rgba(255,255,255,.05)!important;
color:white!important;
font-size:15px!important;
}

hr{
border:1px solid rgba(255,255,255,.15);
}

</style>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

st.markdown("""
<div style='text-align:center;color:white;font-size:14px;'>

FleetSense AI • Vehicle Predictive Maintenance System

</div>
""", unsafe_allow_html=True)
