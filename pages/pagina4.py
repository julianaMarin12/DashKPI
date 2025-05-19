import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import login

# Autenticación
login.generarLogin()

if 'usuario' in st.session_state:
    st.markdown("<h1 style='color: black;'>🛍️ KPIs Área Mercadeo </h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='color: black;'>📊 Métricas de los KPIs</h4>", unsafe_allow_html=True)

    st.markdown("""
        <style>
            /* Personaliza botones */
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
                /* Tarjetas de métricas */
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

    df = pd.read_excel("kpi generales.xlsx", sheet_name="COMERCIAL1")
    df.columns = df.columns.str.strip()
    df_general = df[df["Unidad de Negocio"] == "Total general"]

    ventas_2024 = df_general["Ventas 2024 rea"].values[0]
    ventas_2025 = df_general["Ventas 2025 rea"].values[0]
    variacion_abs = df_general["Variación 2024/2025"].values[0]
    variacion_pct = df_general["Var% 2024/2025"].values[0]
    presupuestado = df_general["PRESUPUESTADO"].values[0]
    acumulado_anterior = df_general["ACUMULADO MES ANTERIOR"].values[0]

    
    with st.expander("CANALES TOTAL/B2B/B2C + Digital/EXP"):
        col1, col2, col3 = st.columns([1.8, 1.8, 1.5])

        with col1:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-title">Ventas 2024</div>
                    <div class="metric-value">${ventas_2024:,.0f}</div>
                </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-title">Ventas 2025</div>
                    <div class="metric-value">${ventas_2025:,.0f}</div>
                </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-title">Variación Absoluta</div>
                    <div class="metric-value" style="color: black;">${variacion_abs:,.0f}</div>
                </div>
            """, unsafe_allow_html=True)

       

        valor = variacion_pct * 100
        presupuesto = presupuestado * 100


        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=valor,
            number={
                'suffix': '%'
            },
            delta={
                'reference': presupuesto,
                'increasing': {'color': "green"},
                'decreasing': {'color': "red"},
                'relative': False, 
                'valueformat': '.1f', 
                'suffix': '%'
            },
            gauge={
                'axis': {'range': [0, 100]}, 
                'bar': {'color': "green" if valor >= presupuesto else "red"},
                'steps': [
                    {'range': [0, presupuesto], 'color': '#ffe6e6'},
                    {'range': [presupuesto, 100], 'color': '#e6ffe6'}
                ],
                'threshold': {
                    'line': {'color': "blue", 'width': 4},
                    'thickness': 0.75,
                    'value': presupuesto
                }
            },
            title={
                'text': (
                    "<b style='font-size:25px; color:black;'>🎯 Meta: {presupuesto:.1f}%</b><br>"
                    "<b style='font-size:20px; color:black;'>% Variación vs Presupuesto</b>"
                ).format(presupuesto=presupuesto)
            }
        ))

        st.plotly_chart(fig, use_container_width=True)


        

