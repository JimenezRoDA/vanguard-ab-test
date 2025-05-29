import streamlit as st
from streamlit_option_menu import option_menu
import os
import base64

# Para ejecutar, primero en la terminal: pip install -r requirements.txt
# Después: streamlit run app.py

# Configuración de la Página
st.set_page_config(
    page_title="Vanguard Analytics",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS GLOBAL PARA EL FONDO DE LA SIDEBAR DE STREAMLIT ---
# Este CSS se inyecta para cambiar el color de fondo de toda la st.sidebar
st.markdown(
    """
    <style>
        /* Apunta al contenedor principal de la sidebar de Streamlit */
        section[data-testid="stSidebar"] > div:first-child {
            background-color: #e7f5ff !important; /* Tu azul clarito */
        }
    </style>
    """,
    unsafe_allow_html=True
)


st.markdown(
    """
    <style>
        /* Forzamos transparencia en contenedores padres del nav */
        section[data-testid="stSidebar"] * {
            background-color: transparent !important;
        }

        /* También quitamos sombras o bordes que podrían generar ese gris */
        section[data-testid="stSidebar"] {
            box-shadow: none !important;
            border: none !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <style>
        /* Aplica a los divs padres del option_menu */
        [data-testid="stSidebar"] > div:first-child > div {
            background-color: #e7f5ff !important;  /* azul clarito que quieres */
            padding: 0px !important;
            margin: 0px !important;
        }

        /* Por si hay un fondo dentro del div aún más interno */
        [data-testid="stSidebar"] ul.nav {
            background-color: transparent !important;
        }

        /* También aseguramos que ningún nav-item tenga fondo gris residual */
        [data-testid="stSidebar"] .nav-link {
            background-color: transparent !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)


# FIN DEL CSS


# CONTENIDO DE LA SIDEBAR
with st.sidebar:
    # 1. Logo (en style='width y height' se puede ajustar)
    logo_path = "assets/logo-vanguard.png"
    try:
        with open(logo_path, "rb") as image_file:
            encoded_logo = base64.b64encode(image_file.read()).decode()
        st.markdown(
            f"""
            <div style="display: flex; justify-content: center; margin-top: 15px; margin-bottom: 40px;">
                <img src="data:image/png;base64,{encoded_logo}" alt="Vanguard Logo" style="width: 140px; height: 140px;">
            </div>
            """,
            unsafe_allow_html=True,
        )
    except FileNotFoundError:
        st.markdown(
            f"""
            <div style="display: flex; justify-content: center; margin-top: 15px; margin-bottom: 40px;
                        width: 70px; height: 70px; background-color: #DDD; border-radius: 10px;
                        align-items: center; font-size: 28px; color: #555; font-weight: bold;">
                L
            </div>
            """,
            unsafe_allow_html=True,
        )

    # 2. Menú de Opciones
    option_titles_en = [
        "Overview",
        "Interactive Analysis",
        "Tests & Statistics",
        "ML/DP",
        "Insights & Conclusions",
        "Downloads & Resources",
        "Load & Quick EDA",
        "Settings"
    ]
    
    icons_list = [
        "house-door-fill",
        "bar-chart-line-fill",
        "percent",
        "cpu-fill",
        "clipboard-data-fill",
        "download",
        "folder-fill",
        "gear-fill"
    ]

    selected_title_en = option_menu(
        menu_title=None,
        options=option_titles_en,
        icons=icons_list,
        menu_icon="list", 
        default_index=0,
        orientation="vertical",
        styles={
            "container": { 
                           
                "padding": "5px !important",
                "background-color": "#e7f5ff", # Hacemos que coincida con el fondo de st.sidebar
            },
            "icon": {
                "color": "#0d6efd", 
                "font-size": "24px",
            },
            "nav-link": {
                "font-size": "0px",
                "text-align": "center",
                "margin": "8px 0px",
                "--hover-color": "rgba(13, 110, 253, 0.1)", # Hover sutil sobre el fondo azul claro
                "height": "55px",
                "display": "flex",
                "align-items": "center",
                "justify-content": "center",
                "border-radius": "5px",
            },
            "nav-link span": {
                "display": "none !important"
            },
            "nav-link-selected": {
                "background-color": "rgba(13, 110, 253, 0.15)", # Fondo ligeramente más oscuro para seleccionado
            },
             "nav-link-selected .icon": { 
                "color": "#0a58ca !important", # Icono un poco más oscuro en selección
            }
        }
    )

# CONTENIDO PRINCIPAL DE LA PÁGINA
if 'current_page_key' not in st.session_state:
    st.session_state.current_page_key = selected_title_en

if selected_title_en != st.session_state.current_page_key:
    st.session_state.current_page_key = selected_title_en

if st.session_state.current_page_key == "Overview":
    st.title("Overview")
    st.write("Content for the Overview section.")
elif st.session_state.current_page_key == "Interactive Analysis":
    st.title("Interactive Analysis")
    st.write("Content for the Interactive Analysis section.")
elif st.session_state.current_page_key == "Tests & Statistics":
    st.title("Tests & Statistics")
    st.write("Content for the Tests & Statistics section.")
elif st.session_state.current_page_key == "ML/DP":
    st.title("ML / Deep Learning")
    st.write("Content for the ML/DP section.")
elif st.session_state.current_page_key == "Insights & Conclusions":
    st.title("Insights & Conclusions")
    st.write("Content for the Insights & Conclusions section.")
elif st.session_state.current_page_key == "Downloads & Resources":
    st.title("Downloads & Resources")
    st.write("Content for the Downloads & Resources section.")
elif st.session_state.current_page_key == "Load & Quick EDA":
    st.title("Load & Quick EDA")
    st.write("Content for the Load & Quick EDA section.")
elif st.session_state.current_page_key == "Settings":
    st.title("Settings")
    st.write("Settings accessible from the sidebar menu.")
else:
    st.write("Welcome to Vanguard Analytics. Please select an option.")
