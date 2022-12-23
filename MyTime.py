import api

import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from datetime import datetime

st.title('MyTime')

time_min = st.date_input("from")
time_max = st.date_input("to")


# Pie chart
if st.button('Create pie chart'):
    df = api.get_time_table(time_min, time_max)
    df_grouped_calendars = api.get_groped_calendars(df)

    names = df_grouped_calendars['Calendar'].tolist()
    durations = df_grouped_calendars['Duration seconds'].tolist()

    fig1, ax1 = plt.subplots()
    ax1.pie(durations, labels=names, autopct='%1.1f%%',
            shadow=False, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    st.header("from " + str(time_min) + " to " + str(time_max))
    st.pyplot(fig1)
else:
    st.write('Choose options and press the button to create chart')
