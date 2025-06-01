from plotly.colors import sample_colorscale
import plotly.graph_objects as go
import numpy as np
import streamlit as st
import pandas as pd
from PIL import Image
from io import BytesIO
import io 
import base64

COLOR_PRIMARIO = "#00B0B2"
COLOR_SECUNDARIO = "#EDEBE9"
COLOR_TEXTO_OSCURO = "#2C3E50"
COLOR_TEXTO_CLARO = "#FFFFFF"
COLOR_ACENTO = "#008B8D"  
COLOR_FONDO = "#F8F9FA"

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
        mode="gauge+number+delta",
        value=valor,
        number={
            'suffix': '%',
            'font': {'size': 28}
        },
        delta={
            'reference': referencia,
            'increasing': {'color': "green", 'symbol': "▲"},
            'decreasing': {'color': "red", 'symbol': "▼"},
            'relative': False,
            'valueformat': '.1f',
            'suffix': '%',
            'position': "bottom" 
        },
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': "green"},
            'steps': [
                {'range': [0, referencia], 'color': "#ffe6e6"},
                {'range': [referencia, 100], 'color': "#e6ffe6"}
            ]
        }
    ))
    fig.update_layout(width=200, height=180, margin=dict(l=10, r=10, t=10, b=10))

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

def imagen_base64(ruta):
        try:
            img = Image.open(ruta).convert("RGBA")
            fondo_blanco = Image.new("RGBA", img.size, (255, 255, 255, 255))
            img_con_fondo_blanco = Image.alpha_composite(fondo_blanco, img).convert("RGB")
                
            buffered = BytesIO()
            img_con_fondo_blanco.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode()
            return f"<img src='data:image/png;base64,{img_str}' width='100'/>"
        except Exception as e:
            return f"<div style='color:red;'>X</div>"
        
def crear_indicador_estado(valor, referencia, titulo):
    diferencia = valor - referencia
    
    if diferencia >= 0:
        estado_color = "#28A745"
        estado_icon = "✓"
        estado_text = "OBJETIVO ALCANZADO"
        bg_color = f"linear-gradient(135deg, #28A745 0%, #20C997 100%)"
    elif -50 <= diferencia < 0 :
        estado_color = "#EFCE4B"
        estado_icon = ""
        estado_text = "ESTA EN AUMENTO"
        bg_color = f"linear-gradient(135deg, #FFD700 0%, #EFCE4B 100%)"
    else:
        estado_color = "#DC3545"
        estado_icon = "⚠"
        estado_text = "REQUIERE ATENCIÓN"
        bg_color = f"linear-gradient(135deg, #DC3545 0%, #E74C3C 100%)"
    
    st.markdown(f"""
    <div style="
        background: {bg_color};
        padding: 2rem;
        border-radius: 12px;
        text-align: center;
        color: white;
        height: 320px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        box-shadow: 0 6px 24px rgba(0,0,0,0.15);
        border: 2px solid rgba(255, 255, 255, 0.2);
    ">
        <div style="font-size: 3.5rem; margin-bottom: 1rem;">{estado_icon}</div>
        <h3 style="margin: 0; color: white; font-size: 1rem; font-weight: 600; letter-spacing: 1px;">{estado_text}</h3>
        <h1 style="margin: 1rem 0; color: white; font-size: 2.5rem; font-weight: 700;">{diferencia:+.1f}%</h1>
        <p style="margin: 0; opacity: 0.9; font-size: 0.9rem;">vs Objetivo: {referencia}%</p>
        <div style="
            width: 60px;
            height: 3px;
            background: rgba(255, 255, 255, 0.5);
            margin: 1rem auto 0;
            border-radius: 2px;
        "></div>
    </div>
    """, unsafe_allow_html=True)

def formatear_valor_colombiano(valor):
    valor_str = f"{valor:,.2f}"
    valor_str = valor_str.replace(",", "X").replace(".", ",").replace("X", ".")
    return valor_str


def mostrar_metrica_corporativa(titulo, valor, prefijo="", sufijo="", tipo="default"):
    if isinstance(valor, (int, float)):
     if isinstance(valor, (int, float)):
        if sufijo == "%":
            valor_formateado = str(valor)
        else:
            if abs(valor) >= 1_000_000_000:
                valor_formateado = valor / 1_000_000_000
                valor_formateado = formatear_valor_colombiano(valor_formateado) 
            elif abs(valor) >= 1_000_000:
                valor_formateado = valor / 1_000_000
                valor_formateado = formatear_valor_colombiano(valor_formateado) 
            elif abs(valor) >= 1_000:
                valor_formateado = valor / 1_000
                valor_formateado = formatear_valor_colombiano(valor_formateado) 
    else:
        valor_formateado = formatear_valor_colombiano(valor)


    
    if tipo == "primario":
        background = f"linear-gradient(135deg, {COLOR_PRIMARIO} 0%, {COLOR_ACENTO} 100%)"
        text_color = COLOR_TEXTO_CLARO
    elif tipo == "secundario":
        background = f"linear-gradient(135deg, {COLOR_SECUNDARIO} 0%, #E0DDD8 100%)"
        text_color = COLOR_TEXTO_OSCURO
        border = f"2px solid {COLOR_PRIMARIO}"
    else:
        background = f"linear-gradient(135deg, {COLOR_SECUNDARIO} 0%, #F5F3F1 100%)"
        text_color = COLOR_TEXTO_OSCURO
        border = f"1px solid {COLOR_PRIMARIO}40"
    
    border_style = f"border: {border};" if tipo == "secundario" else f"border: 1px solid {COLOR_PRIMARIO}20;"
    
    st.markdown(f"""
    <div style="
        background: {background};
        padding: 1.8rem;
        border-radius: 12px;
        {border_style}
        box-shadow: 0 4px 20px rgba(0, 176, 178, 0.15);
        text-align: center;
        margin-bottom: 1rem;
        transition: all 0.3s ease;
    ">
        <h4 style="
            color: {text_color};
            margin: 0 0 0.8rem 0;
            font-size: 0.95rem;
            font-weight: 600;
            letter-spacing: 0.5px;
            text-transform: uppercase;
            opacity: 0.9;
        ">{titulo}</h4>
        <h2 style="
            color: {text_color};
            margin: 0;
            font-size: 2.2rem;
            font-weight: 700;
            line-height: 1.1;
            font-family: 'Segoe UI', sans-serif;
        ">{prefijo}{valor_formateado}{sufijo}</h2>
    </div>
    """, unsafe_allow_html=True)

