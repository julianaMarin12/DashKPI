import streamlit as st
import plotly.graph_objects as go
import login

login.generarLogin()

if 'usuario' in st.session_state:
    st.markdown("<h1 style='color: black;'>🛒 KPIs Área Comercial</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='color: black;'>📊 Métricas de los KPIs</h4>", unsafe_allow_html=True)

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
            svg {
                fill: #333333 !important;
            }
            .streamlit-expanderContent {
                background-color: #ffffff;
                padding: 20px;
                border-radius: 0 0 12px 12px;
                color: #333333;
            }
        </style>
    """, unsafe_allow_html=True)

    # Lista de KPIs
    kpis = [
        {
            "nombre": "VOLUMEN DE VENTA TOTAL / CANAL",
            "valor": 25000,
            "variación": 5,
            "descripcion": "Total vendido por canal en el mes actual.",
            "valor_max": 50000
        },
        {
            "nombre": "CLIENTES NUEVOS",
            "valor": 120,
            "variación": 8,
            "descripcion": "Nuevos clientes registrados este mes.",
            "valor_max": 200
        },
    ]

    for kpi in kpis:
        with st.expander(f"📊 {kpi['nombre']}"):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.metric(label="Valor", value=f"${kpi['valor']}", delta=f"{kpi['variación']}%")
                st.write(kpi["descripcion"])

            with col2:
                # Gauge personalizado
                fig = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=kpi["valor"],
                    number={'suffix': "k", 'font': {'size': 30}},
                    gauge={
                        'axis': {'range': [0, kpi["valor_max"]], 'tickwidth': 1},
                        'bar': {'color': "lightblue"},
                        'bgcolor': "white",
                        'borderwidth': 1,
                        'steps': [
                            {'range': [0, kpi["valor_max"] * 0.5], 'color': '#e6f2ff'},
                            {'range': [kpi["valor_max"] * 0.5, kpi["valor_max"]], 'color': '#b3d1ff'}
                        ]
                    },
                    domain={'x': [0, 1], 'y': [0, 1]}
                ))
                fig.update_layout(
                    margin=dict(l=10, r=10, t=10, b=10),
                    paper_bgcolor="white",
                    height=200
                )
                st.plotly_chart(fig, use_container_width=True)
