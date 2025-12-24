import streamlit as st
import requests
import pandas as pd
import time

API_BASE_URL = "http://127.0.0.1:8000"

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------
st.set_page_config(
    page_title="AI Data Cleaning Assistant",
    layout="wide"
)

# -------------------------------------------------
# CUSTOM STYLING
# -------------------------------------------------
st.markdown(
    """
    <style>
    body {
        background: linear-gradient(135deg, #f7f9fc, #eef2f7);
    }
    .main-title {
        font-size: 36px;
        font-weight: 700;
        margin-bottom: 10px;
    }
    .subtitle {
        color: #555;
        margin-bottom: 30px;
    }
    .section-title {
        font-size: 22px;
        font-weight: 600;
        margin-top: 30px;
        margin-bottom: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<div class="main-title">AI Data Cleaning Assistant</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Automated CSV Analysis, Cleaning and Quality Scoring</div>', unsafe_allow_html=True)

# -------------------------------------------------
# SESSION STATE
# -------------------------------------------------
if "token" not in st.session_state:
    st.session_state.token = None

if "page" not in st.session_state:
    st.session_state.page = "login"

if "user_email" not in st.session_state:
    st.session_state.user_email = None

# -------------------------------------------------
# REGISTER PAGE
# -------------------------------------------------
if st.session_state.page == "register":
    st.markdown('<div class="section-title">User Registration</div>', unsafe_allow_html=True)

    email = st.text_input("Email address")
    password = st.text_input("Password", type="password")

    if st.button("Create Account"):
        response = requests.post(
            f"{API_BASE_URL}/users/register",
            json={"email": email, "password": password}
        )

        if response.status_code in (200, 201):
            st.success("Registration completed. Please login.")
            st.session_state.page = "login"
            st.rerun()
        else:
            st.error(response.text)

    if st.button("Back to Login"):
        st.session_state.page = "login"
        st.rerun()

# -------------------------------------------------
# LOGIN PAGE
# -------------------------------------------------
elif st.session_state.token is None:
    st.markdown('<div class="section-title">User Login</div>', unsafe_allow_html=True)

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        response = requests.post(
            f"{API_BASE_URL}/users/login",
            data={
                "username": email,
                "password": password
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )

        if response.status_code == 200:
            st.session_state.token = response.json()["access_token"]
            st.session_state.user_email = email
            st.success("Authentication successful")
            st.rerun()
        else:
            st.error("Invalid email or password")

    if st.button("New user? Register"):
        st.session_state.page = "register"
        st.rerun()

# -------------------------------------------------
# PIPELINE PAGE
# -------------------------------------------------
else:
    st.caption(f"Authenticated user: {st.session_state.user_email}")

    st.markdown('<div class="section-title">Upload Dataset</div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Select a CSV file", type=["csv"])

    if uploaded_file:
        headers = {"Authorization": f"Bearer {st.session_state.token}"}

        if st.button("Run Data Cleaning Pipeline"):
            progress = st.progress(0)
            status = st.empty()

            pipeline_steps = [
                "Uploading dataset",
                "Analyzing dataset structure",
                "Removing duplicate records",
                "Fixing missing values",
                "Calculating data quality score"
            ]

            for i, step in enumerate(pipeline_steps):
                status.info(step)
                time.sleep(0.6)
                progress.progress((i + 1) / len(pipeline_steps))

            with st.spinner("Finalizing output..."):
                response = requests.post(
                    f"{API_BASE_URL}/pipeline/clean-csv",
                    headers=headers,
                    files={"file": uploaded_file}
                )

            if response.status_code == 200:
                data = response.json()
                status.success("Pipeline execution completed successfully")

                summary = data["cleaning_summary"]

                # -------------------------------------------------
                # BEFORE vs AFTER METRICS
                # -------------------------------------------------
                st.markdown('<div class="section-title">Cleaning Overview</div>', unsafe_allow_html=True)

                c1, c2, c3, c4 = st.columns(4)
                c1.metric("Rows Before", summary["rows_before"])
                c2.metric("Rows After", summary["rows_after"])
                c3.metric("Duplicates Removed", summary["duplicates_removed"])
                c4.metric("Missing Values Fixed", summary["missing_values_fixed"])

                # -------------------------------------------------
                # ANIMATED QUALITY SCORE
                # -------------------------------------------------
                st.markdown('<div class="section-title">Data Quality Score</div>', unsafe_allow_html=True)
                score_placeholder = st.empty()
                score = summary["data_quality_score"]

                for i in range(0, score + 1, 5):
                    score_placeholder.metric("Quality Score", f"{i} / 100")
                    time.sleep(0.04)

                if score >= 80:
                    st.success("Excellent data quality achieved")
                elif score >= 60:
                    st.warning("Moderate data quality")
                else:
                    st.error("Poor data quality")

                # -------------------------------------------------
                # DATASET ANALYSIS TABLE
                # -------------------------------------------------
                with st.expander("View dataset analysis"):
                    analysis = data["analysis"]
                    analysis_df = pd.DataFrame({
                        "Column Name": analysis["columns"].keys(),
                        "Data Type": analysis["columns"].values(),
                        "Missing Values": analysis["missing_values"].values()
                    })
                    st.dataframe(analysis_df, use_container_width=True)

                # -------------------------------------------------
                # CLEANING STEPS
                # -------------------------------------------------
                with st.expander("View cleaning actions performed"):
                    if data["cleaning_steps"]:
                        for step in data["cleaning_steps"]:
                            st.write(step)
                    else:
                        st.write("No cleaning actions were required.")

                # -------------------------------------------------
                # OUTPUT FILE
                # -------------------------------------------------
                st.markdown('<div class="section-title">Cleaned Output File</div>', unsafe_allow_html=True)
                st.code(data["cleaned_file_path"])

            else:
                st.error("Pipeline execution failed")

    st.divider()

    if st.button("Logout"):
        st.session_state.token = None
        st.session_state.page = "login"
        st.rerun()