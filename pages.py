from datetime import datetime, timedelta

import pandas as pd
import streamlit as st
import matplotlib.colors as mcolors

import visualizer


def extract_time(app, time_min, time_max):
    st.session_state['time_min'] = time_min
    st.session_state['time_max'] = time_max
    # Getting timetable from Google Calendar API
    with st.spinner("Getting timetable from Google Calendar"):
        df_main = app.get_time_table(time_min, time_max)
        st.session_state['df_main'] = df_main


def side_bar_time(app, time_min_initial, time_max_initial):
    with st.sidebar:
        st.title('⌚ MyTime ')

        col1, col2 = st.columns(2)
        with col1:
            btn_this_week = st.button('↑ This week')
            btn_last_week = st.button('↟ Last week')
        with col2:
            btn_this_month = st.button('⇧ This month ')
            btn_last_month = st.button('⇮ Last month ')

        st.markdown("""---""")
        time_min, time_max = st.date_input("Date range", value=(time_min_initial, time_max_initial))

        if btn_this_week:
            now = datetime.now()
            monday = now - timedelta(days=now.weekday())
            time_min = monday
            time_max = now

            extract_time(app, time_min, time_max)
        elif btn_last_week:
            now = datetime.now()
            week_ago = now - timedelta(days=7)
            start_of_week = week_ago - timedelta(days=week_ago.weekday())
            end_of_week = start_of_week + timedelta(days=6)
            time_min = start_of_week
            time_max = end_of_week

            extract_time(app, time_min, time_max)
        elif btn_this_month:
            today = datetime.now().today()
            first = today.replace(day=1)
            time_min = first
            time_max = today

            extract_time(app, time_min, time_max)

        elif btn_last_month:
            today = datetime.now().today()
            first = today.replace(day=1)
            last_month_end = first - timedelta(days=1)
            last_month_start = last_month_end.replace(day=1)
            time_min = last_month_start
            time_max = last_month_end

            extract_time(app, time_min, time_max)
            # --------------------------------------------------------------------------------------------------------------------
        # BUTTON

        # Pie chart
        if st.button('Extract time :arrow_right:'):
            st.session_state['time_min'] = time_min
            st.session_state['time_max'] = time_max

            # Getting timetable from Google Calendar API
            with st.spinner("Getting timetable from Google Calendar"):
                df_main = app.get_time_table(time_min, time_max)
                st.session_state['df_main'] = df_main
        else:
            st.write('Choose options and press the button to create chart')


def from_to_header(time_min, time_max):
    st.info('From **:blue[' +
            str(time_min.strftime('%A %d %B %Y')) +
            ']** To **:blue[' +
            str(time_max.strftime('%A %d %B %Y')) + ']**')


def result_table():
    if 'df_main' not in st.session_state:
        st.warning('Extract time from some period on the side bar')
    else:
        df_main = st.session_state['df_main']

        # st.header('Summary table 📃')
        # from_to_header(st.session_state['time_min'], st.session_state['time_max'])

        time_options = ['Hours', 'Minutes', 'Seconds']
        selected_time_format = st.selectbox('Time format', time_options)

        groped_table = visualizer.get_pretty_calendars_table(df_main, selected_time_format)

        st.table(groped_table)


def events_table(app):
    if 'df_main' not in st.session_state:
        st.warning('Extract time from some period on the side bar')
    else:
        df_main = st.session_state['df_main']

        calendar_options = [x.get('summary') for x in app.get_calendars_list()]
        selected_calendar = st.selectbox('Calendar', calendar_options)

        time_options = ['Hours', 'Minutes', 'Seconds']
        selected_time_format = st.selectbox('Time format', time_options)

        table = visualizer.get_calendar_events_table(df_main, selected_calendar, selected_time_format)

        st.table(table)

        pie_chart_ = visualizer.create_events_pie_chart(table)

        st.pyplot(pie_chart_)


