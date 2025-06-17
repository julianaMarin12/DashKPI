from estilos import crear_header_corporativo
from login import set_background
from estilos import aplicar_estilos
import streamlit as st
import login
 
st.set_page_config(layout="wide")
login.generarLogin()
set_background("images/fondo4.jpg")
if 'usuario' in st.session_state:
    crear_header_corporativo(
        "KPIs ÁREA OPERACIONES",
        "Indicadores para el área"
    )

    aplicar_estilos()