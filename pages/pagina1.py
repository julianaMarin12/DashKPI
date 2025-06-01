from funciones import cargar_excel
from funciones import mostrar_gauge_financiero
from funciones import cargar_excel
from funciones import crear_indicador_estado
from funciones import crear_header_corporativo
from funciones import crear_seccion_corporativa
from funciones import crear_gauge_corporativo
from funciones import mostrar_metrica_corporativa
from funciones import crear_indicador_estado
from plotly.colors import sample_colorscale
from PIL import Image
from login import set_background
from estilos import aplicar_estilos
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import login

login.generarLogin()
set_background("images/fondo1.jpg")
if 'usuario' in st.session_state:
    crear_header_corporativo(
        "🛍️ KPIs ÁREA FINANCIERO",
        "Indicadores para el área financiera"
    )

    aplicar_estilos()
    
    df_mes = pd.read_excel("kpi generales.xlsx", sheet_name="financiera mes", header=None)
    df_mes[0] = df_mes[0].astype(str).str.strip().str.upper()
    margen_bruto_mes = df_mes.loc[df_mes[0] == "MARGEN BRUTO FINAL", 1].values[0] * 100
    margen_neto_mes = df_mes.loc[df_mes[0] == "MARGEN NETO FINAL", 1].values[0] * 100

    crear_seccion_corporativa(
        "Rentabilidad del mes", 
        "💰", 
        "Análisis de rendimiento "
    )

    col_gauge, col_estado = st.columns([2, 2])
    
    with col_gauge:
        valor =margen_neto_mes
        fig = crear_gauge_corporativo(valor, "% EJECUTADO VS PROYECTADO", referencia=18)
        st.plotly_chart(fig, use_container_width=True)
    
    with col_estado:
        crear_indicador_estado(valor,18,"Estado VS Objetivo")

    df_acum = pd.read_excel("kpi generales.xlsx", sheet_name="financiera acum", header=None)
    df_acum[0] = df_acum[0].astype(str).str.strip().str.upper()
    margen_bruto_acum = df_acum.loc[df_acum[0] == "MARGEN BRUTO FINAL", 1].values[0] * 100
    margen_neto_acum = df_acum.loc[df_acum[0] == "MARGEN NETO FINAL", 1].values[0] * 100

    mostrar_gauge_financiero(
        titulo_margen=["Margen Bruto", "Margen Neto"],
        valor=[margen_bruto_acum, margen_neto_acum],
        referencia=[51.4, 18],
        color_fondo="white",
        titulo_seccion="Rentabilidad acumulada"
    )

