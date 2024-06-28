import streamlit as st
import joblib
import pandas as pd
import datetime
import os
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

st.set_page_config(
    page_title='Bulk Predict',
    page_icon='📦',
    layout='wide'
)

with open('./config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['pre-authorized']
)

name, username, authentication_status = authenticator.login(location='sidebar')

if st.session_state['authentication_status'] == True:

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

    def csv_form():
        st.write("Please upload your table in csv format only, Kindly ensure it contain all the necessary columns")

        # Display file uploader
        uploaded_file = st.file_uploader("Upload a CSV file", type="csv")

        if uploaded_file is not None:
            # Read the uploaded file as a pandas DataFrame
            df = pd.read_csv(uploaded_file)

            # Display the DataFrame
            st.dataframe(df)


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

        df['PredictionTime'] = datetime.date.today()
        df['ModelUsed'] = st.session_state['selected_model']
        df['Prediction'] = st.session_state['prediction']

        # Make prediction
        pred = pipeline.predict(df)
        pred = int(pred[0])
        prediction = encoder.inverse_transform([pred])

        # Get probabilities
        probability = pipeline.predict_proba(df)

        # Write to CSV
        df.to_csv('./data/history.csv', mode='a', header=not os.path.exists('./data/history.csv'), index=False)

        # Updating state
        st.session_state['prediction'] = prediction
        st.session_state['probability'] = probability

        return prediction, probability


    if __name__ == "__main__":

        st.info('Please ensure your table has the following columns and headers' 
                ['gender', 'SeniorCitizen', 'Partner', 'Dependents', 'tenure', 'PhoneService',
                'MultipleLines', 'InternetService', 'OnlineSecurity', 'OnlineBackup',
                'DeviceProtection', 'TechSupport', 'StreamingTV', 'StreamingMovies',
                'Contract', 'PaperlessBilling', 'PaymentMethod', 'MonthlyCharges', 'TotalCharges'
                ]
        )

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


elif st.session_state['authentication_status'] == False:
    st.error('Wrong username or password')
elif st.session_state['authentication_status'] == None:
    st.info('Kindly login on the sidebar to gain access to the app')
    st.code('''
        Guest Account
        Username: guest
        Password: Guest123
    ''')