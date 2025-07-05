import numpy as np 
import pandas as pd
import streamlit as st
import plotly.express as px

df=pd.read_csv("covid_19_clean_complete.csv")
df.drop(['Lat','Long','WHO Region','Active'],axis=1,inplace=True)
df.rename(columns={'Province/State':'Province','Country/Region':'Country'},inplace=True)
df['Date']=pd.to_datetime(df['Date'])
df.fillna('NaN', inplace=True)



st.sidebar.title("Filter Options")
countries =df['Country'].unique()
select_country =st.sidebar.selectbox("Select Country", sorted(countries))

countryDf=df[df['Country']==select_country]

last_date = countryDf['Date'].max()
last= countryDf[countryDf['Date']==last_date].groupby('Country').sum(numeric_only=True)


st.title(f"COVID-19 Dashboard - {select_country}")
st.markdown(f"Data as of {last_date.date()}")

col1, col2, col3 = st.columns(3)
col1.metric("🟡 Confirmed", f"{int(last['Confirmed'])}")
col2.metric("🔴 Deaths", f"{int(last['Deaths'])}")
col3.metric("🟢 Recovered", f"{int(last['Recovered'])}")


fig=px.line(
    countryDf, 
    x='Date', 
    y='Confirmed', 
    title=f"📈 COVID-19 Trends Over Time in {select_country}",
    labels={"value": "Cases", "Date": "Date", "variable": "Metric"},
)

st.plotly_chart(fig, use_container_width=True)


st.subheader("🗺️ Global Spread (Choropleth Map)")
latest_global_date = df['Date'].max()
latest_global = df[df['Date'] == latest_global_date]
global_summary = latest_global.groupby('Country')[['Confirmed', 'Deaths', 'Recovered']].sum().reset_index()

with st.expander("📄 View Raw Data"):
    st.dataframe(countryDf.reset_index(drop=True), use_container_width=True)