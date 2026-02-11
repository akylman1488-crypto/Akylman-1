import streamlit as st
import pandas as pd
import numpy as np

def create_chart(data_type="line"):
    df = pd.DataFrame(np.random.randn(20, 3), columns=['a', 'b', 'c'])
    if data_type == "line":
        st.line_chart(df)
    elif data_type == "bar":
        st.bar_chart(df)
