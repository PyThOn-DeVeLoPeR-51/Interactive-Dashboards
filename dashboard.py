import streamlit as st
import pandas as pd
import plotly.express as px
from numerize.numerize import numerize
from streamlit import title

st.set_page_config(page_title="Dashboard", page_icon=":earth_americas:", layout="wide")
st.markdown("<style>div.block-container{padding-top:1rem;}</style>", unsafe_allow_html=True)
html_title = """
    <style>
        .title-test {
        font-weight:bold;
        padding:5px;
        border-radius:6px}
    </style>
    <center><h1 class='title-test'>Insurance Descriptive Analytics</h1></center>    
        """
st.markdown(html_title, unsafe_allow_html=True)

df = pd.read_excel('python_query.xlsx')


# Sidebar
st.sidebar.image("data/logo1.png", caption="Online Analytics")
st.sidebar.header("Please filter")

region = st.sidebar.multiselect("Select region", options=df['Region'].unique(), default=df['Region'].unique())
location = st.sidebar.multiselect("Select location", options=df['Location'].unique(), default=df['Location'].unique())
construction = st.sidebar.multiselect("Select construction", options=df['Construction'].unique(), default=df['Construction'].unique())


df_selection = df.query("Region==@region & Location==@location & Construction==@construction")


# Total investment and rating
def home():
    with st.expander("Tabular"):
        showData = st.multiselect("Filter: ", df_selection.columns)
        st.write(df_selection[showData])


    total_investment = pd.to_numeric(df_selection['Investment']).sum()
    investment_mean = pd.to_numeric(df_selection['Investment']).mean()
    investment_median = pd.to_numeric(df_selection['Investment']).median()
    rating = pd.to_numeric(df_selection['Rating']).sum()

    total1, total2, total3, total4 = st.columns(4, gap='large')
    with total1:
        st.info("Total investment", icon="💲")
        st.metric(label="sum TZS", value=f"{total_investment:,.0f}")

    with total2:
        st.info("Average investment", icon="💲")
        st.metric(label="average TZS", value=f"{investment_mean:,.0f}")

    with total3:
        st.info("Central Earnings", icon="💲")
        st.metric(label="median TZS", value=f"{investment_median:,.0f}")

    with total4:
        st.info("Rating", icon="💲")
        st.metric(label="Rating", value=numerize(rating), help=f"""Total Rating: {rating}""")

    st.divider()

home()


# Graphs
#line graph
def graph():
    investment_by_business_type=df_selection.groupby(by=['BusinessType']).count()[['Investment']].sort_values(by='Investment')
    fig_investment = px.bar(
        investment_by_business_type,
        x='Investment',
        y=investment_by_business_type.index,
        orientation="h",
        title="<b>Investment by Business Type</b>",
        color_discrete_sequence=["#0083b8"]*len(investment_by_business_type),
        template="plotly_white")

    #bar graph
    investment_by_state=df_selection.groupby(by=['State']).count()[['Investment']]
    fig_state = px.line(
        investment_by_state,
        x=investment_by_state.index,
        y='Investment',
        orientation="v",
        title="<b>Investment by State</b>",
        color_discrete_sequence=["#0083b8"]*len(investment_by_state),
        template="plotly_white")
    fig_state.update_layout(xaxis=dict(tickmode="linear"))

    col1, col2 = st.columns(2)
    with col1:
     st.plotly_chart(fig_state, use_container_width=True)

    with col2:
        st.plotly_chart(fig_investment, use_container_width=True)

    st.divider()

    # Investment by Region
    df_pie1 = df_selection.groupby(by=['Region'])['Investment'].sum().reset_index()
    pie_chart1 = px.pie(df_pie1, values="Investment", names='Region', hole=0.5, title='Investment by Region')
    pie_chart1.update_traces(text=df_pie1['Region'], textposition="outside")

    # Investment by State
    df_pie2 = df_selection.groupby(by=['State'])['Investment'].sum().reset_index()
    pie_chart2 = px.pie(df_pie2, values="Investment", names='State', hole=0.5, title='Investment by State')
    pie_chart2.update_traces(text=df_pie2['State'], textposition="outside")

    # Investment by Location
    df_pie3 = df_selection.groupby(by=['Location'])['Investment'].sum().reset_index()
    pie_chart3 = px.pie(df_pie3, values="Investment", names='Location', hole=0.5, title='Investment by Location')
    pie_chart3.update_traces(text=df_pie3['Location'], textposition="outside")

    # Investment by Business Type
    df_pie4 = df_selection.groupby(by=['BusinessType'])['Investment'].sum().reset_index()
    pie_chart4 = px.pie(df_pie4, values="Investment", names='BusinessType', hole=0.5, title='Investment by Business Type')
    pie_chart4.update_traces(text=df_pie4['BusinessType'], textposition="outside")

    # Columns-1
    pie1, pie2 = st.columns((2))
    with pie1:
        st.plotly_chart(pie_chart1, use_container_width=True)
    with pie2:
        st.plotly_chart(pie_chart2, use_container_width=True)

    # Columns-2
    pie3, pie4 = st.columns((2))
    with pie3:
        st.plotly_chart(pie_chart3, use_container_width=True)
    with pie4:
        st.plotly_chart(pie_chart4, use_container_width=True)

    st.divider()
graph()


#treemap graph
def tree_graph():
    treemap = df_selection[['State', 'Investment', 'BusinessType']].groupby(by=['State', 'BusinessType'])['Investment'].sum().reset_index()
    fig_tree = px.treemap(treemap, path=['State', 'BusinessType'], values='Investment', height=700, width=600, color="BusinessType")

    fig_tree.update_traces(textinfo="label+value")
    st.plotly_chart(fig_tree, use_container_width=True)

tree_graph()

