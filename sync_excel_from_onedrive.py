import subprocess
import pandas as pd
import streamlit as st
import os

def sync_excel_from_sharepoint_con_rclone():
    """
    Usa rclone para copiar el archivo .xlsx desde SharePoint/OneDrive
    hacia un path local (/tmp o carpeta fija). Luego lo carga con pandas.
    """
    remote = "miOneDrive"
    ruta_remota = "KPIS GENERALES/kpi generales.xlsx"

    # 2) Define a dónde lo vas a copiar temporalmente en tu máquina.
    #    Puede ser /tmp/datos.xlsx (en Windows ajusta a algo como "C:/Temp/kpi generales.xlsx")
    local_dest = "/tmp/kpi generales.xlsx"
    # Si quieres que cada vez se sobreescriba, bórralo si existe:
    if os.path.exists(local_dest):
        os.remove(local_dest)

    try:
        # 3) Llamamos a rclone copy: rclone copy remote:ruta_remota local_dest_folder
        #    NOTA: rclone copy copia al directorio destino, no al archivo directamente.
        #    Por eso usamos el folder padre como destino. 
        carpeta_local = os.path.dirname(local_dest)
        # Comando equivalente a: rclone copy "miOneDrive:Documentos compartidos/MiCarpeta" "/tmp"
        comando = [
            "rclone",
            "copy",
            f"{remote}:{os.path.dirname(ruta_remota)}",
            carpeta_local,
            "--include",
            os.path.basename(ruta_remota),
            "--quiet"  # opcional: para no ver mucho output
        ]

        resultado = subprocess.run(
            comando,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        if resultado.returncode != 0:
            # Si rclone devolvió error, lo capturamos y lo devolvemos.
            return None, f"rclone error: {resultado.stderr.strip()}"

        # 4) Ahora que el archivo ya debería estar en local_dest, lo leemos con pandas:
        df_dict = pd.read_excel(local_dest, sheet_name=None)
        return df_dict, None

    except Exception as e:
        return None, str(e)
