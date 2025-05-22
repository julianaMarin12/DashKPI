import streamlit as st
import pandas as pd
from plotly.colors import sample_colorscale
import plotly.graph_objects as go
import plotly.express as px
from PIL import Image
import numpy as np
import login

login.generarLogin()

if 'usuario' in st.session_state:
    st.markdown("<h1 style='color: white;'>🛒 KPIs Área Comercial</h1>",
                unsafe_allow_html=True)
    st.markdown("<h4 style='color: black;'>📊 Métricas de los KPIs</h4>",
                unsafe_allow_html=True)

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

    df = pd.read_excel("kpi generales.xlsx", sheet_name="Cartera1")
    df.columns = df.columns.str.strip()
    df['ZONA'] = df['ZONA'].str.upper()

    df_general = df[df["Supervisor"] == "Total general"]

    total_vencido = df_general["TOTAL VENCIDO"].values[0]
    total_corriente = df_general["TOTAL CORRIENTE"].values[0]
    total_cartera = df_general["TOTAL CARTERA"].values[0]
    indicador_f = df_general["INDICADOR"].values[0]
    indicador = indicador_f * 100

    indicador = indicador_f * 100

    if 0 < indicador <= 60:
        color = "red"
    elif 60 < indicador <= 80:
        color = "#E7E200"
    elif 80 < indicador <= 100:
        color = "green"
    else:
        color = "gray"

    st.markdown("<h3 style='color: white;'>Indicador de Cartera </h3>",
                unsafe_allow_html=True)
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
            text=f"<b>{indicador:.1f}%</b>",
            x=0.5,
            y=0.5,
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

    with st.expander("CARTERA"):
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

        df_mapa = df.dropna(subset=["lat", "lon", "INDICADOR"])
        df_mapa = df_mapa[df_mapa['ZONA'] != "GENERAL"]

        def aplicar_jitter(df, factor=0.02):
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

        color_scale = ['#25ABB9', '#28BBCA',
                       '#2BC5D5', '#3CC9D8', '#52CFDC', '#70D7E2']
        df_mapa['color'] = df_mapa['INDICADOR'].apply(
            lambda x: sample_colorscale(color_scale, x)[0])

        for i, row in df_mapa.iterrows():
            hover_text = (
                f"<b>{row['Supervisor']}</b><br>"
                f"Indicador: {row['INDICADOR']*100:.1f}%<br>"
                f"Total Vencido: ${row['TOTAL VENCIDO']:,.0f}<br>"
                f"Total Corriente: ${row['TOTAL CORRIENTE']:,.0f}<br>"
                f"Total Cartera: ${row['TOTAL CARTERA']:,.0f}<br>"
            )

            fig.add_trace(go.Scattermapbox(
                lon=[row['lon']],
                lat=[row['lat']],
                mode="markers+text",
                marker=dict(size=10 + row['INDICADOR']*40, color=row['color']),
                text=[(
                    f"{row['Supervisor']}<br>"
                    f"{row['INDICADOR']*100:.1f}%<br>"
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
            mapbox_center={
                "lat": df_mapa['lat'].mean(), "lon": df_mapa['lon'].mean()},
            margin=dict(l=0, r=0, t=30, b=0),
            height=600
        )

        st.plotly_chart(fig, use_container_width=True)

        st.markdown(
            "<h3 style='color: white;'>Indicadores por Supervisor</h3>", unsafe_allow_html=True)

        df_supervisores = df_mapa[df_mapa["Supervisor"] != "Total general"]
        cols_per_row = 3

        for i in range(0, len(df_supervisores), cols_per_row):
            cols = st.columns(cols_per_row)
            for j, (_, row) in enumerate(df_supervisores.iloc[i:i+cols_per_row].iterrows()):
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
                        text=f"<b>{indicador_sup:.1f}%</b>",
                        x=0.5,
                        y=0.5,
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

    # -KPI 2------------------------------------------------------------------------------------------------------------------------------------------------
    df = pd.read_excel("kpi generales.xlsx", sheet_name="Comercial1")
    df.columns = df.columns.str.strip()

    df_general = df[df["Productos"] == "Total general"]

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

    st.markdown("<h3 style='color: white;'>Ventas Comerciales Generales</h3>",
                unsafe_allow_html=True)

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
                <div class="metric-value">{diferencia_comer:.1f}%</div>
            </div>
        """, unsafe_allow_html=True)

    col4, col5, col6 = st.columns(3)
    with col4:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Proyectado</div>
                <div class="metric-value">{proyectado_comer:.1f}%</div>
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
                <div class="metric-value">{diferencia_comer:.1f}%</div>
            </div>
        """, unsafe_allow_html=True)


st.markdown("<h3 style='color: white;'>📦 Indicadores por Producto</h3>", unsafe_allow_html=True)
df_productos = df[df["Productos"] != "Total general"]

for _, row in df_productos.iterrows():
    ejecutado = row["P% COMERCIAL 2024"] * 100
    presup = row["PRESUPUESTO CON LINEA"]
    ventas = row["Ventas 2025 rea"]
    diferencia = row["prueba DIFERENCIA"]*100
    ruta_imagen = row["Ruta Imagen"]

    if diferencia < 0:
        color = "red"
    elif diferencia < 5:
        color = "#E7E200"
    else:
        color = "green"

    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=diferencia,
        number={
                'suffix': '%'
            },
        delta={'reference': 0, 'increasing': {'color': "green"}, 'decreasing': {'color': "red"}},
        gauge={
            'axis': {'range': [-10, 67], 'tickwidth': 1, 'tickcolor': "gray"},
            'bar': {'color': color},
            'steps': [
                {'range': [-10, 0], 'color': 'rgba(255, 0, 0, 0.2)'},
                {'range': [0, 20], 'color': 'rgba(231, 226, 0, 0.2)'},
                {'range': [20, 67], 'color': 'rgba(0, 255, 0, 0.2)'}
            ],
            'threshold': {
                'line': {'color': "black", 'width': 2},
                'thickness': 0.75,
                'value': diferencia
            }
        }
    ))

    fig_gauge.update_layout(
        margin=dict(t=20, b=20, l=20, r=20),
        height=200,
        width=250
    )

    with st.expander(f"🔹 {row['Productos']}", expanded=False):
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
                    <p><b>Ejecutado:</b> {ejecutado:.1f}%</p>
                    <p><b>Diferencia Meta 67%:</b> {diferencia:+.1f} pts</p>
                </div>
                """,
                unsafe_allow_html=True
            )

        with col3:
            st.plotly_chart(fig_gauge, use_container_width=True)