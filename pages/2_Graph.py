import streamlit as st
import pandas as pd

import visualizer
from MyTime import side_bar_time

side_bar_time()

##################################
# Graphs
##################################
if 'df_main' not in st.session_state:
    st.warning('Extract time from some period on the side bar')
else:
    df_main = st.session_state['df_main']
    st.header('Summary graph')
    st.subheader('From ' + str(st.session_state['time_min']) + ' To ' + str(st.session_state['time_max']))

    table_by_days = visualizer.get_calendars_table_by_days(df_main)

    st.write(table_by_days)

    calendar_names = table_by_days['Calendar'].unique()

    calendar_dates = table_by_days['Start date'].unique()
    calendar_dates.sort()
    plot_df = pd.DataFrame(calendar_dates)
    plot_df['Start date'] = calendar_dates
    plot_df = plot_df.set_index('Start date')

    for calendar_name in calendar_names:
        calendar_table = table_by_days.loc[table_by_days['Calendar'] == calendar_name, :]
        calendar_table = calendar_table.set_index('Start date')
        calendar_table = calendar_table.loc[:, ['Duration seconds']]
        calendar_table = calendar_table.rename(columns={'Duration seconds': calendar_name})

        calendar_column_lst = calendar_table.values.tolist()

        plot_df[calendar_name] = calendar_table

    x = plot_df.loc[:, [0]]
    y = plot_df.loc[:, ['Сон']]

    plot_df = plot_df.drop(0, axis=1)
    plot_df = plot_df.fillna(0)

    st.line_chart(plot_df)
    st.bar_chart(plot_df)
