# SFO Passenger Traffic Dashboard

A Streamlit-powered interactive dashboard for analyzing and forecasting monthly airline passenger trends at San Francisco International Airport (SFO). This app uses historical data and the Prophet time series model to generate short-term passenger forecasts.

---

## Features

- Interactive Line Chart: Visualize monthly passenger volume by airline.
- Date Range Filter: Focus on specific time periods for selected airlines.
- Forecasting with Prophet: Predict passenger count for the next 6 months.
- Traffic Composition: See the share of domestic vs international passengers.
- Trend Insights: View seasonal patterns and long-term movement in passenger traffic.
- Summary Metrics: Key statistics including total passengers and data coverage period.

---

## Dataset

The application uses data from https://catalog.data.gov/dataset/air-traffic-passenger-statistics, which includes:
- `Operating Airline`
- `Passenger Count`
- `Activity Period Start Date`
- `GEO Summary` (Domestic or International)

---

## How to Run

1. Clone the repo or copy the app code into a Python file (e.g., `app.py`).
2. Install the required packages:

   ```bash
   pip install -r requirements.txt

## Demo
https://youtu.be/UMsRASAm1Mk
