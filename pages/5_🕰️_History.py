import streamlit as st
import numpy as np
import pandas as pd
from typing import List, Tuple
import os
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader



st.set_page_config(
page_title="Prediction History",
page_icon="🕰️",
layout="wide",
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

    # function to display title in a streamlit container
    def display_title_container():
        with st.container(border=True):
            st.markdown(""" ### 🕰️ Prediction History """)

        st.markdown(
            "<style>div.block-container{padding-top:1rem;}</style>", unsafe_allow_html=True
        )


    def display_history():
        try:
            data = pd.read_csv("./data/history.csv")
            st.dataframe(data)
        except FileNotFoundError:
            st.info("No predictions have been made yet!")


    def main():
        display_title_container()
        display_history()


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