import streamlit as st 

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
    st.session_state.page = 1  # 1..5

def go_to_page(page_number: int):
    st.session_state.page = page_number

# =====================================================
# COMPLETION LOGIC (✓ COMPLETED)
# =====================================================
def is_section1_completed() -> bool:
    covered = st.session_state.get("covered")

    # todavía no responden covered
    if covered is None:
        return False

    # Si responde NO, la sección se considera completa
    if covered == "No":
        return True

    # Si responde YES, debe llenar el resto
    if covered == "Yes":
        systems = st.session_state.get("systems") or []
        if not systems:
            return False

        # -------- UMS --------
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

        # -------- Upsolut --------
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

    # NO → completo
    if open_air == "No":
        return True

    # YES → debe elegir al menos un sensor
    if open_air == "Yes":
        rooftop_sensors = st.session_state.get("rooftop_sensors") or []
        if not rooftop_sensors:
            return False
        return True

    return False


def is_section3_completed() -> bool:
    signage_included = st.session_state.get("signage_included")

    if signage_included is None:
        return False

    # NO → completo
    if signage_included == "No":
        return True

    # YES → hay que elegir al menos un tipo
    signage_types = st.session_state.get("signage_types") or []
    if not signage_types:
        return False

    # Si incluye Profile signs → archivo obligatorio
    if "Profile signs" in signage_types:
        profile_file = st.session_state.get("profile_signs_file")
        if profile_file is None:
            return False

    return True


def is_section4_completed() -> bool:
    drawings_file = st.session_state.get("drawings_file")
    if drawings_file is None:
        return False
    if isinstance(drawings_file, list):
        return len(drawings_file) > 0
    return True


def is_section5_completed() -> bool:
    server_file = st.session_state.get("server_topology_file")
    return server_file is not None

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
# SIDEBAR – NAV CON 5 MÓDULOS
# =====================================================
with st.sidebar:
    st.markdown("### Navigation")

    sec1_completed = is_section1_completed()
    sec2_completed = is_section2_completed()
    sec3_completed = is_section3_completed()
    sec4_completed = is_section4_completed()
    sec5_completed = is_section5_completed()

    label1 = ("✓ " if sec1_completed else "") + "1. Covered spaces"
    label2 = ("✓ " if sec2_completed else "") + "2. Rooftop / open-air solutions"
    label3 = ("✓ " if sec3_completed else "") + "3. Signage"
    label4 = ("✓ " if sec4_completed else "") + "4. Drawings"
    label5 = ("✓ " if sec5_completed else "") + "5. Server"

    def button_type(page_num, completed):
        if st.session_state.page == page_num:
            return "primary"
        elif completed:
            return "primary"
        else:
            return "secondary"

    if st.button(label1, type=button_type(1, sec1_completed), use_container_width=True):
        go_to_page(1)

    if st.button(label2, type=button_type(2, sec2_completed), use_container_width=True):
        go_to_page(2)

    if st.button(label3, type=button_type(3, sec3_completed), use_container_width=True):
        go_to_page(3)

    if st.button(label4, type=button_type(4, sec4_completed), use_container_width=True):
        go_to_page(4)

    if st.button(label5, type=button_type(5, sec5_completed), use_container_width=True):
        go_to_page(5)

# =====================================================
# HEADER
# =====================================================
st.markdown("<h1 class='pgs-title'>PGS Submittals Setup Form</h1>", unsafe_allow_html=True)

