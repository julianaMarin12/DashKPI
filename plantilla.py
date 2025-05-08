import streamlit as st


st.set_page_config(page_title="Dashboard Interactivo", layout="wide")

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

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap');

    html, body, [class*="css"]  {
        font-family: 'Inter', sans-serif;
    }
    
    section[data-testid="stSidebar"] {
        background-color: white;
    }

    /* Texto del sidebar */
    section[data-testid="stSidebar"] * {
        color: black !important;
        font-family: 'Inter', sans-serif;
        
    }

    /* Títulos globales */
    h1, h2, h3, h4 {
        color: white!important; 
    }

    </style>
    """,
    unsafe_allow_html=True
)

set_background("images/fondo.jpg")

st.sidebar.title("〽️KPIS por áreas")
opcion = st.sidebar.radio(
    "Selecciona un área:",
    ["🏠︎ Inicio", "💰Financiera", "👥Recursos Humanos", "📈Ventas"]
)

st.title("📊 Dashboard KPI por Área")

if opcion == "🏠︎ Inicio":
    st.subheader("👋 Bienvenido ")
    st.markdown("Selecciona un área a la izquierda para ver los indicadores de desempeño.")
    
elif opcion == "💰Financiera":
    st.subheader("Área: Financiera")
    st.info("Sección aún sin datos")

elif opcion == "👥Recursos Humanos":
    st.subheader("Área: Recursos Humanos")
    st.info("Sección aún sin datos")

elif opcion == "📈Ventas":
    st.subheader("Área: Ventas")
    st.warning("Sección aún sin datos.")
