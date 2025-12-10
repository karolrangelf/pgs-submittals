import streamlit as st
from datetime import date
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
import io

# =====================================================
# PAGE CONFIG
# =====================================================
st.set_page_config(
    page_title="PGS submittals setup form",
    layout="centered"
)

# =====================================================
# SESSION STATE: PAGE NAVIGATION
# =====================================================
if "page" not in st.session_state:
    st.session_state.page = 0  # Intro Page

def go_to_page(page_number: int):
    st.session_state.page = page_number


# =====================================================
# PDF GENERATOR – COVER PAGE
# =====================================================
def generate_cover_pdf(project_name: str, date_str: str, logo_file):
    """
    Genera un PDF de portada usando CoverTemplate.png como fondo
    y colocando:
      - project_name centrado debajo de 'Project:'
      - date_str centrado más abajo en el círculo
      - logo opcional en un cuadro de 2"x2" en la esquina inferior derecha
    """
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)

    # Página tamaño carta: 612 x 792 puntos
    page_width, page_height = letter  # (612, 792)

    # Fondo (tu diseño de Canva)
    bg = ImageReader("CoverTemplate.png")
    c.drawImage(bg, 0, 0, width=page_width, height=page_height)

    # ===============================
    #   PROJECT NAME (texto dinámico)
    # ===============================
    c.setFont("Helvetica", 14)
    c.setFillColorRGB(0, 0, 0)  # negro

    # Coordenadas aproximadas debajo de "Project:" según tu plantilla
    project_y = 430  # puedes ajustar fino si quieres
    c.drawCentredString(page_width / 2, project_y, project_name)

    # ===============================
    #   DATE (texto dinámico)
    # ===============================
    if date_str:
        c.setFont("Helvetica", 12)
        date_y = 310   # posición baja del círculo según la plantilla
        c.drawCentredString(page_width / 2, date_y, date_str)

    # ===============================
    #   CLIENT LOGO (si existe)
    # ===============================
    if logo_file is not None:
        logo = ImageReader(logo_file)

        # Tamaño del cuadro: 2" x 2" → 144 x 144 puntos
        logo_w = 144
        logo_h = 144

        # Posición inferior derecha con pequeño margen
        logo_x = page_width - logo_w - 30
        logo_y = 30

        c.drawImage(
            logo,
            logo_x,
            logo_y,
            width=logo_w,
            height=logo_h,
            preserveAspectRatio=True,
            mask='auto'
        )

    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer


# =====================================================
# COMPLETION CHECKS
# =====================================================
def is_section0_completed() -> bool:
    project_name = st.session_state.get("project_name")
    pm = st.session_state.get("project_manager")
    if not project_name or project_name.strip() == "":
        return False
    if pm in [None, "Select project manager"]:
        return False
    return True


def is_section1_completed():
    covered = st.session_state.get("covered")
    if covered is None:
        return False
    if covered == "No":
        return True

    systems = st.session_state.get("systems") or []
    if not systems:
        return False

    if "UMS" in systems:
        if not st.session_state.get("ums_led") or not st.session_state.get("ums_install"):
            return False
        if st.session_state.get("ums_install") == "Embedded" and not st.session_state.get("ums_embedded"):
            return False
        if st.session_state.get("ums_install") == "Conduit" and not st.session_state.get("ums_conduit"):
            return False

    if "Upsolut" in systems:
        if not st.session_state.get("up_led") or not st.session_state.get("up_install"):
            return False
        if st.session_state.get("up_install") == "Embedded" and not st.session_state.get("up_emb"):
            return False
        if st.session_state.get("up_install") == "Conduit" and not st.session_state.get("up_cond"):
            return False

    return True


def is_section2_completed():
    open_air = st.session_state.get("open_air")
    if open_air is None:
        return False
    if open_air == "No":
        return True
    sensors = st.session_state.get("rooftop_sensors") or []
    return len(sensors) > 0


def is_section3_completed():
    inc = st.session_state.get("signage_included")
    if inc is None:
        return False
    if inc == "No":
        return True
    types = st.session_state.get("signage_types") or []
    if not types:
        return False
    if "Profile signs" in types and not st.session_state.get("profile_signs_file"):
        return False
    return True


def is_section4_completed():
    f = st.session_state.get("drawings_file")
    if f is None:
        return False
    return isinstance(f, list) and len(f) > 0


def is_section5_completed():
    return st.session_state.get("server_topology_file") is not None