def crear_header_corporativo(titulo, subtitulo=""):
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, {COLOR_PRIMARIO} 0%, {COLOR_ACENTO} 100%);
        padding: 2.5rem 2rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(0, 176, 178, 0.25);
        position: relative;
        overflow: hidden;
    ">
        <div style="
            position: absolute;
            top: -50%;
            right: -10%;
            width: 200px;
            height: 200px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 50%;
        "></div>
        <div style="
            position: absolute;
            bottom: -30%;
            left: -5%;
            width: 150px;
            height: 150px;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 50%;
        "></div>
        <div style="position: relative; z-index: 2;">
            <h1 style="
                color: {COLOR_TEXTO_CLARO};
                margin: 0;
                font-size: 2.8rem;
                font-weight: 700;
                text-align: center;
                letter-spacing: -0.5px;
            ">{titulo}</h1>
            {f'<p style="color: rgba(255, 255, 255, 0.9); margin: 0.8rem 0 0 0; font-size: 1.2rem; text-align: center; font-weight: 300;">{subtitulo}</p>' if subtitulo else ''}
        </div>
    </div>
    """, unsafe_allow_html=True)

def crear_seccion_corporativa(titulo, icono="", descripcion=""):
    """Crea un header de sección corporativo"""
    st.markdown(f"""
    <div style="
        background: {COLOR_SECUNDARIO};
        border-left: 6px solid {COLOR_PRIMARIO};
        padding: 1.5rem 2rem;
        border-radius: 0 12px 12px 0;
        margin: 2.5rem 0 1.5rem 0;
        box-shadow: 0 4px 16px rgba(0, 176, 178, 0.1);
    ">
        <h3 style="
            color: {COLOR_TEXTO_OSCURO};
            margin: 0;
            font-size: 1.4rem;
            font-weight: 700;
            display: flex;
            align-items: center;
            gap: 0.8rem;
            letter-spacing: 0.3px;
        ">
            {f'<span style="font-size: 1.6rem;">{icono}</span>' if icono else ''}
            {titulo}
        </h3>
        {f'<p style="color: {COLOR_TEXTO_OSCURO}; margin: 0.8rem 0 0 0; font-size: 0.95rem; opacity: 0.8; line-height: 1.4;">{descripcion}</p>' if descripcion else ''}
    </div>
    """, unsafe_allow_html=True)

def crear_gauge_corporativo(valor, titulo, referencia=None):
    """Crea un gauge con diseño corporativo"""
    if referencia:
        if valor >= referencia:
            color_principal = COLOR_PRIMARIO
            color_fondo = "#E8F8F8"
            color_threshold = "#28A745"
        else:
            color_principal = "#DC3545"
            color_fondo = "#FDEAEA"
            color_threshold = "#FFC107"
    else:
        color_principal = COLOR_PRIMARIO
        color_fondo = "#E8F8F8"
        color_threshold = COLOR_ACENTO
    
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = valor,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {
            'text': titulo, 
            'font': {
                'size': 18, 
                'color': COLOR_TEXTO_OSCURO, 
                'family': 'Segoe UI, sans-serif',
                'weight': 600
            }
        },
        delta = {
            'reference': referencia if referencia else 0, 
            'suffix': '%',
            'font': {'size': 16, 'color': COLOR_TEXTO_OSCURO}
        },
        gauge = {
            'axis': {
                'range': [None, max(50, valor * 1.2)], 
                'tickwidth': 2, 
                'tickcolor': COLOR_TEXTO_OSCURO,
                'tickfont': {'size': 12, 'color': COLOR_TEXTO_OSCURO}
            },
            'bar': {'color': color_principal, 'thickness': 0.35},
            'bgcolor': "white",
            'borderwidth': 3,
            'bordercolor': COLOR_SECUNDARIO,
            'steps': [
                {'range': [0, referencia if referencia else 25], 'color': color_fondo},
                {'range': [referencia if referencia else 25, max(50, valor * 1.2)], 'color': '#F8F9FA'}
            ],
            'threshold': {
                'line': {'color': color_threshold, 'width': 4},
                'thickness': 0.75,
                'value': referencia if referencia else 30
            }
        },
        number = {
            'font': {
                'size': 36, 
                'color': color_principal, 
                'family': 'Segoe UI, sans-serif',
                'weight': 700
            },
            'suffix': '%'
        }
    ))
    
    fig.update_layout(
        height=380,
        margin=dict(l=30, r=30, t=80, b=30),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'color': COLOR_TEXTO_OSCURO, 'family': "Segoe UI, sans-serif"}
    )
    
    return fig
