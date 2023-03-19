import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

import api
import analyzer
import visualizer

# --------------------------------------------------------------------------------------------------------------------
# WEB-PAGE LAYOUT
st.title('⌚ MyTime ')


# --------------------------------------------------------------------------------------------------------------------
# DATE SELECTION
def side_bar_time():
    with st.sidebar:
        st.title('⌚ MyTime ')

        col1, col2 = st.columns(2)
        with col1:
            time_min = st.date_input("From")
        with col2:
            time_max = st.date_input("To")

        # --------------------------------------------------------------------------------------------------------------------
        # BUTTON

        # Pie chart
        if st.button('Extract time :arrow_right:'):
            st.session_state['time_min'] = time_min
            st.session_state['time_max'] = time_max

            # Getting timetable from Google Calendar API
            with st.spinner("Getting timetable from Google Calendar"):
                df_main = api.get_time_table(time_min, time_max)
                st.session_state['df_main'] = df_main
        else:
            st.write('Choose options and press the button to create chart')


# --------------------------------------------------------------------------------------------------------------------

side_bar_time()

# PIE CHART
# Calendars chart
if 'calendar_pie_chart' in st.session_state:
    # st.header("From " + str(time_min) + " To " + str(time_max))
    st.pyplot(st.session_state['calendar_pie_chart'])
