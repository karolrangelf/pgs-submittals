import streamlit as st
import base64
from pathlib import Path

# =====================================================
# PAGE CONFIG
# =====================================================
st.set_page_config(page_title="PGS submittals setup form", layout="centered")

# =====================================================
# BACKGROUND IMAGE
# =====================================================
def set_bg(png_file):
    file_path = Path(png_file)
    with open(file_path, "rb") as f:
        data = f.read()
    encoded = base64.b64encode(data).decode()

    css = f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{encoded}");
        background-size: cover;
        background-attachment: fixed;
        background-position: center;
        color: white !important;
    }}

    /* ---------------------- AGUAMARINA ---------------------- */
    div[data-baseweb="tag"] {{
        background-color: #69F2C4 !important;
        color: black !important;
        border-radius: 6px !important;
        font-weight: 600 !important;
    }}

    div[data-baseweb="tag"] svg {{
        fill: black !important;
    }}

    input[type="radio"], input[type="checkbox"] {{
        accent-color: #69F2C4 !important;
    }}

    .stSelectbox:focus-within, .stMultiSelect:focus-within {{
        border-color: #69F2C4 !important;
        box-shadow: 0 0 0 2px #69F2C4 !important;
    }}

    .stTextInput input::placeholder,
    .stSelectbox div[data-baseweb="select"] div {{
        color: #ffffff !important;
    }}

    /* ---------------------- NUEVO: TEXTOS BLANCOS ---------------------- */

    /* Etiquetas de radios, checkboxes y selects */
    .stRadio label, .stCheckbox label, .stSelectbox label, label {{
        color: white !important;
    }}

    /* Opciones dentro del dropdown */
    div[role="listbox"] div {{
        color: white !important;
    }}

    /* ---------------------- FUENTES ---------------------- */
    @import url('https://fonts.googleapis.com/css2?family=Oswald:wght@500;700&display=swap');

    .pgs-title {{
        font-family: 'Oswald', sans-serif;
        font-size: 72px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 2px;
        color: white;
        width: 100%;
        text-align: center;
        margin-top: 20px;
        margin-bottom: 10px;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

set_bg("background.png")

# =====================================================
# HEADER
# =====================================================
st.markdown("<h1 class='pgs-title'>PGS Submittals Setup Form</h1>", unsafe_allow_html=True)

# =====================================================
# FORM CONTENT
# =====================================================
st.markdown("### Covered spaces")
covered = st.radio(
    "Does this project include covered parking?",
    ["Yes", "No"],
    horizontal=True,
    key="covered"
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
        st.markdown("## UMS")

        st.markdown("#### LED type")
        ums_led = st.radio(
            "",
            ["Internal", "External"],
            horizontal=True,
            key="ums_led"
        )

        st.markdown("#### Installation type")
        ums_install = st.radio(
            "",
            ["C-channel", "Embedded", "Conduit"],
            key="ums_install"
        )

        if ums_install == "Embedded":
            st.markdown("##### Embedded installation type")
            ums_embedded = st.radio(
                "",
                ["Direct ceiling", "Suspended"],
                key="ums_embedded"
            )

        if ums_install == "Conduit":
            st.markdown("##### Conduit installation type")
            ums_conduit = st.radio(
                "",
                ["Direct ceiling", "Suspended"],
                key="ums_conduit"
            )

    # ----------------- UPSOLUT -----------------
    if "Upsolut" in systems:
        st.markdown("## Upsolut")

        st.markdown("#### LED type")
        up_led = st.radio(
            "",
            ["Internal", "External"],
            horizontal=True,
            key="up_led"
        )

        st.markdown("#### Installation type")
        up_install = st.radio(
            "",
            ["C-channel", "Embedded", "Conduit"],
            key="up_install"
        )

        if up_install == "Embedded":
            st.markdown("##### Embedded installation type")
            up_emb = st.radio(
                "",
                ["Direct ceiling", "Suspended"],
                key="up_emb"
            )

        if up_install == "Conduit":
            st.markdown("##### Conduit installation type")
            up_cond = st.radio(
                "",
                ["Direct ceiling", "Suspended"],
                key="up_cond"
            )

else:
    st.info("No covered spaces selected. Hardware section is skipped.")

st.markdown("---")
st.caption("© PGS – internal UI prototype for visual review only.")
