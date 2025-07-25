import os
os.environ["STREAMLIT_WATCH_FOR_CHANGES"] = "false"
import pandas as pd
import streamlit as st
import login as login
import os
from sync_excel_from_onedrive import sync_excel_from_sharepoint_con_rclone
from estilos import crear_header_corporativo
from estilos import crear_seccion_corporativa
from estilos import aplicar_estilos
from load_excel import load_excel
from login import set_background

st.set_page_config(layout="wide")
login.generarLogin()
if 'usuario' in st.session_state:
    aplicar_estilos()

    set_background("images/fondo3.png")
    crear_header_corporativo(
        "📊 Dashboard KPIs",
        "Indicadores de la compañía",
    )

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