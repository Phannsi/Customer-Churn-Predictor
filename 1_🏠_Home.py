import streamlit as st



## page configuration settings
st.set_page_config(
page_title="Home", page_icon="🏠", layout="wide"
)


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
how_to_run_text = "To run the application, simply navigate through the sidebar and select the dataset you wish to analyze. Follow the instructions on each page."

key_features_text = """
- Data Visualization
- Predictive Analytics
- Customizable Reports
- Interactive Dashboards
"""
user_benefits_text = """
- Understand employee attrition trends
- Identify key factors affecting attrition
- Make data-driven decisions
- Improve employee retention strategies
"""
def logo():
    col1, col2, col3 = st.columns(3)

    with col1:
        pass

    with col2:
        with st.container(border=True):
                st.image('https://upload.wikimedia.org/wikipedia/commons/thumb/f/ff/Logo_vodafone_new.png/1200px-Logo_vodafone_new.png')
    with col3:
        pass

# Layout with columns
def home_intro_text():
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("Customer Churn Insight")
        st.write(home_text)

    with col2:
        # Key features section
        st.subheader("Key Features")
        st.write(key_features_text)
    
    with col3:
        # User benefits section
        st.subheader("User Benefits")
        st.write(user_benefits_text)

    
    st.subheader("How to Run Application")
    st.write(how_to_run_text)


def display_home_body():
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Key Features")
        st.markdown(
            """     
                    - **A Data Page:** explore the content of proprietory data loaded in real-time form the remote server
                    - **A Dashboard Page:** presents visualizations on both the exploratory data and the KPIs
                    - **A Predict Page:** predict customer churn using a selected model of choice
                    - **A History Page:** contains saved predictions for further analysis later. Users can view the history of their prediction input values
            """
        )

    with col2:
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
                    - Follow instructions on each page to interact with the App
                    """
        )


def main():
    
    display_contact()

    display_home_title()

    logo()

    home_intro_text()

    display_home_body()

    


if __name__ == "__main__":

    main()


