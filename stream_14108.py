import streamlit as st
import joblib
import numpy as np
import pandas as pd

# Load model
model = joblib.load("simpan_model/Decision_Tree_tuned (1).pkl")

# Mapping hasil prediksi numerik ke label asli
mapping_nobeyesdad = {
    'Insufficient_Weight': 0,
    'Normal_Weight': 1,
    'Overweight_Level_I': 2,
    'Overweight_Level_II': 3,
    'Obesity_Type_I': 4,
    'Obesity_Type_II': 5,
    'Obesity_Type_III': 6
}
reverse_mapping_nobeyesdad = {v: k for k, v in mapping_nobeyesdad.items()}

# Tambahkan background dan style dengan markdown + HTML
st.markdown(
    """
    <style>
        body {
            background-color: #f0f2f6;
        }
        .main {
            background-color: #ffffff;
            padding: 2rem;
            border-radius: 10px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        }
        h1 {
            color: #0066cc;
            text-align: center;
            margin-bottom: 30px;
        }
        .stButton>button {
            background-color: #0066cc;
            color: white;
            font-weight: bold;
            border-radius: 5px;
            padding: 0.5em 1em;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Judul
st.markdown('<div class="main">', unsafe_allow_html=True)
st.title("🔍 Prediksi Tingkat Obesitas Berdasarkan Data Pribadi")

# Input user
st.subheader("📋 Silakan Isi Data Berikut:")
gender = st.selectbox("👤 Jenis Kelamin", ["Male", "Female"])
age = st.number_input("🎂 Usia", min_value=1, max_value=120)
height = st.number_input("📏 Tinggi Badan (meter)", min_value=1.0, step=0.01)
weight = st.number_input("⚖️ Berat Badan (kg)", min_value=1.0, step=0.1)
family_history = st.selectbox("🧬 Riwayat obesitas di keluarga?", ["yes", "no"])
favc = st.selectbox("🍔 Konsumsi makanan tinggi kalori?", ["yes", "no"])
fcvc = st.slider("🥦 Konsumsi sayur tiap makan (1=Jarang, 3=Sering)", 1, 3)
ncp = st.slider("🍽️ Jumlah makan besar per hari", 1, 5)
caec = st.selectbox("🍪 Ngemil di luar jam makan?", ["no", "Sometimes", "Frequently", "Always"])
smoke = st.selectbox("🚬 Apakah Anda merokok?", ["yes", "no"]) 
ch2o = st.slider("💧 Konsumsi air harian (liter)", 0.5, 5.0, step=0.1)
scc = st.selectbox("🧾 Pantau asupan kalori harian?", ["yes", "no"])
faf = st.slider("🏃 Frekuensi olahraga per minggu (jam)", 0.0, 10.0, step=0.5)
tue = st.slider("💻 Waktu menggunakan teknologi per hari (jam)", 0, 24)
calc = st.selectbox("🍷 Konsumsi alkohol", ["no", "Sometimes", "Frequently", "Always"])
mtrans = st.selectbox("🚗 Transportasi utama", ["Public_Transportation", "Walking", "Automobile", "Motorbike", "Bike"])

# Mapping input user ke numerik
def encode_input():
    return [
        1 if gender == "Male" else 0,
        age,
        height,
        weight,
        1 if family_history == "yes" else 0,
        1 if favc == "yes" else 0,
        fcvc,
        ncp,
        {"no": 0, "Sometimes": 1, "Frequently": 2, "Always": 3}[caec],
        1 if smoke == "yes" else 0,
        ch2o,
        1 if scc == "yes" else 0,
        faf,
        tue,
        {"no": 0, "Sometimes": 1, "Frequently": 2, "Always": 3}[calc],
        {
            "Public_Transportation": 0,
            "Walking": 1,
            "Automobile": 2,
            "Motorbike": 3,
            "Bike": 4
        }[mtrans]
    ]

# Tombol prediksi
if st.button("🎯 Prediksi Tingkat Obesitas"):
    input_data = np.array([encode_input()])
    prediction_num = model.predict(input_data)[0]
    prediction_label = reverse_mapping_nobeyesdad[prediction_num]
    
    st.markdown(f"""
    <div style="background-color:#dff0d8; padding: 1rem; border-radius: 10px; text-align: center; margin-top: 20px;">
        <h3>✅ Hasil Prediksi:</h3>
        <h2 style="color:#3c763d;">{prediction_label.replace("_", " ")}</h2>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
