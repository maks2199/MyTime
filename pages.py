import streamlit as st

import visualizer


def from_to_header(time_min, time_max):
    st.subheader('From **:blue[' +
                 str(time_min.strftime('%A %d %B %Y')) +
                 ']** To **:blue[' +
                 str(time_max.strftime('%A %d %B %Y')) + ']**')


def page_result():
    if 'df_main' not in st.session_state:
        st.warning('Extract time from some period on the side bar')
    else:
        df_main = st.session_state['df_main']

        st.header('Summary table 📃')
        from_to_header(st.session_state['time_min'], st.session_state['time_max'])

        time_options = ['Hours', 'Minutes', 'Seconds']
        selected_time_format = st.selectbox('Time format', time_options)

        groped_table = visualizer.get_pretty_calendars_table(df_main, selected_time_format)

        st.table(groped_table)


def page_pie_chart():
    if 'df_main' not in st.session_state:
        st.warning('Extract time from some period on the side bar')
    else:
        df_main = st.session_state['df_main']

        st.header('Summary pie 🥧')
        from_to_header(st.session_state['time_min'], st.session_state['time_max'])

        # Creating pie chart
        pie_chart = visualizer.create_calendar_pie_chart(df_main)

        st.pyplot(pie_chart)

        st.table(visualizer.get_pretty_calendars_table(df_main, 'Hours'))
