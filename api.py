from __future__ import print_function

import datetime
from datetime import datetime
import os.path
from pprint import pprint
import asyncio
from httpx_oauth.clients.google import GoogleOAuth2

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import id_token
from google.auth.transport import requests

import pandas as pd
import streamlit as st
from http import cookies

import matplotlib.pyplot as plt


def main():
    ...


class App:

    def __init__(self, service):
        self.service = service


    def get_ten_upcoming_events(self, calendar_id):
        # Call the Calendar API
        now = datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        print('Getting the upcoming 10 events')
        events_result = self.service.events().list(calendarId=calendar_id, timeMin=now,
                                                   maxResults=10, singleEvents=True,
                                                   orderBy='startTime').execute()
        events = events_result.get('items', [])
        return events

    def get_all_calendar_events(self, calendar_id):
        now = datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        events_result = self.service.events().list(calendarId=calendar_id, singleEvents=True, timeMax=now).execute()
        events = events_result.get('items', [])
        return events

    def get_calendar_events(self, calendar_id, time_min, time_max):
        """Returns events from time_min to time_max for calendar by its id"""
        page_token = None
        events = []

        while True:
            events_result = self.service.events().list(calendarId=calendar_id,
                                                       singleEvents=True,
                                                       timeMin=time_min,
                                                       timeMax=time_max,
                                                       pageToken=page_token).execute()
            events += events_result.get('items', [])
            page_token = events_result.get('nextPageToken')
            if not page_token:
                break

        return events

    def calculate_event_duration(self, event):
        return self.get_event_end_time(event) - self.get_event_start_time(event)

    def get_event_start_time(self, event):
        _string = event.get('start', dict()).get('dateTime')
        if _string is not None:
            # return datetime.fromisoformat(_string)
            return datetime.strptime(_string, "%Y-%m-%dT%H:%M:%S%z")
        else:
            return 0

    def get_event_end_time(self, event):
        _string = event.get('end', dict()).get('dateTime')
        if _string is not None:
            # return datetime.fromisoformat(_string)
            return datetime.strptime(_string, "%Y-%m-%dT%H:%M:%S%z")
        else:
            return 0

    def duration_to_seconds(self, duration):
        """Converts duration from dateTime format to seconds"""
        if isinstance(duration, int):
            duration = pd.to_timedelta(duration)
        return duration.total_seconds()

    #######################################################################################################################
    # Authorization
    #######################################################################################################################

    # creds = None
    # if os.path.exists('token.json'):
    #     creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # # If there are no (valid) credentials available, let the user log in.
    # if not creds or not creds.valid:
    #     if creds and creds.expired and creds.refresh_token:
    #         creds.refresh(Request())
    #     else:
    #         flow = InstalledAppFlow.from_client_secrets_file(
    #             'credentials.json', SCOPES)
    #         creds = flow.run_local_server(port=0)
    #     # Save the credentials for the next run
    #     with open('token.json', 'w') as token:
    #         token.write(creds.to_json())

    #######################################################################################################################
    # Application
    #######################################################################################################################
    def get_time_table(self, time_min, time_max):
        print()
        print("------------------")
        print("GETTING TIME TABLE")
        print("------------------")

        # Converting time to needed format
        # Adding time to date from streamlit
        time_min = datetime.combine(time_min, datetime.min.time())
        time_max = datetime.combine(time_max, datetime.max.time())

        # Calculating total seconds in this range
        total_delta = time_max - time_min
        total_date_range_seconds = total_delta.total_seconds()
        # print('TOTAL total_date_range_seconds')
        # print(total_date_range_seconds)

        # Converting to isoformat (string)
        time_min = datetime.isoformat(time_min) + '+03:00'
        time_max = datetime.isoformat(time_max) + '+03:00'

        # print('CALENDAR LIST:')
        calendar_list_result = self.service.calendarList().list().execute()
        # pprint(calendar_list_result)
        calendar_list = calendar_list_result.get('items', [])
        # pprint(calendar_list)
        # print()
        # print("Calendar[0]: ")
        # pprint(calendar_list[0])

        # pandas table
        table = []

        for calendar in calendar_list:

            calendar_name = calendar.get('summary')
            calendar_color = calendar.get('backgroundColor')

            id_ = calendar.get('id')
            # print(calendar_name, id_)

            # print('EVENTS:')
            events_ = self.get_calendar_events(id_, time_min, time_max)
            # print(events_)


            # print()
            # print("Events[0]: ")
            # print(type(events_))
            # if len(events_) > 0:
            #     pprint(events_[0])

            for event_ in events_:
                # Printing progress bar
                # i += 1
                # if i % 100 == 0:
                #     print('processed event ', i)

                row = dict()
                row['Calendar'] = calendar_name
                row['Calendar color'] = calendar_color
                # pprint(event_)
                # print(event_['summary'])
                # if event_['summary'] is None:
                #     event_name = '-'
                # else:
                #     event_name = event_['summary']
                row['Event'] = event_.get('summary')
                if row['Event'] is None:
                    continue
                row['Event'] = event_.get('summary').strip()
                # print(calculate_event_duration(event_))
                row['Duration'] = self.calculate_event_duration(event_)
                row['Duration seconds'] = self.duration_to_seconds(row['Duration'])
                if row['Duration seconds'] <= 1.0:
                    continue
                if row['Duration seconds'] >= 86400.0:
                    continue
                # pprint(event_)
                # print(type(row['Duration']))

                row['Start time'] = self.get_event_start_time(event_)
                row['End time'] = self.get_event_end_time(event_)

                table.append(row)

        df = pd.DataFrame(table)
        # print(df)
        # print(df.info())

        total_event_seconds = df['Duration seconds'].sum()
        # print()
        # print('total_event_seconds: ', total_event_seconds)
        unfilled_event_seconds = total_date_range_seconds - total_event_seconds
        # TOD correct unfilled_event_seconds, events can intersect!

        row = dict()
        row['Calendar'] = 'Unfilled'
        row['Event'] = 'Unfilled event'
        row['Duration'] = '-'
        row['Duration seconds'] = unfilled_event_seconds

        df = df.append(row, ignore_index=True)

        # with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
        print()
        print("Raw data frame: ")
        print(df)
        print(df.info())

        df.to_csv('raw_time.csv')

        return df

    def get_calendars_list(self):
        calendar_list_result = self.service.calendarList().list().execute()
        calendar_list = calendar_list_result.get('items', [])
        return calendar_list

    def get_groped_events(self, df):
        df_grouped_events = df.loc[:, ['Event', 'Duration seconds']]
        df_grouped_events = df_grouped_events.groupby('Event').sum()
        df_grouped_events = df_grouped_events.reset_index()

        # print('Events')
        # with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
        #     print(df_grouped_events)

        return df_grouped_events

    def get_calendar_events_table(self, df, calendar_name):
        df_calendar_events = df.loc[df['Calendar'] == calendar_name]
        df_calendar_events = df_calendar_events.loc[:, ['Event', 'Duration']]
        return df_calendar_events

    def create_days_plot(self, table_by_days):
        table_by_days = table_by_days.loc['Статья', :]
        table_by_days = table_by_days.reset_index()
        print(table_by_days)

        x = table_by_days.loc[:, ['Start date']]
        y = table_by_days.loc[:, ['Duration seconds']]

        # plot_ = plt.plot(x, y)
        # plt.show()

        return table_by_days


if __name__ == '__main__':
    main()
