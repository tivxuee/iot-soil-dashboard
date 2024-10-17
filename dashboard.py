import streamlit as st
import pandas as pd

# Set Streamlit to use a wide layout
st.set_page_config(layout="wide")

# Function to load the local data file
def load_local_data(file_path):
    try:
        # Load the CSV data
        df = pd.read_csv(file_path)
        
        # Convert the timestamp to a datetime object and remove the timezone info
        df['timestamp'] = pd.to_datetime(df['timestamp']).dt.strftime('%Y-%m-%d %H:%M:%S')
        
        # Sort by timestamp in descending order (latest first)
        df = df.sort_values(by='timestamp', ascending=False)
        
        return df
    except FileNotFoundError:
        st.error("Local data file not found. Please fetch the data first.")
        return pd.DataFrame()

# Function to display prominent alert
def show_alert(message, alert_type="danger"):
    if alert_type == "danger":
        st.markdown(f"""
            <div style='background-color:#f44336;padding:10px;border-radius:5px'>
            <span style='color:white;font-size:20px;'>{message}</span>
            </div>
        """, unsafe_allow_html=True)
    elif alert_type == "warning":
        st.markdown(f"""
            <div style='background-color:#ff9800;padding:10px;border-radius:5px'>
            <span style='color:white;font-size:20px;'>{message}</span>
            </div>
        """, unsafe_allow_html=True)
    elif alert_type == "success":
        st.markdown(f"""
            <div style='background-color:#4CAF50;padding:10px;border-radius:5px'>
            <span style='color:white;font-size:20px;'>{message}</span>
            </div>
        """, unsafe_allow_html=True)

# Load the data from the local file
local_file = 'soil_data.csv'
df = load_local_data(local_file)

if df.empty:
    st.error("No data available in the local file.")
else:
    # Streamlit app to create the dashboard
    def create_dashboard(df):
        st.title("Soil Condition Dashboard")

        # Check moisture levels for alerts
        threshold_maxmoisture = 80
        if df['moisture'].max() > threshold_maxmoisture:
            show_alert(f"Critical Alert: Moisture exceeded {threshold_maxmoisture}%!", "danger")
        elif df['moisture'].min() < 20:
            show_alert(f"Warning: Moisture is below 20%", "warning")
        else:
            show_alert(f"Moisture levels are within safe range", "success")
        
        # Check temperature levels for alerts
        threshold_temperature = 30  # You can set any threshold value
        if df['temperature'].max() > threshold_temperature:
            show_alert(f"Critical Alert: Temperature exceeded {threshold_temperature}°C!", "danger")
        else:
            show_alert(f"Temperature levels are within safe range", "success")

        # Use columns for layout
        col1, col2 = st.columns([1, 3])  # Make the chart section wider

        # Add data overview on the left (col1)
        with col1:
            st.subheader("Data Overview")
            st.write(df)
        
        # Add charts on the right (col2)
        with col2:           
            # Plot temperature second with title
            st.markdown("<h3 style='text-align: center; color: #007BFF;'>Temperature Levels Over Time</h3>", unsafe_allow_html=True)
            st.line_chart(df.set_index('timestamp')['temperature'])

            # Plot pH last with title
            st.markdown("<h3 style='text-align: center; color: #007BFF;'>pH Levels Over Time</h3>", unsafe_allow_html=True)
            st.line_chart(df.set_index('timestamp')['pH'])

            st.markdown("<h3 style='text-align: center; color: #007BFF;'>Moisture Levels Over Time</h3>", unsafe_allow_html=True)
            st.line_chart(df.set_index('timestamp')['moisture'])

    # Call the create_dashboard function with the defined df
    create_dashboard(df)
