
from funciones import cargar_excel
from funciones import crear_mapa
from estilos import aplicar_estilos
from funciones import crear_gauge_base64
from funciones import render_df_html
from funciones import imagen_base64
from estilos import crear_header_corporativo
from estilos import crear_seccion_corporativa
from funciones import crear_gauge_corporativo
from funciones import mostrar_metrica_corporativa
from funciones import mostrar_metrica_corporativa_mercadeo
from funciones import mostrar_tipologia
from funciones import crear_donut
from funciones import grafico_linea_corporativo
from funciones import grafico_barras_corporativo
from login import set_background
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import io
from io import BytesIO
import base64
import login


st.set_page_config(layout="wide")
login.generarLogin()
if 'usuario' in st.session_state:
    set_background("images/fondo2.jpg")
    aplicar_estilos()
    crear_header_corporativo("🛒 KPIs Área Comercial","Kpis del area comercial")

    tipo_kpi = st.selectbox(
        "Selecciona KPI que desea:",
        ["Indicador Cartera", "Rentabilidad Mensual y Acumulada","Presupuesto de Ventas Vs Ejecutado Mensual", "Presupuesto de Ventas Vs Ejecutado Acumulado"],
    )

    tipos = [
        "GRANDES SUPERFICIES", "TIENDA ESPECIALIZADA", "CADENAS REGIONALES",
        "FOOD SERVICE PREMIUM", "AUTOSERVICIOS", "DISTRIBUIDOR", "OTROS CLIENTES NACIONALES"
    ]

    if tipo_kpi == "Indicador Cartera":
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
        crear_seccion_corporativa(
            "INDICADOR CARTERA", 
            "🪙"                
        )

        fig = crear_donut(indicador, color=color, height=320, font_size=28)
        st.plotly_chart(fig, use_container_width=True)

        col1, col2, col3 = st.columns(3)
        with col1:
            mostrar_metrica_corporativa("TOTAL VENCIDO", total_vencido, "$", tipo="secundario")

        with col2:
            mostrar_metrica_corporativa("TOTAL CORRIENTE", total_corriente, "$", tipo="primario")

        with col3:
            mostrar_metrica_corporativa("TOTAL CARTERA", total_cartera, "$", tipo="secundario")

        crear_seccion_corporativa(
            "INDICADOR CARTERA POR SUPERVISOR", 
            "🪙"                
        )
        fig_mapa, df_mapa = crear_mapa(df)
        df_supervisores = df_mapa[df_mapa["Supervisor"] != "Total general"]
        cols_per_row = 4
        for i in range(0, len(df_supervisores), cols_per_row):
            cols = st.columns(cols_per_row)
            for j, (_, row) in enumerate(df_supervisores.iloc[i:i + cols_per_row].iterrows()):
                indicador_sup = row["INDICADOR"] * 100
                color_sup = (
                        "#DC3545" if 0 < indicador_sup <= 60 else
                            "#FFC107" if indicador_sup <= 80 else
                            "#00B0B2" if indicador_sup <= 100 else
                            "gray"
                        )
                fig_donut = crear_donut(indicador_sup, color=color_sup)
                with cols[j]:
                    st.markdown(
                                f"<div style='text-align:center; font-size:14px; font-weight:600; color:black; margin-bottom:5px'>{row['Supervisor']}</div>",
                                unsafe_allow_html=True
                            )
                    st.plotly_chart(fig_donut, use_container_width=True)
        
        crear_seccion_corporativa(
            "INDICADOR CARTERA POR ZONA", 
            "🗺️"                
        )               
        
        st.plotly_chart(fig_mapa, use_container_width=True)

    elif tipo_kpi == "Rentabilidad Mensual y Acumulada":
        #RENTABILIDAD MENSUAL
        df_rent_mes = cargar_excel("kpi generales.xlsx", "rentabilidad comercial mes")
        df_general = df_rent_mes[df_rent_mes["Etiquetas de fila"] == "Total general"]
        utilidad = df_general["UTILIDAD NETA FINAL"].values[0]
        margen = df_general["MARGEN NETO FINAL"].values[0] * 100
        proyectado_rentabilidad_mes = 13

        #RENTABILIDAD ACUMULADA
        df_rentabilidad_acum = cargar_excel("kpi generales.xlsx", sheet="rentabilidad comercial acum")
        df_general = df_rentabilidad_acum[df_rentabilidad_acum["TIPOLOGIA"] == "Total general"]
        utilidad_acum = df_general["UTILIDAD NETA FINAL"].values[0]
        margen_acum = df_general["MARGEN NETO FINAL"].values[0] * 100
        proyectado_rentabilidad_acum = 16

        #TIPOLOGIAS A VER 
        tipos = [
            "GRANDES SUPERFICIES", "TIENDA ESPECIALIZADA", "CADENAS REGIONALES",
            "FOOD SERVICE PREMIUM", "AUTOSERVICIOS", "DISTRIBUIDOR", "OTROS CLIENTES NACIONALES"
        ]

    

        df_barras = pd.DataFrame({
            "Tipo": ["Mensual", "Acumulado"],
            "Proyectado": [proyectado_rentabilidad_mes, proyectado_rentabilidad_acum],
            "Ejecutado": [margen, margen_acum]
        })
        df_barras = df_barras.melt(id_vars=["Tipo"], value_vars=["Proyectado", "Ejecutado"], var_name="Indicador", value_name="Valor")
        grafico_barras_corporativo(
            df_barras,
            x="Tipo",
            y="Valor",
            color="Indicador",
            titulo="Rentabilidad: Proyectado vs Ejecutado",
            etiquetas={"Tipo": "Período", "Valor": "Porcentaje (%)"},
            colores=["#F4869C", "#00B0B2"],
            formato_y="%",
            apilado=True,
            mostrar_valores=True
        )

        df_rent_mes = df_rent_mes.rename(columns={"Etiquetas de fila": "TIPOLOGIA"})
        df_tip_mes = df_rent_mes[df_rent_mes["TIPOLOGIA"].isin(tipos)][["TIPOLOGIA", "MARGEN NETO FINAL"]].copy()
        df_tip_acum = df_rentabilidad_acum[df_rentabilidad_acum["TIPOLOGIA"].isin(tipos)][["TIPOLOGIA", "MARGEN NETO FINAL"]].copy()
        df_tip_mes["MARGEN"] = df_tip_mes["MARGEN NETO FINAL"] * 100
        df_tip_acum["MARGEN"] = df_tip_acum["MARGEN NETO FINAL"] * 100
        df_tip_mes["TIPO"] = "Mensual"
        df_tip_acum["TIPO"] = "Acumulado"
        df_final = pd.concat([
            df_tip_mes[["TIPOLOGIA", "TIPO", "MARGEN"]],
            df_tip_acum[["TIPOLOGIA", "TIPO", "MARGEN"]]
        ], ignore_index=True)
            
        grafico_linea_corporativo(
            df_final,
            x="TIPOLOGIA",
            y="MARGEN",
            color="TIPO",
            titulo="Comparativo de Margen Neto por Tipología",
            etiquetas={"TIPOLOGIA": "Tipología", "MARGEN": "Margen Neto (%)"},
            colores=["#F4869C","#00B0B2"]
        )
        
        crear_seccion_corporativa(
            "RENTABILIDAD MENSUAL", 
            "💵"                
        )
        
        col1, col2 = st.columns([2, 2])
        with col1:
            mostrar_metrica_corporativa("Utilidad Neta", utilidad, "$",tipo="primario")
        with col2:
            mostrar_metrica_corporativa("Margen Neto", margen, sufijo="%",tipo="secundario")
        
        df_tip = df_rent_mes[df_rent_mes["TIPOLOGIA"].isin(tipos)]
        mostrar_tipologia(df_tip, "TIPOLOGIA", referencia=0)
    
        crear_seccion_corporativa(
            "RENTABILIDAD ACUMULADA", 
            "💵"                
        )

        col3, col4 = st.columns([2, 2])
        with col3:
            mostrar_metrica_corporativa("Utilidad Neta", utilidad_acum, "$",tipo="secundario")
        with col4:
            mostrar_metrica_corporativa("Margen Neto", margen_acum, sufijo= "%", tipo="primario")
        
        df_tip_acum = df_rentabilidad_acum[df_rentabilidad_acum["TIPOLOGIA"].isin(tipos)]
        mostrar_tipologia(df_tip_acum, "TIPOLOGIA", referencia=0)

        
            

    elif tipo_kpi == "Presupuesto de Ventas Vs Ejecutado Mensual":
        df1 = cargar_excel("kpi generales.xlsx", sheet="Comercial1_mes")
        df_general = df1[df1["Productos"] == "Total general"].iloc[0]
        crear_seccion_corporativa(
            "PRESUPUESTO VS EJECUTADO MENSUAL", 
            "🎯"                
        )
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

        fig = crear_gauge_corporativo(ejecutado_comer, titulo="Presupuesto vs Ejecutado",referencia=proyectado_comer)
        st.plotly_chart(fig, use_container_width=True)

        col1, col2, col3 = st.columns(3)
        with col1:
            mostrar_metrica_corporativa_mercadeo("Ventas 2025", ventas_2025, "$", tipo="primario")
        with col2:
            mostrar_metrica_corporativa("Presupuesto 2025", presupesto, "$", tipo="secundario")
        with col3:
            mostrar_metrica_corporativa("Ejecutado", ejecutado_comer, sufijo="%", tipo="primario")

        col4, col5, col6 = st.columns(3)
        with col4:
            mostrar_metrica_corporativa("Proyectado", proyectado_comer, sufijo= "%", tipo="secundario")
        with col5:
            mostrar_metrica_corporativa("Diferencia", diferencia,"$", tipo="primario")
        with col6:
            mostrar_metrica_corporativa("Diferencia (%)", diferencia_comer, sufijo="%", tipo="secundario")

        def mostrar_tabla_productos():
            df_productosCategoria = df1[df1["Productos"] != "Total general"].copy()
            df_productosCategoria["Ejecutado (%)"] = df_productosCategoria["P% COMERCIAL 2024"] * 100
            df_productosCategoria["Meta (%)"] = df_productosCategoria["prueba 2"] * 100
            df_productosCategoria["Diferencia (%)"] = df_productosCategoria["prueba DIFERENCIA"] * 100
            df_productosCategoria["Presupuesto"] = df_productosCategoria["PRESUPUESTO CON LINEA"]
            df_productosCategoria["Ventas 2025"] = df_productosCategoria["Ventas 2025 rea"]
            df_productosCategoria["Gauge"] = df_productosCategoria.apply(lambda row: crear_gauge_base64(row["Ejecutado (%)"], row["Meta (%)"]), axis=1)
            df_productosCategoria["Imagen Producto"] = df_productosCategoria["Ruta Imagen"].apply(imagen_base64)
            df_mostrar = df_productosCategoria[
                ["Productos", "Imagen Producto", "Ventas 2025", "Presupuesto", 
                "Ejecutado (%)", "Meta (%)", "Diferencia (%)", "Gauge"]
            ]
            st.markdown(render_df_html(df_mostrar).replace('<table', '<table class="tabla-corporativa"'), unsafe_allow_html=True)

        crear_seccion_corporativa(
            "POR PRODUCTOS MENSUAL", 
            "🪙"                
        )         
        mostrar_tabla_productos()

        crear_seccion_corporativa(
            "POR TIPOLOGÍA MENSUAL", 
            "🪙"                
        )  

        df2 = cargar_excel("kpi generales.xlsx", sheet="Comercial2_mes")
        df_tipo = df2[df2["sub categoria"] != "Total general"].copy()
        df_tipo.loc[:, 'Ejecutado (%)'] = df_tipo['P% COMERCIAL 2024'] * 100
        df_tipo.loc[:, 'Meta (%)'] = df_tipo['prueba 2'] * 100
        df_tipo.loc[:, 'Diferencia (%)'] = df_tipo['prueba DIFERENCIA'] * 100
        df_tipo.loc[:, 'Presupuesto'] = df_tipo['PRESUPUESTO CON LINEA']
        df_tipo.loc[:, 'Ventas 2025'] = df_tipo['Ventas 2025 rea']
        df_tipo['Gauge'] = df_tipo.apply(lambda row: crear_gauge_base64(row['Ejecutado (%)'], row['Meta (%)']), axis=1)
        df_mostrar = df_tipo[['sub categoria', 'Ventas 2025', 'Presupuesto', 'Ejecutado (%)', 'Meta (%)', 'Diferencia (%)', 'Gauge']]
        st.markdown(render_df_html(df_mostrar).replace('<table', '<table class="tabla-corporativa"'), unsafe_allow_html=True)

    elif tipo_kpi == "Presupuesto de Ventas Vs Ejecutado Acumulado":
        df1 = cargar_excel("kpi generales.xlsx", sheet="Comercial1_acum")
        df_general = df1[df1["Productos"] == "Total general"].iloc[0]
        crear_seccion_corporativa(
            "PRESUPUESTO VS EJECUTADO MENSUAL", 
            "🎯"                
        )
        ventas_2025 = df_general["Ventas 2025 rea"]
        presupesto = df_general["PRESUPUESTO CON LINEA"]
        ejecutado = df_general["P% COMERCIAL"]*100
        diferencia = df_general["diferencia $"]
        diferencia_porcent = df_general["diferencia %"]
        imagenes = df_general["Ruta Imagen"]
        diferencia_comer = diferencia_porcent * 100

        fig = crear_gauge_corporativo(ejecutado, titulo="Presupuesto vs Ejecutado",referencia=100)
        st.plotly_chart(fig, use_container_width=True)

        col1, col2, col3 = st.columns(3)
        with col1:
            mostrar_metrica_corporativa_mercadeo("Ventas 2025", ventas_2025, "$", tipo="primario")
        with col2:
            mostrar_metrica_corporativa("Presupuesto 2025", presupesto, "$", tipo="secundario")
        with col3:
            mostrar_metrica_corporativa("Diferencia", diferencia,"$", tipo="primario")

        col4, col5 = st.columns(2)
        with col4:
            mostrar_metrica_corporativa("Ejecutado", ejecutado, sufijo="%", tipo="primario")
        with col5:
            mostrar_metrica_corporativa("Diferencia (%)", diferencia_comer, sufijo="%", tipo="secundario")

        def mostrar_tabla_productos():
            df_productosCategoria = df1[df1["Productos"] != "Total general"].copy()
            df_productosCategoria["Ejecutado (%)"] = df_productosCategoria["P% COMERCIAL"] * 100
            df_productosCategoria["Meta (%)"] = 100
            df_productosCategoria["Diferencia ($)"] = df_productosCategoria["diferencia $"]
            df_productosCategoria["Diferencia (%)"] = df_productosCategoria["diferencia %"] * 100
            df_productosCategoria["Ventas 2025"] = df_productosCategoria["Ventas 2025 rea"]
            df_productosCategoria["Gauge"] = df_productosCategoria.apply(lambda row: crear_gauge_base64(row["Ejecutado (%)"], row["Meta (%)"]), axis=1)
            df_productosCategoria["Imagen Producto"] = df_productosCategoria["Ruta Imagen"].apply(imagen_base64)
            df_mostrar = df_productosCategoria[
                ["Productos", "Imagen Producto", "Ventas 2025", 
                "Ejecutado (%)", "Meta (%)","Diferencia ($)", "Diferencia (%)", "Gauge"]
            ]
            st.markdown(render_df_html(df_mostrar).replace('<table', '<table class="tabla-corporativa"'), unsafe_allow_html=True)

        crear_seccion_corporativa(
            "POR PRODUCTOS ACUMULADO", 
            "🪙"                
        )         
        mostrar_tabla_productos()

        crear_seccion_corporativa(
            "POR TIPOLOGÍA ACUMULADO", 
            "🪙"                
        )  

        df2 = cargar_excel("kpi generales.xlsx", sheet="Comercial2_acum")
        df_tipo = df2[df2["sub categoria"] != "Total general"].copy()
        df_tipo.loc[:, 'Ejecutado (%)'] = df_tipo['P% COMERCIAL'] * 100
        df_tipo.loc[:, 'Meta (%)'] = 100
        df_tipo.loc[:, 'Diferencia ($)'] = df_tipo['diferencia $']
        df_tipo.loc[:, 'Diferencia (%)'] = df_tipo['diferencia %'] * 100
        df_tipo.loc[:, 'Ventas 2025'] = df_tipo['Ventas 2025 rea']
        df_tipo['Gauge'] = df_tipo.apply(lambda row: crear_gauge_base64(row['Ejecutado (%)'], row['Meta (%)']), axis=1)
        df_mostrar = df_tipo[['sub categoria', 'Ventas 2025', 'Diferencia ($)', 'Ejecutado (%)', 'Meta (%)', 'Diferencia (%)', 'Gauge']]
        st.markdown(render_df_html(df_mostrar).replace('<table', '<table class="tabla-corporativa"'), unsafe_allow_html=True)