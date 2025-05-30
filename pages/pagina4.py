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

aplicar_estilos()
login.generarLogin()
if 'usuario' in st.session_state:
    st.markdown("<h1 style='color: black;'>🛍️ KPIs Área Mercadeo </h1>", unsafe_allow_html=True)

    df = cargar_excel("kpi generales.xlsx", "mercadeo2")
    df.columns = df.columns.str.strip()
    df_general = df[df["Unidad de Negocio"] == "Total general"]

    ventas_2024 = df_general["Ventas 2024 rea"].values[0]
    ventas_2025 = df_general["Ventas 2025 rea"].values[0]
    variacion_abs = df_general["Variación 2024/2025"].values[0]
    variacion_pct = df_general["Var% 2024/2025"].values[0]
    presupuestado = df_general["PRESUPUESTADO"].values[0]
    acumulado_anterior = df_general["ACUMULADO MES ANTERIOR"].values[0]

    st.markdown("<h3 style='color: black;'> CANALES TOTAL/B2B/B2C + Digital/EXP </h3>", unsafe_allow_html=True)    
    valor = variacion_pct * 100
    presupuesto = presupuestado * 100

    fig = crear_gauge(valor, "Proyección:36.5%",referencia=36.5)
    st.plotly_chart(fig, use_container_width=True)

    col1, col2, col3 = st.columns([1.8, 1.8, 1.5])

    with col1:
            mostrar_metrica_dinero("Ventas 2024", ventas_2024,"$")

    with col2:
            mostrar_metrica_dinero("Ventas 2025", ventas_2025,"$")

    with col3:
            mostrar_metrica_dinero("Variación Absoluta", variacion_abs,"$")
    
    df1 = cargar_excel("kpi generales.xlsx", "lanzamiento")
    df1.columns = df1.columns.str.strip()

    porcentaje = df1["Porcentaje de Lanzamientos Activos"].values[0]*100
    lanzamientos =df1["Lanzamientos Activos"].values[0]
    ventas = df1["Ventas"].values[0]

    st.markdown("<h3 style='color: black;'> INNOVACIÓN/ PORTAFOLIO </h3>", unsafe_allow_html=True)
    fig = crear_gauge(porcentaje, "Proyección:7%",referencia=7)
    st.plotly_chart(fig, use_container_width=True)

    col1, col2, col3 = st.columns([1.8, 1.8, 1.5])
    with col1:
            mostrar_metrica_porcentual("Porcentaje", porcentaje, "%")
    with col2:
            mostrar_metrica_dinero("Lanzamientos Activos", lanzamientos, "$")
    with col3:
            mostrar_metrica_dinero("Ventas", ventas, "$")



def crear_gauge_moderno(valor, titulo, referencia=None, color_scheme="blue"):
    """Crea un gauge moderno con mejor diseño"""
    
    # Definir colores según el esquema
    color_schemes = {
        "blue": {"primary": "#1f77b4", "secondary": "#aec7e8", "background": "#f0f8ff"},
        "green": {"primary": "#2ca02c", "secondary": "#98df8a", "background": "#f0fff0"},
        "red": {"primary": "#d62728", "secondary": "#ff9896", "background": "#fff0f0"},
        "orange": {"primary": "#ff7f0e", "secondary": "#ffbb78", "background": "#fff8f0"}
    }
    
    colors = color_schemes.get(color_scheme, color_schemes["blue"])
    
    # Determinar color basado en el rendimiento vs referencia
    if referencia:
        if valor >= referencia:
            gauge_color = colors["primary"]
        else:
            gauge_color = "#d62728"  # Rojo si está por debajo
    else:
        gauge_color = colors["primary"]
    
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = valor,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': titulo, 'font': {'size': 20, 'color': '#2c3e50'}},
        delta = {'reference': referencia if referencia else 0, 'suffix': '%'},
        gauge = {
            'axis': {'range': [None, 50], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': gauge_color, 'thickness': 0.3},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, referencia if referencia else 25], 'color': '#ffebee'},
                {'range': [referencia if referencia else 25, 50], 'color': '#e8f5e8'}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': referencia if referencia else 30
            }
        }
    ))
    
    fig.update_layout(
        height=300,
        margin=dict(l=20, r=20, t=60, b=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'color': "#2c3e50", 'family': "Arial"}
    )
    
    return fig

