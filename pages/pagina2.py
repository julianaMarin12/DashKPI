import streamlit as st 
import login 

login.generarLogin()
if 'usuario' in st.session_state:
    st.markdown("<h1 style='color: #fff;'>🛒 KPIs Área Comercial</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='color: #eee;'>📊 Métricas de los KPIs</h4>", unsafe_allow_html=True)

    st.markdown("""
        <style>
            .white-box {
                background-color: white;
                padding: 20px;
                border-radius: 12px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                margin-bottom: 10px;
            }
        </style>
    """, unsafe_allow_html=True)

    kpis = [
        {
            "nombre": "VOLUMEN DE VENTA TOTAL / CANAL",
            "valor": "$25,000",
            "variación": "+5% 📈",
            "descripcion": "Representa el total vendido por cada canal de distribución."
        },
    ]

    for kpi in kpis:
        with st.expander( f" {kpi['nombre']}"):
            st.markdown(f"""
                <div class="white-box">
                    <h4>{kpi['nombre']}</h4>
                    <p><strong>Valor:</strong> {kpi['valor']}</p>
                    <p><strong>Variación:</strong> {kpi['variación']}</p>
                    <p>{kpi['descripcion']}</p>
                </div>
            """, unsafe_allow_html=True)