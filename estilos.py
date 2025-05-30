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
            .main > div {
                padding-top: 1rem;
            }
            
            .stApp {
                    background: linear-gradient(135deg, {COLOR_FONDO} 0%, {COLOR_SECUNDARIO} 100%);
            }
            
            h1, h2, h3 {
                color: {COLOR_TEXTO_OSCURO};
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            }
            
            .metric-card:hover {
                transform: translateY(-3px);
                box-shadow: 0 8px 32px rgba(0, 176, 178, 0.2);
            }
            
            .section-divider {
                height: 4px;
                background: linear-gradient(90deg, {COLOR_PRIMARIO}, {COLOR_ACENTO});
                border: none;
                border-radius: 2px;
                margin: 3rem 0;
                box-shadow: 0 2px 8px rgba(0, 176, 178, 0.3);
            }
            
            .stPlotlyChart {
                background: white;
                border-radius: 12px;
                padding: 1rem;
                box-shadow: 0 4px 16px rgba(0, 176, 178, 0.1);
                border: 1px solid {COLOR_SECUNDARIO};
            }
            </style>
        """, unsafe_allow_html=True)

