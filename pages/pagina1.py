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
    st.markdown("<h1 style='color: white;'>💰 KPIs Área Financiera</h1>", unsafe_allow_html=True)
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

    df_ind = pd.read_excel("kpi generales.xlsx", sheet_name="financiera mes", header=None)
    df_ind[0] = df_ind[0].astype(str).str.strip().str.upper()

    
    margen_bruto = df_ind.loc[df_ind[0] == "MARGEN BRUTO FINAL", 1].values[0]*100
    margen = df_ind.loc[df_ind[0] == "MARGEN NETO FINAL", 1].values[0]*100


    st.markdown("<h3 style='color: white;'>Rentabilidad del mes anterior</h3>", unsafe_allow_html=True)
    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Margen Bruto</div>
            </div>
        """, unsafe_allow_html=True)
        fig = go.Figure(go.Indicator(
                mode="gauge+number+delta",
                value=margen_bruto,
                number={
                    'suffix': '%'
                },
                delta={
                    'reference': 51.4,
                    'increasing': {'color': "green"},
                    'decreasing': {'color': "red"},
                    'relative': False, 
                    'valueformat': '.1f', 
                    'suffix': '%'
                },
                gauge={
                    'axis': {'range': [0, 51.4]}, 
                    'bar': {'color': "green" if margen_bruto >= 51.4 else "red"},
                    'steps': [
                        {'range': [0, 51.4], 'color': '#ffe6e6'},
                        {'range': [51.4, 100], 'color': '#e6ffe6'}
                    ],
                    'threshold': {
                        'line': {'color': "black", 'width': 4},
                        'thickness': 0.75,
                        'value': 51.4
                    }
                },
                title={
                    'text': (
                        "<b style='font-size:20px; color:black;'>Presupuestado: 51.4%</b><br>"
                        "<b style='font-size:15px; color:black;'>% Ejecutado vs Presupuesto</b>"
                    )
                }
            ))
        fig.update_layout(height=300)  
        st.plotly_chart(fig, use_container_width=True)

        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Margen Bruto</div>
                <div class="metric-value">{margen_bruto:,.2f}%</div>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Margen Neto</div>
            </div>
        """, unsafe_allow_html=True)
        fig = go.Figure(go.Indicator(
                mode="gauge+number+delta",
                value=margen,
                number={
                    'suffix': '%'
                },
                delta={
                    'reference': 18,
                    'increasing': {'color': "green"},
                    'decreasing': {'color': "red"},
                    'relative': False, 
                    'valueformat': '.1f', 
                    'suffix': '%'
                },
                gauge={
                    'axis': {'range': [0, 18]}, 
                    'bar': {'color': "green" if margen>= 18 else "red"},
                    'steps': [
                        {'range': [0, 18], 'color': '#ffe6e6'},
                        {'range': [18, 100], 'color': '#e6ffe6'}
                    ],
                    'threshold': {
                        'line': {'color': "black", 'width': 4},
                        'thickness': 0.75,
                        'value': 18
                    }
                },
                title={
                    'text': (
                        "<b style='font-size:20px; color:black;'>Presupuestado: 18%</b><br>"
                        "<b style='font-size:15px; color:black;'>% Ejecutado vs Presupuesto</b>"
                    )
                }
            ))
        fig.update_layout(height=300)  
        st.plotly_chart(fig, use_container_width=True)
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Margen Neto</div>
                <div class="metric-value">{margen:,.2f}%</div>
            </div>
        """, unsafe_allow_html=True)

    df_ind = pd.read_excel("kpi generales.xlsx", sheet_name="financiera acum", header=None)
    df_ind[0] = df_ind[0].astype(str).str.strip().str.upper()

    
    margen_bruto = df_ind.loc[df_ind[0] == "MARGEN BRUTO FINAL", 1].values[0]*100
    margen = df_ind.loc[df_ind[0] == "MARGEN NETO FINAL", 1].values[0]*100


    st.markdown("<h3 style='color: white;'>Rentabilidad acumulada </h3>", unsafe_allow_html=True)
    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Margen Bruto</div>
            </div>
        """, unsafe_allow_html=True)
        fig = go.Figure(go.Indicator(
                mode="gauge+number+delta",
                value=margen_bruto,
                number={
                    'suffix': '%'
                },
                delta={
                    'reference': 51.4,
                    'increasing': {'color': "green"},
                    'decreasing': {'color': "red"},
                    'relative': False, 
                    'valueformat': '.1f', 
                    'suffix': '%'
                },
                gauge={
                    'axis': {'range': [0, 51.4]}, 
                    'bar': {'color': "green" if margen_bruto >= 51.4 else "red"},
                    'steps': [
                        {'range': [0, 51.4], 'color': '#ffe6e6'},
                        {'range': [51.4, 100], 'color': '#e6ffe6'}
                    ],
                    'threshold': {
                        'line': {'color': "black", 'width': 4},
                        'thickness': 0.75,
                        'value': 51.4
                    }
                },
                title={
                    'text': (
                        "<b style='font-size:20px; color:black;'> Presupuestado: 51.4%</b><br>"
                        "<b style='font-size:15px; color:black;'>% Ejecutado vs Presupuesto</b>"
                    )
                }
            ))
        fig.update_layout(height=300)  
        st.plotly_chart(fig, use_container_width=True)

        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Margen Bruto</div>
                <div class="metric-value">{margen_bruto:,.2f}%</div>
            </div>
        """, unsafe_allow_html=True)

    with col2:

        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Margen Neto</div>
            </div>
        """, unsafe_allow_html=True) 


        fig = go.Figure(go.Indicator(
                mode="gauge+number+delta",
                value=margen,
                number={
                    'suffix': '%'
                },
                delta={
                    'reference': 18,
                    'increasing': {'color': "green"},
                    'decreasing': {'color': "red"},
                    'relative': False, 
                    'valueformat': '.1f', 
                    'suffix': '%'
                },
                gauge={
                    'axis': {'range': [0, 18]}, 
                    'bar': {'color': "green" if margen>= 18 else "red"},
                    'steps': [
                        {'range': [0, 18], 'color': '#ffe6e6'},
                        {'range': [18, 100], 'color': '#e6ffe6'}
                    ],
                    'threshold': {
                        'line': {'color': "black", 'width': 4},
                        'thickness': 0.75,
                        'value': 18
                    }
                },
                title={
                    'text': (
                        "<b style='font-size:20px; color:black;'>Presupuestado: 18%</b><br>"
                        "<b style='font-size:15px; color:black;'>% Ejecutado vs Presupuesto</b>"
                    )
                }
            ))
        fig.update_layout(height=300)  
        st.plotly_chart(fig, use_container_width=True)
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Margen Neto</div>
                <div class="metric-value">{margen:,.2f}%</div>
            </div>
        """, unsafe_allow_html=True)
