from funciones import mostrar_metrica_porcentual
from funciones import mostrar_metrica_dinero
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
    st.markdown("<h1 style='color: white;'>🛍️ KPIs Área Mercadeo </h1>", unsafe_allow_html=True)

    df = cargar_excel("kpi generales.xlsx", "mercadeo2")
    df.columns = df.columns.str.strip()
    df_general = df[df["Unidad de Negocio"] == "Total general"]

    ventas_2024 = df_general["Ventas 2024 rea"].values[0]
    ventas_2025 = df_general["Ventas 2025 rea"].values[0]
    variacion_abs = df_general["Variación 2024/2025"].values[0]
    variacion_pct = df_general["Var% 2024/2025"].values[0]
    presupuestado = df_general["PRESUPUESTADO"].values[0]
    acumulado_anterior = df_general["ACUMULADO MES ANTERIOR"].values[0]

    st.markdown("<h3 style='color: white;'> CANALES TOTAL/B2B/B2C + Digital/EXP </h3>", unsafe_allow_html=True)    
    valor = variacion_pct * 100
    presupuesto = presupuestado * 100

    fig = crear_gauge(valor, "Proyección:36.5%",referencia=36.5)
    st.plotly_chart(fig, use_container_width=True)

    col1, col2, col3 = st.columns([1.8, 1.8, 1.5])

    with col1:
            mostrar_metrica_dinero("Ventas 2024", ventas_2024,"$")

    with col2:
            mostrar_metrica_dinero("Ventas 2025", ventas_2025,"$")

    with col3:
            mostrar_metrica_dinero("Variación Absoluta", variacion_abs,"$")
    
    df1 = cargar_excel("kpi generales.xlsx", "lanzamiento")
    df1.columns = df1.columns.str.strip()

    porcentaje = df1["Porcentaje de Lanzamientos Activos"].values[0]*100
    lanzamientos =df1["Lanzamientos Activos"].values[0]
    ventas = df1["Ventas"].values[0]

    st.markdown("<h3 style='color: white;'> INNOVACIÓN/ PORTAFOLIO </h3>", unsafe_allow_html=True)
    fig = crear_gauge(porcentaje, "Proyección:7%",referencia=7)
    st.plotly_chart(fig, use_container_width=True)

    col1, col2, col3 = st.columns([1.8, 1.8, 1.5])
    with col1:
            mostrar_metrica_porcentual("Porcentaje", porcentaje, "%")
    with col2:
            mostrar_metrica_dinero("Lanzamientos Activos", lanzamientos, "$")
    with col3:
            mostrar_metrica_dinero("Ventas", ventas, "$")
