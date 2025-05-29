
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title='RevLens - Adobe Revenue Engine', layout='wide')

@st.cache_data
def load_data():
    df = pd.read_csv('data/adobe_segment_financials.csv')
    df['Quarter'] = pd.Categorical(df['Quarter'], categories=[
        "Q1 FY23", "Q2 FY23", "Q3 FY23", "Q4 FY23",
        "Q1 FY24", "Q2 FY24", "Q3 FY24", "Q4 FY24"
    ], ordered=True)
    df = df.sort_values(['Segment', 'Quarter'])
    df['Margin Delta (%)'] = df.groupby('Segment')["Gross Margin (%)"].diff()
    df['Flag'] = df['Margin Delta (%)'].apply(lambda x: "🚨 Drop" if x is not None and x < -2.5 else "")
    return df

df = load_data()

tab1, tab2, tab3 = st.tabs(["📊 Margin Trends", "📈 Revenue Trends", "🔮 Forecast Simulator"])

with tab1:
    st.subheader("Segment Gross Margin Over Time")
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.lineplot(data=df, x='Quarter', y='Gross Margin (%)', hue='Segment', marker='o', ax=ax)
    plt.xticks(rotation=45)
    plt.title("Adobe Segment Gross Margin")
    st.pyplot(fig)

    st.subheader("📌 Segment Insights")
    segments = df['Segment'].unique()

    for segment in segments:
        seg_df = df[df['Segment'] == segment]
        margin_trend = seg_df[['Quarter', 'Gross Margin (%)']].dropna()
        deltas = seg_df['Margin Delta (%)'].dropna()

        avg_delta = deltas.mean()
        trend_description = "stable" if abs(avg_delta) < 1 else "improving" if avg_delta > 0 else "declining"
        last_margin = seg_df['Gross Margin (%)'].iloc[-1]

        if trend_description == "declining":
            recommendation = "🔍 Review cost structure or pricing strategy."
        elif trend_description == "improving":
            recommendation = "✅ Consider increasing GTM investment to sustain momentum."
        else:
            recommendation = "📌 Monitor for potential volatility."

        st.markdown(f"""

        ### 📌 {segment}
        - **Trend:** {trend_description.capitalize()}
        - **Latest Margin:** {last_margin:.2f}%
        - **Avg Margin Change:** {avg_delta:.2f} pts/quarter
        - **Recommendation:** {recommendation}
        """)

        st.markdown("---")

with tab2:
    st.subheader("Revenue Trends by Segment")
    fig2, ax2 = plt.subplots(figsize=(10, 5))
    sns.lineplot(data=df, x='Quarter', y='Revenue ($B)', hue='Segment', marker='o', ax=ax2)
    plt.xticks(rotation=45)
    plt.title("Adobe Segment Revenue Over Time")
    st.pyplot(fig2)

with tab3:
    st.subheader("📈 Forecast Simulator")
    selected_segment = st.selectbox("Choose Segment", df['Segment'].unique())
    seg_data = df[df['Segment'] == selected_segment].sort_values('Quarter')
    last_revenue = seg_data['Revenue ($B)'].iloc[-1]
    recent_growth = seg_data['Revenue ($B)'].pct_change().dropna().mean()

    st.metric(label="Last Reported Revenue ($B)", value=f"{last_revenue:.2f}")
    st.metric(label="Average Quarterly Growth Rate", value=f"{recent_growth*100:.2f}%")

    forecast_growth = st.slider("Adjust Forecast Growth Rate (%)", min_value=-10.0, max_value=15.0, value=recent_growth*100)
    quarters_ahead = st.slider("Forecast Quarters Ahead", min_value=1, max_value=4, value=2)

    forecast = []
    rev = last_revenue
    for _ in range(quarters_ahead):
        rev *= (1 + forecast_growth / 100)
        forecast.append(rev)

    st.write("### Forecasted Revenue")
    for i, value in enumerate(forecast):
        st.write(f"Q{i+1} Forecast: ${value:.2f}B")
