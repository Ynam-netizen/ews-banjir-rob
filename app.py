import streamlit as st
import pandas as pd
import numpy as np
import joblib
import time
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go

# =========================
# CONFIG PAGE
# =========================
st.set_page_config(
    page_title="EWS Banjir Rob",
    layout="wide"
)


# =========================
# LOAD MODEL
# =========================
model = joblib.load("model.pkl")

# =========================
# HEADER + LOGO
# =========================
col1, col2, col3 = st.columns([1,6,1])

with col1:
    st.image("https://upload.wikimedia.org/wikipedia/id/c/ca/Stmkg-new.png", width=80)

with col2:
    st.markdown("<h1 style='text-align:center;'>🌊 Early Warning System Banjir Rob</h1>", unsafe_allow_html=True)

with col3:
    st.image("https://upload.wikimedia.org/wikipedia/commons/1/12/Logo_BMKG_%282010%29.png", width=80)

# =========================
# SIDEBAR INPUT
# =========================
st.sidebar.header("📥 Input Parameter")

curah_hujan = st.sidebar.slider("Curah Hujan (mm)", 0, 300, 100)
tekanan_udara = st.sidebar.slider("Tekanan Udara (hPa)", 950, 1050, 1005)
arah_angin = st.sidebar.slider("Arah Angin (°)", 0, 360, 180)
kecepatan_angin = st.sidebar.slider("Kecepatan Angin (m/s)", 0, 20, 5)
pasang_surut = st.sidebar.slider("Pasang Surut (m)", 0.0, 3.0, 1.5)
tinggi_gelombang = st.sidebar.slider("Tinggi Gelombang (m)", 0.0, 5.0, 2.0)

# =========================
# MAIN LAYOUT
# =========================
colA, colB = st.columns(2)

# =========================
# PREDIKSI
# =========================
input_data = pd.DataFrame([{
    'curah_hujan': curah_hujan,
    'tekanan_udara': tekanan_udara,
    'arah_angin': arah_angin,
    'kecepatan_angin': kecepatan_angin,
    'pasang_surut': pasang_surut,
    'tinggi_gelombang': tinggi_gelombang
}])

pred = model.predict(input_data)[0]

if hasattr(model, "predict_proba"):
    prob = model.predict_proba(input_data)[0][1]
else:
    prob = 0.5

# =========================
# OUTPUT STATUS
# =========================
with colA:
    st.subheader("🚨 Status Prediksi")

    if pred == 1:
        st.error("⚠️ BANJIR ROB TERDETEKSI")
    else:
        st.success("✅ TIDAK TERDETEKSI")

    # Gauge chart
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=prob*100,
        title={'text': "Probabilitas (%)"},
        gauge={
            'axis': {'range': [0,100]},
            'bar': {'color': "red"},
        }
    ))
    st.plotly_chart(fig, use_container_width=True)

# =========================
# PARAMETER VISUAL
# =========================
with colB:
    st.subheader("📊 Visual Parameter")

    param_df = pd.DataFrame({
        "Parameter": ["Hujan","Tekanan","Angin","Gelombang","Pasut"],
        "Nilai": [curah_hujan, tekanan_udara, kecepatan_angin, tinggi_gelombang, pasang_surut]
    })

    fig2 = px.bar(param_df, x="Parameter", y="Nilai", text="Nilai")
    st.plotly_chart(fig2, use_container_width=True)

# =========================
# REAL-TIME SIMULATION
# =========================
st.subheader("📈 Simulasi Data Real-Time (Dummy)")

placeholder = st.empty()

data = []

for i in range(20):
    new_data = {
        "waktu": datetime.now().strftime("%H:%M:%S"),
        "pasang_surut": pasang_surut + np.random.uniform(-0.3,0.3),
        "hujan": curah_hujan + np.random.uniform(-20,20)
    }

    data.append(new_data)
    df = pd.DataFrame(data)

    fig3 = px.line(df, x="waktu", y=["pasang_surut","hujan"],
                   title="Monitoring Real-Time")

    placeholder.plotly_chart(fig3, use_container_width=True)

    time.sleep(0.5)

# =========================
# HISTORY
# =========================
st.subheader("📋 Riwayat Prediksi")

if "history" not in st.session_state:
    st.session_state.history = []

st.session_state.history.append({
    "Waktu": datetime.now(),
    "Hujan": curah_hujan,
    "Pasut": pasang_surut,
    "Prediksi": "Banjir" if pred == 1 else "Aman"
})

hist_df = pd.DataFrame(st.session_state.history)
st.dataframe(hist_df.tail(5))

# =========================
# FOOTER
# =========================
st.markdown("---")
st.markdown("📡 Sistem Early Warning Banjir Rob Berbasis Machine Learning | STMKG")