# =====================================================
# PAGE 1 – GENERAL + COVERED SPACES
# =====================================================
if st.session_state.page == 1:

    st.markdown("### General project information")

    # Project Manager (pregunta general, fuera del módulo 1)
    pm = st.selectbox(
        "Project manager",
        ["Select project manager", "PM1", "PM2", "PM3"],
        key="project_manager"
    )

    st.markdown("## 1. Covered spaces")

    covered = st.radio(
        "Does this project include covered parking?",
        ["Yes", "No"],
        horizontal=True,
        key="covered",
        index=None
    )

    if covered == "Yes":

        st.markdown("### Systems included in the project")
        systems = st.multiselect(
            "Select systems",
            ["UMS", "Upsolut"],
            placeholder="Select systems",
            key="systems"
        )

        # ----------------- UMS -----------------
        if "UMS" in systems:
            st.markdown("#### UMS")

            ums_led = st.radio(
                "LED type",
                ["Internal", "External"],
                horizontal=True,
                key="ums_led",
                index=None
            )

            ums_install = st.radio(
                "Installation type",
                ["C-channel", "Embedded", "Conduit"],
                key="ums_install",
                index=None
            )

            if ums_install == "Embedded":
                ums_embedded = st.radio(
                    "Embedded installation type",
                    ["Direct ceiling", "Suspended"],
                    key="ums_embedded",
                    index=None
                )

            if ums_install == "Conduit":
                ums_conduit = st.radio(
                    "Conduit installation type",
                    ["Direct ceiling", "Suspended"],
                    key="ums_conduit",
                    index=None
                )

        # ----------------- UPSOLUT -----------------
        if "Upsolut" in systems:
            st.markdown("#### Upsolut")

            up_led = st.radio(
                "LED type",
                ["Internal", "External"],
                horizontal=True,
                key="up_led",
                index=None
            )

            up_install = st.radio(
                "Installation type",
                ["C-channel", "Embedded", "Conduit"],
                key="up_install",
                index=None
            )

            if up_install == "Embedded":
                up_emb = st.radio(
                    "Embedded installation type",
                    ["Direct ceiling", "Suspended"],
                    key="up_emb",
                    index=None
                )

            if up_install == "Conduit":
                up_cond = st.radio(
                    "Conduit installation type",
                    ["Direct ceiling", "Suspended"],
                    key="up_cond",
                    index=None
                )

    elif covered == "No":
        st.info("No covered spaces selected. Please proceed to the next section.")
    else:
        st.caption("Please answer if the project includes covered parking.")

    # ---------- NAVIGATION ----------
    st.markdown("---")
    col1, col2 = st.columns([1, 1])
    with col2:
        if st.button("Next ➜"):
            go_to_page(2)

# =====================================================
# PAGE 2 – ROOFTOP / OPEN-AIR SOLUTIONS
# =====================================================
elif st.session_state.page == 2:

    st.markdown("## 2. Rooftop / open-air solutions")

    open_air = st.radio(
        "Does this project include rooftop or open-air solutions?",
        ["Yes", "No"],
        horizontal=True,
        key="open_air",
        index=None
    )

    if open_air == "Yes":
        rooftop_sensors = st.multiselect(
            "Select the sensors included:",
            ["11-X Pucks", "iVision", "Optex", "Views"],
            placeholder="Select sensors",
            key="rooftop_sensors"
        )
    elif open_air == "No":
        st.info("No rooftop or open-air solutions selected. Please proceed to the next section.")
    else:
        st.caption("Please answer if the project includes rooftop or open-air solutions.")

    st.markdown("---")
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("⬅ Back"):
            go_to_page(1)
    with col2:
        if st.button("Next ➜"):
            go_to_page(3)

# =====================================================
# PAGE 3 – SIGNAGE
# =====================================================
elif st.session_state.page == 3:

    st.markdown("## 3. Signage")

    signage_included = st.radio(
        "Does this project include signage?",
        ["Yes", "No"],
        horizontal=True,
        key="signage_included",
        index=None
    )

    if signage_included == "Yes":
        signage_types = st.multiselect(
            "Select signage types included in this project:",
            ["Profile signs", "Matrix sign", "Monument sign"],
            placeholder="Select signage types",
            key="signage_types"
        )

        if "Profile signs" in (signage_types or []):
            profile_file = st.file_uploader(
                "Upload signage design created using Indect Project Calculator",
                type=["pdf", "xlsx", "xls", "csv", "png", "jpg", "jpeg"],
                key="profile_signs_file"
            )
    elif signage_included == "No":
        st.info("No signage selected. Please proceed to the next section.")
    else:
        st.caption("Please answer if the project includes signage.")

    st.markdown("---")
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("⬅ Back"):
            go_to_page(2)
    with col2:
        if st.button("Next ➜"):
            go_to_page(4)

# =====================================================
# PAGE 4 – DRAWINGS
# =====================================================
elif st.session_state.page == 4:

    st.markdown("## 4. Drawings")

    drawings_file = st.file_uploader(
        "Upload most updated drawings for the project",
        type=["pdf", "dwg", "dxf", "zip", "rar"],
        key="drawings_file",
        accept_multiple_files=True
    )

    st.markdown("---")
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("⬅ Back"):
            go_to_page(3)
    with col2:
        if st.button("Next ➜"):
            go_to_page(5)

# =====================================================
# PAGE 5 – SERVER / NETWORK TOPOLOGY
# =====================================================
elif st.session_state.page == 5:

    st.markdown("## 5. Server")

    server_file = st.file_uploader(
        "Upload specific network topology for this project created by IT team",
        type=["pdf", "png", "jpg", "jpeg", "vsdx", "zip"],
        key="server_topology_file"
    )

    st.markdown("---")
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("⬅ Back"):
            go_to_page(4)

# =====================================================
# FOOTER
# =====================================================
st.markdown("---")
st.caption("© PGS – internal UI prototype for visual review only.")
