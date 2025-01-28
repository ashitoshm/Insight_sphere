import streamlit as st

# Configure the page
st.set_page_config(
    page_title="InsightSphere",
    page_icon="🔄",
    layout="centered",
    initial_sidebar_state="expanded",
)

# Define colors from the palette
PRIMARY_COLOR = "#8E9AAF"
SECONDARY_COLOR = "#CBC0D3"
ACCENT_COLOR = "#EFD3D7"
BACKGROUND_COLOR = "#FEEAFA"
HIGHLIGHT_COLOR = "#DEE2FF"

# Custom CSS styling
st.markdown(
    f"""
    <style>
    /* Page background color */
    .main {{
        background-color: {BACKGROUND_COLOR};
    }}

    /* Main header styling */
    .main-header {{
        font-size: 45px;
        font-weight: bold;
        color: {PRIMARY_COLOR};
        text-align: center;
        margin-top: 20px;
        margin-bottom: 10px;
    }}

    /* Sub-header styling */
    .sub-header {{
        font-size: 20px;
        color: {SECONDARY_COLOR};
        text-align: center;
        margin-bottom: 30px;
    }}

    /* Features list styling */
    .feature-list {{
        font-size: 18px;
        color: {PRIMARY_COLOR};
        line-height: 1.6;
    }}

    /* Footer styling */
    .footer {{
        text-align: center;
        color: {SECONDARY_COLOR};
        margin-top: 40px;
        font-size: 14px;
    }}

    /* Button styling */
    div.stButton > button {{
        background-color: {PRIMARY_COLOR};
        color: white;
        border: none;
        border-radius: 5px;
        padding: 10px 20px;
        font-size: 16px;
        cursor: pointer;
    }}

    div.stButton > button:hover {{
        background-color: {ACCENT_COLOR};
        color: black;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# Main Header
st.markdown("<div class='main-header'>🔄 Welcome to InsightSphere</div>", unsafe_allow_html=True)

# Sub-header
st.markdown("<div class='sub-header'>Analyze, Predict, and Recommend with Precision</div>", unsafe_allow_html=True)

# Feature Highlights
st.write("## 🌟 Features of InsightSphere:")
st.markdown(
    f"""
    <ul class="feature-list">
        <li><b>📊 Analytics Dashboard:</b> Visualize key trends in real estate prices.</li>
        <li><b>📍 Interactive Map:</b> Explore property locations and average pricing.</li>
        <li><b>🤖 Price Prediction Tool:</b> Predict property prices with advanced ML models.</li>
        <li><b>📂 Data Insights:</b> Drill down into granular data.</li>
    </ul>
    """,
    unsafe_allow_html=True,
)

# Get Started Button
if st.button("Get Started"):
    st.write("### Here's how to proceed:")
    st.markdown(
        """
        - Navigate to the **sidebar** on the left.
        - Select **Analytics Dashboard** to explore data trends.
        - Choose **Price Predictor Tool** to predict property prices.
        """
    )
    st.info("Use the sidebar to switch between app pages.")

# Footer
st.markdown(
    "<div class='footer'>Developed with ❤️ by Ashitosh</div>",
    unsafe_allow_html=True,
)
