from funciones import crear_indicador_estado
from estilos import crear_header_corporativo
from estilos import crear_seccion_corporativa
from funciones import crear_gauge_corporativo
from funciones import mostrar_metrica_corporativa
from funciones import crear_indicador_estado
from funciones import grafico_barras_corporativo
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
 
st.set_page_config(layout="wide")
login.generarLogin()
set_background("images/fondo4.jpg")
if 'usuario' in st.session_state:
    crear_header_corporativo(
        "🛍️ KPIs ÁREA FINANCIERO",
        "Indicadores para el área financiera"
    )
 
    aplicar_estilos()
    #MES
    df_mes = pd.read_excel("kpi generales.xlsx", sheet_name="financiera mes", header=None)
    df_mes[0] = df_mes[0].astype(str).str.strip().str.upper()
    margen_bruto_mes = df_mes.loc[df_mes[0] == "MARGEN BRUTO FINAL", 1].values[0] * 100
    margen_neto_mes = df_mes.loc[df_mes[0] == "MARGEN NETO FINAL", 1].values[0] * 100
    #ACUM
    df_acum = pd.read_excel("kpi generales.xlsx", sheet_name="financiera acum", header=None)
    df_acum[0] = df_acum[0].astype(str).str.strip().str.upper()
    margen_bruto_acum = df_acum.loc[df_acum[0] == "MARGEN BRUTO FINAL", 1].values[0] * 100
    margen_neto_acum = df_acum.loc[df_acum[0] == "MARGEN NETO FINAL", 1].values[0] * 100

    tipo_rentabilidad = st.selectbox( " Seleccione el KPI que desea visualizar:",
            [   
                "Cumplimiento de Rentabilidad",
                "Rentabilidad Mensual",
                "Rentabilidad Acumulada",
            ],
        )
    referencia_neto_acum= 18.13
    referencia_neto_mes = 15.62
    referencia_bruto=51.4
    if tipo_rentabilidad =="Cumplimiento de Rentabilidad":
        titulo_seccion = "Cumplimiento de Rentabilidad"
        valor = margen_neto_mes
        crear_seccion_corporativa(titulo_seccion, "🎯", "")
        df_barras = pd.DataFrame({
            "Tipo": ["Neta Mensual", "Neta Acumulada", "Bruta Mensual", "Bruta Acumulada"],
            "Ejecutado": [margen_neto_mes, margen_neto_acum, margen_bruto_mes, margen_bruto_acum],
            "Referencia": [referencia_neto_mes, referencia_neto_acum, referencia_bruto, referencia_bruto]
        })
        df_barras = df_barras.melt(id_vars=["Tipo"], value_vars=["Ejecutado", "Referencia"], var_name="Indicador", value_name="Valor")
        grafico_barras_corporativo(
            df_barras,
            x="Tipo",
            y="Valor",
            color="Indicador",
            titulo="Rentabilidad: Ejecutado vs Proyectado",
            etiquetas={"Tipo": "Tipo de Rentabilidad", "Valor": "Porcentaje (%)"},
            colores=["#00B0B2", "#F4869C"],
            formato_y="%",
            apilado=True,
            mostrar_valores=True
        )
 
 
    elif tipo_rentabilidad == "Rentabilidad Mensual":
        titulo_seccion = "Rentabilidad Neta del mes"
        valor = margen_neto_mes
        crear_seccion_corporativa(titulo_seccion, "💵", "")
        col_gauge, col_estado = st.columns([2, 1])
 
        with col_gauge:
            fig = crear_gauge_corporativo(valor, "% EJECUTADO VS PROYECTADO", referencia=referencia_neto_mes)
            st.plotly_chart(fig, use_container_width=True, key=f"gauge_{tipo_rentabilidad.lower()}")
 
        with col_estado:
            crear_indicador_estado(valor, referencia_neto_mes, "Estado VS Objetivo")
        titulo_seccion = "Rentabilidad Bruta mensual"
 
        crear_seccion_corporativa(titulo_seccion, "💵", "")
        valor = margen_bruto_mes
        col_gauge, col_estado = st.columns([2, 1])
 
        with col_gauge:
            fig = crear_gauge_corporativo(valor, "% EJECUTADO VS PROYECTADO", referencia=referencia_bruto)
            st.plotly_chart(fig, use_container_width=True, key=f"gauge_{titulo_seccion.lower()}")
 
        with col_estado:
            crear_indicador_estado(valor, referencia_bruto, "Estado VS Objetivo")
    elif tipo_rentabilidad == "Rentabilidad Acumulada": 
        titulo_seccion = "Rentabilidad Neta acumulada"
        crear_seccion_corporativa(titulo_seccion, "💰", "")
        valor = margen_neto_acum
        col_gauge, col_estado = st.columns([2, 1])
 
        with col_gauge:
            fig = crear_gauge_corporativo(valor, "% EJECUTADO VS PROYECTADO", referencia=referencia_neto_acum)
            st.plotly_chart(fig, use_container_width=True, key=f"gauge_{tipo_rentabilidad.lower()}")
 
        with col_estado:
            crear_indicador_estado(valor, referencia_neto_acum, "Estado VS Objetivo")
        titulo_seccion = "Rentabilidad Bruta Acumulada"
        valor = margen_bruto_acum
        crear_seccion_corporativa(titulo_seccion, "💰", "")
        col_gauge, col_estado = st.columns([2, 1])
 
        with col_gauge:
            fig = crear_gauge_corporativo(valor, "% EJECUTADO VS PROYECTADO", referencia=referencia_bruto)
            st.plotly_chart(fig, use_container_width=True, key=f"gauge_{titulo_seccion.lower()}")
 
        with col_estado:
            crear_indicador_estado(valor, referencia_bruto, "Estado VS Objetivo")