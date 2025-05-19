import subprocess
import streamlit as st
import pandas as pd

@st.cache_data
def load_excel():
    return pd.read_excel("kpi generales.xlsx", sheet_name=None)
