import streamlit as st
st.set_page_config(
    page_title="Summary graphs",
    page_icon="📈",
)
#st.set_page_config(layout="wide")

import pages

pages.side_bar_time(st.session_state['app'], st.session_state['time_min_initial'], st.session_state['time_max_initial'])

##################################
# Graphs
##################################
if 'df_main' not in st.session_state:
    st.warning('Extract time from some period on the side bar')
else:
    st.header('Summary graphs 📈')
    pages.from_to_header(st.session_state['time_min'], st.session_state['time_max'])

    pages.line_chart()
    pages.bar_chart()
    pages.bar_chart_clickable()

