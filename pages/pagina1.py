from funciones import cargar_excel
from funciones import mostrar_gauge_financiero
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
    
    st.markdown("<h1 style='color: white;'>💰 KPIs Área Financiera</h1>", unsafe_allow_html=True)
    aplicar_estilos()
    
    df_mes = pd.read_excel("kpi generales.xlsx", sheet_name="financiera mes", header=None)
    df_mes[0] = df_mes[0].astype(str).str.strip().str.upper()
    margen_bruto_mes = df_mes.loc[df_mes[0] == "MARGEN BRUTO FINAL", 1].values[0] * 100
    margen_neto_mes = df_mes.loc[df_mes[0] == "MARGEN NETO FINAL", 1].values[0] * 100

    mostrar_gauge_financiero(
        titulo_margen=["Margen Bruto", "Margen Neto"],
        valor=[margen_bruto_mes, margen_neto_mes],
        referencia=[51.4, 18],
        color_fondo="white",
        titulo_seccion="Rentabilidad del mes anterior"
    )

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

