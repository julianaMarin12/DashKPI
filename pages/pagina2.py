from funciones import mostrar_metrica_porcentual
from funciones import mostrar_metrica_dinero
from funciones import mostrar_tipologia
from funciones import cargar_excel
from funciones import crear_gauge
from funciones import crear_donut
from funciones import crear_mapa
from estilos import aplicar_estilos
from funciones import crear_gauge_base64
from funciones import render_df_html
from st_aggrid import AgGrid, GridOptionsBuilder
from PIL import Image
from login import set_background
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import io
import base64
import	kaleido
import login


st.set_page_config(layout="wide")
login.generarLogin()
if 'usuario' in st.session_state:
    set_background("images/fondo2.jpg")
    st.markdown("<h1 style='color: black;'>🛒 KPIs Área Comercial</h1>", unsafe_allow_html=True)
    aplicar_estilos()
    df_rent_mes = cargar_excel("kpi generales.xlsx", "rentabilidad comercial mes")
    df_general = df_rent_mes[df_rent_mes["Etiquetas de fila"] == "Total general"]
    utilidad = df_general["UTILIDAD NETA FINAL"].values[0]
    margen = df_general["MARGEN NETO FINAL"].values[0] * 100
    proyectado_rentabilidad_mes = 13
    st.markdown("<h3 style='color: black;'>Rentabilidad Mensual</h3>", unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2])
    with col1:
        st.plotly_chart(crear_gauge(margen, "Rentabilidad Mensual",referencia=proyectado_rentabilidad_mes), use_container_width=True)
    with col2:
        mostrar_metrica_dinero("Utilidad Neta", utilidad, "$")
        mostrar_metrica_porcentual("Margen Neto", margen, "%")

    tipos = [
        "GRANDES SUPERFICIES", "TIENDA ESPECIALIZADA", "CADENAS REGIONALES",
        "FOOD SERVICE PREMIUM", "AUTOSERVICIOS", "DISTRIBUIDOR", "OTROS CLIENTES NACIONALES"
    ]
    df_tip = df_rent_mes[df_rent_mes["Etiquetas de fila"].isin(tipos)]
    mostrar_tipologia(df_tip, "Etiquetas de fila",referencia=proyectado_rentabilidad_mes)

    #RENTABILIDAD ACUMULADA
    df_rentabilidad_acum = cargar_excel("kpi generales.xlsx", sheet="rentabilidad comercial acum")
    df_general = df_rentabilidad_acum[df_rentabilidad_acum["TIPOLOGIA"] == "Total general"]
    utilidad_acum = df_general["UTILIDAD NETA FINAL"].values[0]
    margen_acum = df_general["MARGEN NETO FINAL"].values[0] * 100
    proyectado_rentabilidad_acum = 16
    st.markdown("<h3 style='color: black;'>Rentabilidad Acumulado</h3>", unsafe_allow_html=True)

    col_grafico02, col_utilidad_acum = st.columns([1, 2])
    with col_grafico02:
        fig = crear_gauge(margen_acum, "Proyección:16%",referencia=proyectado_rentabilidad_acum)
        st.plotly_chart(fig, use_container_width=True)

    with col_utilidad_acum:
        mostrar_metrica_dinero("Utilidad Neta", utilidad_acum, "$")
        mostrar_metrica_porcentual("Margen Neto", margen_acum, "%")
    
    df_tipologia_acum = df_rentabilidad_acum[df_rentabilidad_acum["TIPOLOGIA"].isin(tipos)]
    mostrar_tipologia(df_tipologia_acum, etiqueta_col="TIPOLOGIA",referencia=proyectado_rentabilidad_acum)

    #INDICADOR DE CARTERA
    df = cargar_excel("kpi generales.xlsx", "Cartera1")
    df['ZONA'] = df['ZONA'].str.upper()
    df_general = df[df["Supervisor"] == "Total general"]
    total_vencido = df_general["TOTAL VENCIDO"].values[0]
    total_corriente = df_general["TOTAL CORRIENTE"].values[0]
    total_cartera = df_general["TOTAL CARTERA"].values[0]
    indicador_f = df_general["INDICADOR"].values[0]
    indicador = indicador_f * 100
    color = (
        "red" if 0 < indicador <= 60 else
        "#E7E200" if indicador <= 80 else
        "green" if indicador <= 100 else
        "gray"
    )

    zona_coords = {
        "ARMENIA": {"lat": 4.533889, "lon": -75.681106},
        "BOGOTÁ": {"lat": 4.711, "lon": -74.0721},
        "ANTIOQUIA": {"lat": 6.2442, "lon": -75.5812},
        "COSTA": {"lat": 10.391, "lon": -75.4794},
        "PACÍFICO": {"lat": 3.4516, "lon": -76.532},
    }
    df['lat'] = df['ZONA'].map(lambda x: zona_coords.get(x, {}).get('lat'))
    df['lon'] = df['ZONA'].map(lambda x: zona_coords.get(x, {}).get('lon'))

    st.markdown("<h3 style='color: black;'>Indicador de Cartera</h3>", unsafe_allow_html=True)

    col_grafico, col_expander = st.columns([1, 2])
    with col_grafico:
        fig = crear_donut(indicador, color=color, height=320, font_size=28)
        st.plotly_chart(fig, use_container_width=True)

    with col_expander:
        col1, col2, col3 = st.columns(3)
        with col1:
            mostrar_metrica_dinero("Total Vencido", total_vencido,"$")
        with col2:
            mostrar_metrica_dinero("Total Corriente", total_corriente,"$")
        with col3:
            mostrar_metrica_dinero("Total Cartera", total_cartera,"$")

        with st.expander("MAPA"):
            fig_mapa, df_mapa = crear_mapa(df)
            st.plotly_chart(fig_mapa, use_container_width=True)

        with st.expander("INDICADORES POR SUPERVISOR"):
            st.markdown("<h3 style='color: black;'>Indicadores por Supervisor</h3>", unsafe_allow_html=True)
            df_supervisores = df_mapa[df_mapa["Supervisor"] != "Total general"]
            cols_per_row = 3
            for i in range(0, len(df_supervisores), cols_per_row):
                cols = st.columns(cols_per_row)
                for j, (_, row) in enumerate(df_supervisores.iloc[i:i + cols_per_row].iterrows()):
                    indicador_sup = row["INDICADOR"] * 100
                    color_sup = (
                        "red" if 0 < indicador_sup <= 60 else
                        "#E7E200" if indicador_sup <= 80 else
                        "green" if indicador_sup <= 100 else
                        "gray"
                    )
                    fig_donut = crear_donut(indicador_sup, color=color_sup)
                    with cols[j]:
                        st.markdown(
                            f"<div style='text-align:center; font-size:14px; font-weight:600; color:black; margin-bottom:5px'>{row['Supervisor']}</div>",
                            unsafe_allow_html=True
                        )
                        st.plotly_chart(fig_donut, use_container_width=True)
    
    df1 = cargar_excel("kpi generales.xlsx", sheet="Comercial1")
    df_general = df1[df1["Productos"] == "Total general"].iloc[0]

    ventas_2025 = df_general["Ventas 2025 rea"]
    presupesto = df_general["PRESUPUESTO CON LINEA"]
    ejecutado = df_general["P% COMERCIAL 2024"]
    proyectado = df_general["prueba"]
    proyectado_porcent = df_general["prueba 2"]
    diferencia = df_general["prueba DIFERENCIA DINERO"]
    diferencia_porcent = df_general["prueba DIFERENCIA"]
    imagenes = df_general["Ruta Imagen"]

    ejecutado_comer = ejecutado * 100
    proyectado_comer = proyectado_porcent * 100
    diferencia_comer = diferencia_porcent * 100

    st.markdown("<h3 style='color: black;'>Presupuesto de Ventas vs Ejecutado</h3>", unsafe_allow_html=True)

    col_grafico1, col_presupuesto = st.columns([1, 2])

    with col_grafico1:
        fig = crear_gauge(ejecutado_comer, titulo="Presupuesto vs Ejecutado",referencia=proyectado_comer)
        st.plotly_chart(fig, use_container_width=True)

    with col_presupuesto:
        col1, col2, col3 = st.columns(3)
        with col1:
            mostrar_metrica_dinero("Ventas 2025", ventas_2025, "$")
        with col2:
            mostrar_metrica_dinero("Presupuesto 2025", presupesto, "$")
        with col3:
            mostrar_metrica_porcentual("Ejecutado", ejecutado_comer, "%")

        col4, col5, col6 = st.columns(3)
        with col4:
            mostrar_metrica_porcentual("Proyectado", proyectado_comer, "%")
        with col5:
            mostrar_metrica_dinero("Diferencia", diferencia,"$")
        with col6:
            mostrar_metrica_porcentual("Diferencia (%)", diferencia_comer, "%")

    st.markdown("<h3 style='color: black;'>Indicadores de Ventas por Producto</h3>", unsafe_allow_html=True)
    df_productos = df1[df1["Productos"] != "Total general"].copy()
    def img_formatter(path):
        if path:
            return f'<img src="{path}" width="50" />'
        return ""

    df_productos["Imagen"] = df_productos["Ruta Imagen"].apply(img_formatter)

    df_display = df_productos[["Productos", "Imagen", "Ventas 2025 rea", "PRESUPUESTO CON LINEA", "P% COMERCIAL 2024", "prueba DIFERENCIA"]].copy()
    df_display.rename(columns={
        "Ventas 2025 rea": "Ventas 2025",
        "PRESUPUESTO CON LINEA": "Presupuesto",
        "P% COMERCIAL 2024": "Ejecutado %",
        "prueba DIFERENCIA": "Diferencia %",
    }, inplace=True)

    gb = GridOptionsBuilder.from_dataframe(df_display)
    gb.configure_column("Imagen", cellRenderer='html')  
    gb.configure_pagination()
    gridOptions = gb.build()

    st.markdown("### Indicadores de Ventas por Producto")
    AgGrid(df_display, gridOptions=gridOptions, enable_enterprise_modules=False, fit_columns_on_grid_load=True, height=300)

    st.markdown("### Gauges por Producto")
    for _, row in df_productos.iterrows():
        ejecutado = row["P% COMERCIAL 2024"] * 100
        meta = row["prueba 2"] * 100
        fig_gauge = crear_gauge(ejecutado, titulo=f"Proyección {row['Productos']}", referencia=meta)
        st.plotly_chart(fig_gauge, use_container_width=True)

    df2 = cargar_excel("kpi generales.xlsx", sheet="Comercial2")
    df_general = df2[df2["sub categoria"] == "Total general"]
    ventas_2025_tipo = df_general["Ventas 2025 rea"].values[0]
    presupuesto_tipo = df_general["PRESUPUESTO CON LINEA"].values[0]
    ejecutado_tipo = df_general["P% COMERCIAL 2024"].values[0] * 100
    proyectado_tipo = df_general["prueba"].values[0] * 100
    proyectado_porcent_tipo = df_general["prueba 2"].values[0] * 100
    diferencia_tipo = df_general["prueba DIFERENCIA DINERO"].values[0] * 100
    diferencia_porcent_tipo = df_general["prueba DIFERENCIA"].values[0] * 100

    st.markdown("<h3 style='color: black;'>Indicadores de Ventas por Tipología de Cliente</h3>", unsafe_allow_html=True)

    df_tipo = df2[df2["sub categoria"] != "Total general"].copy()
    df_tipo.loc[:, 'Ejecutado (%)'] = df_tipo['P% COMERCIAL 2024'] * 100
    df_tipo.loc[:, 'Meta (%)'] = df_tipo['prueba 2'] * 100
    df_tipo.loc[:, 'Diferencia (%)'] = df_tipo['prueba DIFERENCIA'] * 100
    df_tipo.loc[:, 'Presupuesto'] = df_tipo['PRESUPUESTO CON LINEA']
    df_tipo.loc[:, 'Ventas 2025'] = df_tipo['Ventas 2025 rea']

    df_tipo['Gauge'] = df_tipo.apply(lambda row: crear_gauge_base64(row['Ejecutado (%)'], row['Meta (%)']), axis=1)
    df_mostrar = df_tipo[['sub categoria', 'Ventas 2025', 'Presupuesto', 'Ejecutado (%)', 'Meta (%)', 'Diferencia (%)', 'Gauge']]

    
    st.markdown(render_df_html(df_mostrar), unsafe_allow_html=True)
