import streamlit as st

def aplicar_estilos():
    COLOR_PRIMARIO = "#00B0B2"
    COLOR_SECUNDARIO = "#EDEBE9"
    COLOR_TEXTO_OSCURO = "#2C3E50"
    COLOR_TEXTO_CLARO = "#FFFFFF"
    COLOR_ACENTO = "#008B8D"  
    COLOR_FONDO = "#F8F9FA"

    st.markdown(f"""
        <style>
            /* Estilos generales */
            div[role="button"] {{
                background-color: #ffffff !important;
                color: {COLOR_TEXTO_OSCURO} !important;
                font-weight: 600;
                font-size: 18px;
                border: 1px solid {COLOR_PRIMARIO}40 !important;
                border-radius: 12px;
                padding: 12px;
                margin-bottom: 15px;
                box-shadow: 0px 4px 12px rgba(0,0,0,0.08);
                transition: all 0.3s ease;
            }}
            
            div[role="button"]:hover {{
                border-color: {COLOR_PRIMARIO} !important;
                box-shadow: 0px 6px 16px rgba(0, 176, 178, 0.15);
                transform: translateY(-2px);
            }}

            .metric-title {{
                font-size: 16px;
                font-weight: 600;
                margin-bottom: 8px;
                color: {COLOR_TEXTO_OSCURO};
                letter-spacing: 0.3px;
            }}
                
            .metric-value {{
                font-size: 1.4rem;
                font-weight: bold;
                color: {COLOR_PRIMARIO};
            }}
            
            header, footer, .stDeployButton {{
                visibility: hidden;
            }}
            
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
            
            /* Estilos para el selectbox */
            div[data-testid="stSelectbox"] {{
                background: white;
                border-radius: 10px;
                padding: 0.5rem;
                box-shadow: 0 4px 12px rgba(0, 176, 178, 0.1);
                border: 2px solid {COLOR_PRIMARIO};
                margin-bottom: 1.5rem;
            }}
            
            div[data-testid="stSelectbox"] > label {{
                color: {COLOR_TEXTO_OSCURO} !important;
                font-weight: 600 !important;
                font-size: 1rem !important;
                letter-spacing: 0.5px;
                background: {COLOR_SECUNDARIO};
                padding: 0.5rem 1rem;
                border-radius: 8px 8px 0 0;
                border-bottom: 2px solid {COLOR_PRIMARIO};
                margin-bottom: 0.5rem;
                display: block;
                width: 100%;
            }}
            
            div[data-testid="stSelectbox"] > div > div {{
                background: white;
                border: 1px solid {COLOR_PRIMARIO} !important;
                border-radius: 6px !important;
                color: {COLOR_TEXTO_OSCURO};
                font-weight: 500;
            }}
            
            div[data-testid="stSelectbox"] > div > div:focus {{
                box-shadow: 0 0 0 2px {COLOR_PRIMARIO}40 !important;
                border: 1px solid {COLOR_PRIMARIO} !important;
            }}
            
            .stSelectbox div[role="listbox"] div[role="option"] {{
                background-color: white;
                color: {COLOR_TEXTO_OSCURO};
            }}
            
            .stSelectbox div[role="listbox"] div[role="option"]:hover,
            .stSelectbox div[role="listbox"] div[role="option"][aria-selected="true"] {{
                background-color: {COLOR_PRIMARIO}20 !important;
                color: {COLOR_PRIMARIO} !important;
            }}
            
            div[data-testid="stSelectbox"] svg {{
                color: {COLOR_PRIMARIO} !important;
            }}
            
            /* Contenedor personalizado para elementos de formulario */
            .form-container {{
                background: linear-gradient(135deg, {COLOR_SECUNDARIO} 0%, white 100%);
                padding: 1.5rem;
                border-radius: 12px;
                border-left: 5px solid {COLOR_PRIMARIO};
                margin-bottom: 2rem;
                box-shadow: 0 6px 18px rgba(0, 176, 178, 0.12);
            }}
            
            /* Estilos para otros widgets de Streamlit */
            
            /* Radio buttons */
            div[data-testid="stRadio"] > label {{
                color: {COLOR_TEXTO_OSCURO} !important;
                font-weight: 600 !important;
                font-size: 1rem !important;
            }}
            
            div[data-testid="stRadio"] label[data-baseweb="radio"] {{
                border-color: {COLOR_PRIMARIO} !important;
            }}
            
            div[data-testid="stRadio"] label[data-baseweb="radio"] div[data-testid="stMarkdownContainer"] p {{
                color: {COLOR_TEXTO_OSCURO} !important;
                font-weight: 500;
            }}
            
            /* Checkbox */
            div[data-testid="stCheckbox"] > label {{
                color: {COLOR_TEXTO_OSCURO} !important;
                font-weight: 600 !important;
                font-size: 1rem !important;
            }}
            
            div[data-testid="stCheckbox"] label[data-baseweb="checkbox"] {{
                border-color: {COLOR_PRIMARIO} !important;
            }}
            
            /* Slider */
            div[data-testid="stSlider"] > label {{
                color: {COLOR_TEXTO_OSCURO} !important;
                font-weight: 600 !important;
                font-size: 1rem !important;
            }}
            
            div[data-testid="stSlider"] div[role="slider"] {{
                background-color: {COLOR_PRIMARIO} !important;
            }}
            
            /* Botones */
            .stButton > button {{
                background-color: {COLOR_PRIMARIO} !important;
                color: white !important;
                font-weight: 600 !important;
                border: none !important;
                border-radius: 8px !important;
                padding: 0.5rem 1.5rem !important;
                transition: all 0.3s ease !important;
                box-shadow: 0 4px 12px rgba(0, 176, 178, 0.2) !important;
            }}
            
            .stButton > button:hover {{
                background-color: {COLOR_ACENTO} !important;
                box-shadow: 0 6px 16px rgba(0, 176, 178, 0.3) !important;
                transform: translateY(-2px) !important;
            }}
            
            /* Tabs */
            .stTabs [data-baseweb="tab-list"] {{
                gap: 8px;
                background-color: {COLOR_SECUNDARIO};
                border-radius: 10px;
                padding: 0.5rem;
                box-shadow: 0 2px 10px rgba(0, 176, 178, 0.1);
            }}
            
            .stTabs [data-baseweb="tab"] {{
                background-color: white;
                border-radius: 8px;
                color: {COLOR_TEXTO_OSCURO};
                font-weight: 600;
                border: 1px solid {COLOR_PRIMARIO}20;
            }}
            
            .stTabs [aria-selected="true"] {{
                background-color: {COLOR_PRIMARIO} !important;
                color: white !important;
                box-shadow: 0 4px 12px rgba(0, 176, 178, 0.2);
            }}
            
            /* Dataframe/Tabla */
            .stDataFrame {{
                border-radius: 12px;
                overflow: hidden;
                box-shadow: 0 4px 16px rgba(0, 176, 178, 0.1);
            }}
            
            .stDataFrame thead tr th {{
                background-color: {COLOR_PRIMARIO} !important;
                color: white !important;
                font-weight: 600 !important;
            }}
            
            .stDataFrame tbody tr:nth-child(even) {{
                background-color: {COLOR_SECUNDARIO}50;
            }}
            
            /* Expander */
            .streamlit-expanderHeader {{
                background-color: {COLOR_SECUNDARIO} !important;
                border-radius: 8px !important;
                color: {COLOR_TEXTO_OSCURO} !important;
                font-weight: 600 !important;
                border-left: 4px solid {COLOR_PRIMARIO} !important;
            }}
            
            .streamlit-expanderContent {{
                background-color: white !important;
                border-radius: 0 0 8px 8px !important;
                border: 1px solid {COLOR_SECUNDARIO} !important;
                border-top: none !important;
                box-shadow: 0 4px 12px rgba(0, 176, 178, 0.1) !important;
            }}
            
            /* Métricas */
            div[data-testid="stMetric"] {{
                background: linear-gradient(135deg, {COLOR_PRIMARIO} 0%, {COLOR_ACENTO} 100%);
                border-radius: 12px;
                padding: 1rem;
                box-shadow: 0 6px 18px rgba(0, 176, 178, 0.15);
            }}
            
            div[data-testid="stMetric"] label {{
                color: white !important;
                font-weight: 600 !important;
                text-transform: uppercase;
                letter-spacing: 0.5px;
                font-size: 0.9rem !important;
            }}
            
            div[data-testid="stMetric"] div[data-testid="stMetricValue"] {{
                color: white !important;
                font-weight: 700 !important;
                font-size: 1.8rem !important;
                text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
            }}
            
            div[data-testid="stMetric"] div[data-testid="stMetricDelta"] {{
                color: white !important;
                font-weight: 600 !important;
                background-color: rgba(255, 255, 255, 0.2);
                padding: 0.2rem 0.5rem;
                border-radius: 4px;
            }}
            
            /* Contenedor para selectbox */
            .selectbox-container {{
                background: linear-gradient(135deg, {COLOR_SECUNDARIO} 0%, white 100%);
                padding: 1.5rem;
                border-radius: 12px;
                border-left: 5px solid {COLOR_PRIMARIO};
                margin-bottom: 2rem;
                box-shadow: 0 6px 18px rgba(0, 176, 178, 0.12);
            }}
            
            /* Título para el selectbox */
            .selectbox-title {{
                color: {COLOR_TEXTO_OSCURO};
                font-weight: 700;
                font-size: 1.1rem;
                margin-bottom: 1rem;
                display: flex;
                align-items: center;
                gap: 0.5rem;
            }}
        </style>
    """, unsafe_allow_html=True)