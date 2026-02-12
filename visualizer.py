import streamlit as st
import pandas as pd

def draw_chart(data_str):
    try:
        df = pd.DataFrame([x.split(',') for x in data_str.split('\n')], columns=['X', 'Y'])
        st.line_chart(df.set_index('X'))
    except: st.error("Ошибка формата данных")
