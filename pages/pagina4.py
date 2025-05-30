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

# Función para crear métricas mejoradas
def mostrar_metrica_mejorada(titulo, valor, prefijo="", sufijo="", tipo="default"):
    """Muestra una métrica con diseño mejorado"""
    
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
    
    # Esquemas de color según el tipo
    color_schemes = {
        "ventas": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
        "innovacion": "linear-gradient(135deg, #f093fb 0%, #f5576c 100%)",
        "variacion": "linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)",
        "default": "linear-gradient(135deg, #a8edea 0%, #fed6e3 100%)"
    }
    
    background = color_schemes.get(tipo, color_schemes["default"])
    
    st.markdown(f"""
    <div style="
        background: {background};
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.15);
        border: 1px solid rgba(255,255,255,0.2);
        backdrop-filter: blur(10px);
        text-align: center;
        margin-bottom: 1rem;
        transition: transform 0.3s ease;
    ">
        <h4 style="
            color: white;
            margin: 0 0 0.5rem 0;
            font-size: 0.95rem;
            font-weight: 500;
            opacity: 0.95;
            text-shadow: 0 1px 2px rgba(0,0,0,0.1);
        ">{titulo}</h4>
        <h2 style="
            color: white;
            margin: 0;
            font-size: 2rem;
            font-weight: 700;
            text-shadow: 0 2px 4px rgba(0,0,0,0.2);
            line-height: 1.2;
        ">{prefijo}{valor_formateado}{sufijo}</h2>
    </div>
    """, unsafe_allow_html=True)

