import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go

st.set_page_config(
    page_title='Dashboard',
    page_icon='📊',
    layout='wide'
)

st.set_option('deprecation.showPyplotGlobalUse', False)

# Load your EDA data
eda_data = pd.read_csv("./data/full_train_data.csv")

def show_histogram():
    """
    Displays a histogram of a numerical variable.
    """
    st.subheader('Histogram')
    column = st.selectbox('Select a numerical column', eda_data.columns)
    plt.hist(eda_data[column])
    st.pyplot()

def show_scatterplot():
    """
    Displays a scatter plot of two numerical variables.
    """
    st.subheader('Scatter Plot')
    x_column = st.selectbox('Select X-axis column', eda_data.columns)
    y_column = st.selectbox('Select Y-axis column', eda_data.columns)
    plt.scatter(eda_data[x_column], eda_data[y_column])
    st.pyplot()

def show_correlation_heatmap():
    """
    Displays a correlation heatmap of numerical variables.
    """
    st.subheader('Correlation Heatmap')
    corr = eda_data.corr()
    sns.heatmap(corr, annot=True)
    st.pyplot()

def main():
    st.title('Exploratory Data Analysis')

    # Display EDA visualizations
    show_histogram()
    show_scatterplot()
    show_correlation_heatmap()


def dashboard_page():
    st.title("Dashboard")

    # Check if data and selections are available from session state
    if "data" not in st.session_state or "selected_cat_cols" not in st.session_state or "selected_num_cols" not in st.session_state:
        st.error("Please select data and columns on the Data Page first!")
        return

    data = st.session_state.get("data")
    selected_cat_cols = st.session_state.get("selected_cat_cols")
    selected_num_cols = st.session_state.get("selected_num_cols")

    # Use st.container to structure the dashboard
    dashboard_container = st.container()

    # Categorical Columns Analysis
    with dashboard_container:
        st.write("Categorical Columns Analysis:")
        # Add a dropdown to choose chart type (optional)
        chart_type = st.selectbox("Select Chart Type", ["Bar Chart", "Pie Chart"])

        for col in selected_cat_cols:
            if chart_type == "Bar Chart":
                # Create a bar chart with different colors for each bar
                color_sequence = ["#0000FF", "#007FFF", "#00BFFF", "#1E90FF", "#4169E1", "#6495ED"]
                colors = color_sequence[:len(data[col].value_counts())]
                fig = go.Figure(data=[go.Bar(x=data[col].value_counts().index, y=data[col].value_counts(), marker_color=colors)])
                st.plotly_chart(fig)
            elif chart_type == "Pie Chart":
                # Create a pie chart
                labels = data[col].value_counts().index
                values = data[col].value_counts().values
                fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
                st.plotly_chart(fig)

    # Numerical Columns Analysis
    with dashboard_container:
        st.write("Numerical Columns Analysis:")
        # Add options to customize histogram parameters (optional)
        num_bins = st.slider("Number of Bins", 5, 20, 10)

        for col in selected_num_cols:
            # Create a histogram with different colors for each bar
            color_sequence = ["#0000FF", "#007FFF", "#00BFFF", "#1E90FF", "#4169E1", "#6495ED"]
            # Normalize the data for color assignment
            normalized_data = (data[col] - data[col].min()) / (data[col].max() - data[col].min())
            color_indices = np.round(normalized_data * (len(color_sequence) - 1)).astype(int)
            colors = [color_sequence[i] for i in color_indices]
            fig = go.Figure(data=[go.Histogram(x=data[col], nbinsx=num_bins, marker_color=colors)])
            st.plotly_chart(fig)


if __name__ == "__main__":
    dashboard_page()
    main()