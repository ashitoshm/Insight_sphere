import streamlit as st
import pickle
import pandas as pd
import numpy as np

st.set_page_config(page_title="Recommend Appartments")

location_df = pickle.load(open('datasets/location_distance.pkl', 'rb'))

st.title('Select Location and Radius')

selected_location = st.selectbox('Location',sorted(location_df.columns.to_list()))

radius = st.number_input('Radius in kms')

if st.button('Search'):
    result_ser= location_df[location_df[selected_location] < radius*1000][selected_location].sort_values()

    for key, value in result_ser.items():
        st.text(str(key) + " " + str(round(value/1000)) + 'kms')

        