def crear_seccion_header(titulo, icono="📊", descripcion=""):
    """Crea un header de sección mejorado"""
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
        padding: 1.5rem 2rem;
        border-radius: 15px;
        margin: 2rem 0 1.5rem 0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        border-left: 5px solid #3498db;
    ">
        <h3 style="
            color: white;
            margin: 0;
            font-size: 1.5rem;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        ">
            <span style="font-size: 1.8rem;">{icono}</span>
            {titulo}
        </h3>
        {f'<p style="color: #bdc3c7; margin: 0.5rem 0 0 0; font-size: 0.9rem;">{descripcion}</p>' if descripcion else ''}
    </div>
    """, unsafe_allow_html=True)

def crear_gauge_mejorado(valor, titulo, referencia=None):
    """Crea un gauge con diseño mejorado"""
    # Determinar color basado en el rendimiento
    if referencia:
        if valor >= referencia:
            color_principal = "#2ecc71"  # Verde
            color_fondo = "#d5f4e6"
        else:
            color_principal = "#e74c3c"  # Rojo
            color_fondo = "#fdeaea"
    else:
        color_principal = "#3498db"  # Azul
        color_fondo = "#ebf3fd"
    
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = valor,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {
            'text': titulo, 
            'font': {'size': 18, 'color': '#2c3e50', 'family': 'Arial Black'}
        },
        delta = {'reference': referencia if referencia else 0, 'suffix': '%'},
        gauge = {
            'axis': {
                'range': [None, max(50, valor * 1.2)], 
                'tickwidth': 2, 
                'tickcolor': "#34495e",
                'tickfont': {'size': 12, 'color': '#2c3e50'}
            },
            'bar': {'color': color_principal, 'thickness': 0.4},
            'bgcolor': "white",
            'borderwidth': 3,
            'bordercolor': "#bdc3c7",
            'steps': [
                {'range': [0, referencia if referencia else 25], 'color': color_fondo},
                {'range': [referencia if referencia else 25, max(50, valor * 1.2)], 'color': '#f8f9fa'}
            ],
            'threshold': {
                'line': {'color': "#e67e22", 'width': 5},
                'thickness': 0.8,
                'value': referencia if referencia else 30
            }
        },
        number = {
            'font': {'size': 32, 'color': color_principal, 'family': 'Arial Black'},
            'suffix': '%'
        }
    ))
    
    fig.update_layout(
        height=350,
        margin=dict(l=30, r=30, t=80, b=30),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'color': "#2c3e50", 'family': "Arial"}
    )
    
    return fig

def mostrar_resumen_ejecutivo(ventas_2024, ventas_2025, variacion_pct, presupuestado):
    """Muestra un resumen ejecutivo con insights"""
    crecimiento = ((ventas_2025 - ventas_2024) / ventas_2024) * 100
    diferencia_meta = variacion_pct * 100 - presupuestado
    
    col1, col2 = st.columns(2)
    
    with col1:
        estado_meta = "🎯 Meta Alcanzada" if diferencia_meta >= 0 else "⚠️ Por Debajo de Meta"
        color_estado = "#2ecc71" if diferencia_meta >= 0 else "#e74c3c"
        
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #ffeaa7 0%, #fab1a0 100%);
            padding: 1.5rem;
            border-radius: 15px;
            box-shadow: 0 8px 25px rgba(0,0,0,0.1);
            margin-bottom: 1rem;
        ">
            <h4 style="margin: 0 0 1rem 0; color: #2c3e50; font-weight: 600;">📈 Rendimiento General</h4>
            <div style="color: #2c3e50;">
                <p style="margin: 0.5rem 0;"><strong>Crecimiento Anual:</strong> {crecimiento:.1f}%</p>
                <p style="margin: 0.5rem 0;"><strong>Estado vs Meta:</strong> <span style="color: {color_estado};">{estado_meta}</span></p>
                <p style="margin: 0.5rem 0;"><strong>Diferencia:</strong> {diferencia_meta:+.1f}%</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        recomendacion = "Mantener estrategia actual y optimizar canales de alto rendimiento" if diferencia_meta >= 0 else "Revisar estrategia comercial y acelerar iniciativas de crecimiento"
        
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #a29bfe 0%, #6c5ce7 100%);
            padding: 1.5rem;
            border-radius: 15px;
            box-shadow: 0 8px 25px rgba(0,0,0,0.1);
            margin-bottom: 1rem;
        ">
            <h4 style="margin: 0 0 1rem 0; color: white; font-weight: 600;">💡 Recomendaciones</h4>
            <div style="color: white;">
                <p style="margin: 0.5rem 0; line-height: 1.4;">{recomendacion}</p>
                <p style="margin: 0.5rem 0;">• Monitorear KPIs semanalmente</p>
                <p style="margin: 0.5rem 0;">• Analizar canales de mayor conversión</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

# CSS mejorado
st.markdown("""
<style>
    .main > div {
        padding-top: 1rem;
    }
    
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(0,0,0,0.2);
    }
    
    h1, h2, h3 {
        color: #2c3e50;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    .dashboard-title {
        text-align: center;
        padding: 2rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 20px;
        margin-bottom: 2rem;
        color: white;
        box-shadow: 0 15px 35px rgba(0,0,0,0.2);
    }
    
    .section-divider {
        height: 3px;
        background: linear-gradient(90deg, #667eea, #764ba2);
        border: none;
        border-radius: 2px;
        margin: 2rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Aplicar estilos y login
aplicar_estilos()
login.generarLogin()

if 'usuario' in st.session_state:
    # Header principal mejorado
    st.markdown("""
    <div class="dashboard-title">
        <h1 style="margin: 0; font-size: 2.5rem; font-weight: 700;">🛍️ KPIs Área Mercadeo</h1>
        <p style="margin: 0.5rem 0 0 0; font-size: 1.1rem; opacity: 0.9;">Dashboard Ejecutivo de Rendimiento</p>
    </div>
    """, unsafe_allow_html=True)

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
    crear_seccion_header(
        "CANALES TOTAL/B2B/B2C + Digital/EXP", 
        "🏪", 
        "Análisis de rendimiento por canales de venta"
    )
    
    # Gauge y métricas en layout mejorado
    col_gauge, col_info = st.columns([2, 1])
    
    with col_gauge:
        valor = variacion_pct * 100
        fig = crear_gauge_mejorado(valor, "% Ejecutado vs Proyectado", referencia=36.5)
        st.plotly_chart(fig, use_container_width=True)
    
    with col_info:
        diferencia = valor - 36.5
        estado_icon = "🟢" if diferencia >= 0 else "🔴"
        estado_text = "Superando Meta" if diferencia >= 0 else "Por Debajo de Meta"
        
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #fd79a8 0%, #fdcb6e 100%);
            padding: 2rem;
            border-radius: 15px;
            text-align: center;
            color: white;
            height: 300px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            box-shadow: 0 10px 30px rgba(0,0,0,0.15);
        ">
            <h3 style="margin: 0; color: white; font-size: 1.2rem;">Estado Actual</h3>
            <div style="font-size: 3rem; margin: 0.5rem 0;">{estado_icon}</div>
            <h2 style="margin: 0; color: white; font-size: 1.3rem;">{estado_text}</h2>
            <h1 style="margin: 0.5rem 0; color: white; font-size: 2.2rem;">{diferencia:+.1f}%</h1>
            <p style="margin: 0; opacity: 0.9; font-size: 0.9rem;">vs Meta: 36.5%</p>
        </div>
        """, unsafe_allow_html=True)

    # Métricas financieras
    st.markdown("#### 💰 Métricas Financieras")
    col1, col2, col3 = st.columns(3)

    with col1:
        mostrar_metrica_mejorada("Ventas 2024", ventas_2024, "$", tipo="ventas")

    with col2:
        mostrar_metrica_mejorada("Ventas 2025", ventas_2025, "$", tipo="ventas")

    with col3:
        mostrar_metrica_mejorada("Variación Absoluta", variacion_abs, "$", tipo="variacion")

    # Resumen ejecutivo
    st.markdown("#### 📊 Resumen Ejecutivo")
    mostrar_resumen_ejecutivo(ventas_2024, ventas_2025, variacion_pct, 36.5)

    # Divider
    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

    # Sección 2: Innovación
    df1 = cargar_excel("kpi generales.xlsx", "lanzamiento")
    df1.columns = df1.columns.str.strip()

    porcentaje = df1["Porcentaje de Lanzamientos Activos"].values[0]*100
    lanzamientos = df1["Lanzamientos Activos"].values[0]
    ventas_innov = df1["Ventas"].values[0]

    crear_seccion_header(
        "INNOVACIÓN / PORTAFOLIO", 
        "🚀", 
        "Seguimiento de nuevos productos y lanzamientos"
    )

    # Layout para innovación
    col_gauge2, col_info2 = st.columns([2, 1])
    
    with col_gauge2:
        fig2 = crear_gauge_mejorado(porcentaje, "% Lanzamientos Activos", referencia=7)
        st.plotly_chart(fig2, use_container_width=True)
    
    with col_info2:
        diferencia_innov = porcentaje - 7
        estado_icon2 = "🟢" if diferencia_innov >= 0 else "🔴"
        estado_text2 = "Meta Superada" if diferencia_innov >= 0 else "Necesita Impulso"
        
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #00b894 0%, #00cec9 100%);
            padding: 2rem;
            border-radius: 15px;
            text-align: center;
            color: white;
            height: 300px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            box-shadow: 0 10px 30px rgba(0,0,0,0.15);
        ">
            <h3 style="margin: 0; color: white; font-size: 1.2rem;">Innovación</h3>
            <div style="font-size: 3rem; margin: 0.5rem 0;">{estado_icon2}</div>
            <h2 style="margin: 0; color: white; font-size: 1.3rem;">{estado_text2}</h2>
            <h1 style="margin: 0.5rem 0; color: white; font-size: 2.2rem;">{diferencia_innov:+.1f}%</h1>
            <p style="margin: 0; opacity: 0.9; font-size: 0.9rem;">vs Meta: 7%</p>
        </div>
        """, unsafe_allow_html=True)

    # Métricas de innovación
    st.markdown("#### 🎯 Métricas de Innovación")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        mostrar_metrica_mejorada("Porcentaje", porcentaje, sufijo="%", tipo="innovacion")
    
    with col2:
        mostrar_metrica_mejorada("Lanzamientos Activos", lanzamientos, "$", tipo="innovacion")
    
    with col3:
        mostrar_metrica_mejorada("Ventas Innovación", ventas_innov, "$", tipo="innovacion")

    # Footer con información adicional
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin-top: 3rem;
        text-align: center;
        color: white;
    ">
        <p style="margin: 0; opacity: 0.8;">Dashboard actualizado automáticamente • Datos en tiempo real</p>
    </div>
    """, unsafe_allow_html=True)