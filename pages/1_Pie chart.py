import streamlit as st
# st.set_page_config(layout="wide")

import visualizer
from MyTime import side_bar_time

side_bar_time()

if 'df_main' not in st.session_state:
    st.warning('Extract time from some period on the side bar')
else:
    df_main = st.session_state['df_main']

    st.header('Summary pie 🥧')
    st.subheader('From ' + str(st.session_state['time_min']) + ' To ' + str(st.session_state['time_max']))

    # Creating pie chart
    pie_chart = visualizer.create_calendar_pie_chart(df_main)

    st.pyplot(pie_chart)

    st.table(visualizer.get_pretty_calendars_table(df_main, 'Hours'))
    