# =====================================================
# ESTILOS GENERALES
# =====================================================
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Oswald:wght@500;700&display=swap');

    html, body, [data-testid="stAppViewContainer"] {
        background-color: #FFFFFF !important;
        color: #111111 !important;
    }

    .pgs-title {
        font-family: 'Oswald', sans-serif;
        font-size: 72px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 2px;
        color: #0F2B63;
        width: 100%;
        text-align: center;
        margin-top: 20px;
        margin-bottom: 10px;
    }

    h1, h2, h3, h4, h5, h6, p, label, span, div {
        color: #111111;
    }

    [data-testid="stSidebar"] button {
        font-size: 18px !important;
        font-weight: 600 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# =====================================================
# SIDEBAR NAVIGATION
# =====================================================
with st.sidebar:
    st.markdown("### Navigation")

    sections = [
        ("0. Intro", is_section0_completed(), 0),
        ("1. Covered spaces", is_section1_completed(), 1),
        ("2. Rooftop / open-air solutions", is_section2_completed(), 2),
        ("3. Signage", is_section3_completed(), 3),
        ("4. Drawings", is_section4_completed(), 4),
        ("5. Server", is_section5_completed(), 5),
        ("6. Generate Cover Page", True, 6),
    ]

    def button_type(p, done):
        if st.session_state.page == p:
            return "primary"
        elif done:
            return "primary"
        return "secondary"

    for label, done, pnum in sections:
        display = ("✓ " if done else "") + label
        if st.button(display, type=button_type(pnum, done), use_container_width=True):
            go_to_page(pnum)


# =====================================================
# HEADER
# =====================================================
st.markdown("<h1 class='pgs-title'>PGS Submittals Setup Form</h1>", unsafe_allow_html=True)


# =====================================================
# PAGE 0 — INTRO
# =====================================================
if st.session_state.page == 0:

    st.markdown("## Intro – General project information")

    st.selectbox(
        "Project manager",
        ["Select project manager", "PM1", "PM2"],
        key="project_manager"
    )

    st.text_input(
        "Project name (Required)",
        placeholder="Enter project name",
        key="project_name",
    )
    st.caption("**Please note the text entered in this field will appear exactly as written on the cover page.**")

    # Date input (opcional, pero la guardamos formateada)
    selected_date = st.date_input(
        "Submittal date (optional)",
        value=date.today(),
        key="date_input"
    )
    st.session_state.formatted_date = selected_date.strftime("%m-%d-%Y")

    # Logo uploader (opcional)
    st.file_uploader(
        "Upload client/project logo (optional — PNG preferred)",
        type=["png", "jpg", "jpeg"],
        key="client_logo"
    )

    st.markdown("---")
    if st.button("Next ➜"):
        go_to_page(1)


# =====================================================
# PAGE 1 — COVERED SPACES
# =====================================================
elif st.session_state.page == 1:
    st.markdown("## 1. Covered spaces")

    st.radio(
        "Does this project include covered parking?",
        ["Yes", "No"],
        horizontal=True,
        key="covered"
    )

    covered = st.session_state.get("covered")

    if covered == "Yes":
        st.multiselect(
            "Select systems",
            ["UMS", "Upsolut"],
            key="systems"
        )

        systems = st.session_state.get("systems") or []

        if "UMS" in systems:
            st.markdown("#### UMS")
            st.radio("LED type", ["Internal", "External"], horizontal=True, key="ums_led")
            st.radio("Installation type", ["C-channel", "Embedded", "Conduit"], key="ums_install")

            ums_install = st.session_state.get("ums_install")
            if ums_install == "Embedded":
                st.radio("Embedded installation type", ["Direct ceiling", "Suspended"], key="ums_embedded")
            if ums_install == "Conduit":
                st.radio("Conduit installation type", ["Direct ceiling", "Suspended"], key="ums_conduit")

        if "Upsolut" in systems:
            st.markdown("#### Upsolut")
            st.radio("LED type", ["Internal", "External"], horizontal=True, key="up_led")
            st.radio("Installation type", ["C-channel", "Embedded", "Conduit"], key="up_install")

            up_install = st.session_state.get("up_install")
            if up_install == "Embedded":
                st.radio("Embedded installation type", ["Direct ceiling", "Suspended"], key="up_emb")
            if up_install == "Conduit":
                st.radio("Conduit installation type", ["Direct ceiling", "Suspended"], key="up_cond")

    elif covered == "No":
        st.info("No covered spaces selected. Please proceed to the next section.")
    else:
        st.caption("Please answer if the project includes covered parking.")

    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅ Back"):
            go_to_page(0)
    with col2:
        if st.button("Next ➜"):
            go_to_page(2)


# =====================================================
# PAGE 2 — ROOFTOP / OPEN-AIR SOLUTIONS
# =====================================================
elif st.session_state.page == 2:
    st.markdown("## 2. Rooftop / open-air solutions")

    st.radio(
        "Does this project include rooftop or open-air solutions?",
        ["Yes", "No"],
        horizontal=True,
        key="open_air",
    )

    open_air = st.session_state.get("open_air")

    if open_air == "Yes":
        st.multiselect(
            "Select the sensors included:",
            ["11-X Pucks", "iVision", "Optex", "Views"],
            key="rooftop_sensors"
        )
    elif open_air == "No":
        st.info("No rooftop or open-air solutions selected. Please proceed to the next section.")
    else:
        st.caption("Please answer if the project includes rooftop or open-air solutions.")

    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅ Back"):
            go_to_page(1)
    with col2:
        if st.button("Next ➜"):
            go_to_page(3)


# =====================================================
# PAGE 3 — SIGNAGE
# =====================================================
elif st.session_state.page == 3:
    st.markdown("## 3. Signage")

    st.radio(
        "Does this project include signage?",
        ["Yes", "No"],
        horizontal=True,
        key="signage_included"
    )

    signage_included = st.session_state.get("signage_included")

    if signage_included == "Yes":
        st.multiselect(
            "Select signage types included in this project:",
            ["Profile signs", "Matrix sign", "Monument sign"],
            key="signage_types"
        )

        signage_types = st.session_state.get("signage_types") or []

        if "Profile signs" in signage_types:
            st.file_uploader(
                "Upload signage design created using Indect Project Calculator",
                type=["pdf", "xlsx", "xls", "csv", "png", "jpg", "jpeg"],
                key="profile_signs_file"
            )
    elif signage_included == "No":
        st.info("No signage selected. Please proceed to the next section.")
    else:
        st.caption("Please answer if the project includes signage.")

    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅ Back"):
            go_to_page(2)
    with col2:
        if st.button("Next ➜"):
            go_to_page(4)


# =====================================================
# PAGE 4 — DRAWINGS
# =====================================================
elif st.session_state.page == 4:
    st.markdown("## 4. Drawings")

    st.file_uploader(
        "Upload most updated drawings for the project",
        type=["pdf", "dwg", "dxf", "zip", "rar"],
        key="drawings_file",
        accept_multiple_files=True
    )

    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅ Back"):
            go_to_page(3)
    with col2:
        if st.button("Next ➜"):
            go_to_page(5)


# =====================================================
# PAGE 5 — SERVER / NETWORK TOPOLOGY
# =====================================================
elif st.session_state.page == 5:
    st.markdown("## 5. Server")

    st.file_uploader(
        "Upload specific network topology for this project created by IT team",
        type=["pdf", "png", "jpg", "jpeg", "vsdx", "zip"],
        key="server_topology_file"
    )

    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅ Back"):
            go_to_page(4)
    with col2:
        if st.button("Next ➜"):
            go_to_page(6)


# =====================================================
# PAGE 6 — GENERATE COVER PAGE (PDF)
# =====================================================
elif st.session_state.page == 6:
    st.markdown("## 6. Generate Cover Page")

    project_name = st.session_state.get("project_name", "")
    date_str = st.session_state.get("formatted_date", "")
    logo_file = st.session_state.get("client_logo", None)

    st.write(f"**Project name:** {project_name}")
    st.write(f"**Date:** {date_str}")
    if logo_file:
        st.write("**Client logo uploaded:** ✅")
    else:
        st.write("**Client logo uploaded:** No logo (field left blank)")

    st.markdown("---")

    if st.button("Generate Cover Page PDF"):
        pdf_bytes = generate_cover_pdf(project_name, date_str, logo_file)

        st.success("Cover Page PDF generated successfully!")

        st.download_button(
            label="Download Cover Page (PDF)",
            data=pdf_bytes,
            file_name="CoverPage.pdf",
            mime="application/pdf"
        )

        st.write("### Preview")
        st.pdf(pdf_bytes)

    st.markdown("---")
    if st.button("⬅ Back"):
        go_to_page(5)


# =====================================================
# FOOTER
# =====================================================
st.markdown("---")
st.caption("© PGS – internal UI prototype for visual review only.")
