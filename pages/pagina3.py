from funciones import mostrar_metrica_corporativa
from estilos import crear_header_corporativo
from estilos import crear_seccion_corporativa
from estilos import aplicar_estilos
from login import set_background
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
    set_background("images/fondo7.jpg")
    crear_header_corporativo(
        "⛴ KPIs ÁREA DE EXPORTACIONES",
        "Indicadores para el área de exportaciones"
    )

    tipo_kpi = st.selectbox(
        "Selecciona KPI que desea:",
        ["Rentabilidad Mensual y Acumulada", "Barranquero Mensual y Acumulada"],
    )

    if tipo_kpi == "Rentabilidad Mensual y Acumulada":
        df_ind = pd.read_excel("kpi generales.xlsx", sheet_name="rentabilidad exportaciones mes", header=None)
        df_ind[0] = df_ind[0].astype(str).str.strip().str.upper()

        utilidad = df_ind.loc[df_ind[0] == "UTILIDAD NETA FINAL", 1].values[0]
        margen = df_ind.loc[df_ind[0] == "MARGEN NETO FINAL", 1].values[0]*100
        crear_seccion_corporativa("Rentabilidad Exportaciones por mes", "💰", "")

        col1, col2 = st.columns([1, 1])

        with col1:
            mostrar_metrica_corporativa ("Utilidad Neta", utilidad, "$", tipo="primario")

        with col2:
            mostrar_metrica_corporativa ("Margen Neto", margen, sufijo="%", tipo="secundario")
            
        df_ind = pd.read_excel("kpi generales.xlsx", sheet_name="rentabilidad exportaciones acum", header=None)
        df_ind[0] = df_ind[0].astype(str).str.strip().str.upper()

        utilidad = df_ind.loc[df_ind[0] == "UTILIDAD NETA FINAL", 1].values[0]
        margen = df_ind.loc[df_ind[0] == "MARGEN NETO FINAL", 1].values[0]*100

        crear_seccion_corporativa("Rentabilidad Exportaciones acumulado", "💵", "")
        col1, col2 = st.columns([1, 1])

        with col1:
            mostrar_metrica_corporativa ("Utilidad Neta", utilidad, "$", tipo="primario")

        with col2:
            mostrar_metrica_corporativa ("Margen Neto", margen, sufijo="%", tipo="secundario")

    elif tipo_kpi == "Barranquero Mensual y Acumulada":
        df_barranquero = pd.read_excel("kpi generales.xlsx", sheet_name="Mensual Barranquero", header=None)
        df_net_margin = df_barranquero.iloc[0:3, 0:5]  
        df_net_margin.columns = ["CALCULO", "ENERO", "FEBRERO", "MARZO", "ABRIL"]

        df_net = df_net_margin.set_index("CALCULO").T.reset_index()
        df_net.columns = [str(col).strip().upper().replace("Á", "A").replace("É", "E").replace("Í", "I").replace("Ó", "O").replace("Ú", "U") for col in df_net.columns]
        df_net = df_net.rename(columns={
            "MARGEN NETO PROYECTADO": "Proyectado",
            "MARGEN NETO REAL": "Real",
            "INDEX": "Mes"
        })

        crear_seccion_corporativa("Indicadores de rentabilidad mensual de Barranquero", "📊")

        col1= st.columns(2)
        with col1[0]:
            mes = st.selectbox("Selecciona un mes", df_net["Mes"].unique(), key="barranquero_mes")

        valores = df_net[df_net["Mes"] == mes].iloc[0]*100

        col1, col2 = st.columns(2)
        
        with col1:
            mostrar_metrica_corporativa(f"Margen Neto Proyectado ({mes})", f"{valores['Proyectado']:.2f}", sufijo="%", tipo="primario")
        with col2:
            mostrar_metrica_corporativa(f"Margen Neto Real ({mes})", f"{valores['Real']:.2f}", sufijo="%", tipo="secundario")

        df_barranquero = pd.read_excel("kpi generales.xlsx", sheet_name="Acumulado Barranquero", header=None)
        df_barranquero[0] = df_barranquero[0].astype(str).str.strip().str.upper()
        ingreso = df_barranquero.loc[df_barranquero[0] == "INGRESO PROYECTADO", 1].values[0]
        utilidad = df_barranquero.loc[df_barranquero[0] == "UTILIDAD", 1].values[0]
        margen_neto = df_barranquero.loc[df_barranquero[0] == "MARGEN NETO", 1].values[0]*100

        crear_seccion_corporativa("Indicadores de rentabilidad Acumulada de Barranquero", "📊")

        col1, col2, col3 = st.columns(3)
        with col1:
            mostrar_metrica_corporativa(f"Ingreso Proyectado ", ingreso, prefijo="USD ", tipo="secundario")

        with col2:
            mostrar_metrica_corporativa(f"Utilidad", utilidad, prefijo="USD ", tipo="primario")

        with col3:
            mostrar_metrica_corporativa(f"Margen Neto ", margen_neto, sufijo="%", tipo="secundario")
