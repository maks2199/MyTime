import streamlit as st
# st.set_page_config(layout="wide")
import seaborn as sns
import matplotlib.pyplot as plt

import visualizer
from MyTime import side_bar_time

side_bar_time()

if 'df_main' not in st.session_state:
    st.warning('Extract time from some period on the side bar')
else:
    df_main = st.session_state['df_main']

    st.header('Correlations')
    st.subheader('From ' + str(st.session_state['time_min']) + ' To ' + str(st.session_state['time_max']))

    st.table(visualizer.get_calendars_table_by_weeks(df_main))

    correlation_matrix = visualizer.create_correlation_matrix(df_main)
    st.table(correlation_matrix)

    fig, ax = plt.subplots(figsize=(15,5))
    fig1 = sns.heatmap(correlation_matrix, annot=True)
    st.write(fig)

