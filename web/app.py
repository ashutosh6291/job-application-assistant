import streamlit as st

st.set_page_config(
    page_title="AI Job Seeker",
    page_icon="💼",
    layout="wide"
)

st.title("💼 AI Job Seeker")
st.subheader("Your AI-powered job application assistant")

st.markdown("""
### 🎯 What this app will do

- 🔎 Find relevant job opportunities
- 🤖 Match jobs with your profile
- 📊 Calculate job match scores
- ⭐ Prioritize the best opportunities
- 📄 Prepare tailored applications
- 🔗 Provide direct application links
- 📋 Track your applications
""")

st.divider()

st.success("🚀 AI Job Seeker interface is running successfully!")

st.info(
    "The live job-search and matching engine will be connected next."
)

st.subheader("Your preferred opportunities")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("GET / Graduate Engineer", "Priority")

with col2:
    st.metric("Data Analyst", "Priority")

with col3:
    st.metric("Banking Operations", "Priority")

st.divider()

st.caption("AI Job Seeker • Built with Python + Streamlit")
