import api

import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from datetime import datetime

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
    st.session_state['calendar_names'] = calendar_names
    calendar_durations = df_grouped_calendars['Duration seconds'].tolist()

    # Calendars chart
    fig1, ax1 = plt.subplots()
    ax1.pie(calendar_durations, labels=calendar_names, autopct='%1.1f%%',
            shadow=False, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

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

