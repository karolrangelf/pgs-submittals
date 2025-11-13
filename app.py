import streamlit as st

# ============================
# BACKGROUND IMAGE
# ============================

background_url = "https://raw.githubusercontent.com/karolrangelf/pgs-submittals/main/background.png"

st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("{background_url}");
        background-size: cover;
        background-attachment: fixed;
        background-position: center;
    }}

    /* Form styling */
    .section-title {{
        font-size: 1.35rem;
        font-weight: 600;
        margin-top: 1.5rem;
        margin-bottom: .5rem;
    }}

    /* tab buttons */
    .stTabs [data-baseweb="tab"] {{
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        padding-top: 0.6rem !important;
        padding-bottom: 0.6rem !important;
    }}

    /* remove excessive spacing under radio/dropdowns */
    div[data-testid="stRadio"] > label, 
    div[data-testid="stSelectbox"] > label {{
        margin-bottom: 0.1rem !important;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# ============================
# PAGE CONFIG
# ============================

st.set_page_config(page_title="PGS submittals setup form", layout="centered")

st.title("PGS submittals setup form")
st.caption("This preview shows only how the questions would appear in the web app. No logic or file handling yet.")

# ============================
# STEP 0 – COVERED SPACES
# ============================

st.markdown("<div class='section-title'>Covered spaces</div>", unsafe_allow_html=True)
covered = st.radio(" ", ["Yes", "No"], horizontal=True)

if covered == "No":
    st.info("No covered spaces → hardware section will be skipped.")
    st.stop()

# ============================
# STEP 1 – SYSTEM SELECTION
# ============================

st.markdown("<div class='section-title'>Systems included in the project</div>", unsafe_allow_html=True)

systems = st.multiselect(
    "",
    ["UMS", "Upsolut"],
)

if len(systems) == 0:
    st.stop()

# ============================
# SYSTEM TABS
# ============================

st.markdown("<div class='section-title'>Hardware details per system</div>", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["UMS", "Upsolut"])

# ---- UMS TAB ----
with tab1:

    if "UMS" not in systems:
        st.info("UMS is not selected in this project.")
    else:

        st.markdown("<div class='section-title'>LED type</div>", unsafe_allow_html=True)
        ums_led = st.radio(
            "",
            ["Internal", "External"],
            horizontal=True
        )

        st.markdown("<div class='section-title'>Installation type</div>", unsafe_allow_html=True)
        ums_install = st.radio(
            "",
            ["C-channel", "Embedded", "Conduit"]
        )

        # Embedded / Conduit sub-options
        if ums_install == "Embedded":
            st.markdown("<div class='section-title'>Embedded installation type</div>", unsafe_allow_html=True)
            ums_emb = st.radio("", ["Direct ceiling", "Suspended"])

        if ums_install == "Conduit":
            st.markdown("<div class='section-title'>Conduit installation type</div>", unsafe_allow_html=True)
            ums_cond = st.radio("", ["Direct ceiling", "Suspended"])

        # COMO/POSU
        st.markdown("<div class='section-title'>COMO / POSU requirement (UMS only)</div>", unsafe_allow_html=True)
        remove_posu = st.checkbox("POSU is NOT required for this project (only COMO will be included).")

        if remove_posu:
            st.info("Only COMO spec will be included for this UMS project. POSU will be excluded.")
        else:
            st.info("Default behavior: COMO and POSU specs will be included for this UMS project.")

# ---- UPSOLUT TAB ----
with tab2:

    if "Upsolut" not in systems:
        st.info("Upsolut is not selected in this project.")
    else:

        st.markdown("<div class='section-title'>LED type</div>", unsafe_allow_html=True)
        up_led = st.radio(
            "",
            ["Internal", "External"],
            horizontal=True
        )

        st.markdown("<div class='section-title'>Installation type</div>", unsafe_allow_html=True)
        up_install = st.radio(
            "",
            ["C-channel", "Embedded", "Conduit"]
        )

        if up_install == "Embedded":
            st.markdown("<div class='section-title'>Embedded installation type</div>", unsafe_allow_html=True)
            up_emb = st.radio("", ["Direct ceiling", "Suspended"])

        if up_install == "Conduit":
            st.markdown("<div class='section-title'>Conduit installation type</div>", unsafe_allow_html=True)
            up_cond = st.radio("", ["Direct ceiling", "Suspended"])


# Divider
st.markdown("---")
st.caption("© PGS – internal UI prototype for visual review only.")
