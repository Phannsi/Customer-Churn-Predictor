import streamlit as st
import joblib
import pandas as pd
import datetime
import os

st.set_page_config(
    page_title='Bulk Predict',
    page_icon='📦',
    layout='wide'
)

st.title('Bulk Churn Prediction')

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

if 'uploaded_file' not in st.session_state:
    st.session_state['uploaded_file'] = None

def csv_form():
    pipeline, encoder = select_model()

    st.write("Please upload your table in CSV format. Kindly ensure it contains all the necessary columns.")

    # Display file uploader
    uploaded_file = st.file_uploader("Upload a CSV file", type="csv")

    if uploaded_file is not None:
        # Read the uploaded file as a pandas DataFrame
        df = pd.read_csv(uploaded_file)

        # Make predictions
        predictions = []
        for index, row in df.iterrows():
            pred = pipeline.predict([row])
            pred = pred[0]
            prediction = encoder.inverse_transform([pred])
            predictions.append(prediction[0])

            # Assign prediction result to the specific cell
            df.at[index, 'PredictionTime'] = datetime.datetime.now().strftime('%m-%d-%Y %H:%M:%S')
            df.at[index, 'ModelUsed'] = st.session_state['selected_model']
            df.at[index, 'Churn'] = prediction[0]

        # Get probabilities
        probability = pipeline.predict_proba(df)

        # Write to CSV
        df.to_csv('./data/history.csv', mode='a', header=not os.path.exists('./data/bulk_history.csv'), index=False)

        # Update session state
        st.session_state['prediction'] = predictions
        st.session_state['probability'] = probability
        st.session_state['df'] = df


if __name__ == "__main__":
    csv_form()

    #df = st.session_state['df']
    prediction = st.session_state['prediction']
    probability = st.session_state['probability']

    if df is None:
        st.write("Please upload a CSV file to make a prediction.")
    else:
        st.write(st.session_state['df'])