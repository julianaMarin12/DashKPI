from funciones import mostrar_metrica_porcentual
from funciones import mostrar_metrica_dinero
from funciones import mostrar_tipologia
from funciones import cargar_excel
from funciones import crear_gauge
from funciones import crear_donut
from funciones import crear_mapa
from plotly.colors import sample_colorscale
from estilos import aplicar_estilos
from PIL import Image
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import login

# Colores corporativos
COLOR_PRIMARIO = "#00B0B2"
COLOR_SECUNDARIO = "#EDEBE9"
COLOR_TEXTO_OSCURO = "#2C3E50"
COLOR_TEXTO_CLARO = "#FFFFFF"
COLOR_ACENTO = "#008B8D"  # Versión más oscura del primario
COLOR_FONDO = "#F8F9FA"

def mostrar_metrica_corporativa(titulo, valor, prefijo="", sufijo="", tipo="default"):
    """Muestra una métrica con diseño corporativo"""
    
    # Formatear el valor según el tipo
    if isinstance(valor, (int, float)):
        if abs(valor) >= 1000000000:
            valor_formateado = f"{valor/1000000000:.1f}B"
        elif abs(valor) >= 1000000:
            valor_formateado = f"{valor/1000000:.1f}M"
        elif abs(valor) >= 1000:
            valor_formateado = f"{valor/1000:.1f}K"
        else:
            valor_formateado = f"{valor:,.0f}"
    else:
        valor_formateado = str(valor)
    
    # Esquemas de color corporativos
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
    """Crea un header corporativo"""
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
    # Determinar colores basado en el rendimiento
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

def crear_indicador_estado(valor, referencia, titulo):
    """Crea un indicador de estado corporativo"""
    diferencia = valor - referencia
    
    if diferencia >= 0:
        estado_color = "#28A745"
        estado_icon = "✓"
        estado_text = "OBJETIVO ALCANZADO"
        bg_color = f"linear-gradient(135deg, #28A745 0%, #20C997 100%)"
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

def mostrar_resumen_corporativo(ventas_2024, ventas_2025, variacion_pct, presupuestado):
    """Muestra un resumen ejecutivo corporativo"""
    crecimiento = ((ventas_2025 - ventas_2024) / ventas_2024) * 100
    diferencia_meta = variacion_pct * 100 - presupuestado
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div style="
            background: {COLOR_SECUNDARIO};
            border: 2px solid {COLOR_PRIMARIO};
            padding: 2rem;
            border-radius: 12px;
            margin-bottom: 1rem;
        ">
            <h4 style="margin: 0 0 1.5rem 0; color: {COLOR_TEXTO_OSCURO}; font-weight: 700; font-size: 1.1rem;">📊 ANÁLISIS DE RENDIMIENTO</h4>
            <div style="color: {COLOR_TEXTO_OSCURO}; line-height: 1.6;">
                <div style="display: flex; justify-content: space-between; margin: 1rem 0; padding: 0.5rem 0; border-bottom: 1px solid {COLOR_PRIMARIO}40;">
                    <span style="font-weight: 600;">Crecimiento Anual:</span>
                    <span style="color: {COLOR_PRIMARIO}; font-weight: 700;">{crecimiento:.1f}%</span>
                </div>
                <div style="display: flex; justify-content: space-between; margin: 1rem 0; padding: 0.5rem 0; border-bottom: 1px solid {COLOR_PRIMARIO}40;">
                    <span style="font-weight: 600;">Diferencia vs Meta:</span>
                    <span style="color: {'#28A745' if diferencia_meta >= 0 else '#DC3545'}; font-weight: 700;">{diferencia_meta:+.1f}%</span>
                </div>
                <div style="display: flex; justify-content: space-between; margin: 1rem 0; padding: 0.5rem 0;">
                    <span style="font-weight: 600;">Estado General:</span>
                    <span style="color: {'#28A745' if diferencia_meta >= 0 else '#DC3545'}; font-weight: 700;">{'POSITIVO' if diferencia_meta >= 0 else 'A MEJORAR'}</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        recomendaciones = [
            "Mantener estrategia actual" if diferencia_meta >= 0 else "Revisar estrategia comercial",
            "Optimizar canales de alto rendimiento",
            "Monitorear KPIs semanalmente",
            "Analizar tendencias del mercado"
        ]
        
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, {COLOR_PRIMARIO} 0%, {COLOR_ACENTO} 100%);
            padding: 2rem;
            border-radius: 12px;
            margin-bottom: 1rem;
            color: white;
        ">
            <h4 style="margin: 0 0 1.5rem 0; color: white; font-weight: 700; font-size: 1.1rem;">💡 RECOMENDACIONES ESTRATÉGICAS</h4>
            <div style="color: white; line-height: 1.6;">
                {''.join([f'<div style="margin: 0.8rem 0; display: flex; align-items: center;"><span style="margin-right: 0.8rem; color: rgba(255,255,255,0.8);">▸</span>{rec}</div>' for rec in recomendaciones])}
            </div>
        </div>
        """, unsafe_allow_html=True)

# CSS corporativo
st.markdown(f"""
<style>
    .main > div {{
        padding-top: 1rem;
    }}
    
    .stApp {{
        background: linear-gradient(135deg, {COLOR_FONDO} 0%, {COLOR_SECUNDARIO} 100%);
    }}
    
    h1, h2, h3 {{
        color: {COLOR_TEXTO_OSCURO};
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }}
    
    .metric-card:hover {{
        transform: translateY(-3px);
        box-shadow: 0 8px 32px rgba(0, 176, 178, 0.2);
    }}
    
    .section-divider {{
        height: 4px;
        background: linear-gradient(90deg, {COLOR_PRIMARIO}, {COLOR_ACENTO});
        border: none;
        border-radius: 2px;
        margin: 3rem 0;
        box-shadow: 0 2px 8px rgba(0, 176, 178, 0.3);
    }}
    
    .stPlotlyChart {{
        background: white;
        border-radius: 12px;
        padding: 1rem;
        box-shadow: 0 4px 16px rgba(0, 176, 178, 0.1);
        border: 1px solid {COLOR_SECUNDARIO};
    }}
