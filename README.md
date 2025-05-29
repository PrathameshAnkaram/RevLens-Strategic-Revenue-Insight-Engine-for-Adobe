# 🔍 RevLens: Strategic Revenue Insight Engine for Adobe

**RevLens** is a real-time revenue and margin insight engine built using **Adobe’s actual financial data**.

This project simulates what a Strategic Finance Analyst might build inside Adobe to monitor segment performance, detect revenue/margin risks, and simulate forward-looking decisions.

---

## 💡 Why I Built This

While editing in Premiere Pro, I realized more creators are shifting to DaVinci Resolve or Final Cut Pro. That sparked a bigger question:

> *Is Creative Cloud losing strategic ground?*

That curiosity led to more:
- Where does Adobe’s most reliable revenue come from?
- Are any segments bleeding margin quietly?
- What kind of dashboard would help Adobe’s FP&A team respond faster?

---

## 🧠 What RevLens Does

- 📊 **Tracks revenue and gross margin** trends for Adobe's 3 main business segments:
  - Digital Media
  - Digital Experience
  - Publishing & Advertising

- 🚨 **Flags margin anomalies** (e.g., drops > 2.5%) and provides insight summaries

- 🔮 **Includes a Forecast Simulator** where users can:
  - Choose a segment
  - Adjust expected growth rate
  - Forecast revenue for upcoming quarters

---

## 🔧 Built With

- **Python** (pandas, seaborn, matplotlib)
- **Streamlit** – for an interactive dashboard
- **Adobe public data** – extracted from 10-K / 10-Q filings
