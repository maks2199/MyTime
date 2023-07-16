import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

import api
import analyzer
import visualizer
from pages import page_result, page_pie_chart

st.set_page_config(layout="wide")
# --------------------------------------------------------------------------------------------------------------------
if st.button("Sign in with Google"):
    # Redirect the user to the Google Sign-In page
    auth_url = "https://accounts.google.com/o/oauth2/auth"
    client_id = "564171152911-3f6baosrv1eg82qk8itf9rldk8o0i605.apps.googleusercontent.com"  # Replace with your actual client ID
    redirect_uri = "http://localhost:8501"  # Replace with your redirect URI
    scope = "https://www.googleapis.com/auth/calendar.readonly"  # Replace with the desired scopes
    state = "12345"  # Replace with a unique state value
    auth_endpoint = f"{auth_url}?response_type=code&client_id={client_id}&redirect_uri={redirect_uri}&scope={scope}&state={state}"
    st.markdown(f'<a href="{auth_endpoint}">Click here to sign in with Google</a>', unsafe_allow_html=True)

# WEB-PAGE LAYOUT
st.title('⌚ MyTime ')

# Initial extract
now = datetime.now()
monday = now - timedelta(days=now.weekday())
time_min_initial = monday
time_max_initial = now


# if 'df_main' not in st.session_state:
#     df_main = api.get_time_table(time_min_initial, time_max_initial)
#     st.session_state['df_main'] = df_main


# --------------------------------------------------------------------------------------------------------------------
# DATE SELECTION
def side_bar_time():
    with st.sidebar:
        st.title('⌚ MyTime ')

        time_min, time_max = st.date_input("Date range", value=(time_min_initial, time_max_initial))

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

# -----------------------------------------------------------------------
col1, col2 = st.columns(2)
with col1:
    page_result()
with col2:
    page_pie_chart()
