import streamlit as st

COLOR_PRIMARIO = "#00B0B2"
COLOR_SECUNDARIO = "#EDEBE9"
COLOR_TEXTO_OSCURO = "#2C3E50"
COLOR_TEXTO_CLARO = "#FFFFFF"
COLOR_ACENTO = "#008B8D"  
COLOR_FONDO = "#F8F9FA"

def aplicar_estilos():
    st.markdown(f"""
        <style>
            div[role="button"] {{
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
                margin-bottom: 2px;
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
                margin: 2rem 0;
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
                background: {COLOR_PRIMARIO};
                border-radius: 15px;
                padding: 20px;
                box-shadow: 0 4px 12px rgba(0, 176, 178, 0.2);
                border: 2px solid {COLOR_PRIMARIO};
                margin-bottom: 0.1rem;
                display: flex !important;
                align-items: center !important;
                gap: 20px !important;
            }}
            
            div[data-testid="stSelectbox"] > label {{
                color: {COLOR_TEXTO_CLARO} !important;
                font-weight: 600 !important;
                font-size: 2rem !important;
            }}

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
            
            .stButton > button {{
                background-color: {COLOR_SECUNDARIO} !important;
                color: black !important;
                font-weight: 600 !important;
                border: none !important;
                border-radius: 8px !important;
                padding: 0.5rem 1.5rem !important;
                transition: all 0.3s ease !important;
                box-shadow: 0 4px 12px rgba(0, 176, 178, 0.2) !important;
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
            
            .tabla-corporativa, .tabla-tipologia {{
                width: 100%;
                border-collapse: separate;
                border-spacing: 0;
                background: #fff;
                border-radius: 16px;
                box-shadow: 0 4px 16px rgba(0,176,178,0.10);
                overflow: hidden;
                margin-bottom: 2rem;
            }}
            .tabla-corporativa th, .tabla-tipologia th {{
                background: {COLOR_PRIMARIO};
                color: #fff;
                font-weight: 700;
                font-size: 1.1rem;
                padding: 0.8rem 0.5rem;
                border-bottom: 2px solid {COLOR_SECUNDARIO};
                text-align: center;
            }}
            .tabla-corporativa td, .tabla-tipologia td {{
                padding: 0.7rem 0.5rem;
                text-align: center;
                font-size: 1rem;
                color: {COLOR_TEXTO_OSCURO};
                border-bottom: 1px solid {COLOR_SECUNDARIO};
                background: {COLOR_FONDO};
            }}
            .tabla-corporativa tr:last-child td, .tabla-tipologia tr:last-child td {{
                border-bottom: none;
            }}

            [data-testid="stSidebar"] {{
            background-color: #00B0B2 !important;
            color: #fff !important;
            border-right: 2px solid #00B0B2;
            box-shadow: 2px 0 16px rgba(0,176,178,0.08);
            }}
            [data-testid="stSidebar"] .css-1d391kg {{
                color: #fff !important;
            }}
            .sidebar-hola {{
                font-size: 1.6rem !important;
                font-weight: 700;
                color: #fff !important;
                margin-bottom: 1.2rem;
                margin-top: 0.5rem;
                text-align: left;
                letter-spacing: 0.5px;
            }}
            [data-testid="stSidebar"] a, [data-testid="stSidebar"] a span, [data-testid="stSidebar"] .stPageLink, [data-testid="stSidebar"] .stPageLink span {{
                color: #fff !important;
            }}
            [data-testid="stSidebar"] .stSubheader {{
                color: #fff !important;
            }}

            .tabla-tipologia {{
                width: 100%;
                border-collapse: separate;
                border-spacing: 0;
                background: #fff;
                border-radius: 16px;
                box-shadow: 0 4px 16px rgba(0,176,178,0.10);
                overflow: hidden;
                margin-bottom: 2rem;
            }}
            .tabla-tipologia th {{
                background: #00B0B2;
                color: #fff;
                font-weight: 700;
                font-size: 1.1rem;
                padding: 0.8rem 0.5rem;
                border-bottom: 2px solid #EDEBE9;
                text-align: center;
            }}
            .tabla-tipologia td {{
                padding: 0.7rem 0.5rem;
                text-align: center;
                font-size: 1rem;
                color: #2C3E50;
                border-bottom: 1px solid #EDEBE9;
                background: #F8F9FA;
            }}
            .tabla-tipologia tr:last-child td {{
                border-bottom: none;
            }}

            
        </style>
    """, unsafe_allow_html=True)

def crear_header_corporativo(titulo, subtitulo=""):
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