def mostrar_metrica_mejorada(titulo, valor, prefijo="", sufijo="", delta=None, delta_color="normal"):
    """Muestra una métrica con diseño mejorado"""
    
    # Formatear el valor
    if isinstance(valor, (int, float)) and abs(valor) >= 1000000:
        valor_formateado = f"{valor/1000000:.1f}M"
    elif isinstance(valor, (int, float)) and abs(valor) >= 1000:
        valor_formateado = f"{valor/1000:.1f}K"
    else:
        valor_formateado = f"{valor:,.0f}" if isinstance(valor, (int, float)) else str(valor)
    
    # CSS personalizado para la métrica
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        border: 1px solid rgba(255,255,255,0.2);
        backdrop-filter: blur(10px);
        text-align: center;
        margin-bottom: 1rem;
    ">
        <h4 style="
            color: white;
            margin: 0 0 0.5rem 0;
            font-size: 0.9rem;
            font-weight: 500;
            opacity: 0.9;
        ">{titulo}</h4>
        <h2 style="
            color: white;
            margin: 0;
            font-size: 1.8rem;
            font-weight: 700;
            text-shadow: 0 2px 4px rgba(0,0,0,0.3);
        ">{prefijo}{valor_formateado}{sufijo}</h2>
        {f'<p style="color: {"#4ade80" if delta_color == "normal" else "#ef4444"}; margin: 0.5rem 0 0 0; font-size: 0.8rem; font-weight: 500;">{delta}</p>' if delta else ''}
    </div>
    """, unsafe_allow_html=True)

def crear_grafico_comparativo(ventas_2024, ventas_2025, variacion_abs):
    """Crea un gráfico comparativo de ventas"""
    
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=('Comparación Anual', 'Crecimiento'),
        specs=[[{"type": "bar"}, {"type": "indicator"}]]
    )
    
    # Gráfico de barras comparativo
    fig.add_trace(
        go.Bar(
            x=['2024', '2025'],
            y=[ventas_2024/1000000, ventas_2025/1000000],
            marker_color=['#3498db', '#2ecc71'],
            text=[f'${ventas_2024/1000000:.0f}M', f'${ventas_2025/1000000:.0f}M'],
            textposition='auto',
            name='Ventas (Millones)'
        ),
        row=1, col=1
    )
    
    # Indicador de crecimiento
    crecimiento_pct = ((ventas_2025 - ventas_2024) / ventas_2024) * 100
    fig.add_trace(
        go.Indicator(
            mode = "number+delta",
            value = crecimiento_pct,
            number = {'suffix': "%", 'font': {'size': 40}},
            title = {"text": "Crecimiento<br>Anual", 'font': {'size': 16}},
            delta = {'reference': 0, 'relative': True},
        ),
        row=1, col=2
    )
    
    fig.update_layout(
        height=400,
        showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=20, r=20, t=60, b=20)
    )
    
    return fig

# Configuración de la página
st.set_page_config(
    page_title="Dashboard de Ventas",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS personalizado para mejorar el diseño
st.markdown("""
<style>
    .main > div {
        padding-top: 2rem;
    }
    
    .stMetric {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .metric-container {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        border: 1px solid rgba(255,255,255,0.2);
        margin-bottom: 1rem;
    }
    
    h1, h2, h3 {
        color: #2c3e50;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    .dashboard-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 20px;
        margin-bottom: 2rem;
        color: white;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
</style>
""", unsafe_allow_html=True)

# Header principal
st.markdown("""
<div class="dashboard-header">
    <h1 style="margin: 0; font-size: 2.5rem; font-weight: 700;">📊 Dashboard de Ventas</h1>
    <h3 style="margin: 0.5rem 0 0 0; font-weight: 400; opacity: 0.9;">CANALES TOTAL/B2B/B2C + Digital/EXP</h3>
</div>
""", unsafe_allow_html=True)
st.markdown("### 🎯 Rendimiento vs Proyección")
col_gauge1, col_gauge2 = st.columns([2, 1])

with col_gauge1:
        fig_gauge = crear_gauge_moderno(
                variacion_pct, 
                "% Ejecutado vs Proyectado",
                referencia=presupuestado,
                color_scheme="blue"
        )
        st.plotly_chart(fig_gauge, use_container_width=True)

with col_gauge2:
        diferencia = variacion_pct - presupuestado
        estado = "🟢 Por encima" if diferencia >= 0 else "🔴 Por debajo"
        
        st.markdown(f"""
        <div style="
                background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                padding: 2rem;
                border-radius: 15px;
                text-align: center;
                color: white;
                height: 250px;
                display: flex;
                flex-direction: column;
                justify-content: center;
        ">
                <h3 style="margin: 0; color: white;">Estado vs Meta</h3>
                <h2 style="margin: 0.5rem 0; color: white;">{estado}</h2>
                <h1 style="margin: 0; color: white; font-size: 2rem;">{diferencia:+.2f}%</h1>
                <p style="margin: 0.5rem 0 0 0; opacity: 0.9;">Meta: {presupuestado}%</p>
        </div>
        """, unsafe_allow_html=True)

                # Métricas principales
        st.markdown("### 💰 Métricas Financieras")
        col1, col2, col3 = st.columns(3)

with col1:
        mostrar_metrica_mejorada(
                "Ventas 2024", 
                ventas_2024, 
                prefijo="$",
                delta="Año base"
        )

with col2:
        crecimiento = ((ventas_2025 - ventas_2024) / ventas_2024) * 100
        mostrar_metrica_mejorada(
                "Ventas 2025", 
                ventas_2025, 
                prefijo="$",
                delta=f"+{crecimiento:.1f}% vs 2024",
                delta_color="normal"
        )

with col3:
        mostrar_metrica_mejorada(
                "Variación Absoluta", 
                variacion_abs, 
                prefijo="$",
                delta="Crecimiento neto"
        )

        # Gráfico comparativo
st.markdown("### 📈 Análisis Comparativo")
fig_comparativo = crear_grafico_comparativo(ventas_2024, ventas_2025, variacion_abs)
st.plotly_chart(fig_comparativo, use_container_width=True)

        # Resumen ejecutivo
st.markdown("### 📋 Resumen Ejecutivo")
col_res1, col_res2 = st.columns(2)

with col_res1:
        st.markdown(f"""
        <div style="
                background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
                padding: 1.5rem;
                border-radius: 15px;
                margin-bottom: 1rem;
        ">
                <h4 style="margin: 0 0 1rem 0; color: #2c3e50;">🎯 Logros Destacados</h4>
                <ul style="color: #2c3e50; margin: 0;">
                <li>Crecimiento del {variacion_pct:.1f}% vs año anterior</li>
                <li>Variación absoluta de ${variacion_abs/1000000:.1f}M</li>
                <li>Tendencia {'positiva' if diferencia >= 0 else 'a mejorar'} vs meta</li>
                </ul>
        </div>
        """, unsafe_allow_html=True)

with col_res2:
        recomendacion = "Mantener estrategia actual" if diferencia >= 0 else "Revisar estrategia comercial"
        st.markdown(f"""
        <div style="
                background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
                padding: 1.5rem;
                border-radius: 15px;
                margin-bottom: 1rem;
        ">
                <h4 style="margin: 0 0 1rem 0; color: #2c3e50;">💡 Recomendaciones</h4>
                <ul style="color: #2c3e50; margin: 0;">
                <li>{recomendacion}</li>
                <li>Monitorear tendencias mensuales</li>
                <li>Optimizar canales de mayor rendimiento</li>
                </ul>
        </div>
        """, unsafe_allow_html=True)