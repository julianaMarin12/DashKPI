import streamlit as st 
import pandas as pd 
from PIL import Image
import base64

def validarUsuario(usuario,clave):
    dfusuarios = pd.read_csv('usuarios.csv')
    if len(dfusuarios[(dfusuarios['usuario']==usuario) & (dfusuarios['clave']==clave)])> 0:
        return True
    else:
        return False
    
def generarMenu(usuario):
    with st.sidebar:
        st.image("images/Logo.png", width=300)  
        dfusuarios = pd.read_csv('usuarios.csv')
        dfusuarios = dfusuarios[(dfusuarios['usuario']==usuario)]
        nombre = dfusuarios['nombre'].values[0]
        st.markdown(
            f"<div class='sidebar-hola'>Hola {nombre}</div>",
            unsafe_allow_html=True
        )
        st.markdown("""
            <style>
            .sidebar-hola {
                text-align: center;
                font-size: 1rem;
                margin-bottom: 1.5rem;
            }
            section[data-testid="stSidebar"] a {
                font-size: 1.3rem !important;
            }
            </style>
        """, unsafe_allow_html=True)
        st.page_link("inicio.py", label= " 📊Dash de KPI por área")
        st.subheader("Tableros")
        st.page_link("pages/pagina2.py", label="🛒 Comercial")
        st.page_link("pages/pagina1.py", label="💰 Financiera")
        st.page_link("pages/pagina3.py", label="⛴ Exportaciones")
        st.page_link("pages/pagina4.py", label="🛍️ Mercadeo")
        st.page_link("pages/pagina5.py", label="🏪 Tiendas")
        st.page_link("pages/pagina6.py", label=" Administrativo")
        st.page_link("pages/pagina7.py", label=" Operaciones")
        st.page_link("pages/pagina8.py", label=" Calidad Café")
        st.page_link("pages/pagina9.py", label=" Arquitectura")
        st.markdown("</div>", unsafe_allow_html=True)
        btnSalir = st.button("Salir")
        if btnSalir:
            st.session_state.clear()
            st.rerun()
        
def set_background(image_file):
    with open(image_file, "rb") as image:
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
        set_background("images/fondo.jpg") 
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