import streamlit as st
import pandas as pd
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import seaborn as sns
import ast

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
    .main {{
        background-color: {BACKGROUND_COLOR};
    }}
    .header {{
        font-size: 35px;
        font-weight: bold;
        color: {PRIMARY_COLOR};
        text-align: center;
        margin-top: 20px;
        margin-bottom: 10px;
    }}
    .sub-header {{
        font-size: 18px;
        color: {SECONDARY_COLOR};
        text-align: center;
        margin-bottom: 20px;
    }}
    .footer {{
        text-align: center;
        color: {SECONDARY_COLOR};
        margin-top: 40px;
        font-size: 14px;
    }}
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

# Title and Description
st.markdown("<div class='header'>📊 Real Estate Analytics Dashboard</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-header'>Explore interactive visualizations and insights into property prices, features, and trends across sectors.</div>", unsafe_allow_html=True)

# Load Data
new_df = pd.read_csv('datasets/data_viz1.csv')
wordcloud_df = pd.read_csv('datasets/wordcloud.csv')

# Function to get features by sector
def get_features_by_sector(df, sector):
    filtered_df = df[df['sector'] == sector]
    main = []
    for item in filtered_df['features'].dropna().apply(ast.literal_eval):
        main.extend(item)
    return main

# Section: Sector Price per Sqft Geomap
st.markdown("<div class='header'>🗺️ Sector Price per Sqft Geomap</div>", unsafe_allow_html=True)
group_df = new_df.groupby('sector').mean(numeric_only=True)[['price', 'price_per_sqft', 'built_up_area', 'latitude', 'longitude']]

fig = px.scatter_mapbox(
    group_df,
    lat="latitude",
    lon="longitude",
    color="price_per_sqft",
    size="built_up_area",
    color_continuous_scale=px.colors.cyclical.IceFire,
    zoom=10,
    mapbox_style="carto-positron",
    hover_name=group_df.index,
    title="Average Price per Sqft by Sector"
)
st.plotly_chart(fig, use_container_width=True)

# Section: Word Cloud
st.markdown("<div class='header'>☁️ Sector Features Word Cloud</div>", unsafe_allow_html=True)
sector_options = wordcloud_df['sector'].unique().tolist()
selected_sector = st.selectbox('Select Sector for Word Cloud', sector_options)

if selected_sector:
    features = get_features_by_sector(wordcloud_df, selected_sector)
    if features:
        wordcloud = WordCloud(
            width=800,
            height=400,
            background_color='white',
            colormap='viridis'
        ).generate(' '.join(features))

        st.subheader(f'Word Cloud for Sector: {selected_sector}')
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        plt.tight_layout(pad=0)
        st.pyplot(plt)
    else:
        st.warning(f"No features found for sector '{selected_sector}'.")

# Section: Area vs Price
st.markdown("<div class='header'>📈 Area vs Price Scatterplot</div>", unsafe_allow_html=True)
property_type = st.selectbox('Select Property Type', ['flat', 'house'])

filtered_df = new_df[new_df['property_type'] == property_type]
fig1 = px.scatter(
    filtered_df,
    x="built_up_area",
    y="price",
    color="bedRoom",
    title=f"Built-Up Area vs Price for {property_type.title()}s",
    labels={"bedRoom": "Number of Bedrooms"}
)
st.plotly_chart(fig1, use_container_width=True)

# Section: BHK Pie Chart
st.markdown("<div class='header'>🍰 BHK Distribution</div>", unsafe_allow_html=True)
sector_option = new_df['sector'].unique().tolist()
sector_option.insert(0, 'overall')
selected_sector = st.selectbox('Select Sector for BHK Distribution', sector_option, key="bhk_pie_chart")

if selected_sector == 'overall':
    fig2 = px.pie(
        new_df,
        names='bedRoom',
        title="Overall BHK Distribution",
        color_discrete_sequence=px.colors.sequential.RdBu
    )
else:
    fig2 = px.pie(
        new_df[new_df['sector'] == selected_sector],
        names='bedRoom',
        title=f"BHK Distribution in Sector {selected_sector}",
        color_discrete_sequence=px.colors.sequential.RdBu
    )
st.plotly_chart(fig2, use_container_width=True)

# Section: BHK Price Comparison
st.markdown("<div class='header'>🏠 Side-by-Side BHK Price Comparison</div>", unsafe_allow_html=True)
fig3 = px.box(
    new_df[new_df['bedRoom'] <= 4],
    x='bedRoom',
    y='price',
    title='BHK Price Range Comparison',
    color='bedRoom',
    labels={"bedRoom": "Number of Bedrooms", "price": "Price (in ₹)"}
)
st.plotly_chart(fig3, use_container_width=True)

# Section: Distplot for Property Types
st.markdown("<div class='header'>📊 Price Distribution by Property Type</div>", unsafe_allow_html=True)
fig4 = plt.figure(figsize=(10, 4))
sns.histplot(new_df[new_df['property_type'] == 'house']['price'], kde=True, label='House', color='blue')
sns.histplot(new_df[new_df['property_type'] == 'flat']['price'], kde=True, label='Flat', color='green')
plt.title("Price Distribution for Houses and Flats")
plt.xlabel("Price (in ₹)")
plt.ylabel("Density")
plt.legend()
st.pyplot(fig4)

# Footer
st.markdown(
    f"""
    <div class='footer'>
    ---
    **Note:** Data is aggregated and visualized to provide insights into sector trends and property prices.
    </div>
    """,
    unsafe_allow_html=True,
)
