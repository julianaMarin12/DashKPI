from plotly.colors import sample_colorscale
import plotly.graph_objects as go
import numpy as np
import streamlit as st
import pandas as pd
import io 
import base64

def cargar_excel(path, sheet):
    df = pd.read_excel(path, sheet_name=sheet)
    df.columns = df.columns.str.strip()
    return df

def crear_gauge(valor, titulo, referencia, height=300):
    color_bar = "green" if valor >= referencia else "red"
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=valor,
        number={'suffix': '%'},
        delta={
            'reference': referencia,
            'increasing': {'color': "green"},
            'decreasing': {'color': "red"},
            'relative': False,
            'valueformat': '.2f',
            'suffix': '%'
        },
        gauge={
            'axis': {'range': [0,  referencia]},
            'bar': {'color': color_bar},
            'steps': [
                {'range': [0, referencia], 'color': '#ffe6e6'},
                {'range': [referencia, 100], 'color': '#e6ffe6'}
            ],
            'threshold': {
                'line': {'color': "black", 'width': 4},
                'thickness': 0.75,
                'value': referencia
            }
        },
        title={
            'text': f"<b style='font-size:20px; color:black;'> Proyección: {referencia:,.2f}%</b><br>"
                    "<b style='font-size:15px; color:black;'>% Ejecutado vs Proyectado</b>"
        }
    ))
    fig.update_layout(height=height)
    return fig

def mostrar_metrica_porcentual(titulo, valor, sufijo=""):
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">{titulo}</div>
            <div class="metric-value">{valor:,.2f}{sufijo}</div>
        </div>
    """, unsafe_allow_html=True)

def mostrar_metrica_dinero(titulo, valor, prefijo=""):
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">{titulo}</div>
            <div class="metric-value">{prefijo}{valor:,.1f}</div>
        </div>
    """, unsafe_allow_html=True)

def mostrar_tipologia(dataframe, etiqueta_col,referencia):
    for _, row in dataframe.iterrows():
        ejecutado = row["MARGEN NETO FINAL"] * 100
        utilidad = row["UTILIDAD NETA FINAL"]
        fig = crear_gauge(ejecutado, "Proyección:16%",referencia)
        with st.expander(f"{row[etiqueta_col]}", expanded=False):
            col1, col2 = st.columns(2)
            with col1:
                st.plotly_chart(fig, use_container_width=True)
            with col2:
                st.markdown(f"""
                    <div style="background-color:white; padding:15px; border-radius:15px;
                                box-shadow:0 2px 5px rgba(0,0,0,0.1); color:#333">
                        <p><b>Utilidad:</b> ${utilidad:,.0f}</p>
                        <p><b>Margen:</b> {ejecutado:+.2f} %</p>
                    </div>
                """, unsafe_allow_html=True)

def crear_donut(indicador, color="#25ABB9", height=200, width=200, font_size=14):
    fig = go.Figure(data=[go.Pie(
        values=[indicador, 100 - indicador],
        labels=["Avance", "Restante"],
        hole=0.65,
        marker=dict(colors=[color, "#F0F0F0"]),
        textinfo="none",
        hoverinfo="label+percent",
        sort=False
    )])
    fig.update_layout(
        showlegend=False,
        annotations=[dict(
            text=f"<b>{indicador:.2f}%</b>",
            x=0.5, y=0.5,
            font=dict(size=font_size, color="black"),
            showarrow=False
        )],
        margin=dict(t=10, b=10, l=10, r=10),
        height=height,
        width=width
    )
    return fig

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

def crear_mapa(df):
    df_mapa = df.dropna(subset=["lat", "lon", "INDICADOR"])
    df_mapa = df_mapa[df_mapa['ZONA'] != "GENERAL"]
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
    return fig, df_mapa


def mostrar_gauge_financiero(titulo_margen, valor, referencia, color_fondo, titulo_seccion):
    st.markdown(f"<h3 style='color: white;'>{titulo_seccion}</h3>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    for col, nombre, val, ref in zip([col1, col2], ["Margen Bruto", "Margen Neto"], valor, referencia):
        with col:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-title">{nombre}</div>
                </div>
            """, unsafe_allow_html=True)

            color_bar = "green" if val >= ref else "red"
            fig = go.Figure(go.Indicator(
                mode="gauge+number+delta",
                value=val,
                number={'suffix': '%'},
                delta={
                    'reference': ref,
                    'increasing': {'color': "green"},
                    'decreasing': {'color': "red"},
                    'relative': False,
                    'valueformat': '.1f',
                    'suffix': '%'
                },
                gauge={
                    'axis': {'range': [0, ref]},
                    'bar': {'color': color_bar},
                    'steps': [
                        {'range': [0, ref], 'color': '#ffe6e6'},
                        {'range': [ref, 100], 'color': '#e6ffe6'}
                    ],
                    'threshold': {
                        'line': {'color': "black", 'width': 4},
                        'thickness': 0.75,
                        'value': ref
                    }
                },
                title={
                    'text': (
                        f"<b style='font-size:20px; color:black;'>Presupuestado: {ref:.1f}%</b><br>"
                        "<b style='font-size:15px; color:black;'>% Ejecutado vs Presupuesto</b>"
                    )
                }
            ))
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)

            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-title">{nombre}</div>
                    <div class="metric-value">{val:,.2f}%</div>
                </div>
            """, unsafe_allow_html=True)

def crear_gauge_base64(valor, referencia):
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=valor,
            number={'suffix': '%'},
            delta={
                    'reference': referencia,
                    'increasing': {'color': "green"},
                    'decreasing': {'color': "red"},
                    'relative': False,
                    'valueformat': '.1f',
                    'suffix': '%'
                },
            gauge={
                'axis': {'range': [None, 100]},
                'bar': {'color': "green"},
                'steps': [
                    {'range': [0, referencia], 'color': "#ffe6e6"},
                    {'range': [referencia, 100], 'color': "#e6ffe6"}
                ]
            }
        ))
        fig.update_layout(width=200, height=150, margin=dict(l=10, r=10, t=10, b=10))
        
        buf = io.BytesIO()
        fig.write_image(buf, format='png')
        buf.seek(0)
        img_base64 = base64.b64encode(buf.read()).decode('utf-8')
        return f'<img src="data:image/png;base64,{img_base64}" width="150"/>'

def render_df_html(df):
        return df.to_html(escape=False, index=False, formatters={
            'Ventas 2025': lambda x: f"${x:,.0f}",
            'Presupuesto': lambda x: f"${x:,.0f}",
            'Ejecutado (%)': lambda x: f"{x:.2f}%",
            'Meta (%)': lambda x: f"{x:.2f}%",
            'Diferencia (%)': lambda x: f"{x:+.2f}%"
        })