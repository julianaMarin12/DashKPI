import streamlit as st
import login as login

st.header("Iniciar Sección")
login.generarLogin()
if 'usuario' in st.session_state:
    st.subheader("Información")