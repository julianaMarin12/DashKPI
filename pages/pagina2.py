import streamlit as st
import plotly.graph_objects as go
import login

login.generarLogin()

if 'usuario' in st.session_state:
    st.markdown("<h1 style='color: white;'>🛒 KPIs Área Comercial</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='color: black;'>📊 Métricas de los KPIs</h4>", unsafe_allow_html=True)