import streamlit as st
import pandas as pd
from plotly.colors import sample_colorscale
import plotly.graph_objects as go
import plotly.express as px
from PIL import Image
import numpy as np
import login

login.generarLogin()
if 'usuario' in st.session_state:
    st.markdown("<h1 style='color: white;'>⛴ KPIs Área de Exportaciones</h1>", unsafe_allow_html=True)
    st.markdown("""
    <style>
    .metric-card {
        background-color: #f9f9f9;
        padding: 1.2rem;
        border-radius: 1rem;
        box-shadow: 0 4px 8px rgba(0,0,0,0.05);
        text-align: center;
    }
    .metric-title {
        font-size: 1rem;
        color: #555;
        margin-bottom: 0.3rem;
    }
    .metric-value {
        font-size: 1.5rem;
        font-weight: bold;
        color: #222;
    }
    </style>
    """, unsafe_allow_html=True)


    df_ind = pd.read_excel("kpi generales.xlsx", sheet_name="rentabilidad exportaciones mes", header=None)
    df_ind[0] = df_ind[0].astype(str).str.strip().str.upper()

    utilidad = df_ind.loc[df_ind[0] == "UTILIDAD NETA FINAL", 1].values[0]
    margen = df_ind.loc[df_ind[0] == "MARGEN NETO FINAL", 1].values[0]*100

    st.markdown("<h3 style='color: white;'>Rentabilidad Exportaciones por mes </h3>", unsafe_allow_html=True)
    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Utilidad Neta</div>
                <div class="metric-value">${utilidad:,.0f}</div>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Margen Neto</div>
                <div class="metric-value">{margen:,.2f}%</div>
            </div>
        """, unsafe_allow_html=True)
        
    df_ind = pd.read_excel("kpi generales.xlsx", sheet_name="rentabilidad exportaciones acum", header=None)
    df_ind[0] = df_ind[0].astype(str).str.strip().str.upper()

    utilidad = df_ind.loc[df_ind[0] == "UTILIDAD NETA FINAL", 1].values[0]
    margen = df_ind.loc[df_ind[0] == "MARGEN NETO FINAL", 1].values[0]*100

    st.markdown("<h3 style='color: white;'>Rentabilidad Exportaciones acumulado </h3>", unsafe_allow_html=True)
    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Utilidad Neta</div>
                <div class="metric-value">${utilidad:,.0f}</div>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Margen Neto</div>
                <div class="metric-value">{margen:,.2f}%</div>
            </div>
        """, unsafe_allow_html=True)
        