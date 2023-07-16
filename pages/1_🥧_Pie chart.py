import streamlit as st

st.set_page_config(
    page_title="Pie chart",
    page_icon="🥧",
)
# st.set_page_config(layout="wide")


from MyTime import side_bar_time
from pages import page_pie_chart

side_bar_time()

page_pie_chart()
