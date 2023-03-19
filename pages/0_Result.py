import streamlit as st

import visualizer
from MyTime import side_bar_time

side_bar_time()

if 'df_main' not in st.session_state:
    st.warning('Extract time from some period on the side bar')
else:
    df_main = st.session_state['df_main']

    st.header('Summary table')
    st.subheader('From ' + str(st.session_state['time_min']) + ' To ' + str(st.session_state['time_max']))

    time_options = ['Hours', 'Minutes', 'Seconds']
    selected_time_format = st.selectbox('Time format', time_options)

    groped_table = visualizer.get_pretty_calendars_table(df_main, selected_time_format)

    st.table(groped_table)



