import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def create_chart():
    st.subheader("Построение графика")
    data_input = st.text_area("Введи данные (Год, Значение) через запятую:", "2020,10\n2021,15\n2022,20")
    if st.button("Построить"):
        try:
            # Простая логика парсинга
            lines = data_input.split('\n')
            data = [line.split(',') for line in lines]
            df = pd.DataFrame(data, columns=['X', 'Y'])
            st.line_chart(df)
        except:
            st.error("Ошибка данных")
