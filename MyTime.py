import asyncio
import os

import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

from httpx_oauth.clients.google import GoogleOAuth2
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import id_token
from google.auth.transport import requests

import api
import analyzer
import visualizer
import pages

import configs

st.set_page_config(layout="wide")


async def write_authorization_url(client,
                                  redirect_uri):
    authorization_url = await client.get_authorization_url(
        redirect_uri,
        scope=["https://www.googleapis.com/auth/calendar.readonly"],
        extras_params={"access_type": "offline"},
    )
    return authorization_url


async def write_access_token(client,
                             redirect_uri,
                             code):
    token = await client.get_access_token(code, redirect_uri)
    return token




# --------------------------------------------------------------------------------------------------------------------
# AUTHORIZATION

client_id = os.environ['GOOGLE_CLIENT_ID']
client_secret = os.environ['GOOGLE_CLIENT_SECRET']
redirect_uri = os.environ['REDIRECT_URI']
# client_id = credentials.client_id
# client_secret = credentials.client_secret

# Local
# import credentials
# redirect_uri = 'http://localhost:8501'
# TODOo:: change when deploy
# Docker
# redirect_uri = configs.redirect_uri

client = GoogleOAuth2(client_id, client_secret)

authorization_url = asyncio.run(
    write_authorization_url(client=client,
                            redirect_uri=redirect_uri)
)

if 'df_main' not in st.session_state:
    st.write(f'''<h1>
                            👋 Please login using this <a target="_self"
                            href="{authorization_url}">url</a></h1>''',
                         unsafe_allow_html=True)

if 'code' not in st.experimental_get_query_params():
    st.write('Authorization is needed')
else:
    code = st.experimental_get_query_params()['code']

    if 'token' not in st.session_state:
        try:
            token = asyncio.run(
                write_access_token(client=client,
                                   redirect_uri=redirect_uri,
                                   code=code))
            token['scope'] = 'https://www.googleapis.com/auth/calendar.readonly'
            st.session_state['token'] = token
        except:

            st.write('Authorization is needed')

    # SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

    if 'token' not in st.session_state:
        ...
    else:
        creds = Credentials(token=st.session_state['token']['access_token'])
        service = build('calendar', 'v3', credentials=creds)
        st.session_state['service'] = service

        app = api.App(service)
        st.session_state['app'] = app
# ----------------------------------------------------------------------------------------------------------------

        # WEB-PAGE LAYOUT
        st.title('⌚ MyTime ')

        # Initial extract
        now = datetime.now()
        monday = now - timedelta(days=now.weekday())
        time_min_initial = monday
        time_max_initial = now
        st.session_state['time_min_initial'] = time_min_initial
        st.session_state['time_max_initial'] = time_max_initial

        # if 'df_main' not in st.session_state:
        #     df_main = api.get_time_table(time_min_initial, time_max_initial)
        #     st.session_state['df_main'] = df_main


# --------------------------------------------------------------------------------------------------------------------
# DATE SELECTION



# --------------------------------------------------------------------------------------------------------------------

        pages.side_bar_time(app, time_min_initial, time_max_initial)

        # PIE CHART
        # Calendars chart
        if 'calendar_pie_chart' in st.session_state:
            # st.header("From " + str(time_min) + " To " + str(time_max))
            st.pyplot(st.session_state['calendar_pie_chart'])

        # -----------------------------------------------------------------------
        if 'df_main' not in st.session_state:
            st.warning('Extract time from some period on the side bar')
        else:
            pages.from_to_header(st.session_state['time_min'], st.session_state['time_max'])
            col1, col2 = st.columns(2)
            with col1:
                pages.pie_chart()
            with col2:
                pages.bar_chart_clickable()

            col1, col2 = st.columns(2)
            with col1:
                pages.line_chart()
            with col2:
                pages.bar_chart()

            pages.result_table()


pages.footer()