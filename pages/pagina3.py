from funciones import mostrar_metrica_corporativa
from funciones import mostrar_tipologia
from funciones import crear_header_corporativo
from funciones import crear_seccion_corporativa
from funciones import cargar_excel
from funciones import crear_donut
from funciones import crear_mapa
from estilos import aplicar_estilos
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import login

st.set_page_config(layout="wide")
aplicar_estilos()
login.generarLogin()
if 'usuario' in st.session_state:
    crear_header_corporativo(
        "⛴ KPIs ÁREA DE EXPORTACIONES",
        "Indicadores para el área de exportaciones"
    )
    df_ind = pd.read_excel("kpi generales.xlsx", sheet_name="rentabilidad exportaciones mes", header=None)
    df_ind[0] = df_ind[0].astype(str).str.strip().str.upper()

    utilidad = df_ind.loc[df_ind[0] == "UTILIDAD NETA FINAL", 1].values[0]
    margen = df_ind.loc[df_ind[0] == "MARGEN NETO FINAL", 1].values[0]*100
    crear_seccion_corporativa("Rentabilidad Exportaciones por mes", "💰", "Análisis de rendimiento")

    col1, col2 = st.columns([1, 1])

    with col1:
        mostrar_metrica_corporativa ("Utilidad Neta", utilidad, "$", tipo="primario")

    with col2:
        mostrar_metrica_corporativa ("Margen Neto", margen, sufijo="%", tipo="secundario")
        
    df_ind = pd.read_excel("kpi generales.xlsx", sheet_name="rentabilidad exportaciones acum", header=None)
    df_ind[0] = df_ind[0].astype(str).str.strip().str.upper()

    utilidad = df_ind.loc[df_ind[0] == "UTILIDAD NETA FINAL", 1].values[0]
    margen = df_ind.loc[df_ind[0] == "MARGEN NETO FINAL", 1].values[0]*100

    crear_seccion_corporativa("Rentabilidad Exportaciones acumulado", "💰", "Análisis de rendimiento")
    col1, col2 = st.columns([1, 1])

    with col1:
        mostrar_metrica_corporativa ("Utilidad Neta", utilidad, "$", tipo="primario")

    with col2:
        mostrar_metrica_corporativa ("Margen Neto", margen, sufijo="%", tipo="secundario")
        