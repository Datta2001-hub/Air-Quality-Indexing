import os
import joblib
import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="AirSource | GP-01", page_icon="🌍", layout="wide")
st.title("🌍 AirSource")
st.caption("GP-01 · Air Quality Monitoring & Exploratory Source Attribution")
st.info("Prototype notice: upload real station data for analysis. Source shares are heuristic indicators, not verified source-apportionment measurements.")

DATA_PATH = "data/air_quality.csv"
MODEL_PATH = "models/aqi_bucket_model.joblib"

@st.cache_data
def load_data(path):
    return pd.read_csv(path)

df = None
uploaded = st.sidebar.file_uploader("Upload air_quality.csv", type=["csv"])
try:
    if uploaded is not None:
        df = pd.read_csv(uploaded)
    elif os.path.exists(DATA_PATH):
        df = load_data(DATA_PATH)
except Exception as e:
    st.error(f"Could not read dataset: {e}")

if df is None:
    st.warning("No dataset loaded. Download the India Air Quality dataset and place its CSV at data/air_quality.csv, or upload it in the sidebar.")
    st.markdown("[Dataset source: Kaggle – Air Quality Data in India](https://www.kaggle.com/datasets/rohanrao/air-quality-data-in-india)")
    st.stop()

df.columns = [str(c).strip() for c in df.columns]
numeric_candidates = ["PM2.5", "PM10", "NO", "NO2", "NOx", "NH3", "CO", "SO2", "O3", "AQI"]
available = [c for c in numeric_candidates if c in df.columns]
for c in available:
    df[c] = pd.to_numeric(df[c], errors="coerce")

if "City" in df.columns:
    cities = ["All"] + sorted(df["City"].dropna().astype(str).unique().tolist())
    city = st.sidebar.selectbox("City", cities)
    if city != "All":
        df = df[df["City"].astype(str) == city]

if "Date" in df.columns:
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

if "AQI" in df.columns and df["AQI"].notna().any():
    aqi = df["AQI"].median()
    st.metric("Median AQI in selected data", f"{aqi:.0f}")
else:
    aqi = None
    st.metric("Records loaded", f"{len(df):,}")

c1, c2, c3 = st.columns(3)
for col, label in zip([c1,c2,c3], ["PM2.5","PM10","NO2"]):
    if label in df.columns and df[label].notna().any():
        col.metric(f"Median {label}", f"{df[label].median():.1f}")
    else:
        col.metric(f"Median {label}", "Not available")

st.subheader("Pollutant trends")
trend_col = st.selectbox("Pollutant", available, index=available.index("PM2.5") if "PM2.5" in available else 0) if available else None
if trend_col:
    plot_df = df.dropna(subset=[trend_col]).copy()
    if "Date" in plot_df.columns and plot_df["Date"].notna().any():
        trend = plot_df.groupby("Date", as_index=False)[trend_col].mean()
        st.plotly_chart(px.line(trend, x="Date", y=trend_col, title=f"{trend_col} over time"), use_container_width=True)
    else:
        st.plotly_chart(px.histogram(plot_df, x=trend_col, title=f"{trend_col} distribution"), use_container_width=True)

st.subheader("AQI category model")
if os.path.exists(MODEL_PATH):
    bundle = joblib.load(MODEL_PATH)
    features = bundle["features"]
    model = bundle["model"]
    if all(f in df.columns for f in features):
        sample = df[features].dropna()
        if not sample.empty:
            pred = model.predict(sample.tail(1))[0]
            st.success(f"Model prediction for the latest complete row: **{pred}**")
            st.caption("This predicts the dataset's AQI_Bucket label. It does not identify emission sources.")
        else:
            st.warning("No complete feature row available for prediction.")
    else:
        st.warning("Dataset is missing one or more model features: " + ", ".join(features))
else:
    st.warning("Model not trained yet. Run `python train_model.py` after placing the dataset in data/.")

st.subheader("Exploratory source indicators")
st.caption("These transparent rules are illustrative only. They are not a trained source-apportionment model and must not be interpreted as proof of source contribution.")
latest = df.dropna(subset=[c for c in ["PM2.5","PM10","NO2","SO2","CO"] if c in df.columns]).tail(1)
if not latest.empty:
    r = latest.iloc[0]
    indicators = {
        "Traffic-related indicator": float(r.get("NO2", 0) or 0) + float(r.get("CO", 0) or 0),
        "Dust-related indicator": float(r.get("PM10", 0) or 0),
        "Combustion/industrial indicator": float(r.get("SO2", 0) or 0) + float(r.get("PM2.5", 0) or 0),
    }
    total = sum(max(v,0) for v in indicators.values())
    if total > 0:
        shares = pd.DataFrame({"Indicator": list(indicators), "Relative score (%)": [max(v,0)/total*100 for v in indicators.values()]})
        st.plotly_chart(px.bar(shares, x="Indicator", y="Relative score (%)", range_y=[0,100]), use_container_width=True)
    else:
        st.write("Insufficient pollutant values to calculate exploratory indicators.")
else:
    st.write("No complete pollutant row available.")

st.subheader("Data preview")
st.dataframe(df.head(100), use_container_width=True)
st.caption("For operational use, integrate validated ground-station feeds, satellite observations (e.g. tropospheric NO₂/AOD), meteorology and location metadata.")
