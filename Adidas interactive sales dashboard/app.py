import pandas as pd
import datetime as dt
import streamlit as st
from PIL import Image
import plotly.express as px
import plotly.graph_objects as go
from streamlit import plotly_chart

#reading data

df = pd.read_excel('Adidas.xlsx')


#setting page
st.set_page_config(layout="wide")
st.markdown("<style>div.block-container{padding-top:1rem;}</style>", unsafe_allow_html=True)


#read logo company
img = Image.open('adidas-logo.jpg')


#header
col1, col2 = st.columns([0.1, 0.9])
with col1:
    st.image(img, width=100)

html_title = """
    <style>
        .title-test {
        font-weight:bold;
        padding:5px;
        border-radius:6px}
    </style>
    <center><h1 class='title-test'>Adidas Interactive Sales Dashboard</h1></center>    
        """

with col2:
    st.markdown(html_title, unsafe_allow_html=True)


#body1
col3, col4, col5 = st.columns([0.1, 0.45, 0.45])
with col3:
    box_data = str(dt.datetime.now().strftime("%d %B %Y"))
    st.write(f"Last updated by:  \n {box_data}")

with col4:
    fig = px.bar(df, x="Retailer", y="TotalSales", labels={"TotalSales": "Total Sales {$}"},
                 title="Total Sales by Retailer", hover_data=['TotalSales'],
                 template="gridon", height=500)
    st.plotly_chart(fig, use_container_width=True)

df["Month_Year"] = df['InvoiceDate'].dt.strftime("%b %Y")
result = df.groupby(by=df["Month_Year"])['TotalSales'].sum().reset_index()

with col5:
    fig = px.line(result, x="Month_Year", y="TotalSales", labels={"TotalSales": "Total Sales {$}"},
                          title="Total sales over time", template="gridon", height=500)
    st.plotly_chart(fig, use_container_width=True)

#view and download - 1
_, view1, dwn1, view2, dwn2 = st.columns([0.15, 0.20, 0.20, 0.20, 0.20])
with view1:
    expander = st.expander("Retailer wise Sales")
    data = df[["Retailer", "TotalSales"]].groupby(by='Retailer')['TotalSales'].sum()
    expander.write(data)

with dwn1:
    st.download_button("Get data", data=data.to_csv().encode("utf-8"),
                       file_name="RetailerSales.csv", mime="text/csv")


#view and download - 2
with view2:
    expander = st.expander("Monthly Sales")
    data = result
    expander.write(data)

with dwn2:
    st.download_button("Get data", data=data.to_csv().encode("utf-8"),
                       file_name="MonthlySales.csv", mime="text/csv")


# Divider
st.divider()


# Body 2
# add the units sold as a line chart on a secondary y-axis
result1 = df.groupby(by="State")[['TotalSales', 'UnitsSold']].sum().reset_index()

fig3 = go.Figure()
fig3.add_trace(go.Bar(x=result1['State'], y=result1['TotalSales'], name="Total sales"))
fig3.add_trace(go.Scatter(x=result1['State'], y=result1['UnitsSold'], name="Units sold",
                          mode='lines', yaxis="y2"))
fig3.update_layout(
    title = "Total sales and Units sold by State",
    xaxis = dict(title="State"),
    yaxis = dict(title="Total Sales", showgrid=False),
    yaxis2 = dict(title="Units Sold", overlaying='y', side="right"),
    template="gridon",
    legend = dict(x=1, y=1)
)

_, col6 = st.columns([0.1, 0.9])
with col6:
    st.plotly_chart(fig3, use_container_width=True)


# view and download - 3
_, view3, dwn3 = st.columns([0.3, 0.3, 0.3])
with view3:
    expander = st.expander("View data for sales by Units sold")
    data = result1
    expander.write(data)

with dwn3:
    st.download_button("Get data", data=data.to_csv().encode('utf-8'),
                       file_name="Sales_by_UnitsSold.csv", mime="text/csv")


# Divide
st.divider()


# Body 3
# treemap
treemap = df[['Region', 'City', 'TotalSales']].groupby(by = ['Region', 'City'])['TotalSales'].sum().reset_index()
fig4 = px.treemap(treemap, path=['Region', 'City'], values='TotalSales',
                  color='City', height=700, width=600)
fig4.update_traces(textinfo="label+value")

_, col7 = st.columns([0.1, 0.9])
with col7:
    st.subheader(":point_right: Total Sales by Region and City in Treemap")
    st.plotly_chart(fig4, use_container_width=True)


# view and download - 4
_, view4, dwn4 = st.columns([0.33, 0.33, 0.33])
with view4:
    expander = st.expander("View data for Sales by Region and City")
    data = treemap
    expander.write(treemap)

with dwn4:
    st.download_button("Get data", data=data.to_csv().encode('utf-8'),
                       file_name="Sales_by_Region.csv", mime="text/csv")