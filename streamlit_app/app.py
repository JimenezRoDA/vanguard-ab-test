import streamlit as st
from streamlit_option_menu import option_menu
import streamlit.components.v1 as components
import pandas as pd
import pydeck as pdk
import altair as alt
import numpy as np
import datetime
import zipfile
import base64
import io
import os

# Para ejecutar, primero en la terminal: pip install -r requirements.txt
# Después: streamlit run app.py


# Cargar datos necesarios para el apartado de Statistics




# Configuración de la Página
st.set_page_config(
    layout="wide",       
    initial_sidebar_state="expanded",
    page_title="Vanguard Analytics",
    page_icon="📈",       
)


# Ocultar settings y demás menús con CSS
st.markdown("""
    <style>
        #MainMenu, footer, header {
            display: none;
        }
        [data-testid="stToolbar"] {
            display: none;
        }
    </style>
""", unsafe_allow_html=True)


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

# Para que la sidebar aparezca delgada por defecto y se mantenga así
st.markdown(
    """
    <style>
        /* Fija el ancho de la sidebar */
        section[data-testid="stSidebar"] {
            min-width: 180px !important;
            max-width: 180px !important;
            width: 180px !important;
            transition: none !important;
        }

        /* Evita que se expanda si el usuario intenta redimensionar */
        section[data-testid="stSidebar"] > div:first-child {
            overflow-x: hidden !important;
        }

        /* En caso de hover o arrastre, mantener el ancho */
        [data-testid="stSidebar"] {
            resize: none !important;
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
        "Statistics",
        "ML/DP",
        "Conclusions",
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
    # Título fijo arriba
    st.title("Overview")

    # Inicializamos el slide actual y lo ponemos en la primera slide (0) por defecto
    if "ov_page" not in st.session_state:
        st.session_state.ov_page = 0

    # Botones de navegación
    nav_col1, _, nav_col3 = st.columns([1, 6, 1])
    with nav_col1:
        if st.button("←", disabled=(st.session_state.ov_page == 0)):
            st.session_state.ov_page -= 1
    with nav_col3:
        if st.button("→", disabled=(st.session_state.ov_page == 2)):
            st.session_state.ov_page += 1

    # SLIDE 0: Who Are We?
    if st.session_state.ov_page == 0:
        st.subheader("🧑‍💼 Who Are We?")
        df = pd.DataFrame([
            {
            "city": "Barcelona", "lat": 41.3851, "lon": 2.1734,
            "github": "https://github.com/xavistem",
            "label": "@xavistem"
            },
            {
            "city": "Madrid",    "lat": 40.4168, "lon": -3.7038,
            "github": "https://github.com/JimenezRoDA",
            "label": "@JimenezRoDA"
            }
        ])

        # Usamos un ScatterplotLayer con puntas rojas tipo chincheta
        layer = pdk.Layer(
            "ScatterplotLayer",
            data=df,
            get_position=["lon", "lat"],
            get_fill_color=[255, 75, 75, 200],  # rojo
            get_radius=20000,
            pickable=True,
            auto_highlight=True
        )

        deck = pdk.Deck(
            map_style="mapbox://styles/mapbox/light-v9",
            initial_view_state=pdk.ViewState(
                latitude=41.0, longitude=0.0, zoom=4.5, pitch=0
            ),
            layers=[layer],
            tooltip={
                "html": "<b>{city}</b><br><a href='{github}' target='_blank'>Go to profile</a>",
                "style": {"backgroundColor": "rgba(255,75,75,0.8)", "color": "#fff"}
            }
        )
        st.pydeck_chart(deck, use_container_width=True)

        # Enlaces con badges tipo shields.io parecido a los del readme
        st.markdown("**Connect with us on GitHub:**")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(
                """
                [![Rocío Jiménez](https://img.shields.io/badge/@JimenezRoDA-GitHub-181717?logo=github&style=flat-square)](https://github.com/JimenezRoDA)
                """,
                unsafe_allow_html=True
            )
            st.markdown(
                """
                [![Xavi Fernández](https://img.shields.io/badge/@xavistem-GitHub-181717?logo=github&style=flat-square)](https://github.com/xavistem)
                """,
                unsafe_allow_html=True
            )

    # SLIDE 1: Data Sources & Timeline
    elif st.session_state.ov_page == 1:
        st.subheader("📑 Data Sources & Project Timeline")
        left, right = st.columns(2)
        with left:
            st.markdown("""
**Data Sources Used**  
- `df_final_demo`  
- `df_final_experiment_clients`  
- `df_final_web_data_pt_1m`  
- `df_final_web_data_pt_2`  
""")
        with right:
            st.markdown("**Project Active Dates**")
            col_a, col_b = st.columns(2)
            with col_a:
                # Phase 1 calendar siempre visible
                st.date_input(
                    "Phase 1: May 19–23, 2025",
                    value=(datetime.date(2025,5,19), datetime.date(2025,5,23)),
                    min_value=datetime.date(2025,5,1),
                    max_value=datetime.date(2025,5,31),
                    key="phase1",
                    label_visibility="collapsed"
                )
            with col_b:
                # Phase 2 calendar siempre visible
                st.date_input(
                    "Phase 2: May 26–30, 2025",
                    value=(datetime.date(2025,5,26), datetime.date(2025,5,30)),
                    min_value=datetime.date(2025,5,1),
                    max_value=datetime.date(2025,5,31),
                    key="phase2",
                    label_visibility="collapsed"
                )

    # SLIDE 2: Texto e imagen
    else:
        left_col, right_col = st.columns([2, 1])
        with left_col:
            st.markdown("""
    ### 🎯 Vanguard Digital Redesign: Assessing the Impact with A/B Testing

    Vanguard, one of the world’s most influential investment firms, has undertaken an ambitious redesign of its web experience.  
    The goal is clear: to improve the **conversion process for new financial products** by making it more **intuitive, efficient, and user-focused**.

    To validate this change, an A/B test was conducted:
    - 🧪 **Control group** accessed the original design  
    - 🚀 **Test group** interacted with the newly redesigned version

    ---

    #### 📊 Key Metrics Analyzed:
    - Completion rate  
    - First-attempt completion rate  
    - Average time (total and per step)  
    - Errors within the funnel

    #### 🎯 Success Criterion:
    > **Increase the completion rate by at least 5%.**

    ---

    On this page, we will explore the experiment data, analyze key metrics, identify behavioral patterns, and answer a fundamental question:

    > 🧠 *Does the redesign truly enhance the user experience…  
    > or is it just an aesthetic upgrade with no real impact?*

    👉 Join us in this analysis to discover whether the new design makes a meaningful difference in site performance.
            """)
        with right_col:
            st.image("assets/overview.png", use_column_width=True)


elif st.session_state.current_page_key == "Interactive Analysis":
    st.title("Interactive Analysis")

    # Pestañas principales: Demographics vs KPIs
    demo_tab, kpi_tab = st.tabs(["📊 Demographics", "📈 KPIs"])

    # Demographics: un único dashboard con tus 4 visualizaciones
    with demo_tab:
        st.subheader("Demographics Overview")
        components.iframe(
            "https://public.tableau.com/views/Clients_17485213608790/Dashboard1"
            "?:language=es-ES&publish=yes&:showVizHome=no&:embed=y",
            height=700,
            scrolling=True,
        )

    # KPIs: sub-pestañas para cada uno de los 4 dashboards
    with kpi_tab:
        st.subheader("Key Performance Indicators")
        kpi_subtabs = kpi_tab.tabs([
            "Completion Rate",
            "First-Time Completion",
            "Time Invested",
            "Error Rate"
        ])

        # 1️⃣ Completion Rate
        with kpi_subtabs[0]:
            st.markdown("#### Completion Rate")
            components.iframe(
                "https://public.tableau.com/views/Insights_17485215898210/CompletionRate"
                "?:language=es-ES&publish=yes&:showVizHome=no&:embed=y",
                height=650,
                scrolling=True,
            )

            # Robot: Completion Rate
            html_code = """
            <style>
            .tooltip {
              position: relative;
              display: inline-block;
              cursor: pointer;
            }
            .tooltip .tooltiptext {
              visibility: hidden;
              width: 220px;
              background-color: #555;
              color: #fff;
              text-align: center;
              border-radius: 6px;
              padding: 5px 8px;
              position: absolute;
              z-index: 1;
              bottom: 125%;
              left: 50%;
              margin-left: -110px;
              opacity: 0;
              transition: opacity 0.3s;
              font-size: 14px;
              pointer-events: none;
              white-space: nowrap;
            }
            .tooltip:hover .tooltiptext {
              visibility: visible;
              opacity: 1;
            }
            .tooltip .tooltiptext::after {
              content: "";
              position: absolute;
              top: 100%;
              left: 50%;
              margin-left: -5px;
              border-width: 5px;
              border-style: solid;
              border-color: #555 transparent transparent transparent;
            }
            </style>
            <script
              src="https://unpkg.com/@dotlottie/player-component@2.7.12/dist/dotlottie-player.mjs"
              type="module"
            ></script>
            <div class="tooltip">
              <dotlottie-player
                src="https://lottie.host/24393e73-f3c0-43bc-b296-3695056055a6/rnxrzeYROf.lottie"
                background="transparent"
                speed="1"
                style="width: 150px; height: 150px;"
                loop
                autoplay
              ></dotlottie-player>
              <span class="tooltiptext">Click to see the hypothesis results</span>
            </div>
            """
            components.html(html_code, height=180)
            if st.button("Show hypothesis results", key="hypo1"):
                st.markdown("""
**H₀**: completion_rate(Control) = completion_rate(Test)  
**H₁**: completion_rate(Control) ≠ completion_rate(Test)  
We rejected **H₀**, so the difference is significant.  
However, the increase is below the **+5% threshold**, so it doesn’t meet the business criterion.
                """)

        # 2️⃣ Completion Rate at the First Time
        with kpi_subtabs[1]:
            st.markdown("#### Completion Rate at the First Time")
            components.iframe(
                "https://public.tableau.com/views/Completion_17485219424030/Firsttime"
                "?:language=es-ES&publish=yes&:showVizHome=no&:embed=y",
                height=650,
                scrolling=True,
            )

            # Robot: First Attempt Success
            components.html(html_code.replace(
                "Click to see the hypothesis results",
                "Click to see first attempt success results"
            ), height=180)
            if st.button("Show hypothesis results", key="hypo2"):
                st.markdown("""
**H₀**: first_attempt_success(Control) = first_attempt_success(Test)  
**H₁**: first_attempt_success(Control) ≠ first_attempt_success(Test)  
We performed the test and rejected **H₀**.  
:apuntando_hacia_la_derecha: So, the difference in first attempt success rate is statistically significant.  
Although more users in the Test group completed the process, the success rate on the first attempt was **lower** than in the Control group (**43.67% vs. 47.39%**).
                """)

        # 3️⃣ Time Invested
        with kpi_subtabs[2]:
            st.markdown("#### Time Invested")
            components.iframe(
                "https://public.tableau.com/views/Timeinvested/Timeinvested"
                "?:language=es-ES&publish=yes&:showVizHome=no&:embed=y",
                height=650,
                scrolling=True,
            )

            # Robot: UX Insights
            components.html(html_code.replace(
                "Click to see the hypothesis results",
                "Click to see UX performance insights"
            ), height=180)
            if st.button("Show hypothesis results", key="hypo3"):
                st.markdown("""
**UX Insights**:  
• Test starts faster → less initial friction  
• Test slower at step_1 & confirm → +5s and +23s (not significant)  
• Big speedup at step_3 (**+7s**, highly significant)  
• Mixed results: some steps better, others worse  
• Statistically solid effects, but overall UX needs review
                """)

        # 4️⃣ Error Rate
        with kpi_subtabs[3]:
            st.markdown("#### Error Rate")
            components.iframe(
                "https://public.tableau.com/views/Errorrate_17485220756100/ErrorRate"
                "?:language=es-ES&publish=yes&:showVizHome=no&:embed=y",
                height=650,
                scrolling=True,
            )

            # Robot: Error Rate
            components.html(html_code.replace(
                "Click to see the hypothesis results",
                "Click to see error rate results"
            ), height=180)
            if st.button("Show hypothesis results", key="hypo4"):
                st.markdown("""
**H₀**: error_rate(Control) ≤ error_rate(Test)  
**H₁**: error_rate(Control) > error_rate(Test)  
We performed the test and rejected **H₀**.  
:apuntando_hacia_la_derecha: So, the global error rate in **Control** is significantly higher than in **Test**.  
Control had an error rate of **0.19%**, while Test reduced this to **0.07%**, indicating a clear improvement in the new design’s performance.
                """)


elif st.session_state.current_page_key == "Statistics":
    st.title("Statistics")

elif st.session_state.current_page_key == "ML/DP":
    st.title("ML / Deep Learning")
elif st.session_state.current_page_key == "Conclusions":
    st.title("🔍 Conclusions")

    # Wrap in an expander so it's not overwhelming at first glance
    with st.expander("Show Summary of Findings", expanded=False):
        st.markdown("""
The digital redesign (**Test group**) has shown **statistically significant improvements** in key aspects of the process, but it **does not fully meet all operational effectiveness criteria** defined by Vanguard.  
Below is a summary of the final trade-off between the two versions:
""")

        # Clear Advantages
        st.markdown("### ✅ Clear Advantages of the Test Group")
        st.markdown("""
- **Higher completion rate**: 69.3% vs. 65.6% (p < 0.001)  
- **Lower overall technical error rate**: 0.076% vs. 0.193% (p < 0.001)  
- **Critical “confirm” step errors** reduced from 0.577% to 0.066%  
  > +0.51 pp improvement, 95% CI mostly above the minimum threshold  
""")

        # Limitations
        st.markdown("### ⚠️ Limitations of the Test Group")
        st.markdown("""
- **Lower first-attempt completion**: 43.7% vs. 47.4%  
  > Indicates higher friction and reduced initial clarity  
- **Slightly higher average total completion time** (p < 0.001)  
  > Medians nearly identical → practically similar efficiency  
- **Slower performance** in key steps  
  - Step 1: +5 seconds  
  - Confirm: +23 seconds  
  > Potential bottlenecks introduced by redesign  
""")

        # Hypotheses & Business Considerations
        st.markdown("### 🧠 Hypotheses & Business Considerations")
        st.markdown("""
- Some improvements exceed statistical significance but **fall short of Vanguard’s 5% cost-benefit threshold**  
  > e.g. +3.7 pp completion gain vs. 5 pp success criterion  
- **Exception**: “Confirm”-step error reduction **does** surpass the threshold → clear operational gain  
""")

        # Final Recommendation
        st.markdown("### 🧭 Final Recommendation")
        st.markdown("""
It is recommended to **adopt the Test redesign** as the new standard—but **with targeted optimizations** in the **Step 1** and **Confirm** stages, where friction increased:

> - Enhance upfront guidance and contextual cues  
> - Streamline interactions in Step 1 to reduce delays  
> - Maintain technical robustness to keep error rates low  

The new design **stabilizes the process**, **reduces technical errors**, and **increases overall completions**, yet requires **improved clarity** to boost first-attempt success.  
This represents a **solid foundation** for future iterations; we advise a **second optimization phase** focused on the identified friction points.
""")


elif st.session_state.current_page_key == "Downloads & Resources":
    st.title("📂 Downloads & Resources")

    # 1️⃣ Executive Summary Reports
    st.markdown("### 📄 Executive Summary Reports")
    st.markdown(
        """
        For those who couldn't attend the live presentation—or anyone who wants a quick, formal
        overview—please select your preferred language and download the concise executive summary.
        """
    )

    # Language selector
    lang = st.selectbox("Choose report language", ["English", "Español"])

    # Base path para los reports
    report_base = os.path.join("data", "reports")

    if lang == "English":
        report_path = os.path.join(report_base, "Executive_Summary_EN.pdf")
        with open(report_path, "rb") as f:
            pdf_bytes = f.read()
        st.download_button(
            label="📥 Download Executive Summary (English)",
            data=pdf_bytes,
            file_name="Vanguard_Digital_Redesign_Summary_EN.pdf",
            mime="application/pdf",
        )
    else:
        report_path = os.path.join(report_base, "Executive_Summary_ES.pdf")
        with open(report_path, "rb") as f:
            pdf_bytes = f.read()
        st.download_button(
            label="📥 Descargar Resumen Ejecutivo (Español)",
            data=pdf_bytes,
            file_name="Vanguard_Digital_Redesign_Resumen_ES.pdf",
            mime="application/pdf",
        )

    st.markdown("---")

    # 2️⃣ Data Downloads
    st.markdown("### 🗄️ Data Downloads")
    st.markdown(
        """
        You can download the raw and processed datasets used in our analysis.  
        - **Raw**: Original exported tables, before any cleaning.  
        - **Processed**: Final cleaned and joined tables ready for analysis.
        """
    )

    # Helper para comprimir cualquier carpeta en memoria
    def zip_folder_to_bytes(folder_path):
        buffer = io.BytesIO()
        with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as z:
            for root, _, files in os.walk(folder_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, start=folder_path)
                    z.write(file_path, arcname=arcname)
        buffer.seek(0)
        return buffer.read()

    # Raw data
    raw_zip = zip_folder_to_bytes(os.path.join("data", "raw"))
    st.download_button(
        label="📥 Download Raw Data (ZIP)",
        data=raw_zip,
        file_name="vanguard_raw_data.zip",
        mime="application/zip",
    )

    # Processed data
    processed_zip = zip_folder_to_bytes(os.path.join("data", "processed"))
    st.download_button(
        label="📥 Download Processed Data (ZIP)",
        data=processed_zip,
        file_name="vanguard_processed_data.zip",
        mime="application/zip",
    )

    st.markdown(
        """
        ---
        *These datasets are provided under internal Vanguard use—please do not redistribute.*
        """
    )


elif st.session_state.current_page_key == "Load & Quick EDA":
    st.title("Load & Quick EDA")


elif st.session_state.current_page_key == "Settings":
    st.title("Settings")


else:
    st.write("Welcome to Vanguard Analytics. Please select an option.")
