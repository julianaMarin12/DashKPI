from estilos import aplicar_estilos
from estilos import crear_header_corporativo
from estilos import crear_seccion_corporativa
from funciones import crear_gauge_corporativo
from funciones import crear_indicador_estado
from funciones import grafico_barras_dinero_horizontal
from funciones import grafico_barras_corporativo
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
        " 🏪 KPIs ÁREA DE TIENDAS",
        "Indicadores para el área de tiendas"
    )

    tipo_kpi = st.selectbox(
        "Selecciona KPI que desea:",
        ["Rentabilidad Mensual", "Rentabilidad Acumulada"],
    )
    
    if tipo_kpi == "Rentabilidad Acumulada":
        df_acum = pd.read_excel("kpi generales.xlsx", sheet_name="Rentabilidad1_acum", header=None)
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
        colores=["#00B0B2"] * len(df_top5)
        
        grafico_barras_dinero_horizontal(
            df_top5,
            x="Tiendas",
            y="Dinero",
            titulo="Top 5 Tiendas con Mejor Utilidad ",
            etiquetas={"Tiendas": "Tiendas", "Dinero": "Dinero"},
            color_barra= colores,
            orden_descendente=False
        )

        df_top5_margen = pd.read_excel("kpi generales.xlsx", sheet_name="Top5")
        df_top5_margen = df_top5_margen[df_top5_margen["Etiquetas de fila"] != "Total general"]
        df_top5_margen = df_top5_margen.rename(columns={"Etiquetas de fila": "Tiendas", "MARGEN NETO FINAL": "Margen Neto"})
        df_top5_margen["Margen Neto"] = pd.to_numeric(df_top5_margen["Margen Neto"], errors="coerce")*100
        df_top5_margen["Tiendas"] = df_top5_margen["Tiendas"].str.replace("CAFE QUINDIO EXPRESS ", "", regex=False)
        df_top5_margen["Tiendas"] = df_top5_margen["Tiendas"].str.replace("CAFE QUINDIO EXPRES ", "", regex=False)
        df_top5_margen["Tiendas"] = df_top5_margen["Tiendas"].str.replace("CAFE QUINDIO EXPR. ", "", regex=False)

        df_top5_margen = df_top5_margen[df_top5_margen["Tiendas"].str.upper() != "EVENTOS"]

        grafico_barras_corporativo(
            df_top5_margen,
            x="Tiendas",
            y="Margen Neto",
            color=None,
            titulo="Top 5 Mejores Tiendas por Margen Neto",
            etiquetas={"Tiendas": "Tiendas", "Margen Neto": "Margen Neto (%)"},
            colores=["#00B0B2"], 
            formato_y="%",
            apilado=False,
            mostrar_valores=True,
            key="grafico_top5_margen"
        )

        df_inf5 = pd.read_excel("kpi generales.xlsx", sheet_name="Inf5_dinero_acum")
        df_inf5 = df_inf5[df_inf5["Etiquetas de fila"] != "Total general"]
        df_inf5 = df_inf5.rename(columns={"Etiquetas de fila": "Tiendas", "UTILIDAD NETA FINAL": "Dinero"})
        df_inf5["Dinero"] = pd.to_numeric(df_inf5["Dinero"], errors="coerce")
        df_inf5["Tiendas"] = df_inf5["Tiendas"].str.replace("CAFE QUINDIO EXPRESS ", "", regex=False)
        df_inf5["Tiendas"] = df_inf5["Tiendas"].str.replace("CAFE QUINDIO EXPRES ", "", regex=False)
        df_inf5["Tiendas"] = df_inf5["Tiendas"].str.replace("CAFE QUINDIO EXPR. ", "", regex=False)
        colores = ["#F4869C"] * len(df_inf5) 

        grafico_barras_dinero_horizontal(
            df_inf5,
            x="Tiendas",
            y="Dinero",
            titulo="Tiendas con Menor Utilidad ",
            etiquetas={"Tiendas": "Tiendas", "Dinero": "Dinero"},
            color_barra=colores,
            orden_descendente=True
        )

        df_inf_acum = pd.read_excel("kpi generales.xlsx", sheet_name="Inf5")
        df_inf_acum = df_inf_acum[df_inf_acum["Etiquetas de fila"] != "Total general"]
        df_inf_acum = df_inf_acum.rename(columns={"Etiquetas de fila": "Tiendas", "MARGEN NETO FINAL": "Margen Neto"})
        df_inf_acum["Margen Neto"] = pd.to_numeric(df_inf_acum["Margen Neto"], errors="coerce")*100
        df_inf_acum["Tiendas"] = df_inf_acum["Tiendas"].str.replace("CAFE QUINDIO EXPRESS ", "", regex=False)
        df_inf_acum["Tiendas"] = df_inf_acum["Tiendas"].str.replace("CAFE QUINDIO EXPRES ", "", regex=False)
        df_inf_acum["Tiendas"] = df_inf_acum["Tiendas"].str.replace("CAFE QUINDIO EXPR. ", "", regex=False)

        df_inf_acum = df_inf_acum[df_inf_acum["Tiendas"].str.upper() != "CARIBE"]


        grafico_barras_corporativo(
            df_inf_acum,
            x="Tiendas",
            y="Margen Neto",
            color=None,
            titulo="Tiendas con Menor Margen Neto",
            etiquetas={"Tiendas": "Tiendas", "Margen Neto": "Margen Neto (%)"},
            colores=["#F4869C"], 
            formato_y="%",
            apilado=False,
            mostrar_valores=True,
            key="grafico_inf5_margen"
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

    elif tipo_kpi == "Rentabilidad Mensual":
        df_mes = pd.read_excel("kpi generales.xlsx", sheet_name="Rentabilidad1_mes", header=None)
        df_mes[0] = df_mes[0].astype(str).str.strip().str.upper()
        margen_bruto_acum = df_mes.loc[df_mes[0] == "MARGEN BRUTO FINAL", 1].values[0] * 100
        utilidad_neto_acum = df_mes.loc[df_mes[0] == "UTILIDAD NETA FINAL", 1].values[0]
        margen_neto_acum = df_mes.loc[df_mes[0] == "MARGEN NETO FINAL", 1].values[0] * 100

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

        df_top5 = pd.read_excel("kpi generales.xlsx", sheet_name="Top5_mes")
        df_top5 = df_top5[df_top5["Etiquetas de fila"] != "Total general"]
        df_top5 = df_top5.rename(columns={"Etiquetas de fila": "Tiendas", "UTILIDAD NETA FINAL": "Dinero"})
        df_top5["Dinero"] = pd.to_numeric(df_top5["Dinero"], errors="coerce")
        df_top5["Tiendas"] = df_top5["Tiendas"].str.replace("CAFE QUINDIO EXPRESS ", "", regex=False)
        df_top5["Tiendas"] = df_top5["Tiendas"].str.replace("CAFE QUINDIO EXPRES ", "", regex=False)
        colores=["#00B0B2"] * len(df_top5)
        
        grafico_barras_dinero_horizontal(
            df_top5,
            x="Tiendas",
            y="Dinero",
            titulo="Top 5 Tiendas con Mejor Utilidad ",
            etiquetas={"Tiendas": "Tiendas", "Dinero": "Dinero"},
            color_barra= colores,
            orden_descendente=False
        )

        df_top5_margen = pd.read_excel("kpi generales.xlsx", sheet_name="Top5_mesp")
        df_top5_margen = df_top5_margen[df_top5_margen["Etiquetas de fila"] != "Total general"]
        df_top5_margen = df_top5_margen.rename(columns={"Etiquetas de fila": "Tiendas", "MARGEN NETO FINAL": "Margen Neto"})
        df_top5_margen["Margen Neto"] = pd.to_numeric(df_top5_margen["Margen Neto"], errors="coerce")*100
        df_top5_margen["Tiendas"] = df_top5_margen["Tiendas"].str.replace("CAFE QUINDIO EXPRESS ", "", regex=False)
        df_top5_margen["Tiendas"] = df_top5_margen["Tiendas"].str.replace("CAFE QUINDIO EXPRES ", "", regex=False)
        df_top5_margen["Tiendas"] = df_top5_margen["Tiendas"].str.replace("CAFE QUINDIO EXPR. ", "", regex=False)

        df_top5_margen = df_top5_margen[df_top5_margen["Tiendas"].str.upper() != "EVENTOS"]

        grafico_barras_corporativo(
            df_top5_margen,
            x="Tiendas",
            y="Margen Neto",
            color=None,
            titulo="Top 5 Mejores Tiendas por Margen Neto",
            etiquetas={"Tiendas": "Tiendas", "Margen Neto": "Margen Neto (%)"},
            colores=["#00B0B2"], 
            formato_y="%",
            apilado=False,
            mostrar_valores=True,
            key="grafico_top5_margen"
        )

        df_inf5_mes = pd.read_excel("kpi generales.xlsx", sheet_name="Inferior")
        df_inf5_mes = df_inf5_mes[df_inf5_mes["Etiquetas de fila"] != "Total general"]
        df_inf5_mes = df_inf5_mes.rename(columns={"Etiquetas de fila": "Tiendas", "UTILIDAD NETA FINAL": "Dinero"})
        df_inf5_mes["Dinero"] = pd.to_numeric(df_inf5_mes["Dinero"], errors="coerce")
        df_inf5_mes["Tiendas"] = df_inf5_mes["Tiendas"].str.replace("CAFE QUINDIO EXPRESS ", "", regex=False)
        df_inf5_mes["Tiendas"] = df_inf5_mes["Tiendas"].str.replace("CAFE QUINDIO EXPRES ", "", regex=False)
        df_inf5_mes["Tiendas"] = df_inf5_mes["Tiendas"].str.replace("CAFE QUINDIO EXPR. ", "", regex=False)
        
        df_inf5_mes = df_inf5_mes[
            ~df_inf5_mes["Tiendas"].str.upper().isin(["GERENCIA", "VIA"])
        ]

        colores = ["#F4869C"] * len(df_inf5_mes) 

        grafico_barras_dinero_horizontal(
            df_inf5_mes,
            x="Tiendas",
            y="Dinero",
            titulo="Tiendas con Menor Utilidad ",
            etiquetas={"Tiendas": "Tiendas", "Dinero": "Dinero"},
            color_barra=colores,
            orden_descendente=True
        )

        df_inf_mes = pd.read_excel("kpi generales.xlsx", sheet_name="Inf5_mesp")
        df_inf_mes = df_inf_mes[df_inf_mes["Etiquetas de fila"] != "Total general"]
        df_inf_mes = df_inf_mes.rename(columns={"Etiquetas de fila": "Tiendas", "MARGEN NETO FINAL": "Margen Neto"})
        df_inf_mes["Margen Neto"] = pd.to_numeric(df_inf_mes["Margen Neto"], errors="coerce")*100
        df_inf_mes["Tiendas"] = df_inf_mes["Tiendas"].str.replace("CAFE QUINDIO EXPRESS ", "", regex=False)
        df_inf_mes["Tiendas"] = df_inf_mes["Tiendas"].str.replace("CAFE QUINDIO EXPRES ", "", regex=False)
        df_inf_mes["Tiendas"] = df_inf_mes["Tiendas"].str.replace("CAFE QUINDIO EXPR. ", "", regex=False)
        
        df_inf_mes = df_inf_mes[df_inf_mes["Tiendas"].str.upper() != "PRIMAVERA"]
        df_inf_mes = df_inf_mes[df_inf_mes["Tiendas"].str.upper() != "CARIBE"]



        grafico_barras_corporativo(
            df_inf_mes,
            x="Tiendas",
            y="Margen Neto",
            color=None,
            titulo="Tiendas con Menor Margen Neto",
            etiquetas={"Tiendas": "Tiendas", "Margen Neto": "Margen Neto (%)"},
            colores=["#F4869C"], 
            formato_y="%",
            apilado=False,
            mostrar_valores=True,
            key="grafico_inf5_margen"
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