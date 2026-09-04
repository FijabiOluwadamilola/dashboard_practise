import pandas as pd
import plotly.express as px
import streamlit as st
from PIL import Image



##=========================
#Page Configuration
##==========================
#logo = Image.open("assests/curriculumlogo.jpg")
st.set_page_config(page_title="Sales Dashboard",
                   page_icon="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTbYqkQBMAWXL-Ck94B9L9piFM0cMkAnW9bSB-8PEya1g&s=10", 
                   layout="wide")

data = {
    "Product": [
        "Laptop",
        "Phone",
        "Tablet",
        "Monitor",
        "Laptop",
        "Phone",
        "Tablet",
        "Monitor",
        "Laptop",
        "Phone",
        "Tablet",
        "Monitor",
    ],
    "Region": [
        "Lagos",
        "Lagos",
        "Lagos",
        "Lagos",
        "Abuja",
        "Abuja",
        "Abuja",
        "Abuja",
        "Kano",
        "Kano",
        "Kano",
        "Kano",
    ],
    "Sales": [
        1200000,
        900000,
        500000,
        700000,
        800000,
        700000,
        400000,
        600000,
        600000,
        500000,
        300000,
        450000,
    ],
    "Profit": [
        250000,
        180000,
        100000,
        140000,
        170000,
        150000,
        80000,
        120000,
        120000,
        100000,
        60000,
        90000,
    ],
}
df = pd.DataFrame(data)

#st.title("Sales Dashboard")

logo_url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTbYqkQBMAWXL-Ck94B9L9piFM0cMkAnW9bSB-8PEya1g&s=10"
st.markdown(
    f"""
    <div style="display: flex", align-item: center; gap: 20px; margin-bottom: 10px>
        <img src="{logo_url}" width="40", style="Object-fit: contain;">
        <h1 style="margin: 0; padding: 0; line-height: 1;"> Sales Analytics Dashboard</h1>
    </div>
    """, 
    unsafe_allow_html=True
)

st.write("This is the monthly sales analysis for microsoft.")

# Filter Setup
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    region = st.selectbox("Select Region", 
                          ["All"] + list(df["Region"].unique())
                          )
with col2:
    products = st.multiselect(
        "Select Products", df['Product'].unique(), default=list(df['Product'].unique())
    )

with col3:
    show_data = st.checkbox("show raw data")

with col4:
    minimum_sales = st.slider("Minimum Sales", 0, 200000, 300000)

with col5:
    option = st.radio("Choose View", ["Sales", "Profit"])


## Filter Logic
filtered_df = df.copy()

# checking if region is not equal to All
if region != "All":
    filtered_df = filtered_df[filtered_df['Region'] == region]

# Apply multiselect to Product
if products:
    filtered_df = filtered_df[filtered_df["Product"].isin(products)]

# Apply Slider 
filtered_df = filtered_df[filtered_df['Sales'] >= minimum_sales]

# Conditionally show or hide Raw Data
if show_data: 
#it means if box is checked. i.e if checkbox is true
    st.subheader("Raw Data View")
    st.dataframe(df)

## METRICS 
#using filtered_df means  when any any filter is applied, the metric will be affected
total_sales = df['Sales'].sum()
total_profit = df['Profit'].sum()

metric_col1, metric_col2 = st.columns(2)

with metric_col1:
    st.metric("Total Sales", total_sales)

with metric_col2:
    st.metric("Total Profit", total_profit)

## Data Table 
st.subheader("Filtered Data")
st.dataframe(filtered_df)


## Chars Side by Side 
chart_col1, chart_col2 = st.columns(2)
with chart_col1:
    fig_bar = px.bar(
        filtered_df, 
        x = "Product",
        y = option, # Dynamically rendering the radio choice
        title=f"{option} by Product",
        color="Product"
    )

    st.plotly_chart(fig_bar, use_container_width=True)

with chart_col2:
    fig_scatter = px.scatter(
        filtered_df,
        x="Sales",
        y="Profit", 
        color="Product",
        size="Profit",
        hover_data=["Region"], 
        title= "Relationship between sales and profit"
    )

    st.plotly_chart(fig_scatter, use_container_width=True)
