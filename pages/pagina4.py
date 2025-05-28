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

    fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=valor,
            number={
                'suffix': '%'
            },
            delta={
                'reference': presupuesto,
                'increasing': {'color': "green"},
                'decreasing': {'color': "red"},
                'relative': False, 
                'valueformat': '.1f', 
                'suffix': '%'
            },
            gauge={
                'axis': {'range': [0, 36.5]}, 
                'bar': {'color': "green" if valor >= presupuesto else "red"},
                'steps': [
                    {'range': [0, presupuesto], 'color': '#ffe6e6'},
                    {'range': [presupuesto, 36.5], 'color': '#e6ffe6'}
                ],
                'threshold': {
                    'line': {'color': "black", 'width': 4},
                    'thickness': 0.75,
                    'value': presupuesto
                }
            },
            title={
                'text': (
                    "<b style='font-size:25px; color:black;'>🎯 Meta: {presupuesto:.1f}%</b><br>"
                    "<b style='font-size:20px; color:black;'>% Variación vs Presupuesto</b>"
                ).format(presupuesto=presupuesto)
            }
        ))
    fig.update_layout(height=400)  
    st.plotly_chart(fig, use_container_width=True)

    col1, col2, col3 = st.columns([1.8, 1.8, 1.5])

    with col1:
            mostrar_metrica_dinero("Ventas 2024", ventas_2024,"$")

    with col2:
            mostrar_metrica_dinero("Ventas 2025", ventas_2025,"$")

    with col3:
            mostrar_metrica_dinero("Variación Absoluta", variacion_abs,"$")

        

        

