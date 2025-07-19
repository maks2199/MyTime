from pprint import pprint

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import altair as alt


# ---------------------------------------------------------------------------------------------------------------------
# FOR SERVICE

def get_groped_calendars(df_main):
    df_grouped_calendars = df_main.loc[:, ['Calendar', 'Duration seconds', 'Calendar color']]
    df_grouped_calendars = df_grouped_calendars.groupby('Calendar').agg(
        {'Duration seconds': 'sum', 'Calendar color': 'first'})
    df_grouped_calendars = df_grouped_calendars.reset_index()

    return df_grouped_calendars


# ---------------------------------------------------------------------------------------------------------------------
# TABLES
def get_pretty_calendars_table(df_main: pd.DataFrame, time_format) -> pd.DataFrame:
    if time_format == 'Seconds':
        k = 1
    elif time_format == 'Minutes':
        k = 60
    elif time_format == 'Hours':
        k = 3600

    df_result = df_main.loc[:, ['Calendar', 'Duration seconds']]
    df_result = df_result.groupby('Calendar').agg(
        {'Duration seconds': 'sum'})
    df_result = df_result.reset_index()
    df_result['Duration seconds'] = df_result['Duration seconds'].apply(lambda x: round((x / k) * 2) / 2)
    df_result = df_result.rename(columns={'Duration seconds': 'Duration'})
    df_result = df_result.set_index('Calendar')
    df_result = df_result.sort_values(by=['Duration'], ascending=False)

    # Percentage
    df_result['Percent'] = (df_result['Duration'] / df_result['Duration'].sum()) * 100

    df_result.to_csv('df_result.csv')

    return df_result


def get_calendars_table_by_days(raw_timetable_df):
    table_by_days = raw_timetable_df.loc[:, ['Calendar', 'Duration seconds', 'Start time', 'End time']]
    # pd.set_option('display.max_rows', None)
    # print(table_by_days)

    table_by_days['Duration hours'] = table_by_days['Duration seconds'].apply(lambda x: round((x / 3600) * 2) / 2)

    # deleting odd calendars
    table_by_days.drop(table_by_days[table_by_days['Start time'] == 0].index, inplace=True)
    table_by_days.drop(table_by_days[table_by_days['Start time'] == 0.0].index, inplace=True)
    table_by_days.drop(table_by_days[table_by_days['Calendar'] == 'Unfilled'].index, inplace=True)

    table_by_days['Start date'] = table_by_days.apply(lambda x: x['Start time'].date(), axis=1)
    table_by_days['End date'] = table_by_days.apply(lambda x: x['End time'].date(), axis=1)
    table_by_days['Week'] = table_by_days.apply(lambda x: x['Start time'].isocalendar().week, axis=1)

    table_by_days = table_by_days.loc[:, ['Calendar', 'Duration hours', 'End date']]

    table_by_days = table_by_days.groupby(['Calendar', 'End date'], as_index=False).sum()

    return table_by_days


def get_calendars_table_by_weeks(raw_timetable_df):
    table_by_days = raw_timetable_df.loc[:, ['Calendar', 'Duration seconds', 'Start time', 'End time']]
    # pd.set_option('display.max_rows', None)
    # print(table_by_days)

    table_by_days['Duration hours'] = table_by_days['Duration seconds'].apply(lambda x: round((x / 3600) * 2) / 2)

    # deleting odd calendars
    table_by_days.drop(table_by_days[table_by_days['Start time'] == 0].index, inplace=True)
    table_by_days.drop(table_by_days[table_by_days['Start time'] == 0.0].index, inplace=True)
    table_by_days.drop(table_by_days[table_by_days['Calendar'] == 'Unfilled'].index, inplace=True)

    table_by_days['Start date'] = table_by_days.apply(lambda x: x['Start time'].date(), axis=1)
    table_by_days['End date'] = table_by_days.apply(lambda x: x['End time'].date(), axis=1)
    table_by_days['Week'] = table_by_days.apply(lambda x: x['Start time'].isocalendar().week, axis=1)

    table_by_days = table_by_days.loc[:, ['Calendar', 'Duration hours', 'Week']]

    table_by_days = table_by_days.groupby(['Calendar', 'Week'], as_index=False).sum()

    return table_by_days


def get_calendar_events_table(df_main, calendar, time_format):
    if time_format == 'Seconds':
        k = 1
    elif time_format == 'Minutes':
        k = 60
    elif time_format == 'Hours':
        k = 3600

    df = df_main.loc[df_main['Calendar'] == calendar, ['Event', 'Duration seconds']]
    df_result = df.groupby('Event').agg(
        {'Duration seconds': 'sum'})
    df_result['Count'] = df.groupby('Event')['Event'].count()
    df_result = df_result.reset_index()
    df_result['Duration seconds'] = df_result['Duration seconds'].apply(lambda x: round((x / k) * 2) / 2)
    df_result = df_result.rename(columns={'Duration seconds': 'Duration'})
    df_result = df_result.set_index('Event')
    df_result = df_result.sort_values(by=['Duration'], ascending=False)

    # Percentage
    df_result['Percent'] = (df_result['Duration'] / df_result['Duration'].sum()) * 100

    df_result = df_result.reset_index()

    print('DF EVENTS')
    print(df_result)

    return df_result


# ---------------------------------------------------------------------------------------------------------------------
# CHARTS

