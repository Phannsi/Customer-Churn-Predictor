import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

st.set_page_config(
    page_title='Data',
    page_icon='📃',
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

    def load_data():
        df = pd.read_csv("./data/full_train_data.csv")
        return df

    def display_visualizations(data, selected_num_cols):
        st.title("Dashboard")
        
        # Example: Histograms for numerical columns
        for col in selected_num_cols:
            plt.figure(figsize=(8, 6))
            sns.histplot(data=data, x=col)
            st.pyplot()

    def data_page():
        st.title("Data Page")
        data = load_data()

        # Retrieve selected columns from the session state
        selected_cat_cols = st.session_state.get("selected_cat_cols", [])
        selected_num_cols = st.session_state.get("selected_num_cols", [])

        with st.sidebar:
            # Add selection widgets for categorical and numerical columns
            selected_cat_cols = st.multiselect("Select Categorical Columns", data.select_dtypes(include=['object']).columns, selected_cat_cols)
            selected_num_cols = st.multiselect("Select Numerical Columns", data.select_dtypes(include=['int64', 'float64']).columns, selected_num_cols)

            # Store the selections in Streamlit's session state
            st.session_state["selected_cat_cols"] = selected_cat_cols
            st.session_state["selected_num_cols"] = selected_num_cols
            st.session_state["data"] = data

            # Add checkbox to toggle displaying the whole dataset
            show_full_data = st.checkbox("Show Full Dataset")

            # Add checkbox to toggle displaying summary statistics
            show_summary_stats = st.checkbox("Show Summary Statistics")

        # Display summary statistics
        if show_summary_stats:
            rows, columns = data.shape
            st.subheader("Summary Statistics")
            st.write("Number of Rows:", rows)
            st.write("Number of Columns:", columns)

            for col in data.columns:
                if col in selected_cat_cols:
                    response_counts = data[col].value_counts()
                    st.write(f"\nColumn: {col}")
                    st.write(response_counts)

        # Display the selected columns of the data
        selected_data = data.loc[:, selected_cat_cols + selected_num_cols]
        st.subheader("Selected Data")
        st.dataframe(selected_data)

        # Display full dataset if selected
        if show_full_data:
            st.write(data)

        # Display visualizations on the dashboard page
        if "page" in st.session_state and st.session_state["page"] == "dashboard":
            display_visualizations(data, selected_num_cols)

    if __name__ == "__main__":
        
        data_page()


elif st.session_state['authentication_status'] == False:
    st.error('Wrong username or password')
elif st.session_state['authentication_status'] == None:
    st.info('Kindly login on the sidebar to gain access to the app')
    st.code('''
        Guest Account
        Username: guest
        Password: Guest123
    ''')