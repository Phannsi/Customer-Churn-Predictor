import streamlit as st
import joblib
import pandas as pd
import datetime
import os

st.set_page_config(
    page_title='Predict',
    page_icon='🔮',
    layout='wide'
)

st.title('Churn Prediction')

def load_Logistic_regression_pipeline():
    pipeline = joblib.load("./models/logistic_reg_pipeline.joblib")
    return pipeline


def load_Gradient_boost_pipeline():
    pipeline = joblib.load("./models/gradient_boost_pipeline.joblib")
    return pipeline


def load_Support_vector_pipeline():
    pipeline = joblib.load("./models/support_vector_pipeline.joblib")
    return pipeline


@st.cache_data(show_spinner="Models Loading")
def cached_load_Logistic_regression_pipeline():
    return load_Logistic_regression_pipeline()


@st.cache_data(show_spinner="Models Loading")
def cached_load_Gradient_boost_pipeline():
    return load_Gradient_boost_pipeline()


@st.cache_data(show_spinner="Models Loading")
def cached_load_Support_vector_pipeline():
    return load_Support_vector_pipeline()


def select_model():
    col1, col2 = st.columns(2)

    with col1:
        selected_model = st.selectbox('Select a Model', options=['Logistic Regression', 'Gradient Boost', 'Support Vector'], key='selected_model')

    with col2:
        pass

    if selected_model == 'Logistic Regression':
        pipeline = cached_load_Logistic_regression_pipeline()
    elif selected_model == 'Support Vector':
        pipeline = cached_load_Support_vector_pipeline()
    else:
        pipeline = cached_load_Gradient_boost_pipeline()

    encoder = joblib.load("./models/encoder.joblib")

    return pipeline, encoder

if 'prediction' not in st.session_state:
    st.session_state['prediction'] = None

if 'probability' not in st.session_state:
    st.session_state['probability'] = None


def display_form():
    pipeline, encoder = select_model()

    with st.form('input-feature'):
        col1, col2, col3 = st.columns(3)

        with col1:
            st.write('### Personal Information')
            st.selectbox('Gender', options=['Male', 'Female'], key='gender')
            st.number_input('Senior Citizen', min_value=0, max_value=1, key='SeniorCitizen')
            st.selectbox('Partner', options=['Yes', 'No'], key='Partner')
            st.selectbox('Dependents', options=['Yes', 'No'], key='Dependents')
            st.number_input('Tenure', min_value=0, key='tenure')
            st.selectbox('Phone Service', options=['Yes', 'No'], key='PhoneService')
            st.selectbox('Multiple Lines', options=['Yes', 'No'], key='MultipleLines')

        with col2:
            st.write('### Work Information')
            st.selectbox('Internet Service', options=['DSL', 'Fiber optic', 'No'], key='InternetService')
            st.selectbox('Online Security', options=['No', 'Yes', 'No internet service'], key='OnlineSecurity')
            st.selectbox('Online Backup', options=['No', 'Yes', 'No internet service'], key='OnlineBackup')
            st.selectbox('Device Protection', options=['No', 'Yes', 'No internet service'], key='DeviceProtection')
            st.selectbox('Tech Support', options=['No', 'Yes', 'No internet service'], key='TechSupport')
            st.selectbox('Streaming TV', options=['No', 'Yes', 'No internet service'], key='StreamingTV')

        with col3:
            st.write('### Contract Information')
            st.selectbox('Streaming Movies', options=['No', 'Yes', 'No internet service'], key='StreamingMovies')
            st.selectbox('Contract', options=['Month-to-month', 'One year', 'Two year'], key='Contract')
            st.selectbox('Paperless Billing', options=['Yes', 'No'], key='PaperlessBilling')
            st.selectbox('Payment Method', options=['Electronic check', 'Mailed check', 'Bank transfer (automatic)', 'Credit card (automatic)'], key='PaymentMethod')
            st.number_input('Monthly Charges ($)', min_value=0.0, value=0.0, key='MonthlyCharges')
            st.number_input('Total Charges ($)', min_value=0.0, value=0.0, key='TotalCharges')
        
        submit_button = st.form_submit_button("Submit")

        if submit_button:
            prediction, probability = make_prediction(pipeline, encoder)
            st.session_state['prediction'] = prediction
            st.session_state['probability'] = probability

def make_prediction(pipeline, encoder):
    gender = st.session_state['gender']
    senior_citizen = st.session_state['SeniorCitizen']
    partner = st.session_state['Partner']
    dependents = st.session_state['Dependents']
    tenure = st.session_state['tenure']
    phone_service = st.session_state['PhoneService']
    multiple_lines = st.session_state['MultipleLines']
    internet_service = st.session_state['InternetService']
    online_security = st.session_state['OnlineSecurity']
    online_backup = st.session_state['OnlineBackup']
    device_protection = st.session_state['DeviceProtection']
    tech_support = st.session_state['TechSupport']
    streaming_tv = st.session_state['StreamingTV']
    streaming_movies = st.session_state['StreamingMovies']
    contract = st.session_state['Contract']
    paperless_billing = st.session_state['PaperlessBilling']
    payment_method = st.session_state['PaymentMethod']
    monthly_charges = st.session_state['MonthlyCharges']
    total_charges = st.session_state['TotalCharges']

    columns = ['gender', 'SeniorCitizen', 'Partner', 'Dependents', 'tenure', 'PhoneService',
               'MultipleLines', 'InternetService', 'OnlineSecurity', 'OnlineBackup',
               'DeviceProtection', 'TechSupport', 'StreamingTV', 'StreamingMovies',
               'Contract', 'PaperlessBilling', 'PaymentMethod', 'MonthlyCharges', 'TotalCharges']

    data = [[gender, senior_citizen, partner, dependents, tenure, phone_service,
             multiple_lines, internet_service, online_security, online_backup,
             device_protection, tech_support, streaming_tv, streaming_movies,
             contract, paperless_billing, payment_method, monthly_charges, total_charges]]


    # Create a DataFrame
    df = pd.DataFrame(data, columns=columns)
    
    # Make prediction
    pred = pipeline.predict(df)
    pred = int(pred[0])
    prediction = encoder.inverse_transform([pred])


    df['PredictionTime'] = datetime.datetime.now().strftime('%m-%d-%Y %H:%M:%S')
    df['ModelUsed'] = st.session_state['selected_model']
    df['Churn'] = prediction

    # Get probabilities
    probability = pipeline.predict_proba(df)

    # Write to CSV
    df.to_csv('./data/history.csv', mode='a', header=not os.path.exists('./data/history.csv'), index=False)

    # Updating state
    st.session_state['prediction'] = prediction
    st.session_state['probability'] = probability

    return prediction, probability


if __name__ == "__main__":

    display_form()

    prediction = st.session_state['prediction']
    probability = st.session_state['probability']

    if prediction is None:
        st.markdown("### The predicted outcome will show here")
    elif prediction == "Yes":
        probability_of_yes = probability[0][1] * 100
        st.markdown(f"### The customer will cease using your services with a probability of {round(probability_of_yes, 2)}%")
    else:
        probability_of_no = probability[0][0] * 100
        st.markdown(f"### customer will continue using your services with a probability of {round(probability_of_no, 2)}%")
