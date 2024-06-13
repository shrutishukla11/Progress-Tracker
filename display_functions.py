import random
import pandas as pd
import streamlit as st
import time
from datetime import date


def project_completion(df):
    completed_tasks = 0
    for i in df['Status']:
        if i == 1:
            completed_tasks += 1
    if completed_tasks == df.shape[0] and completed_tasks != 0:
        a = random.randint(0, 1)
        if a == 1:
            st.snow()
        else:
            st.balloons()
        st.info(f'Congratulations, You completed this Project')


def progress():
    prog = st.progress(0)
    for i in range(100):
        time.sleep(0.01)
        prog.progress(i + 1)