def create_calendar_pie_chart(df_main):
    df_grouped_calendars = get_groped_calendars(df_main)

    # Отладка: проверяем, что у нас в данных
    print("DEBUG: Grouped calendars:")
    print(df_grouped_calendars)

    # Убираем отрицательные или нулевые значения
    df_grouped_calendars = df_grouped_calendars[df_grouped_calendars['Duration seconds'] > 0]

    if df_grouped_calendars.empty:
        raise ValueError("Нет данных для построения диаграммы (все длительности <= 0).")

    calendar_names = df_grouped_calendars['Calendar'].tolist()
    calendar_durations = df_grouped_calendars['Duration seconds'].tolist()
    colors = df_grouped_calendars['Calendar color'].tolist()

    # Двигаем самый большой кусок
    explode = [0.0 if el == max(calendar_durations) else 0.0 for el in calendar_durations]

    # Создаем диаграмму
    fig, ax = plt.subplots()
    patches, texts, autotexts = ax.pie(
        calendar_durations,
        labels=calendar_names,
        autopct='%1.0f%%',
        shadow=False,
        startangle=90,
        colors=colors,
        explode=explode,
        pctdistance=0.85,
        labeldistance=1.1,
        wedgeprops={"edgecolor": "none", 'linewidth': 1, 'linestyle': 'solid', 'antialiased': False}
    )

    # Убираем маленькие куски (<2%)
    threshold = 2
    for label, pct_label in zip(texts, autotexts):
        pct_value = pct_label.get_text().rstrip('%')
        if float(pct_value) < threshold:
            label.set_text('')
            pct_label.set_text('')

    # Цвет текста
    for text in texts:
        text.set_color('black')
    for autotext in autotexts:
        autotext.set_color('white')
    sns.set(font="Sans serif")

    ax.axis('equal')  # Рисуем круг

    # Легенда
    ax.legend(bbox_to_anchor=(1.1, 1.05))

    # Рисуем дырку в центре
    centre_circle = plt.Circle((0, 0), 0.70, fc='white')
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)

    return fig



def create_events_pie_chart(df_events):
    event_names = df_events['Event'].tolist()
    event_durations = df_events['Duration'].tolist()

    def absolute_value(val):
        a = str(round(val / 100. * sum(event_durations)))
        return ' '.join([str(a), 'ч'])

    # Pie chart
    fig, ax = plt.subplots()
    patches, texts, autotexts = ax.pie(
        event_durations,
        labels=event_names,
        autopct=absolute_value,
        # autopct=lambda pct: '{:1.1f}%'.format(pct) if pct > 5 else '',
        shadow=False,
        startangle=90,
        pctdistance=0.85,
        labeldistance=1.1,
    )

    # Removing little pieces
    percent = 5
    threshold = percent * sum(event_durations)/100
    for label, pct_label in zip(texts, autotexts):
        pct_value = pct_label.get_text().rstrip('ч')
        if float(pct_value) < threshold:
            label.set_text('')
            pct_label.set_text('')

    # Text color
    for text in texts:
        text.set_color('black')
    for autotext in autotexts:
        autotext.set_color('white')
    sns.set(font="Sans serif")

    # ------
    # Annotations

    # ------

    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    # Legend
    ax.legend(bbox_to_anchor=(1.1, 1.05))

    # draw hole in center
    centre_circle = plt.Circle((0, 0), 0.70, fc='white')
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)

    return fig


def create_altair_bar_char_calendars(raw_timetable_df):
    table_by_days = raw_timetable_df.loc[:,
                    ['Calendar', 'Duration seconds', 'Start time', 'End time', 'Calendar color']]
    # pd.set_option('display.max_rows', None)
    # print(table_by_days)

    table_by_days['Duration hours'] = table_by_days['Duration seconds'].apply(lambda x: round((x / 3600) * 2) / 2)

    # deleting odd calendars
    table_by_days.drop(table_by_days[table_by_days['Start time'] == 0].index, inplace=True)
    table_by_days.drop(table_by_days[table_by_days['Start time'] == 0.0].index, inplace=True)
    table_by_days.drop(table_by_days[table_by_days['Calendar'] == 'Unfilled'].index, inplace=True)

    table_by_days['Start date'] = table_by_days.apply(lambda x: x['Start time'].date(), axis=1)
    table_by_days['End date'] = table_by_days.apply(lambda x: x['End time'].date(), axis=1)
    table_by_days['Week'] = table_by_days.apply(lambda x: x['Start time'].isocalendar().week, axis=1)

    table_by_days = table_by_days.loc[:, ['Calendar', 'Duration hours', 'End date']]

    table_by_days = table_by_days.groupby(['Calendar', 'End date'], as_index=False).sum()

    # Enable selection by click
    selector = alt.selection_single(encodings=['color'])  # Encodings by each group selection

    chart = alt.Chart(table_by_days).mark_bar().encode(
        x='End date',
        y='Duration hours',
        color=alt.condition(selector, 'Calendar', alt.value('lightgray'))).add_selection(selector)

    return chart


def create_correlation_matrix(raw_timetable_df):
    correlation_table = get_calendars_table_by_days(raw_timetable_df)
    correlation_table = correlation_table.drop(correlation_table[correlation_table['Calendar'] == '_Timetable'].index,
                                               inplace=False)
    correlation_table = correlation_table.sort_values(by=['End date'])
    correlation_table = correlation_table.pivot(index='End date', columns='Calendar')
    correlation_table = correlation_table.fillna(0)

    correlation_matrix = correlation_table.corr(method='kendall')

    return correlation_matrix
