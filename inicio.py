import pandas as pd
import streamlit as st
import login as login
import os
from sync_excel_from_onedrive import sync_excel_from_onedrive
from load_excel import load_excel
from login import set_background

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
    st.title("📊 Dashboard KPIs")
    video_path = "video/bodegon_1.mov"

    video_html = f"""
        <video width="700" autoplay loop muted>
            <source src="{video_path}" type="video/mp4">
            Tu navegador no soporta el video.
        </video>
    """

    st.markdown(video_html, unsafe_allow_html=True)


    st.subheader("Bienvenido")
    st.write("Dar click al botón de sincronizar datos")
    if st.button("🔄 Sincronizar datos"):
        with st.spinner("Sincronizando..."):
            out, err = sync_excel_from_onedrive()
            if err:
                st.error(f"Error al sincronizar:\n{err}")
            else:
                st.success("Archivo sincronizado correctamente.")