</style>
""", unsafe_allow_html=True)

# Aplicar estilos y login
aplicar_estilos()
login.generarLogin()

if 'usuario' in st.session_state:
    # Header principal corporativo
    crear_header_corporativo(
        "🛍️ KPIs ÁREA MERCADEO",
        "Dashboard Ejecutivo de Rendimiento Comercial"
    )

    # Cargar datos
    df = cargar_excel("kpi generales.xlsx", "mercadeo2")
    df.columns = df.columns.str.strip()
    df_general = df[df["Unidad de Negocio"] == "Total general"]

    ventas_2024 = df_general["Ventas 2024 rea"].values[0]
    ventas_2025 = df_general["Ventas 2025 rea"].values[0]
    variacion_abs = df_general["Variación 2024/2025"].values[0]
    variacion_pct = df_general["Var% 2024/2025"].values[0]
    presupuestado = df_general["PRESUPUESTADO"].values[0]
    acumulado_anterior = df_general["ACUMULADO MES ANTERIOR"].values[0]

    # Sección 1: Canales
    crear_seccion_corporativa(
        "CANALES TOTAL/B2B/B2C + DIGITAL/EXP", 
        "🏪", 
        "Análisis integral de rendimiento por canales de distribución y venta"
    )
    
    # Layout principal con gauge e indicador
    col_gauge, col_estado = st.columns([2.2, 1])
    
    with col_gauge:
        valor = variacion_pct * 100
        fig = crear_gauge_corporativo(valor, "% EJECUTADO VS PROYECTADO", referencia=36.5)
        st.plotly_chart(fig, use_container_width=True)
    
    with col_estado:
        crear_indicador_estado(valor, 36.5, "Estado vs Objetivo")

    # Métricas financieras principales
    st.markdown("#### 💰 INDICADORES FINANCIEROS CLAVE")
    col1, col2, col3 = st.columns(3)

    with col1:
        mostrar_metrica_corporativa("VENTAS 2024", ventas_2024, "$", tipo="secundario")

    with col2:
        mostrar_metrica_corporativa("VENTAS 2025", ventas_2025, "$", tipo="primario")

    with col3:
        mostrar_metrica_corporativa("VARIACIÓN ABSOLUTA", variacion_abs, "$", tipo="secundario")

    # Resumen ejecutivo
    st.markdown("#### 📈 RESUMEN EJECUTIVO")
    mostrar_resumen_corporativo(ventas_2024, ventas_2025, variacion_pct, 36.5)

    # Divider corporativo
    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

    # Sección 2: Innovación
    df1 = cargar_excel("kpi generales.xlsx", "lanzamiento")
    df1.columns = df1.columns.str.strip()

    porcentaje = df1["Porcentaje de Lanzamientos Activos"].values[0]*100
    lanzamientos = df1["Lanzamientos Activos"].values[0]
    ventas_innov = df1["Ventas"].values[0]

    crear_seccion_corporativa(
        "INNOVACIÓN Y DESARROLLO DE PORTAFOLIO", 
        "🚀", 
        "Seguimiento estratégico de nuevos productos y lanzamientos comerciales"
    )

    # Layout para innovación
    col_gauge2, col_estado2 = st.columns([2.2, 1])
    
    with col_gauge2:
        fig2 = crear_gauge_corporativo(porcentaje, "% LANZAMIENTOS ACTIVOS", referencia=7)
        st.plotly_chart(fig2, use_container_width=True)
    
    with col_estado2:
        crear_indicador_estado(porcentaje, 7, "Estado Innovación")

    # Métricas de innovación
    st.markdown("#### 🎯 INDICADORES DE INNOVACIÓN")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        mostrar_metrica_corporativa("PORCENTAJE ACTIVO", porcentaje, sufijo="%", tipo="primario")
    
    with col2:
        mostrar_metrica_corporativa("LANZAMIENTOS ACTIVOS", lanzamientos, "$", tipo="secundario")
    
    with col3:
        mostrar_metrica_corporativa("VENTAS INNOVACIÓN", ventas_innov, "$", tipo="primario")

    # Footer corporativo
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, {COLOR_TEXTO_OSCURO} 0%, #34495E 100%);
        padding: 2rem;
        border-radius: 12px;
        margin-top: 3rem;
        text-align: center;
        color: white;
        border-top: 4px solid {COLOR_PRIMARIO};
    ">
        <div style="display: flex; justify-content: center; align-items: center; gap: 2rem; flex-wrap: wrap;">
            <div style="display: flex; align-items: center; gap: 0.5rem;">
                <span style="color: {COLOR_PRIMARIO};">●</span>
                <span>Dashboard Actualizado en Tiempo Real</span>
            </div>
            <div style="display: flex; align-items: center; gap: 0.5rem;">
                <span style="color: {COLOR_PRIMARIO};">●</span>
                <span>Datos Corporativos Verificados</span>
            </div>
            <div style="display: flex; align-items: center; gap: 0.5rem;">
                <span style="color: {COLOR_PRIMARIO};">●</span>
                <span>Análisis Estratégico Automatizado</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)