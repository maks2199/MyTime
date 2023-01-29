import os
from pprint import pprint

import pandas
# import streamlit_google_oauth as oauth
# from dotenv import load_dotenv
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

import api

import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from datetime import datetime

# import matplotlib.pyplot as plt
# import mpl_toolkits
# from mpl_toolkits.mplot3d import Axes3D

######################################################################################################################
# Authorization
######################################################################################################################
# load_dotenv()
# client_id = '564171152911-3f6baosrv1eg82qk8itf9rldk8o0i605.apps.googleusercontent.com'
# client_secret = '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'
# redirect_uri = 'http://localhost:8501'
#
# login_info = oauth.login(
#         client_id=client_id,
#         client_secret=client_secret,
#         redirect_uri=redirect_uri,
#         login_button_text="Continue with Google",
#         logout_button_text="Logout",
#     )
#
# if login_info:
#         user_id, user_email = login_info
#         st.write(f"Welcome {user_email}")
# else:
#         st.write("Please login")
#
#
#
# Example from quickstart
#
# If modifying these scopes, delete the file token.json.
# SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
#
# creds = None
# # The file token.json stores the user's access and refresh tokens, and is
# # created automatically when the authorization flow completes for the first
# # time.
#
# if 'token' in st.session_state:
#     st.session_state['creds'] = Credentials.from_authorized_user_file('token.json', SCOPES)
#     creds = st.session_state['creds']
# # If there are no (valid) credentials available, let the user log in.
# if not creds or not creds.valid:
#     if creds and creds.expired and creds.refresh_token:
#         creds.refresh(Request())
#     else:
#         flow = InstalledAppFlow.from_client_secrets_file(
#             'credentials.json', SCOPES)
#         creds = flow.run_local_server(port=0)
#     # Save the credentials for the next run
#     st.session_state['token'] = creds.to_json()
#
# service = build('calendar', 'v3', credentials=creds)
######################################################################################################################
st.title('MyTime')

time_min = st.date_input("from")
time_max = st.date_input("to")

# Pie chart
if st.button('Create calendars pie 🥧'):
    df = api.get_time_table(time_min, time_max)
    st.session_state['df'] = df
    df_grouped_calendars = api.get_groped_calendars(df)
    df_grouped_events = api.get_groped_events(df)
    st.session_state['df_grouped_events'] = df_grouped_events

    # Calendars
    calendar_names = df_grouped_calendars['Calendar'].tolist()
    calendar_colors = df_grouped_calendars['Calendar color'].tolist()
    calendar_durations = df_grouped_calendars['Duration seconds'].tolist()
    st.session_state['calendar_names'] = calendar_names
    st.session_state['calendar_colors'] = calendar_colors

    # Calendars chart
    fig1, ax1 = plt.subplots()
    ax1.pie(calendar_durations, labels=calendar_names, autopct='%1.1f%%',
            shadow=False, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    ax1.legend(bbox_to_anchor=(1.1, 1.05))

    # st.header("from " + str(time_min) + " to " + str(time_max))
    # st.pyplot(fig1)
    st.session_state['fig1'] = fig1

    # Table
    # df_calendar_events = api.get_calendar_events_table(df, 'Unfilled')
    # st.dataframe(df_calendar_events)
    # st.session_state['df_calendar_events'] = df_calendar_events

    # Events
    event_names = df_grouped_events['Event'].tolist()
    st.session_state['event_names'] = event_names
    event_durations = df_grouped_events['Duration seconds'].tolist()
    # selected_event_names = st.multiselect('Select events', event_names, event_names)
    # st.session_state['selected_event_names'] = selected_event_names
    # df_selected_events = df_grouped_events.loc[df_grouped_events['Event'].isin(selected_event_names)]
    # selected_event_durations = df_selected_events['Duration seconds'].tolist()

    # Events chart
    # if st.button('Create events pie'):
    # Events
    fig2, ax2 = plt.subplots()
    ax2.pie(event_durations, labels=event_names, autopct='%1.1f%%',
            shadow=False, startangle=90)
    ax2.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    # st.pyplot(fig2)
    st.session_state['fig2'] = fig2

else:
    st.write('Choose options and press the button to create chart')

# Calendars chart
st.header("from " + str(time_min) + " to " + str(time_max))
st.pyplot(st.session_state['fig1'])

###############
# Event Table
###############
selected_calendar_name = st.selectbox('Select calendar', st.session_state['calendar_names'])
df_calendar_events = api.get_calendar_events_table(st.session_state['df'], selected_calendar_name)
st.session_state['df_calendar_events'] = df_calendar_events
st.code(st.session_state['df_calendar_events'])

###############
# Events chart
###############
if 'selected_event_names' not in st.session_state:
    st.session_state['selected_event_names'] = st.session_state['event_names']
elif not st.session_state['selected_event_names']:
    st.session_state['selected_event_names'] = st.session_state['event_names']

selected_event_names = st.multiselect('Select events', st.session_state['event_names'], st.session_state['event_names'])
# st.session_state['selected_event_names'] = selected_event_names

# if st.button('Create events pie 🥧'):
df_grouped_events = st.session_state['df_grouped_events']
# selected_event_names = st.session_state['selected_event_names']
df_selected_events = df_grouped_events.loc[df_grouped_events['Event'].isin(selected_event_names)]
selected_event_durations = df_selected_events['Duration seconds'].tolist()
fig2, ax2 = plt.subplots()
ax2.pie(selected_event_durations, labels=selected_event_names, autopct='%1.1f%%',
        shadow=False, startangle=90)
ax2.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
st.session_state['fig2'] = fig2

st.pyplot(st.session_state['fig2'])

##################################
# Graphs
##################################
table_by_days = api.get_calendars_table_by_days(df)
print("\n Table by days: \n", table_by_days)
for col in table_by_days.columns:
    print(col)
# table_by_days = api.create_days_plot(api.get_calendars_table_by_days(df))
#
st.write(table_by_days)

one_calendar = table_by_days.loc[table_by_days['Calendar'] == '22_Диплом', :]
print(one_calendar)

calendar_names = table_by_days['Calendar'].unique()
print(calendar_names)


calendar_dates = table_by_days['Start date'].unique()
calendar_dates.sort()
plot_df = pd.DataFrame(calendar_dates)
plot_df['Start date'] = calendar_dates
plot_df = plot_df.set_index('Start date')
print(plot_df)


for calendar_name in calendar_names:
    print('table by days tyope', type(table_by_days))
    calendar_table = table_by_days.loc[table_by_days['Calendar'] == calendar_name, :]
    calendar_table = calendar_table.set_index('Start date')
    calendar_table = calendar_table.loc[:, ['Duration seconds']]
    calendar_table = calendar_table.rename(columns={'Duration seconds': calendar_name})
    print(calendar_table)
    print(type(calendar_table))
    calendar_column_lst = calendar_table.values.tolist()
    print(calendar_column_lst)

    plot_df[calendar_name] = calendar_table

print(plot_df)

x = plot_df.loc[:, [0]]
y = plot_df.loc[:, ['Сон']]
print(x)
print(y)
#
# fig = plt.figure()
# ax = plt.axes()
#
# ax.plot(x, y)
#
# st.pyplot(fig)


plot_df = plot_df.drop(0, axis=1)
plot_df = plot_df.fillna(0)


print(plot_df)
st.line_chart(plot_df)
