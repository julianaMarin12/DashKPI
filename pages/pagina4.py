from funciones import cargar_excel
from funciones import crear_indicador_estado
from estilos import crear_header_corporativo
from estilos import crear_seccion_corporativa
from funciones import crear_gauge_corporativo
from funciones import mostrar_metrica_corporativa_mercadeo
from funciones import crear_indicador_estado
from estilos import aplicar_estilos
from login import set_background
from PIL import Image
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
    set_background("images/fondo3.png")
    crear_header_corporativo(
        "🛍️ KPIs ÁREA MERCADEO",
        "Indicadores para el área de mercadeo"
    )

    df = cargar_excel("kpi generales.xlsx", "mercadeo2")
    df.columns = df.columns.str.strip()
    df_general = df[df["Unidad de Negocio"] == "Total general"]

    ventas_2024 = df_general["Ventas 2024 rea"].values[0]
    ventas_2025 = df_general["Ventas 2025 rea"].values[0]
    variacion_abs = df_general["Variación 2024/2025"].values[0]
    variacion_pct = df_general["Var% 2024/2025"].values[0]
    presupuestado = df_general["PRESUPUESTADO"].values[0]
    acumulado_anterior = df_general["ACUMULADO MES ANTERIOR"].values[0]

    crear_seccion_corporativa(
        "CANALES TOTAL/B2B/B2C + DIGITAL/EXP", 
        "🏪", 
        "Análisis integral de rendimiento por canales de distribución y venta"
    )
    
    col_gauge, col_estado = st.columns([2, 1])
    
    with col_gauge:
        valor = variacion_pct * 100
        fig = crear_gauge_corporativo(valor, "% EJECUTADO VS PROYECTADO", referencia=36.5)
        st.plotly_chart(fig, use_container_width=True)
    
    with col_estado:
        crear_indicador_estado(valor, 36.5, "Estado vs Objetivo")

    st.markdown(" 💰 INDICADORES FINANCIEROS CLAVE")
    col1, col2, col3 = st.columns(3)

    with col1:
        mostrar_metrica_corporativa_mercadeo("VENTAS 2024", ventas_2024, "$", tipo="secundario")

    with col2:
        mostrar_metrica_corporativa_mercadeo("VENTAS 2025", ventas_2025, "$", tipo="primario")

    with col3:
        mostrar_metrica_corporativa_mercadeo("VARIACIÓN ABSOLUTA", variacion_abs, "$", tipo="secundario")


    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

    df1 = cargar_excel("kpi generales.xlsx", "lanzamiento")
    df1.columns = df1.columns.str.strip()

    porcentaje = df1["Porcentaje de Lanzamientos Activos"].values[0]*100
    lanzamientos = df1["Lanzamientos Activos"].values[0]
    ventas_innov = df1["Ventas"].values[0]

    crear_seccion_corporativa(
        "INNOVACIÓN Y DESARROLLO DE PORTAFOLIO", 
        "🚀", 
        "Seguimiento estratégico de nuevos productos y lanzamientos comerciales"
    )

    col_gauge2, col_estado2 = st.columns([2, 1])
    
    with col_gauge2:
        fig2 = crear_gauge_corporativo(porcentaje, "% LANZAMIENTOS ACTIVOS", referencia=7)
        st.plotly_chart(fig2, use_container_width=True)
    
    with col_estado2:
        crear_indicador_estado(porcentaje, 7, "Estado Innovación")

    st.markdown("#### 🎯 INDICADORES DE INNOVACIÓN")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        mostrar_metrica_corporativa_mercadeo("PORCENTAJE ACTIVO", porcentaje, sufijo="%", tipo="primario")
    
    with col2:
        mostrar_metrica_corporativa_mercadeo("LANZAMIENTOS ACTIVOS", lanzamientos, "$", tipo="secundario")
    
    with col3:
        mostrar_metrica_corporativa_mercadeo("VENTAS DE LA COMPAÑIA", ventas_innov, "$", tipo="primario")
