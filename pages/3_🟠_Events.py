import streamlit as st


st.set_page_config(
    page_title="Results",
    page_icon="🧮",
)

import pages

if 'df_main' not in st.session_state:
    st.warning('Extract time from some period on the side bar')
else:
    pages.side_bar_time(st.session_state['app'], st.session_state['time_min_initial'], st.session_state['time_max_initial'])

    st.header('Events ')

    pages.from_to_header(st.session_state['time_min'], st.session_state['time_max'])

    pages.events_table(st.session_state['app'])
