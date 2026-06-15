%%writefile app_diabetes.py
import streamlit as st
import numpy as np
import pickle

# Setup interface properties
st.set_page_config(
    page_title="Diabetes AI Diagnostic Center",
    page_icon="🩺",
    layout="centered"
)

# Custom Theme with a Medical Digital Wallpaper Graphic
st.markdown("""
    <style>
    .stApp {
        background-image: linear-gradient(rgba(15, 23, 42, 0.88), rgba(15, 23, 42, 0.96)), 
                          url("https://img.freepik.com/free-vector/abstract-medical-wallpaper-template-design_53876-61841.jpg");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        color: #f8fafc;
    }
    .stNumberInput div div input {
        background-color: rgba(30, 41, 59, 0.9) !important;
        color: #38bdf8 !important;
        border: 2px solid #14b8a6 !important;
        border-radius: 8px;
        font-weight: bold;
    }
    label p {
        color: #e2e8f0 !important;
        font-weight: 600 !important;
    }
    div.stButton > button:first-child {
        background: linear-gradient(90deg, #0284c7 0%, #0d9488 100%);
        color: white;
        border-radius: 10px;
        border: none;
        padding: 14px 20px;
        font-size: 18px;
        font-weight: bold;
        box-shadow: 0 6px 20px rgba(13, 148, 136, 0.4);
        transition: all 0.3s ease;
        width: 100%;
        margin-top: 15px;
    }
    div.stButton > button:first-child:hover {
        background: linear-gradient(90deg, #38bdf8 0%, #14b8a6 100%);
        box-shadow: 0 0 25px #14b8a6;
        color: #0f172a;
    }
    .result-card {
        padding: 25px;
        border-radius: 12px;
        text-align: center;
        font-size: 26px;
        font-weight: bold;
        margin-top: 30px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.4);
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🩺 Diabetes Diagnostic AI  Assistant")
st.markdown("### Early Screening Portal using Machine Learning SVM")
st.write("Fill in the patient's metrics below to run the diagnostic predictive system.")
st.markdown("---")

# Model Loader
try:
    with open('diabetes_model.pkl', 'rb') as f_model:
        model = pickle.load(f_model)
    with open('diabetes_scaler.pkl', 'rb') as f_scaler:
        scaler = pickle.load(f_scaler)
except FileNotFoundError:
    st.error("🚨 Configuration Error: Missing saved data. Please re-run your notebook cells to save the model files.")
    st.stop()

# Split Input Rows
col1, col2 = st.columns(2)
with col1:
    pregnancies = st.number_input("Pregnancies Count", min_value=0, max_value=20, value=8, step=1)
    glucose = st.number_input("Glucose Level (mg/dL)", min_value=0, max_value=300, value=183)
    blood_pressure = st.number_input("Blood Pressure (mm Hg)", min_value=0, max_value=200, value=64)
    skin_thickness = st.number_input("Triceps Skin Fold Thickness (mm)", min_value=0, max_value=100, value=0)

with col2:
    insulin = st.number_input("2-Hour Serum Insulin (mu U/ml)", min_value=0, max_value=900, value=0)
    bmi = st.number_input("Body Mass Index (BMI)", min_value=0.0, max_value=70.0, value=23.3, format="%.1f")
    dpf = st.number_input("Diabetes Pedigree Function Score", min_value=0.000, max_value=3.000, value=0.672, format="%.3f")
    age = st.number_input("Patient Age (Years)", min_value=1, max_value=120, value=32, step=1)

if st.button("RUN DIAGNOSTIC CHECK"):
    features = [pregnancies, glucose, blood_pressure, skin_thickness, insulin, bmi, dpf, age]
    input_array = np.asarray(features).reshape(1, -1)
    standardized_features = scaler.transform(input_array)
    prediction = model.predict(standardized_features)
    
    if prediction[0] == 0:
        st.markdown(
            '<div class="result-card" style="background-color: rgba(34, 197, 94, 0.2); border: 2px solid #22c55e; color: #22c55e;">'
            '💚 THE PATIENT IS NOT DIABETIC'
            '</div>', 
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            '<div class="result-card" style="background-color: rgba(239, 68, 68, 0.2); border: 2px solid #ef4444; color: #ef4444;">'
            '🚨 ALERT: THE PATIENT IS PREDICTED DIABETIC'
            '</div>', 
            unsafe_allow_html=True
        )
