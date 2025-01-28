import streamlit as st
import pickle
import pandas as pd
import numpy as np

# Set up page config
st.set_page_config(page_title="Price Predictor", layout="centered")

# Load data
with open('df.pkl', 'rb') as file:
    df = pickle.load(file)

with open('pipeline.pkl', 'rb') as file:
    pipeline = pickle.load(file)

# Custom CSS to style the page
st.markdown("""
    <style>
        /* Global Styling */
        body {
            font-family: 'Roboto', sans-serif;
            background-color: #FEEAFA;
            color: #333333;
            margin: 0;
        }

        /* Header */
        .header {
            font-size: 38px;
            font-weight: 600;
            color: #8E9AAF;
            text-align: center;
            margin-top: 30px;
            text-transform: uppercase;
        }

        /* Subheader */
        .subheader {
            font-size: 18px;
            font-weight: 400;
            color: #CBC0D3;
            text-align: center;
            margin-bottom: 30px;
        }

        /* Card container with cream background */
        .form-container {
            background-color: #EFD3D7;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0px 8px 20px rgba(0, 0, 0, 0.1);
            margin-top: 40px;
            margin-bottom: 40px;
            transition: all 0.3s ease-in-out;
        }

        .form-container:hover {
            box-shadow: 0px 15px 40px rgba(0, 0, 0, 0.2);
        }

        /* Form Section Header */
        .form-header {
            font-size: 22px;
            font-weight: 500;
            color: #8E9AAF;
            margin-bottom: 15px;
        }

        /* Input Styling */
        .stSelectbox, .stTextInput, .stNumberInput, .stSlider {
            background-color: #8E9AAF;
            border-radius: 6px;
            border: 1px solid #CBC0D3;
            padding: 10px;
            width: 100%;
            margin-bottom: 15px;
            transition: border 0.3s ease-in-out, box-shadow 0.3s ease-in-out;
        }

        .stSelectbox:hover, .stTextInput:hover, .stNumberInput:hover, .stSlider:hover {
            box-shadow: 0px 3px 10px rgba(0, 0, 0, 0.1);
            border: 1px solid #8E9AAF;
        }

        .stSelectbox:focus, .stTextInput:focus, .stNumberInput:focus, .stSlider:focus {
            border: 1px solid #8E9AAF;
            outline: none;
            box-shadow: 0px 0px 8px rgba(142, 154, 175, 0.5);
        }

        /* Button Styling */
        .button-style {
            background-color: #8E9AAF;
            color: white;
            font-size: 16px;
            padding: 12px 25px;
            border-radius: 8px;
            border: none;
            cursor: pointer;
            width: 100%;
            transition: background-color 0.3s, transform 0.3s ease-in-out;
            box-shadow: 0px 5px 15px rgba(0, 0, 0, 0.1);
        }

        .button-style:hover {
            background-color: #6B778D;
            transform: translateY(-2px);
            box-shadow: 0px 10px 25px rgba(0, 0, 0, 0.15);
        }

        .button-style:active {
            transform: translateY(2px);
        }

        /* Prediction Result */
        .prediction {
            font-size: 30px;
            font-weight: 1000;
            color: #CBC0D3;
            text-align: center;
            margin-top: 30px;
            transition: all 0.3s ease;
        }

        .prediction p {
            margin: 0;
            font-size: 22px;
        }

        /* Container Adjustments */
        .container {
            margin-top: 40px;
        }

        /* Custom Form Padding */
        .stForm {
            padding-top: 20px;
        }

        /* Responsive Design (Mobile-friendly) */
        @media (max-width: 768px) {
            .header {
                font-size: 32px;
            }

            .form-container {
                padding: 25px;
            }

            .form-header {
                font-size: 20px;
            }

            .stSelectbox, .stTextInput, .stNumberInput, .stSlider {
                padding: 8px;
            }

            .button-style {
                padding: 10px 20px;
            }
        }

    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("<div class='header'>Real Estate Price Predictor</div>", unsafe_allow_html=True)
st.markdown("<div class='subheader'>Predict the value of your property easily and accurately</div>", unsafe_allow_html=True)

# Form for user input
with st.form(key="property_form"):
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<div class='form-header'>Property Details</div>", unsafe_allow_html=True)
        property_type = st.selectbox('Property Type', ['flat', 'house'], key="property_type", index=0)
        sector = st.selectbox('Sector', sorted(df['sector'].unique().tolist()), key="sector")
        bedroom = float(st.selectbox('Number of Bedrooms', sorted(df['bedRoom'].unique().tolist()), key="bedroom"))
        bathroom = float(st.selectbox('Number of Bathrooms', sorted(df['bathroom'].unique().tolist()), key="bathroom"))
        balcony = st.selectbox('Number of Balconies', sorted(df['balcony'].unique().tolist()), key="balcony")
        built_up_area = float(st.selectbox('Built Up Area (in sq. ft.)', sorted(df['built_up_area'].unique().tolist()), key="built_up_area"))

    with col2:
        st.markdown("<div class='form-header'>Additional Features</div>", unsafe_allow_html=True)
        agePossession = st.selectbox('Age Possession', sorted(df['agePossession'].unique().tolist()), key="agePossession")
        servant_room = float(st.selectbox('Number of Servant Rooms', [0.0, 1.0], key="servant_room"))
        store_room = float(st.selectbox('Number of Storerooms', [0.0, 1.0], key="store_room"))
        furnishing_type = st.selectbox('Furnishing Type', sorted(df['furnishing_type'].unique().tolist()), key="furnishing_type")
        luxury_category = st.selectbox('Luxury Category', sorted(df['luxury_category'].unique().tolist()), key="luxury_category")
        floor_category = st.selectbox('Floor Category', sorted(df['floor_category'].unique().tolist()), key="floor_category")

    submit_button = st.form_submit_button('Predict Price', use_container_width=True)

# Prediction
if submit_button:
    data = [[property_type, sector, bedroom, bathroom, balcony, agePossession, built_up_area, servant_room, store_room, furnishing_type, luxury_category, floor_category]]
    columns = ['property_type', 'sector', 'bedRoom', 'bathroom', 'balcony', 'agePossession', 'built_up_area', 'servant room', 'store room', 'furnishing_type', 'luxury_category', 'floor_category']
    one_df = pd.DataFrame(data, columns=columns)

    base_price = np.expm1(pipeline.predict(one_df))[0]
    low = base_price - 0.22
    high = base_price + 0.22

    st.markdown("<div class='prediction'><p>The predicted price range is between ₹{:.2f} Cr and ₹{:.2f} Cr</p></div>".format(low, high), unsafe_allow_html=True)
