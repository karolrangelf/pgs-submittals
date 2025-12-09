import streamlit as st
from datetime import date
from docxtpl import DocxTemplate, InlineImage
from docx.shared import Mm
from docx2pdf import convert
import os

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
# TEMPLATE PATH (YOUR DRIVE FILE)
# =====================================================
TEMPLATE_PATH = r"G:\My Drive\Submittals_test_KR\PGS_CoverPage_Template.docx"


# =====================================================
# COMPLETION CHECKS
# =====================================================
def is_section0_completed() -> bool:
    if not st.session_state.get("project_name"):
        return False
    if st.session_state.get("project_manager") in [None, "Select project manager"]:
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
        ("6. Generate Package", True, 6),
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

    st.session_state.project_manager = st.selectbox(
        "Project manager",
        ["Select project manager", "PM1", "PM2"],
        key="project_manager"
    )

    st.session_state.project_name = st.text_input(
        "Project name (Required)",
        placeholder="Enter project name",
        key="project_name",
    )
    st.caption("**Please note the text entered in this field will appear exactly as written on the cover page.**")

    # Date input
    selected_date = st.date_input("Submittal date (optional)", value=date.today(), key="date_input")
    st.session_state.formatted_date = selected_date.strftime("%m-%d-%Y")

    # Logo uploader
    st.session_state.client_logo = st.file_uploader(
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

    covered = st.radio(
        "Does this project include covered parking?",
        ["Yes", "No"],
        horizontal=True,
        key="covered"
    )

    if covered == "Yes":
        systems = st.multiselect(
            "Select systems",
            ["UMS", "Upsolut"],
            key="systems"
        )

        if "UMS" in systems:
            st.radio("LED type", ["Internal", "External"], horizontal=True, key="ums_led")
            st.radio("Installation type", ["C-channel", "Embedded", "Conduit"], key="ums_install")

            if st.session_state.ums_install == "Embedded":
                st.radio("Embedded installation type", ["Direct ceiling", "Suspended"], key="ums_embedded")
            if st.session_state.ums_install == "Conduit":
                st.radio("Conduit installation type", ["Direct ceiling", "Suspended"], key="ums_conduit")

        if "Upsolut" in systems:
            st.radio("LED type", ["Internal", "External"], horizontal=True, key="up_led")
            st.radio("Installation type", ["C-channel", "Embedded", "Conduit"], key="up_install")

            if st.session_state.up_install == "Embedded":
                st.radio("Embedded installation type", ["Direct ceiling", "Suspended"], key="up_emb")
            if st.session_state.up_install == "Conduit":
                st.radio("Conduit installation type", ["Direct ceiling", "Suspended"], key="up_cond")

    elif covered == "No":
        st.info("No covered spaces selected. Please proceed to the next section.")

    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅ Back"):
            go_to_page(0)
    with col2:
        if st.button("Next ➜"):
            go_to_page(2)


# =====================================================
# PAGE 2 — ROOFTOP
# =====================================================
elif st.session_state.page == 2:
    st.markdown("## 2. Rooftop / open-air solutions")

    open_air = st.radio(
        "Does this project include rooftop or open-air solutions?",
        ["Yes", "No"],
        horizontal=True,
        key="open_air",
    )

    if open_air == "Yes":
        st.multiselect(
            "Select sensors:",
            ["11-X Pucks", "iVision", "Optex", "Views"],
            key="rooftop_sensors"
        )
    elif open_air == "No":
        st.info("No rooftop or open-air solutions selected. Please proceed to the next section.")

    st.markdown("---")
    if st.button("⬅ Back"):
        go_to_page(1)
    if st.button("Next ➜"):
        go_to_page(3)


# =====================================================
# PAGE 3 — SIGNAGE
# =====================================================
elif st.session_state.page == 3:

    st.markdown("## 3. Signage")

    st.session_state.signage_included = st.radio(
        "Does this project include signage?",
        ["Yes", "No"],
        horizontal=True,
        key="signage_included"
    )

    if st.session_state.signage_included == "Yes":
        st.session_state.signage_types = st.multiselect(
            "Select signage types:",
            ["Profile signs", "Matrix sign", "Monument sign"],
            key="signage_types"
        )

        if "Profile signs" in st.session_state.signage_types:
            st.session_state.profile_signs_file = st.file_uploader(
                "Upload signage design created using Indect Project Calculator",
                type=["pdf", "png", "jpg"],
                key="profile_signs_file"
            )

    st.markdown("---")
    if st.button("⬅ Back"):
        go_to_page(2)
    if st.button("Next ➜"):
        go_to_page(4)


# =====================================================
# PAGE 4 — DRAWINGS
# =====================================================
elif st.session_state.page == 4:

    st.markdown("## 4. Drawings")

    st.session_state.drawings_file = st.file_uploader(
        "Upload most updated drawings",
        type=["pdf", "dwg", "dxf", "zip"],
        accept_multiple_files=True,
        key="drawings_file"
    )

    st.markdown("---")
    if st.button("⬅ Back"):
        go_to_page(3)
    if st.button("Next ➜"):
        go_to_page(5)


# =====================================================
# PAGE 5 — SERVER
# =====================================================
elif st.session_state.page == 5:

    st.markdown("## 5. Server")

    st.session_state.server_topology_file = st.file_uploader(
        "Upload specific network topology for this project",
        type=["pdf", "png", "jpg", "vsdx", "zip"],
        key="server_topology_file"
    )

    st.markdown("---")
    if st.button("⬅ Back"):
        go_to_page(4)
    if st.button("Next ➜"):
        go_to_page(6)


# =====================================================
# PAGE 6 — GENERATE COVER PAGE (PDF)
# =====================================================
elif st.session_state.page == 6:

    st.markdown("## 6. Generate Cover Page")

    st.write("This will generate the cover page using your template and inputs from the Intro Page.")

    # Button
    if st.button("Generate Cover Page (PDF)"):

        # Load Template
        doc = DocxTemplate(TEMPLATE_PATH)

        # Logo processing
        logo_file = st.session_state.get("client_logo")
        if logo_file:
            logo_path = "temp_logo.png"
            with open(logo_path, "wb") as f:
                f.write(logo_file.getbuffer())
            client_logo = InlineImage(doc, logo_path, width=Mm(30))
        else:
            client_logo = ""

        context = {
            "project_name": st.session_state.project_name,
            "date": st.session_state.formatted_date,
            "client_logo": client_logo
        }

        # Save docx
        output_docx = "Generated_CoverPage.docx"
        doc.render(context)
        doc.save(output_docx)

        # Convert to PDF
        output_pdf = "Generated_CoverPage.pdf"
        convert(output_docx, output_pdf)

        st.success("Cover Page PDF generated successfully!")

        # PDF preview
        with open(output_pdf, "rb") as pdf_file:
            st.download_button(
                label="Download Cover Page (PDF)",
                data=pdf_file,
                file_name="CoverPage.pdf",
                mime="application/pdf"
            )

            st.write("### Cover Page Preview:")
            st.pdf(output_pdf)

    st.markdown("---")
    if st.button("⬅ Back"):
        go_to_page(5)


# =====================================================
# FOOTER
# =====================================================
st.markdown("---")
st.caption("© PGS – internal UI prototype for visual review only.")
