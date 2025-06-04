import pandas as pd
import streamlit as st
import login as login
import os
from sync_excel_from_onedrive import sync_excel_from_sharepoint_con_rclone
from funciones import crear_header_corporativo
from funciones import crear_seccion_corporativa
from load_excel import load_excel
from login import set_background

st.set_page_config(layout="wide")
login.generarLogin()
if 'usuario' in st.session_state:
    st.markdown("""
        <style>
            
            h1 {
                color: black !important;
            }
    
            div.stButton > button {
                background-color: white;
                color: black;
               
            }

            .stAlert {
                border-radius: 12px !important;
                padding: 1rem;
                font-size: 16px;
            }
        </style>
    """, unsafe_allow_html=True)
    set_background("images/fondo3.png")
    crear_header_corporativo(
        "📊 Dashboard KPIs",
        "Indicadores de la compañía",
    )

    st.image("video/1.gif", use_container_width=True)

    crear_seccion_corporativa(
        "Bienvenido al Dashboard de KPIs",
        "📈",
    )
    st.write("Da clic al botón de sincronizar datos")

    if st.button("🔄 Sincronizar datos"):
        with st.spinner("Sincronizando..."):
            datos, err = sync_excel_from_sharepoint_con_rclone()
            if err:
                st.error(f"Error al sincronizar:\n{err}")
            else:
                st.success("Archivo sincronizado correctamente.")
