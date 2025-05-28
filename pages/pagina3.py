from funciones import mostrar_metrica_dinero
from funciones import mostrar_metrica_porcentual
from funciones import mostrar_tipologia
from funciones import cargar_excel
from funciones import crear_gauge
from funciones import crear_donut
from funciones import crear_mapa
from plotly.colors import sample_colorscale
from estilos import aplicar_estilos
from PIL import Image
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import login

aplicar_estilos()
login.generarLogin()
if 'usuario' in st.session_state:
    st.markdown("<h1 style='color: white;'>⛴ KPIs Área de Exportaciones</h1>", unsafe_allow_html=True)

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
        