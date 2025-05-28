import streamlit as st
from streamlit_option_menu import option_menu

# Para ejecutar, primero en la terminal: pip install -r requirements.txt
# Después: streamlit run app.py

# Configuración inicial
st.set_page_config(page_title="Vanguard Analytics", layout="wide")

# --- Cargar CSS ---
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# --- Sidebar con navegación personalizada ---
with st.sidebar:
    st.image("assets/logo-vanguard.png", width=150)
    
    selected = option_menu(
        menu_title=None,
        options=["Resumen", "Análisis", "Informe"],
        icons=["bar-chart-line", "graph-up", "file-earmark-text"],
        default_index=0,
        styles={
            "container": {"padding": "5px", "background-color": "#f8f9fa"},
            "icon": {"color": "#1f77b4", "font-size": "20px"},
            "nav-link": {
                "font-size": "16px",
                "text-align": "left",
                "margin": "0px",
                "--hover-color": "#e8f0fe"
            },
            "nav-link-selected": {"background-color": "#d0e3ff"},
        }
    )

# --- Contenido por sección ---
if selected == "Resumen":
    st.title("📊 Resumen Ejecutivo del Análisis Vanguard")
    st.write("Aquí puedes contar brevemente de qué trata tu análisis, tus hipótesis principales, y mostrar KPIs clave.")
    # Ejemplo de KPI
    col1, col2, col3 = st.columns(3)
    col1.metric("Número de Jobs", "64", "+5 desde ayer")
    col2.metric("Tasa de éxito", "89%", "-2%")
    col3.metric("Overdue", "19", "+7")
    
elif selected == "Análisis":
    st.title("📈 Visualización Interactiva")
    st.write("Este apartado muestra dashboards desde Tableau u otros visuales")

    # Aquí embebes tu gráfico de Tableau
    st.components.v1.iframe("https://public.tableau.com/views/TU_DASHBOARD_LINK", height=600)

elif selected == "Informe":
    st.title("📄 Informe & Recursos")
    st.write("Aquí puedes permitir la descarga de un informe PDF o mostrar insights finales.")
    st.download_button("📥 Descargar Informe (PDF)", open("data/Informe_Vanguard.pdf", "rb").read(), file_name="informe.pdf")
