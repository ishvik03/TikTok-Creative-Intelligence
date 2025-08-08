# streamlit_app.py

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
st.title("📊 TikTok Content Intelligence Dashboard")
st.markdown("Analyze viral content patterns across Japan, UK, USA, and Italy")

# Load data
@st.cache_data
def load_data():
    hooks = pd.read_csv("insights/hooks.csv")
    hashtags = pd.read_csv("insights/hashtags.csv")
    keywords = pd.read_csv("insights/viral_keywords.csv")
    formats = pd.read_csv("insights/formats.csv")
    cleaned = pd.read_csv("data/processed/cleaned_tiktok_data.csv")
    return hooks, hashtags, keywords, formats, cleaned

hooks, hashtags, keywords, formats, cleaned = load_data()

# Country Filter
countries = cleaned["country"].unique().tolist()
selected_countries = st.multiselect("🌍 Filter by Country", countries, default=countries)
filtered = cleaned[cleaned["country"].isin(selected_countries)]

st.markdown("---")
col1, col2 = st.columns(2)

# 1. Hook Types
with col1:
    st.subheader("🔗 Hook Type Distribution")
    fig, ax = plt.subplots()
    sns.countplot(data=hooks[hooks["country"].isin(selected_countries)], x="hook_type", ax=ax)
    ax.set_xlabel("Hook Type")
    ax.set_ylabel("Count")
    st.pyplot(fig)

# 2. Duration Bins
with col2:
    st.subheader("⏱️ Video Duration Bins")
    fig, ax = plt.subplots()
    sns.countplot(data=filtered, x="duration_bin", order=filtered["duration_bin"].value_counts().index, ax=ax)
    st.pyplot(fig)

# 3. Top Hashtags
st.markdown("---")
st.subheader("🏷️ Top 15 Hashtags")
top_hashtags = hashtags.sort_values("count", ascending=False).head(15)
st.bar_chart(top_hashtags.set_index("hashtag"))

# 4. Viral Keywords
st.subheader("🔥 Viral Keywords (Min 10 mentions)")
viral_keywords = keywords[keywords["count"] >= 10].sort_values("viral_ratio", ascending=False).head(15)
st.dataframe(viral_keywords[["keyword", "count", "viral_ratio"]])

# 5. Video Formats
st.subheader("🎬 Detected Video Formats")
fig, ax = plt.subplots()
sns.countplot(data=formats, y="video_format", order=formats["video_format"].value_counts().index, ax=ax)
st.pyplot(fig)

# 6. Post Time Patterns
st.markdown("---")
st.subheader("🕒 Post Timing Patterns")

col3, col4 = st.columns(2)
with col3:
    fig, ax = plt.subplots()
    sns.countplot(data=filtered, x="hour_of_day", ax=ax)
    ax.set_title("Post Hour Distribution")
    st.pyplot(fig)

with col4:
    fig, ax = plt.subplots()
    sns.countplot(data=filtered, x="day_of_week", order=[
        "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"
    ], ax=ax)
    ax.set_title("Post Day Distribution")
    st.pyplot(fig)

st.markdown("---")
st.success("✅ Dashboard Ready!")