def pie_chart():
    if 'df_main' not in st.session_state:
        st.warning('Extract time from some period on the side bar')
    else:
        df_main = st.session_state['df_main']

        # Creating pie chart
        pie_chart = visualizer.create_calendar_pie_chart(df_main)

        st.pyplot(pie_chart)

        # st.table(visualizer.get_pretty_calendars_table(df_main, 'Hours'))


def line_chart():
    df_main = st.session_state['df_main']

    # --- TODOo move to visualizer module
    table_by_days = visualizer.get_calendars_table_by_days(df_main)
    calendar_names = table_by_days['Calendar'].unique()
    calendar_dates = table_by_days['End date'].unique()
    calendar_dates.sort()
    plot_df = pd.DataFrame(calendar_dates)
    plot_df['End date'] = calendar_dates
    plot_df = plot_df.set_index('End date')

    for calendar_name in calendar_names:
        calendar_table = table_by_days.loc[table_by_days['Calendar'] == calendar_name, :]
        calendar_table = calendar_table.set_index('End date')
        calendar_table = calendar_table.loc[:, ['Duration hours']]
        calendar_table = calendar_table.rename(columns={'Duration hours': calendar_name})
        calendar_column_lst = calendar_table.values.tolist()
        plot_df[calendar_name] = calendar_table

    plot_df = plot_df.drop(0, axis=1)
    plot_df = plot_df.fillna(0)
    # ---

    st.line_chart(plot_df)


def bar_chart():
    df_main = st.session_state['df_main']

    # --- TODOo move to visualizer module
    table_by_days = visualizer.get_calendars_table_by_days(df_main)
    calendar_names = table_by_days['Calendar'].unique()
    calendar_dates = table_by_days['End date'].unique()
    calendar_dates.sort()
    plot_df = pd.DataFrame(calendar_dates)
    plot_df['End date'] = calendar_dates
    plot_df = plot_df.set_index('End date')

    for calendar_name in calendar_names:
        calendar_table = table_by_days.loc[table_by_days['Calendar'] == calendar_name, :]
        calendar_table = calendar_table.set_index('End date')
        calendar_table = calendar_table.loc[:, ['Duration hours']]
        calendar_table = calendar_table.rename(columns={'Duration hours': calendar_name})
        calendar_column_lst = calendar_table.values.tolist()
        plot_df[calendar_name] = calendar_table

    plot_df = plot_df.drop(0, axis=1)
    plot_df = plot_df.fillna(0)
    # ---

    st.bar_chart(plot_df)


def bar_chart_clickable():
    df_main = st.session_state['df_main']

    # --- TODOo move to visualizer module
    table_by_days = visualizer.get_calendars_table_by_days(df_main)
    calendar_names = table_by_days['Calendar'].unique()
    calendar_dates = table_by_days['End date'].unique()
    calendar_dates.sort()
    plot_df = pd.DataFrame(calendar_dates)
    plot_df['End date'] = calendar_dates
    plot_df = plot_df.set_index('End date')

    for calendar_name in calendar_names:
        calendar_table = table_by_days.loc[table_by_days['Calendar'] == calendar_name, :]
        calendar_table = calendar_table.set_index('End date')
        calendar_table = calendar_table.loc[:, ['Duration hours']]
        calendar_table = calendar_table.rename(columns={'Duration hours': calendar_name})
        calendar_column_lst = calendar_table.values.tolist()
        plot_df[calendar_name] = calendar_table

    plot_df = plot_df.drop(0, axis=1)
    plot_df = plot_df.fillna(0)
    # ---

    st.altair_chart(visualizer.create_altair_bar_char_calendars(df_main))


def footer():
    footer_ = """
    <style>
        .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: white;
        color: black;
        text-align: center;
        }
    </style>
    <div class="footer">
      <p style='color:grey'>
      contact <a style='color:grey' href="mailto: tachkov.maksim@gmail.com" target="_blank">tachkov.maksim@gmail.com</a>
      </p>
    </div>
    """
    st.markdown(footer_, unsafe_allow_html=True)

