from __future__ import print_function

import datetime
from datetime import datetime
import os.path
from pprint import pprint

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import pandas as pd

import streamlit as st
import matplotlib.pyplot as plt


#######################################################################################################################
# Functions
#######################################################################################################################
def get_ten_upcoming_events(calendar_id):
    # Call the Calendar API
    now = datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    print('Getting the upcoming 10 events')
    events_result = service.events().list(calendarId=calendar_id, timeMin=now,
                                          maxResults=10, singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])
    return events


def get_all_calendar_events(calendar_id):
    now = datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    events_result = service.events().list(calendarId=calendar_id, singleEvents=True, timeMax=now).execute()
    events = events_result.get('items', [])
    return events


def calculate_event_duration(event):
    return get_event_end_time(event) - get_event_start_time(event)


def get_event_start_time(event):
    _string = event.get('start', dict()).get('dateTime')
    # if _string is None:
    #     _string = event.get('start', dict()).get('date')
    if _string is not None:
        return datetime.fromisoformat(_string)
    else:
        return 0


def get_event_end_time(event):
    _string = event.get('end', dict()).get('dateTime')
    # if _string is None:
    #     _string = event.get('end', dict()).get('date')
    if _string is not None:
        return datetime.fromisoformat(_string)
    else:
        return 0


def duration_to_seconds(duration):
    if isinstance(duration, int):
        duration = pd.to_timedelta(duration)
    return duration.total_seconds()


#######################################################################################################################
# Authorization
#######################################################################################################################

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

creds = None
# The file token.json stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first
# time.
if os.path.exists('token.json'):
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
# If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open('token.json', 'w') as token:
        token.write(creds.to_json())

#######################################################################################################################
# Application
#######################################################################################################################
service = build('calendar', 'v3', credentials=creds)

# print('CALENDAR LIST:')
calendar_list_result = service.calendarList().list().execute()
# pprint(calendar_list_result)
calendar_list = calendar_list_result.get('items', [])
# pprint(calendar_list)

# pandas table
table = []

for calendar in calendar_list:

    calendar_name = calendar.get('summary')

    id = calendar.get('id')
    print(calendar_name, id)

    # print('EVENTS:')
    _events = get_all_calendar_events(id)
    for _event in _events:
        row = dict()
        row['Calendar'] = calendar_name
        pprint(_event)
        # print(_event['summary'])
        # if _event['summary'] is None:
        #     event_name = '-'
        # else:
        #     event_name = _event['summary']
        row['Event'] = _event.get('summary')
        # print(calculate_event_duration(_event))
        row['Duration'] = calculate_event_duration(_event)
        # pprint(_event)
        # print(type(row['Duration']))
        row['Duration seconds'] = duration_to_seconds(row['Duration'])

        table.append(row)

df = pd.DataFrame(table)
print(df)
with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
    print(df)
#
df_grouped_calendars = df.loc[:, ['Calendar', 'Duration seconds']]
df_grouped_calendars = df_grouped_calendars.groupby('Calendar').sum()
df_grouped_calendars = df_grouped_calendars.reset_index()
with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
    print(df_grouped_calendars)

# print('EVENTS:')
# _events = get_all_calendar_events('primary')
# for _event in _events:
#     print(_event['summary'])
#     print(calculate_event_duration(_event))
#     pprint(_event)

######################################
# WEB
######################################
st.title('MyTime')

names = df_grouped_calendars['Calendar'].tolist()
durations = df_grouped_calendars['Duration seconds'].tolist()

fig1, ax1 = plt.subplots()
ax1.pie(durations, labels=names, autopct='%1.1f%%',
        shadow=False, startangle=90)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

st.pyplot(fig1)
