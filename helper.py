import pandas as pd
import streamlit as st


def dates_in_data(df):
    df['Due Date'] = pd.to_datetime(df['Due Date'])
    df['year'] = df['Due Date'].dt.year
    df['month'] = df['Due Date'].dt.month_name()
    df['day'] = df['Due Date'].dt.day
    df['hour'] = df['Due Date'].dt.hour

    return df


def clean_df(df):
    try:
        df.drop(['Unnamed: 0'], axis=1, inplace=True)
    except Exception as e:
        pass
    return df


def completed_tasks(df):
    status_list = list(df['Status'])
    for i in range(len(df['Task'])):
        try:
            if st.checkbox(str(df['Task'][i]), key=i, value=status_list[i]):
                status_list[i] = 1
            else:
                status_list[i] = 0
        except Exception as e:
            continue

    df['Status'] = status_list



