import subprocess
import streamlit as st
import os

def sync_excel_from_onedrive():
    try:
        comando = [
            "rclone",
            "copy",
            "onedrive:KPIS GENERALES/kpi generales.xlsx",
            "/workspaces/DashKPI/",
            "-P"
        ]
        resultado = subprocess.run(comando, capture_output=True, text=True)
        return resultado.stdout, resultado.stderr
    except Exception as e:
        return "", str(e)
