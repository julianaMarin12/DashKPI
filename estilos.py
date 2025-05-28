import streamlit as st

def aplicar_estilos():
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
                font-size: 16px;
                font-weight: 600;
                margin-bottom: 8px;
                color: #333333;
            }
                
            .metric-value {
                font-size: 1.4rem;
                font-weight: bold;
                color: #222;
            }
            header, footer, .stDeployButton {
                visibility: hidden;
            }
        </style>
    """, unsafe_allow_html=True)

