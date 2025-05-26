import streamlit as st
import pandas as pd
from plotly.colors import sample_colorscale
import plotly.graph_objects as go
import plotly.express as px
from PIL import Image
import numpy as np
import login

st.set_page_config(layout="wide")

login.generarLogin()

if 'usuario' in st.session_state:
    st.markdown("<h1 style='color: white;'>🛒 KPIs Área Comercial</h1>", unsafe_allow_html=True)
    st.markdown("""
        <style>
            div[role="button"] {
                background-color: #ffffff !important;
                color: #333333 !important;
                font-weight: 600;
                font-size: 18px;
                border: 1px solid #dddddd !important;
                border-radius: 12px;
                padding: 12px;
                margin-bottom: 15px;
                box-shadow: 0px 2px 5px rgba(0,0,0,0.1);
            }

            .metric-card {
                background-color: white;
                padding: 20px 10px;
                border-radius: 15px;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                text-align: center;
                margin-bottom: 15px;
            }

            .metric-title {
                font-size: 18px;
                font-weight: 600;
                margin-bottom: 8px;
                color: #333333;
            }
        </style>
    """, unsafe_allow_html=True)

    df_rentabilidad_mes = pd.read_excel("kpi generales.xlsx", sheet_name="rentabilidad comercial mes")
    df_rentabilidad_mes.columns = df_rentabilidad_mes.columns.str.strip()

    df_general = df_rentabilidad_mes[df_rentabilidad_mes["Etiquetas de fila"] == "Total general"]

    utilidad = df_general["UTILIDAD NETA FINAL"].values[0]
    margen = df_general["MARGEN NETO FINAL"].values[0]*100

    st.markdown("<h3 style='color: white;'>Rentabilidad Mensual</h3>",
                    unsafe_allow_html=True)
    
    col_grafico01, col_utilidad = st.columns([1, 2])  
    with col_grafico01:        
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=margen,
            number={'suffix': '%'},
            delta={
                'reference': 20,
                'increasing': {'color': "green"},
                'decreasing': {'color': "red"},
                'relative': False,
                'valueformat': '.2f',
                'suffix': '%'
            },
            gauge={
                'axis': {'range': [0, 20]},
                'bar': {'color': "green" if margen >= 20 else "red"},
                'steps': [
                    {'range': [0, 20], 'color': '#ffe6e6'},
                    {'range': [20, 100], 'color': '#e6ffe6'}
                ],
                'threshold': {
                    'line': {'color': "black", 'width': 4},
                    'thickness': 0.75,
                    'value': 20
                }
            },
            title={
                'text': (
                    "<b style='font-size:20px; color:black;'> Proyección: 20%</b><br>"
                    "<b style='font-size:15px; color:black;'>% Ejecutado vs Proyectado</b>"
                )
            }
        ))
        fig.update_layout(height=300)  
        st.plotly_chart(fig, use_container_width=True)
        

    with col_utilidad:
    
        st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-title">Utilidad Neta</div>
                    <div class="metric-value">${utilidad:,.0f}</div>
                </div>
            """, unsafe_allow_html=True)

        st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-title">Margen Neto</div>
                    <div class="metric-value">{margen:,.2f}%</div>
                </div>
            """, unsafe_allow_html=True)
        
    tipologias_deseadas = [
            "GRANDES SUPERFICIES",
            "TIENDA ESPECIALIZADA",
            "CADENAS REGIONALES",
            "FOOD SERVICE PREMIUM",
            "AUTOSERVICIOS",
            "DISTRIBUIDOR",
            "OTROS CLIENTES NACIONALES"
        ]

    df_tipologia = df_rentabilidad_mes[df_rentabilidad_mes["Etiquetas de fila"].isin(tipologias_deseadas)]

    for _, row in df_tipologia.iterrows():
        ejecutado = row["MARGEN NETO FINAL"] * 100
        utilidad_rentabilidad = row["UTILIDAD NETA FINAL"] 

        color_bar = "green" if ejecutado >= 20 else "red"

        fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number+delta",
                value=ejecutado,
                number={'suffix': '%'},
                delta={
                    'reference': 20,
                    'increasing': {'color': "green"},
                    'decreasing': {'color': "red"},
                    'relative': False,
                    'valueformat': '.2f',
                    'suffix': '%'
                },
                gauge={
                    'axis': {'range': [0, max(67, 20 * 1.1)]},
                    'bar': {'color': color_bar},
                    'steps': [
                        {'range': [0, 20], 'color': '#ffe6e6'},
                        {'range': [20, max(67, 20 * 1.1)], 'color': '#e6ffe6'}
                    ],
                    'threshold': {
                        'line': {'color': "black", 'width': 4},
                        'thickness': 0.75,
                        'value': 20
                    }
                },
                title={
                    'text': (
                        f"<b style='font-size:20px; color:black;'>Proyección:20%</b><br>"
                    )
                }
            ))

        fig_gauge.update_layout(
                margin=dict(t=50, b=20, l=20, r=20),
                height=250,
                width=280
            )
        
        with st.expander(f" {row['Etiquetas de fila']}", expanded=False):
            col1, col2= st.columns(2)
            with col1:
                fig.update_layout(height=200)  
                st.plotly_chart(fig_gauge, use_container_width=True, key=f"gauge_{row['Etiquetas de fila']}")
            with col2:
                st.markdown(
                        f"""
                        <div style="background-color:white; padding:15px; border-radius:15px; box-shadow:0 2px 5px rgba(0,0,0,0.1); color:#333">
                            <p><b>Utilidad:</b> ${utilidad:,.0f}</p>
                            <p><b>Margen:</b> {margen:+.2f} %</p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
    
    df_rentabilidad_acum = pd.read_excel("kpi generales.xlsx", sheet_name="rentabilidad comercial acum")
    df_rentabilidad_acum.columns = df_rentabilidad_acum.columns.str.strip()

    df_general = df_rentabilidad_acum[df_rentabilidad_acum["TIPOLOGIA"] == "Total general"]

    utilidad_acum = df_general["UTILIDAD NETA FINAL"].values[0]
    margen_acum = df_general["MARGEN NETO FINAL"].values[0]*100

    st.markdown("<h3 style='color: white;'>Rentabilidad Acumulado</h3>",
                    unsafe_allow_html=True)
    
    col_grafico02, col_utilidad_acum = st.columns([1, 2])  
    with col_grafico02:        
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=margen_acum,
            number={'suffix': '%'},
            delta={
                'reference': 20,
                'increasing': {'color': "green"},
                'decreasing': {'color': "red"},
                'relative': False,
                'valueformat': '.2f',
                'suffix': '%'
            },
            gauge={
                'axis': {'range': [0, 20]},
                'bar': {'color': "green" if margen_acum >= 20 else "red"},
                'steps': [
                    {'range': [0, 20], 'color': '#ffe6e6'},
                    {'range': [20, 100], 'color': '#e6ffe6'}
                ],
                'threshold': {
                    'line': {'color': "black", 'width': 4},
                    'thickness': 0.75,
                    'value': 20
                }
            },
            title={
                'text': (
                    "<b style='font-size:20px; color:black;'> Proyección: 20%</b><br>"
                    "<b style='font-size:15px; color:black;'>% Ejecutado vs Proyectado</b>"
                )
            }
        ))
        fig.update_layout(height=300)  
        st.plotly_chart(fig, use_container_width=True)
        

    with col_utilidad_acum:
    
        st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-title">Utilidad Neta</div>
                    <div class="metric-value">${utilidad_acum:,.0f}</div>
                </div>
            """, unsafe_allow_html=True)

        st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-title">Margen Neto</div>
                    <div class="metric-value">{margen_acum:,.2f}%</div>
                </div>
            """, unsafe_allow_html=True)

    df_tipologia_acum = df_rentabilidad_acum[df_rentabilidad_acum["TIPOLOGIA"].isin(tipologias_deseadas)]

    for _, row in df_tipologia_acum.iterrows():
        ejecutado_acum = row["MARGEN NETO FINAL"] * 100
        utilidad_rentabilidad_acum = row["UTILIDAD NETA FINAL"] 

        color_bar = "green" if ejecutado_acum >= 20 else "red"

        fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number+delta",
                value=ejecutado,
                number={'suffix': '%'},
                delta={
                    'reference': 20,
                    'increasing': {'color': "green"},
                    'decreasing': {'color': "red"},
                    'relative': False,
                    'valueformat': '.2f',
                    'suffix': '%'
                },
                gauge={
                    'axis': {'range': [0, max(67, 20 * 1.1)]},
                    'bar': {'color': color_bar},
                    'steps': [
                        {'range': [0, 20], 'color': '#ffe6e6'},
                        {'range': [20, max(67, 20 * 1.1)], 'color': '#e6ffe6'}
                    ],
                    'threshold': {
                        'line': {'color': "black", 'width': 4},
                        'thickness': 0.75,
                        'value': 20
                    }
                },
                title={
                    'text': (
                        f"<b style='font-size:20px; color:black;'>Proyección:20%</b><br>"
                    )
                }
            ))

        fig_gauge.update_layout(
                margin=dict(t=50, b=20, l=20, r=20),
                height=250,
                width=280
            )
        
        with st.expander(f" {row['TIPOLOGIA']}", expanded=False):
            col1, col2= st.columns(2)
            with col1:
                fig.update_layout(height=200)  
                st.plotly_chart(fig_gauge, use_container_width=True, key=f"gauge_{row['UTILIDAD NETA FINAL']}")
            with col2:
                st.markdown(
                        f"""
                        <div style="background-color:white; padding:15px; border-radius:15px; box-shadow:0 2px 5px rgba(0,0,0,0.1); color:#333">
                            <p><b>Utilidad:</b> ${utilidad:,.0f}</p>
                            <p><b>Margen:</b> {margen:+.2f} %</p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

    df = pd.read_excel("kpi generales.xlsx", sheet_name="Cartera1")
    df.columns = df.columns.str.strip()
    df['ZONA'] = df['ZONA'].str.upper()
    df_general = df[df["Supervisor"] == "Total general"]

    total_vencido = df_general["TOTAL VENCIDO"].values[0]
    total_corriente = df_general["TOTAL CORRIENTE"].values[0]
    total_cartera = df_general["TOTAL CARTERA"].values[0]
    indicador_f = df_general["INDICADOR"].values[0]
    indicador = indicador_f * 100

    if 0 < indicador <= 60:
        color = "red"
    elif 60 < indicador <= 80:
        color = "#E7E200"
    elif 80 < indicador <= 100:
        color = "green"
    else:
        color = "gray"

    st.markdown("<h3 style='color: white;'>Indicador de Cartera </h3>", unsafe_allow_html=True)
    col_grafico, col_expander = st.columns([1, 2])  

    with col_grafico:
        fig = go.Figure(data=[
            go.Pie(
                values=[indicador, 100 - indicador],
                labels=["Avance", "Restante"],
                hole=0.65,
                marker=dict(colors=[color, "#F0F0F0"]),
                textinfo="none",
                hoverinfo="label+percent",
                sort=False
            )
        ])

        fig.update_layout(
            showlegend=False,
            annotations=[dict(
                text=f"<b>{indicador:.2f}%</b>",
                x=0.5, y=0.5,
                font=dict(size=28, color="black"),
                showarrow=False
            )],
            margin=dict(t=20, b=20, l=20, r=20),
            height=320
        )

        st.plotly_chart(fig, use_container_width=True)

    zona_coords = {
        "ARMENIA": {"lat": 4.533889, "lon": -75.681106},
        "BOGOTÁ": {"lat": 4.711, "lon": -74.0721},
        "ANTIOQUIA": {"lat": 6.2442, "lon": -75.5812},
        "COSTA": {"lat": 10.391, "lon": -75.4794},
        "PACÍFICO": {"lat": 3.4516, "lon": -76.532},
    }

    df['lat'] = df['ZONA'].map(lambda x: zona_coords.get(x, {}).get('lat'))
    df['lon'] = df['ZONA'].map(lambda x: zona_coords.get(x, {}).get('lon'))

    with col_expander:
        col1, col2, col3 = st.columns(3)
        with col1:
                st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-title">Total Vencido</div>
                        <div class="metric-value">${total_vencido:,.0f}</div>
                    </div>
                """, unsafe_allow_html=True)

        with col2:
                st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-title">Total Corriente</div>
                        <div class="metric-value">${total_corriente:,.0f}</div>
                    </div>
                """, unsafe_allow_html=True)

        with col3:
                st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-title">Total Cartera</div>
                        <div class="metric-value">${total_cartera:,.0f}</div>
                    </div>
                """, unsafe_allow_html=True)
        
        with st.expander("MAPA"):
            df_mapa = df.dropna(subset=["lat", "lon", "INDICADOR"])
            df_mapa = df_mapa[df_mapa['ZONA'] != "GENERAL"]

            def aplicar_jitter(df, factor=0.03):
                zona_counts = df['ZONA'].value_counts()
                df_jitter = df.copy()
                for zona, count in zona_counts.items():
                    if count > 1:
                        idx = df_jitter[df_jitter['ZONA'] == zona].index
                        lat_jitter = np.linspace(-factor, factor, count)
                        lon_jitter = np.linspace(-factor, factor, count)
                        df_jitter.loc[idx, 'lat'] += lat_jitter
                        df_jitter.loc[idx, 'lon'] += lon_jitter
                return df_jitter

            df_mapa = aplicar_jitter(df_mapa)

            fig = go.Figure()

            color_scale = ['#25ABB9', '#28BBCA', '#2BC5D5', '#3CC9D8', '#52CFDC', '#70D7E2']
            df_mapa['color'] = df_mapa['INDICADOR'].apply(lambda x: sample_colorscale(color_scale, x)[0])

            for _, row in df_mapa.iterrows():
                fig.add_trace(go.Scattermapbox(
                    lon=[row['lon']],
                    lat=[row['lat']],
                    mode="markers+text",
                    marker=dict(size=10 + row['INDICADOR'] * 40, color=row['color']),
                    text=[(
                        f"{row['Supervisor']}<br>"
                        f"{row['INDICADOR'] * 100:.2f}%<br>"
                        f"${row['TOTAL VENCIDO']:,.0f} vencido<br>"
                        f"${row['TOTAL CORRIENTE']:,.0f} corriente<br>"
                        f"${row['TOTAL CARTERA']:,.0f} cartera"
                    )],
                    textposition="bottom right",
                    showlegend=False
                ))

            fig.update_layout(
                mapbox_style="open-street-map",
                mapbox_zoom=5,
                mapbox_center={"lat": df_mapa['lat'].mean(), "lon": df_mapa['lon'].mean()},
                margin=dict(l=0, r=0, t=30, b=0),
                height=600
            )

            st.plotly_chart(fig, use_container_width=True)

        with st.expander("INDICADORES POR SUPERVISOR"):
            st.markdown("<h3 style='color: white;'>Indicadores por Supervisor</h3>", unsafe_allow_html=True)

            df_supervisores = df_mapa[df_mapa["Supervisor"] != "Total general"]
            cols_per_row = 3

            for i in range(0, len(df_supervisores), cols_per_row):
                cols = st.columns(cols_per_row)
                for j, (_, row) in enumerate(df_supervisores.iloc[i:i + cols_per_row].iterrows()):
    
                  
            
                    indicador_sup = row["INDICADOR"] * 100

                    if 0 < indicador_sup <= 60:
                        color_sup = "red"
                    elif 60 < indicador_sup <= 80:
                        color_sup = "#E7E200"
                    elif 80 < indicador_sup <= 100:
                        color_sup = "green"
                    else:
                        color_sup = "gray"

                    fig_donut = go.Figure(data=[go.Pie(
                        values=[indicador_sup, 100 - indicador_sup],
                        labels=["Avance", "Restante"],
                        hole=0.65,
                        marker=dict(colors=[color_sup, "#F0F0F0"]),
                        textinfo="none",
                        hoverinfo="label+percent",
                        sort=False
                    )])

                    fig_donut.update_layout(
                        showlegend=False,
                        annotations=[dict(
                            text=f"<b>{indicador_sup:.2f}%</b>",
                            x=0.5, y=0.5,
                            font=dict(size=14, color="black"),
                            showarrow=False
                        )],
                        margin=dict(t=10, b=10, l=10, r=10),
                        height=200,
                        width=200
                        
                    )

                
                    with cols[j]:
                        st.markdown(
                            f"<div style='text-align:center; font-size:14px; font-weight:600; color:black; margin-bottom:5px'>{row['Supervisor']}</div>",
                            unsafe_allow_html=True
                        )

                    
                        st.plotly_chart(fig_donut, use_container_width=True)
    
    df1 = pd.read_excel("kpi generales.xlsx", sheet_name="Comercial1")
    df1.columns = df1.columns.str.strip()

    df_general = df1[df1["Productos"] == "Total general"]

    ventas_2025 = df_general["Ventas 2025 rea"].values[0]
    presupesto = df_general["PRESUPUESTO CON LINEA"].values[0]
    ejecutado = df_general["P% COMERCIAL 2024"].values[0]
    proyectado = df_general["prueba"].values[0]
    proyectado_porcent = df_general["prueba 2"].values[0]
    diferencia = df_general["prueba DIFERENCIA DINERO"].values[0]
    diferencia_porcent = df_general["prueba DIFERENCIA"].values[0]
    imagenes = df_general["Ruta Imagen"].values[0]
    ejecutado_comer = ejecutado * 100
    proyectado_comer = proyectado_porcent*100
    diferencia_comer = diferencia_porcent*100

    st.markdown("<h3 style='color: white;'>Presupuesto de Ventas vs Ejecutado</h3>",
                    unsafe_allow_html=True)
    col_grafico1, col_presupuesto = st.columns([1, 2])  
    with col_grafico1:        
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=ejecutado_comer,
            number={'suffix': '%'},
            delta={
                'reference': proyectado_comer,
                'increasing': {'color': "green"},
                'decreasing': {'color': "red"},
                'relative': False,
                'valueformat': '.2f',
                'suffix': '%'
            },
            gauge={
                'axis': {'range': [0, proyectado_comer]},
                'bar': {'color': "green" if ejecutado_comer >= proyectado_comer else "red"},
                'steps': [
                    {'range': [0, proyectado_comer], 'color': '#ffe6e6'},
                    {'range': [proyectado_comer, 75], 'color': '#e6ffe6'}
                ],
                'threshold': {
                    'line': {'color': "black", 'width': 4},
                    'thickness': 0.75,
                    'value': proyectado_comer
                }
            },
            title={
                'text': (
                    "<b style='font-size:20px; color:black;'> Proyección: {proyectado_comer:.2f}%</b><br>"
                    "<b style='font-size:15px; color:black;'>% Variación vs Proyectado</b>"
                ).format(proyectado_comer=proyectado_comer)
            }
        ))
        fig.update_layout(height=300)  
        st.plotly_chart(fig, use_container_width=True)

    with col_presupuesto:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-title">Ventas 2025</div>
                    <div class="metric-value">${ventas_2025:,.0f}</div>
                </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-title">Presupuesto 2025</div>
                    <div class="metric-value">${presupesto:,.0f}</div>
                </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-title">Ejecutado</div>
                    <div class="metric-value">{ejecutado_comer:.2f}%</div>
                </div>
            """, unsafe_allow_html=True)

        col4, col5, col6 = st.columns(3)
        with col4:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-title">Proyectado</div>
                    <div class="metric-value">{proyectado_comer:.2f}%</div>
                </div>
            """, unsafe_allow_html=True)

        with col5:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-title">Diferencia ($)</div>
                    <div class="metric-value">${diferencia:,.0f}</div>
                </div>
            """, unsafe_allow_html=True)

        with col6:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-title">Diferencia (%)</div>
                    <div class="metric-value">{diferencia_comer:.2f}%</div>
                </div>
            """, unsafe_allow_html=True)


    st.markdown("<h3 style='color: white;'> Indicadores de Ventas por Producto</h3>", unsafe_allow_html=True)
    df_productos = df1[df1["Productos"] != "Total general"]

    for _, row in df_productos.iterrows():
        ejecutado = row["P% COMERCIAL 2024"] * 100
        meta = row["prueba 2"] * 100
        diferencia = row["prueba DIFERENCIA"] * 100
        presup = row["PRESUPUESTO CON LINEA"]
        ventas = row["Ventas 2025 rea"]
        ruta_imagen = row["Ruta Imagen"]

        color_bar = "green" if ejecutado >= meta else "red"

        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=ejecutado,
            number={'suffix': '%'},
            delta={
                'reference': meta,
                'increasing': {'color': "green"},
                'decreasing': {'color': "red"},
                'relative': False,
                'valueformat': '.2f',
                'suffix': '%'
            },
            gauge={
                'axis': {'range': [0, max(67, meta * 1.1)]},
                'bar': {'color': color_bar},
                'steps': [
                    {'range': [0, meta], 'color': '#ffe6e6'},
                    {'range': [meta, max(67, meta * 1.1)], 'color': '#e6ffe6'}
                ],
                'threshold': {
                    'line': {'color': "black", 'width': 4},
                    'thickness': 0.75,
                    'value': meta
                }
            },
            title={
                'text': (
                    f"<b style='font-size:20px; color:black;'>Proyección: {meta:.2f}%</b><br>"
                )
            }
        ))

        fig_gauge.update_layout(
            margin=dict(t=50, b=20, l=20, r=20),
            height=250,
            width=280
        )

        with st.expander(f" {row['Productos']}", expanded=False):
            col1, col2, col3 = st.columns([1, 2, 1])

            try:
                img = Image.open(ruta_imagen).convert("RGBA")
                fondo_blanco = Image.new("RGBA", img.size, (255, 255, 255, 255))
                img_con_fondo_blanco = Image.alpha_composite(fondo_blanco, img).convert("RGB")
            except Exception as e:
                st.warning(f"No se pudo cargar la imagen de {row['Productos']}: {e}")
                img_con_fondo_blanco = None

            with col1:
                if img_con_fondo_blanco:
                    st.image(img_con_fondo_blanco, width=300)
                else:
                    st.text("Imagen no disponible")

            with col2:
                st.markdown(
                    f"""
                    <div style="background-color:white; padding:15px; border-radius:15px; box-shadow:0 2px 5px rgba(0,0,0,0.1); color:#333">
                        <p><b>Ventas 2025:</b> ${ventas:,.0f}</p>
                        <p><b>Presupuesto:</b> ${presup:,.0f}</p>
                        <p><b>Ejecutado:</b> {ejecutado:.2f}%</p>
                        <p><b>Diferencia Meta:</b> {diferencia:+.2f} %</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            with col3:
                fig.update_layout(height=300)  
                st.plotly_chart(fig_gauge, use_container_width=True)
    
    df2 = pd.read_excel("kpi generales.xlsx", sheet_name="Comercial2")
    df2.columns = df2.columns.str.strip()

    df_general = df2[df2["sub categoria"] == "Total general"]

    ventas_2025_tipo = df_general["Ventas 2025 rea"].values[0]
    presupesto_tipo = df_general["PRESUPUESTO CON LINEA"].values[0]
    ejecutado_tipo = df_general["P% COMERCIAL 2024"].values[0]
    proyectado_tipo = df_general["prueba"].values[0]
    proyectado_porcent_tipo = df_general["prueba 2"].values[0]
    diferencia_tipo = df_general["prueba DIFERENCIA DINERO"].values[0]
    diferencia_porcent_tipo = df_general["prueba DIFERENCIA"].values[0]
    ejecutado_tipo = ejecutado_tipo * 100
    proyectado_tipo = proyectado_tipo*100
    diferencia_tipo = diferencia_tipo*100

    st.markdown("<h3 style='color: white;'> Indicadores de Ventas por Tipología de Cliente</h3>", unsafe_allow_html=True)
    df_tipo = df2[df2["sub categoria"] != "Total general"]

    for _, row in df_tipo.iterrows():
        ejecutado_tipo = row["P% COMERCIAL 2024"] * 100
        meta_tipo = row["prueba 2"] * 100
        diferencia_tipo = row["prueba DIFERENCIA"] * 100
        presuto_tipo = row["PRESUPUESTO CON LINEA"]
        ventas_tipo = row["Ventas 2025 rea"]

        color_bar = "green" if ejecutado_tipo >= meta_tipo else "red"

        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=ejecutado_tipo,
            number={'suffix': '%'},
            delta={
                'reference': meta_tipo,
                'increasing': {'color': "green"},
                'decreasing': {'color': "red"},
                'relative': False,
                'valueformat': '.2f',
                'suffix': '%'
            },
            gauge={
                'axis': {'range': [0, max(76, meta_tipo * 1.1)]},
                'bar': {'color': color_bar},
                'steps': [
                    {'range': [0, meta_tipo], 'color': '#ffe6e6'},
                    {'range': [meta_tipo, max(76, meta_tipo* 1.1)], 'color': '#e6ffe6'}
                ],
                'threshold': {
                    'line': {'color': "black", 'width': 4},
                    'thickness': 0.75,
                    'value': meta
                }
            },
            title={
                'text': (
                    f"<b style='font-size:20px; color:black;'>Proyección: {meta_tipo:.2f}%</b><br>"
                )
            }
        ))

        fig_gauge.update_layout(
            margin=dict(t=50, b=20, l=20, r=20),
            height=250,
            width=280
        )

        with st.expander(f" {row['sub categoria']}", expanded=False):
            col1, col2 = st.columns([2, 2])
            with col1:
                st.markdown(
                    f"""
                    <div style="background-color:white; padding:15px; border-radius:15px; box-shadow:0 2px 5px rgba(0,0,0,0.1); color:#333">
                        <p><b>Ventas 2025:</b> ${ventas_tipo:,.0f}</p>
                        <p><b>Presupuesto:</b> ${presuto_tipo:,.0f}</p>
                        <p><b>Ejecutado:</b> {ejecutado_tipo:.2f}%</p>
                        <p><b>Diferencia Meta:</b> {diferencia_tipo:+.2f} %</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            with col2:
                fig.update_layout(height=300)  
                st.plotly_chart(fig_gauge, use_container_width=True)