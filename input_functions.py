import random
import pandas as pd
import streamlit as st
import time
import helper

def add_task(task_title,df):
    if st.button('Add task'):
        if task_title in list(df['Task']):
            st.error('Task already exists')
        elif task_title == '':
            task_title = f'Task {len(df["Task"])}'
        else:
            df = helper.clean_df(df)
            df.loc[len(df.index)] = [task_title, 0]
    
