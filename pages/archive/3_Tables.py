import streamlit as st

import api

st.set_page_config(
    page_title="Tables",
    page_icon="⬜",
)
# st.set_page_config(layout="wide")

import visualizer
from MyTime import side_bar_time
from pages import from_to_header

side_bar_time()

if 'df_main' not in st.session_state:
    st.warning('Extract time from some period on the side bar')
else:
    df_main = st.session_state['df_main']

    st.header('Summary pie 🥧')
    from_to_header(st.session_state['time_min'], st.session_state['time_max'])

    # Creating pie chart
    app = api.App(st.session_state['service'])
    calendars = app.get_calendars_list()
    calendars_names = [x.get('summary') for x in calendars]
    selected_calendar = st.selectbox('Calendars', options=calendars_names)



    time_options = ['Hours', 'Minutes', 'Seconds']
    selected_time_format = st.selectbox('Time format', time_options)

    groped_table = visualizer.get_calendar_events_table(df_main, selected_calendar, selected_time_format)

    st.table(groped_table)
    st.dataframe(groped_table)
