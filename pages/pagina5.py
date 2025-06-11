from funciones import cargar_excel
from funciones import crear_mapa
from estilos import aplicar_estilos
from funciones import crear_gauge_base64
from funciones import render_df_html
from funciones import imagen_base64
from estilos import crear_header_corporativo
from estilos import crear_seccion_corporativa
from funciones import crear_gauge_corporativo
from funciones import crear_indicador_estado
from funciones import formatear_valor_colombiano
from funciones import mostrar_metrica_corporativa
from funciones import mostrar_metrica_corporativa_mercadeo
from funciones import mostrar_tipologia
from funciones import crear_donut
from funciones import grafico_linea_corporativo
from funciones import grafico_barras_corporativo
from funciones import grafico_barras_dinero
from login import set_background
import streamlit as st
import pandas as pd
import login

st.set_page_config(layout="wide")
aplicar_estilos()
login.generarLogin()
if 'usuario' in st.session_state:
    set_background("images/fondo7.jpg")
    crear_header_corporativo(
        "KPIs ÁREA DE TIENDAS",
        "Indicadores para el área de tiendas"
    )

    tipo_kpi = st.selectbox(
        "Selecciona KPI que desea:",
        ["Rentabilidad Mensual", "Rentabilidad Acumulada"],
    )
    
    if tipo_kpi == "Rentabilidad Acumulada":
        df_acum = pd.read_excel("kpi generales.xlsx", sheet_name="financiera acum", header=None)
        df_acum[0] = df_acum[0].astype(str).str.strip().str.upper()
        margen_bruto_acum = df_acum.loc[df_acum[0] == "MARGEN BRUTO FINAL", 1].values[0] * 100
        utilidad_neto_acum = df_acum.loc[df_acum[0] == "UTILIDAD NETA FINAL", 1].values[0]
        margen_neto_acum = df_acum.loc[df_acum[0] == "MARGEN NETO FINAL", 1].values[0] * 100

        referencia_neto_acum = 22.40
        referencia_bruto_acum = 71.96

        titulo_seccion = "Rentabilidad Neta Acumulada"
        valor = margen_neto_acum
        crear_seccion_corporativa(titulo_seccion, "💵", "")
        col_gauge, col_estado = st.columns([2, 1])
 
        with col_gauge:
            fig = crear_gauge_corporativo(valor, "% EJECUTADO VS PROYECTADO", referencia=referencia_neto_acum)
            st.plotly_chart(fig, use_container_width=True, key="gauge_rentabilidad_neta_acum")
 
        with col_estado:
            crear_indicador_estado(valor, referencia_neto_acum, "Estado VS Objetivo")

        df_top5 = pd.read_excel("kpi generales.xlsx", sheet_name="Top5_dinero_acum")
        df_top5 = df_top5[df_top5["Etiquetas de fila"] != "Total general"]
        df_top5 = df_top5.rename(columns={"Etiquetas de fila": "Tiendas", "UTILIDAD NETA FINAL": "Dinero"})
        df_top5["Dinero"] = pd.to_numeric(df_top5["Dinero"], errors="coerce")
        df_top5["Tiendas"] = df_top5["Tiendas"].str.replace("CAFE QUINDIO EXPRESS ", "", regex=False)
        df_top5["Tiendas"] = df_top5["Tiendas"].str.replace("CAFE QUINDIO EXPRES ", "", regex=False)

        grafico_barras_dinero(
            df_top5,
            x="Tiendas",
            y="Dinero",
            titulo="Top 5 Dinero Acumulado",
            etiquetas={"Tiendas": "Tiendas", "Dinero": "Dinero"}
        )

        titulo_seccion = "Rentabilidad Bruta Acumulada"
 
        crear_seccion_corporativa(titulo_seccion, "💵", "")
        valor = margen_bruto_acum
        col_gauge, col_estado = st.columns([2, 1])
 
        with col_gauge:
            fig = crear_gauge_corporativo(valor, "% EJECUTADO VS PROYECTADO", referencia=referencia_bruto_acum)
            st.plotly_chart(fig, use_container_width=True, key=f"gauge_rentabilidad_bruta_acum")
 
        with col_estado:
            crear_indicador_estado(valor, referencia_bruto_acum, "Estado VS Objetivo")