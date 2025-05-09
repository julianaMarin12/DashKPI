import streamlit as st 
import pandas as pd 

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
        st.write(f"Hola **:blue-background[{nombre}]") 
        st.page_link("inicio.py", label= "Dash de KPI por área", icon=":materia/icon")
        st.subheader("Tableros")
        st.page_link("pages/pagina1.py", label="Financiera")
        btnSalir = st.button("Salir")
        if btnSalir:
            st.session_state.clear()
            st.rerun
        
def generarLogin ():
    if 'usuario' in st.session_state:
        generarMenu(st.session_state['usuario'])
    else:
        with st.form ('frmLogin'):
            parUsuario = st.text_input('Usuario')
            parPassword = st.text_input('Contraseña', type = 'password')
            btnLogin = st.form_submit_button('Ingresar', type = 'primary')
            if btnLogin:
                if validarUsuario (parUsuario, parPassword):
                    st.session_state['usuario'] = parUsuario
                    st.rerun()
                else:
                    st.error("Usuario o clave inválidos", icon=":material/gpp_maybe:")