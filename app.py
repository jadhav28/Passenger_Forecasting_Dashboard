import streamlit as st
import pandas as pd
import numpy as np
from prophet import Prophet
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="SFO Passenger Dashboard", layout="wide")

# Load Data
df = pd.read_csv("Air_Traffic_Passenger_Statistics.csv")

# Clean and convert
df['Activity Period Start Date'] = pd.to_datetime(df['Activity Period Start Date'], errors='coerce')
df = df.dropna(subset=['Activity Period Start Date', 'Passenger Count', 'Operating Airline'])
df.rename(columns={'Activity Period Start Date': 'date'}, inplace=True)

# Aggregate monthly by airline using 'MS' for month start
monthly_data = df.groupby(
    ['Operating Airline', pd.Grouper(key='date', freq='MS')]
)['Passenger Count'].sum().reset_index()

# Sidebar - Airline and Date Range
st.sidebar.title("🔎 Filter Options")
airlines = sorted(monthly_data['Operating Airline'].unique())
selected_airline = st.sidebar.selectbox("Select Airline", airlines)

# Filter data for selected airline
airline_data = monthly_data[monthly_data['Operating Airline'] == selected_airline]
min_date, max_date = airline_data['date'].min(), airline_data['date'].max()

# Date range slider
date_range = st.sidebar.slider(
    "Select Date Range",
    min_value=min_date.to_pydatetime(),
    max_value=max_date.to_pydatetime(),
    value=(min_date.to_pydatetime(), max_date.to_pydatetime())
)

# Filtered data
filtered_data = airline_data[(airline_data['date'] >= date_range[0]) & (airline_data['date'] <= date_range[1])]

# =========================
# MAIN SECTION
# =========================
st.title("📊 San Francisco International Airport - Passenger Dashboard")
st.subheader(f"Monthly Passenger Count for {selected_airline}")

# Line Chart: Passenger Trend
fig1, ax1 = plt.subplots(figsize=(10, 4))
ax1.plot(filtered_data['date'], filtered_data['Passenger Count'], marker='o')
ax1.set_xlabel("Date")
ax1.set_ylabel("Passenger Count")
ax1.set_title("Passenger Trends")
ax1.grid(True)
st.pyplot(fig1)

# =========================
# PROPHET FORECAST
# =========================
st.subheader("📈 Forecast: Next 6 Months Passenger Count")

# Full airline data for forecasting
full_airline_data = monthly_data[monthly_data['Operating Airline'] == selected_airline]
prophet_df = full_airline_data[['date', 'Passenger Count']].rename(columns={'date': 'ds', 'Passenger Count': 'y'})

if len(prophet_df) < 24:
    st.warning("⚠️ Not enough data to generate a reliable forecast.")
else:
    model = Prophet(yearly_seasonality=True)
    model.fit(prophet_df)

    future = model.make_future_dataframe(periods=6, freq='MS')
    forecast = model.predict(future)
    forecast_filtered = forecast[forecast['ds'] > full_airline_data['date'].max()]

    # Forecast plot
    fig2, ax2 = plt.subplots(figsize=(10, 4))
    ax2.plot(full_airline_data['date'], full_airline_data['Passenger Count'], label="Historical")
    ax2.plot(forecast_filtered['ds'], forecast_filtered['yhat'], color='green', linestyle='--', label="Forecast")
    ax2.fill_between(forecast_filtered['ds'], forecast_filtered['yhat_lower'], forecast_filtered['yhat_upper'], alpha=0.3, color='green')
    ax2.set_title(f"{selected_airline} Forecast (Next 6 Months)")
    ax2.set_xlabel("Date")
    ax2.set_ylabel("Passenger Count")
    ax2.legend()
    ax2.grid(True)
    st.pyplot(fig2)

    with st.expander("🔍 Prophet Seasonality Components"):
        st.pyplot(model.plot_components(forecast))

# =========================
# ADDITIONAL INSIGHTS
# =========================

# Domestic vs International
st.markdown("### 🌍 Domestic vs International Traffic Split")
geo_summary = df.groupby('GEO Summary')['Passenger Count'].sum().reset_index()
fig4, ax4 = plt.subplots()
ax4.pie(geo_summary['Passenger Count'], labels=geo_summary['GEO Summary'], autopct='%1.1f%%', startangle=90)
ax4.axis('equal')
st.pyplot(fig4)

# Summary Stats
st.markdown("### 📊 Summary Stats")
col1, col2 = st.columns(2)
col1.metric("Total Passengers", f"{df['Passenger Count'].sum():,.0f}")
col2.metric("Data Range", f"{df['date'].min().date()} → {df['date'].max().date()}")
