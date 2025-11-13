import streamlit as st

st.set_page_config(
    page_title="PGS submittals setup form",
    page_icon="📄",
    layout="centered"
)

# --- CSS SUAVE: solo margenes, no cambia tamaños base ---
st.markdown("""
    <style>
    /* Reducir un poco el espacio debajo de los h4 (####) */
    h4 {
        margin-bottom: 6px !important;
        margin-top: 22px !important;
    }

    /* Ajustar espacio vertical entre grupos de radio buttons */
    div.stRadio > div {
        gap: 0.3rem !important;
        margin-top: -4px !important;
        margin-bottom: -4px !important;
    }
    </style>
""", unsafe_allow_html=True)

# --------- TAB-STYLE HEADER PARA UMS / UPSOLUT ---------
def system_banner(title: str):
    st.markdown(
        f"""
        <div style="
            margin: 28px 0 14px 0;
            text-align: center;
        ">
            <span style="
                background-color: #f6f7fb;
                padding: 8px 28px;
                border-radius: 6px;
                border: 1px solid #e1e3ee;
                font-size: 20px;
                font-weight: 600;
                display: inline-block;
            ">
                {title}
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )

# -------------------- TÍTULO PRINCIPAL --------------------
st.title("PGS submittals setup form")
st.caption(
    "This preview shows only the questions as they would appear in the web app. "
    "No logic or file handling yet."
)

# -------------------- COVERED SPACES --------------------
st.subheader("Covered spaces")

covered = st.radio(
    "",
    ["Yes", "No"],
    index=None,
    horizontal=True,
    key="covered_parking",
)

if covered is None:
    st.stop()

if covered == "No":
    st.info("No covered spaces – hardware block is skipped.")
    st.stop()

# -------------------- SYSTEMS INCLUDED --------------------
st.subheader("Systems included in the project")

systems = st.multiselect(
    "",
    ["UMS", "UPSOLUT"],
    key="systems",
)

if not systems:
    st.info("Select at least one system to continue.")
    st.stop()

# -------------------- UMS SECTION --------------------
if "UMS" in systems:

    system_banner("UMS")

    # LED type
    st.markdown("#### LED type")
    ums_led = st.radio(
        "",
        ["Internal", "External"],
        horizontal=True,
        key="ums_led",
    )

    # Installation type
    st.markdown("#### Installation type")
    ums_install = st.radio(
        "",
        ["C-channel", "Embedded", "Conduit"],
        horizontal=False,
        key="ums_install",
    )

    # Embedded sub-options
    if ums_install == "Embedded":
        st.markdown("#### Embedded installation type")
        ums_embedded = st.radio(
            "",
            ["Direct ceiling", "Suspended"],
            horizontal=True,
            key="ums_embedded",
        )

    # Conduit sub-options
    if ums_install == "Conduit":
        st.markdown("#### Conduit installation type")
        ums_conduit = st.radio(
            "",
            ["Direct ceiling", "Suspended"],
            horizontal=True,
            key="ums_conduit",
        )

    # COMO / POSU requirement
    st.markdown("#### COMO / POSU requirement (UMS only)")
    ums_posu_excluded = st.checkbox(
        "POSU is NOT required for this project (only COMO will be included).",
        key="ums_exclude_posu",
    )

    if ums_posu_excluded:
        st.info("Only COMO spec will be included for this UMS project. POSU will be excluded.")
    else:
        st.info("Default behavior: COMO and POSU specs will be included for this UMS project.")

# -------------------- UPSOLUT SECTION --------------------
if "UPSOLUT" in systems:

    system_banner("UPSOLUT")

    # LED type
    st.markdown("#### LED type")
    up_led = st.radio(
        "",
        ["Internal", "External"],
        horizontal=True,
        key="up_led",
    )

    # Installation type
    st.markdown("#### Installation type")
    up_install = st.radio(
        "",
        ["C-channel", "Embedded", "Conduit"],
        horizontal=False,
        key="up_install",
    )

    if up_install == "Embedded":
        st.markdown("#### Embedded installation type")
        up_embedded = st.radio(
            "",
            ["Direct ceiling", "Suspended"],
            horizontal=True,
            key="up_embedded",
        )

    if up_install == "Conduit":
        st.markdown("#### Conduit installation type")
        up_conduit = st.radio(
            "",
            ["Direct ceiling", "Suspended"],
            horizontal=True,
            key="up_conduit",
        )

st.divider()
st.caption("© PGS – internal UI prototype for visual review only.")
