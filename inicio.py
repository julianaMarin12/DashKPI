import pandas as pd
import streamlit as st
import login as login
import os
from sync_excel_from_onedrive import sync_excel_from_onedrive
from load_excel import load_excel

login.generarLogin()
if 'usuario' in st.session_state:
    st.subheader("Bienvenido")
    st.title("📊 Dashboard KPIs")

    if st.button("🔄 Sincronizar archivo desde OneDrive"):
        with st.spinner("Sincronizando..."):
            out, err = sync_excel_from_onedrive()
            if err:
                st.error(f"Error al sincronizar:\n{err}")
            else:
                st.success("Archivo sincronizado correctamente.")
