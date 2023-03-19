df_grouped_events = api.get_groped_events(df_main)
st.session_state['df_grouped_events'] = df_grouped_events

# Table
    # df_calendar_events = api.get_calendar_events_table(df, 'Unfilled')
    # st.dataframe(df_calendar_events)
    # st.session_state['df_calendar_events'] = df_calendar_events

    # Events
    event_names = df_grouped_events['Event'].tolist()
    st.session_state['event_names'] = event_names
    event_durations = df_grouped_events['Duration seconds'].tolist()


    # Events chart
    # Events
    fig2, ax2 = plt.subplots()
    ax2.pie(event_durations, labels=event_names, autopct='%1.1f%%',
            shadow=False, startangle=90)
    ax2.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    # st.pyplot(fig2)
    st.session_state['fig2'] = fig2


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