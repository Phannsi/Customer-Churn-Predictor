import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader


## page configuration settings
st.set_page_config(
page_title="Home",
page_icon="🏠",
layout="wide"
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
    def display_contact():
        st.sidebar.write(
            """
        Let's connect, Your feedback, questions and recommendations are welcome.
        """
        )


        with st.container(border=True):st.sidebar.write(
            """
    <div style="display: flex; justify-content: center; background-color: white; padding: 10px; border-radius: 10px;">
        <a href="https://github.com/Phannsi" style="padding: 5px; list-style-type: none; text-decoration: none;">
            <img src="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png" width="35px"></img>
        </a>
        <a href="https://www.linkedin.com/in/ezekielphannsi" style="padding: 5px; list-style-type: none; text-decoration: none;">
            <img src="https://i.pinimg.com/736x/96/8e/a6/968ea62882943e88bbd318ae5fa67429.jpg" width="35px"></img>
        </a>
    </div>
    """,
            unsafe_allow_html=True,
        )


    ## put title element in container
    def display_home_title():
        with st.container(border=True):
            st.markdown(
                "<h1 style='text-align: center;  font-size: 36px; color: red'>Welcome to The Customer Churn Prediction App! </h1>",
                unsafe_allow_html=True,
            )

    # Sample text for the sections
    home_text = "Welcome to the Telco Customer churn predictor application. Here, you can analyze customer churn data to predict churn."
    how_to_run_text = "To run the application, simply login and navigate through the sidebar. Follow the instructions on each page to run application effectively."


    def logo():
        col1, col2, col3 = st.columns(3)

        with col1:
            pass

        with col2:
            with st.container(border=True):
                    st.image('https://upload.wikimedia.org/wikipedia/commons/thumb/f/ff/Logo_vodafone_new.png/1200px-Logo_vodafone_new.png')
        with col3:
            pass


    def display_home_body():
        col1, col2 = st.columns(2)

        with col1:
            with st.container(border=True):
                st.subheader("Key Features")
                st.markdown(
                    """     
                            - **A Data Page:** explore the content of proprietory data loaded
                            - **A Dashboard Page:** presents visualizations on both the exploratory data and the KPIs, you have the option of selection your own columns to visualise
                            - **A Predict Page:** predict customer churn using a selected model of choice
                            - **A Bulk predict page:** allows you to make several predictions at once when you upload in csv format
                            - **A History Page:** contains saved predictions for further analysis later. Users can view the history of their prediction there
                    """
                )

        with col2:
            with st.container(border=True):
                st.subheader("User Benefits")
                st.markdown(
                    """
                            - Make data-driven decisions by leveraging the power of predictive analytics
                            - Free to Select from a list classification models
                            - Simple and straight forward. 
                            """
                )
                st.subheader("Instruction")
                st.markdown(
                    """
                            - Use the side bar to navigate the pages of the App
                            - Follow instructions on each page to interact with the App effectively
                            """
                )

        # Center-align text using CSS styles
        centered_text1 = f"<p style='text-align: center;'>This application was built as a data Science project for Azubi Africa!</p>"
        centered_text2 = f"<p style='text-align: center;'>Copyright © 2024!</p>"
        

        
        st.write(centered_text1, unsafe_allow_html=True)
        
        st.write(centered_text2, unsafe_allow_html=True)
       
        

    def main():
        
        display_contact()

        display_home_title()

        logo()

        display_home_body()


    if __name__ == "__main__":

        main()  


elif st.session_state['authentication_status'] == False:
    st.error('Wrong username or password')
elif st.session_state['authentication_status'] == None:
    st.info('Kindly login on the sidebar to gain access to the app')
    st.code('''
        Guest Account
        Username: guest
        Password: Guest123
    ''')
