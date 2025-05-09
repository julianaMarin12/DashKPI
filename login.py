import streamlit as st 
import pandas as pd 
from PIL import Image

def validarUsuario(usuario,clave):
    dfusuarios = pd.read_csv('usuarios.csv')
    if len(dfusuarios[(dfusuarios['usuario']==usuario) & (dfusuarios['clave']==clave)])> 0:
        return True
    else:
        return False
    
def generarMenu(usuario):     
    with st.sidebar:
        dfusuarios = pd.read_csv('usuarios.csv')
        dfusuarios = dfusuarios[(dfusuarios['usuario']==usuario)]
        nombre = dfusuarios['nombre'].values[0]
        st.write(f"Hola :red-background[{nombre}]") 
        st.page_link("inicio.py", label= " 📊Dash de KPI por área")
        st.subheader("Tableros")
        st.page_link("pages/pagina1.py", label="💰Financiera")
        st.page_link("pages/pagina2.py", label="🛒Comercial")
        btnSalir = st.button("Salir")
        if btnSalir:
            st.session_state.clear()
            st.rerun
        
def set_background(image_file):
    with open(image_file, "rb") as image:
        import base64
        encoded = base64.b64encode(image.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{encoded}");
            background-size: cover;
            background-position: center;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )


def generarLogin():
    set_background("images/fondo.jpg") 
    if 'usuario' in st.session_state:
        generarMenu(st.session_state['usuario'])
    else:
        st.markdown(
            """
            <style>
            h1, h2, h3, h4 {
                color: white!important; 
            }

            </style>
            <div class="login-container">
              <div class="login-box">
            """,
            unsafe_allow_html=True
        )

        with st.form("frmLogin"):
            st.markdown("<center><h1>Iniciar Sesión</h1></center>", unsafe_allow_html=True)
            parUsuario = st.text_input("Usuario")
            parPassword = st.text_input("Contraseña", type="password")
            btnLogin = st.form_submit_button("Ingresar", type="secondary")

        st.markdown("</div></div>", unsafe_allow_html=True)

        if btnLogin:
            if validarUsuario(parUsuario, parPassword):
                st.session_state['usuario'] = parUsuario
                st.rerun()
            else:
                st.error("Usuario o clave inválidos", icon=":material/gpp_maybe:")