import streamlit as st 
from datetime import date

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
    st.session_state.page = 0  # Ahora tenemos página 0 (Intro)

def go_to_page(page_number: int):
    st.session_state.page = page_number

# =====================================================
# COMPLETION LOGIC (✓ COMPLETED)
# =====================================================

def is_section0_completed() -> bool:
    # Project name obligatorio
    project_name = st.session_state.get("project_name")
    if not project_name or project_name.strip() == "":
        return False

    # PM obligatorio?
    pm = st.session_state.get("project_manager")
    if pm is None or pm == "Select project manager":
        return False

    # Date es opcional → no afecta completion
    return True


def is_section1_completed() -> bool:
    covered = st.session_state.get("covered")

    if covered is None:
        return False

    if covered == "No":
        return True

    if covered == "Yes":
        systems = st.session_state.get("systems") or []
        if not systems:
            return False

        if "UMS" in systems:
            ums_led = st.session_state.get("ums_led")
            ums_install = st.session_state.get("ums_install")
            if not ums_led or not ums_install:
                return False

            if ums_install == "Embedded":
                if not st.session_state.get("ums_embedded"):
                    return False
            if ums_install == "Conduit":
                if not st.session_state.get("ums_conduit"):
                    return False

        if "Upsolut" in systems:
            up_led = st.session_state.get("up_led")
            up_install = st.session_state.get("up_install")
            if not up_led or not up_install:
                return False

            if up_install == "Embedded":
                if not st.session_state.get("up_emb"):
                    return False
            if up_install == "Conduit":
                if not st.session_state.get("up_cond"):
                    return False

        return True

    return False


def is_section2_completed() -> bool:
    open_air = st.session_state.get("open_air")

    if open_air is None:
        return False

    if open_air == "No":
        return True

    if open_air == "Yes":
        sensors = st.session_state.get("rooftop_sensors") or []
        return len(sensors) > 0

    return False


def is_section3_completed() -> bool:
    inc = st.session_state.get("signage_included")

    if inc is None:
        return False

    if inc == "No":
        return True

    types = st.session_state.get("signage_types") or []
    if not types:
        return False

    if "Profile signs" in types:
        file_up = st.session_state.get("profile_signs_file")
        if file_up is None:
            return False

    return True


def is_section4_completed() -> bool:
    drawings = st.session_state.get("drawings_file")
    if drawings is None:
        return False
    if isinstance(drawings, list):
        return len(drawings) > 0
    return True


def is_section5_completed() -> bool:
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
# SIDEBAR NAVIGATION — now 6 pages
# =====================================================
with st.sidebar:
    st.markdown("### Navigation")

    sec0 = is_section0_completed()
    sec1 = is_section1_completed()
    sec2 = is_section2_completed()
    sec3 = is_section3_completed()
    sec4 = is_section4_completed()
    sec5 = is_section5_completed()

    labels = [
        ("0. Intro", sec0, 0),
        ("1. Covered spaces", sec1, 1),
        ("2. Rooftop / open-air solutions", sec2, 2),
        ("3. Signage", sec3, 3),
        ("4. Drawings", sec4, 4),
        ("5. Server", sec5, 5),
    ]

    def button_type(page_num, completed):
        if st.session_state.page == page_num:
            return "primary"
        elif completed:
            return "primary"
        else:
            return "secondary"

    for label, completed, num in labels:
        label2 = ("✓ " if completed else "") + label
        if st.button(label2, type=button_type(num, completed), use_container_width=True):
            go_to_page(num)

# =====================================================
# HEADER
# =====================================================
st.markdown("<h1 class='pgs-title'>PGS Submittals Setup Form</h1>", unsafe_allow_html=True)

# =====================================================
# PAGE 0 — INTRO PAGE
# =====================================================
if st.session_state.page == 0:

    st.markdown("## Intro – General project information")

    pm = st.selectbox(
        "Project manager",
        ["Select project manager", "PM1", "PM2"],
        key="project_manager"
    )

    project_name = st.text_input(
        "Project name (Required)",
        key="project_name",
        placeholder="Enter project name"
    )
    st.caption("**Please note the text entered in this field will appear exactly as written on the cover page.**")

    # Date — optional
    selected_date = st.date_input(
        "Submittal date (optional)",
        value=date.today(),
        key="date_input"
    )

    # Ensure correct format (MM-DD-YYYY)
    formatted_date = selected_date.strftime("%m-%d-%Y")
    st.session_state["formatted_date"] = formatted_date

    # Logo uploader
    logo = st.file_uploader(
        "Upload client/project logo (optional — PNG preferred for better quality)",
        type=["png", "jpg", "jpeg"],
        key="client_logo"
    )

    # Navigation
    st.markdown("---")
    col1, col2 = st.columns([1, 1])
    with col2:
        if st.button("Next ➜"):
            go_to_page(1)

# =====================================================
# (rest of your pages remain EXACTLY the same)
# PAGE 1 – COVERED SPACES
# ...
# PAGE 2 – ROOFTOP
# PAGE 3 – SIGNAGE
# PAGE 4 – DRAWINGS
# PAGE 5 – SERVER
# =====================================================

elif st.session_state.page == 1:
    # (YOUR PAGE 1 CODE HERE — unchanged)
    # ...
    pass

# =====================================================
st.markdown("---")
st.caption("© PGS – internal UI prototype for visual review only.")
