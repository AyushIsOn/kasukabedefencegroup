import streamlit as st
import pandas as pd
import pickle
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# Load the trained model
import pickle
# Load the trained model
with open('ML Practice.pkl', 'rb') as model_file:
    logistic = pickle.load(model_file)

# Streamlit app
st.title('Cancer Prediction')

# Sidebar for user input
st.sidebar.title('Enter Patient Information')

# Input fields for user parameters
radius_mean = st.sidebar.number_input('Radius Mean', value=0.0)
texture_mean = st.sidebar.number_input('Texture Mean', value=0.0)
perimeter_mean = st.sidebar.number_input('Perimeter Mean', value=0.0)
area_mean = st.sidebar.number_input('Area Mean', value=0.0)
smoothness_mean = st.sidebar.number_input('Smoothness Mean', value=0.0)
compactness_mean = st.sidebar.number_input('Compactness Mean', value=0.0)
concavity_mean = st.sidebar.number_input('Concavity Mean', value=0.0)
concave_points_mean = st.sidebar.number_input('Concave Points Mean', value=0.0)
symmetry_mean = st.sidebar.number_input('Symmetry Mean', value=0.0)
fractal_dimension_mean = st.sidebar.number_input('Fractal Dimension Mean', value=0.0)

radius_se = st.sidebar.number_input('Radius SE', value=0.0)
texture_se = st.sidebar.number_input('Texture SE', value=0.0)
perimeter_se = st.sidebar.number_input('Perimeter SE', value=0.0)
area_se = st.sidebar.number_input('Area SE', value=0.0)
smoothness_se = st.sidebar.number_input('Smoothness SE', value=0.0)
compactness_se = st.sidebar.number_input('Compactness SE', value=0.0)
concavity_se = st.sidebar.number_input('Concavity SE', value=0.0)
concave_points_se = st.sidebar.number_input('Concave Points SE', value=0.0)
symmetry_se = st.sidebar.number_input('Symmetry SE', value=0.0)
fractal_dimension_se = st.sidebar.number_input('Fractal Dimension SE', value=0.0)

radius_worst = st.sidebar.number_input('Radius Worst', value=0.0)
texture_worst = st.sidebar.number_input('Texture Worst', value=0.0)
perimeter_worst = st.sidebar.number_input('Perimeter Worst', value=0.0)
area_worst = st.sidebar.number_input('Area Worst', value=0.0)
smoothness_worst = st.sidebar.number_input('Smoothness Worst', value=0.0)
compactness_worst = st.sidebar.number_input('Compactness Worst', value=0.0)
concavity_worst = st.sidebar.number_input('Concavity Worst', value=0.0)
concave_points_worst = st.sidebar.number_input('Concave Points Worst', value=0.0)
symmetry_worst = st.sidebar.number_input('Symmetry Worst', value=0.0)
fractal_dimension_worst = st.sidebar.number_input('Fractal Dimension Worst', value=0.0)

# Predict on user input
if st.sidebar.button('Predict'):
    # Make prediction
    user_data = [[radius_mean, texture_mean, perimeter_mean, area_mean, smoothness_mean,
                  compactness_mean, concavity_mean, concave_points_mean, symmetry_mean,
                  fractal_dimension_mean, radius_se, texture_se, perimeter_se, area_se,
                  smoothness_se, compactness_se, concavity_se, concave_points_se, symmetry_se,
                  fractal_dimension_se, radius_worst, texture_worst, perimeter_worst, area_worst,
                  smoothness_worst, compactness_worst, concavity_worst, concave_points_worst,
                  symmetry_worst, fractal_dimension_worst]]  # Adjust input based on your model's requirements
    prediction = logistic.predict(user_data)

    # Display prediction result
    if prediction[0] == 0:
        st.write('Prediction: Benign')
    else:
        st.write('Prediction: Malignant')
