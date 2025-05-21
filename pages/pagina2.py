import streamlit as st
import pandas as pd
from plotly.colors import sample_colorscale
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import login

login.generarLogin()

if 'usuario' in st.session_state:
    st.markdown("<h1 style='color: white;'>🛒 KPIs Área Comercial</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='color: black;'>📊 Métricas de los KPIs</h4>", unsafe_allow_html=True)

    # Estilos CSS
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

    st.markdown("<h3 style='color: white;'>Indicador de Cartera </h3>", unsafe_allow_html=True)
    fig = go.Figure(data=[
        go.Pie(
            values=[indicador, 100 - indicador],
            labels=["Avance", "Restante"],
            hole=0.65,
            marker=dict(colors=["#25ABB9", "#F0F0F0"]),
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
            font=dict(size=28, color="#4CAF50"),
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

        
        color_scale = ['#25ABB9', '#28BBCA', '#2BC5D5', '#3CC9D8', '#52CFDC', '#70D7E2']
        df_mapa['color'] = df_mapa['INDICADOR'].apply(lambda x: sample_colorscale(color_scale, x)[0])


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
                text=[f"{row['Supervisor']}<br>{row['INDICADOR']*100:.1f}%"],
                textposition="top right",
                showlegend=False,
                hoverinfo="text",
                hovertemplate=hover_text
            ))

        fig.update_layout(
            mapbox_style="open-street-map",
            mapbox_zoom=5,
            mapbox_center={"lat": df_mapa['lat'].mean(), "lon": df_mapa['lon'].mean()},
            margin=dict(l=0, r=0, t=30, b=0),
            height=600
        )

        st.plotly_chart(fig, use_container_width=True)