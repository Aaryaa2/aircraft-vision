import streamlit as st
from PIL import Image
from modules.damage import analyze_damage
from modules.runway import analyze_runway
from modules.alignment import analyze_runway_alignment

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Aircraft Vision System",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# AEROSPACE UI THEME
# ============================================================

st.markdown("""
<style>

    /* ---------- MAIN BACKGROUND ---------- */

    .stApp {
        background:
            radial-gradient(
                circle at 85% 5%,
                rgba(37, 99, 235, 0.10),
                transparent 30%
            ),
            radial-gradient(
                circle at 10% 90%,
                rgba(14, 165, 233, 0.08),
                transparent 30%
            ),
            #f7f9fc;
    }

    /* ---------- SIDEBAR ---------- */

    section[data-testid="stSidebar"] {
        background:
            linear-gradient(
                180deg,
                #071426 0%,
                #0b1d35 55%,
                #071426 100%
            );
        border-right: 1px solid rgba(255,255,255,0.08);
    }

    section[data-testid="stSidebar"] * {
        color: #e8f1ff !important;
    }

    section[data-testid="stSidebar"] .stRadio label {
        border-radius: 10px;
        padding: 7px 10px;
        transition: all 0.2s ease;
    }

    section[data-testid="stSidebar"] .stRadio label:hover {
        background: rgba(59,130,246,0.14);
    }

    /* ---------- HEADINGS ---------- */

    h1 {
        font-weight: 800 !important;
        letter-spacing: -1.5px;
    }

    h2 {
        font-weight: 750 !important;
        letter-spacing: -0.8px;
    }

    h3 {
        font-weight: 700 !important;
    }

    /* ---------- METRIC CARDS ---------- */

    div[data-testid="stMetric"] {
        background: rgba(255,255,255,0.72);
        border: 1px solid rgba(148,163,184,0.22);
        border-radius: 16px;
        padding: 18px;
        box-shadow: 0 8px 25px rgba(15,23,42,0.05);
        backdrop-filter: blur(10px);
    }

    div[data-testid="stMetricLabel"] {
        font-size: 0.82rem;
    }

    /* ---------- BUTTONS ---------- */

    .stButton > button {
        border-radius: 12px;
        border: 1px solid rgba(37,99,235,0.25);
        font-weight: 650;
        transition: all 0.2s ease;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(37,99,235,0.18);
    }

    /* ---------- FILE UPLOADER ---------- */

    [data-testid="stFileUploader"] {
        border-radius: 16px;
    }

    /* ---------- TABS ---------- */

    button[data-baseweb="tab"] {
        font-weight: 650;
    }

    /* ---------- DATA TABLE ---------- */

    [data-testid="stDataFrame"] {
        border-radius: 14px;
        overflow: hidden;
    }

    /* ---------- DIVIDERS ---------- */

    hr {
        border-color: rgba(148,163,184,0.20);
    }

    /* ---------- GLASS CARD ---------- */

    .avi-card {
        background: rgba(255,255,255,0.78);
        border: 1px solid rgba(148,163,184,0.22);
        border-radius: 20px;
        padding: 25px;
        box-shadow: 0 12px 35px rgba(15,23,42,0.06);
        backdrop-filter: blur(12px);
        height: 100%;
    }

    .avi-card:hover {
        border-color: rgba(37,99,235,0.28);
        box-shadow: 0 16px 40px rgba(37,99,235,0.08);
    }

    /* ---------- STATUS ---------- */

    .status-pill {
        display: inline-block;
        padding: 7px 13px;
        border-radius: 999px;
        font-size: 0.78rem;
        font-weight: 700;
        background: rgba(16,185,129,0.10);
        color: #047857;
        border: 1px solid rgba(16,185,129,0.18);
    }

    /* ---------- HERO ---------- */

    .avi-hero {
        background:
            linear-gradient(
                135deg,
                #071426 0%,
                #0d2748 55%,
                #075985 100%
            );
        border-radius: 26px;
        padding: 42px;
        color: white;
        position: relative;
        overflow: hidden;
        box-shadow: 0 25px 60px rgba(7,20,38,0.20);
    }

    .avi-hero:after {
        content: "";
        position: absolute;
        width: 420px;
        height: 420px;
        right: -160px;
        top: -180px;
        border-radius: 50%;
        border: 1px solid rgba(125,211,252,0.18);
        box-shadow:
            0 0 0 45px rgba(125,211,252,0.04),
            0 0 0 90px rgba(125,211,252,0.025);
    }

    .avi-kicker {
        color: #7dd3fc;
        font-size: 0.78rem;
        font-weight: 800;
        letter-spacing: 2px;
        margin-bottom: 12px;
    }

    .avi-title {
        font-size: 3.1rem;
        font-weight: 850;
        line-height: 1.05;
        letter-spacing: -2px;
        margin-bottom: 15px;
    }

    .avi-subtitle {
        color: #cbdff5;
        font-size: 1.05rem;
        max-width: 720px;
        line-height: 1.65;
    }

    .avi-tag {
        display: inline-block;
        margin-top: 20px;
        margin-right: 8px;
        padding: 7px 12px;
        border-radius: 999px;
        background: rgba(255,255,255,0.08);
        border: 1px solid rgba(255,255,255,0.12);
        color: #e0f2fe;
        font-size: 0.76rem;
        font-weight: 650;
    }

    /* ---------- SMALL LABEL ---------- */

    .section-label {
        font-size: 0.75rem;
        font-weight: 800;
        letter-spacing: 1.6px;
        color: #64748b;
        text-transform: uppercase;
        margin-bottom: 7px;
    }

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

st.sidebar.title("✈️ Aircraft Vision")

st.sidebar.caption("Computer Vision Based Aircraft Analysis")

page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Home",
        "🛬 Landing Analysis",
        "🔧 Damage Inspection",
        "📊 Model Performance",
        "🧪 Failure Cases"
        
    ]
)

st.sidebar.divider()

st.sidebar.caption(
    "CA-3 Vision-Based Application"
)

# --------------------------------------------------
# HOME
# --------------------------------------------------

if page == "🏠 Home":

    # =========================================================
    # HERO
    # =========================================================

    st.html("""
    <div class="avi-hero">

        <div class="avi-kicker">
            AIRCRAFT VISION // CV-CA3
        </div>

        <div class="avi-title">
            See the runway.<br>
            See the damage.
        </div>

        <div class="avi-subtitle">
            A computer-vision based aircraft assessment system
            combining runway detection, landing alignment analysis,
            and aircraft surface damage detection into one unified
            visual intelligence platform.
        </div>

        <div>
            <span class="avi-tag">YOLO</span>
            <span class="avi-tag">Computer Vision</span>
            <span class="avi-tag">Runway Analysis</span>
            <span class="avi-tag">Aircraft Inspection</span>
        </div>

    </div>
    """)

    st.write("")


    # =========================================================
    # SYSTEM STATUS
    # =========================================================

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Vision Modules",
            "2"
        )

    with col2:
        st.metric(
            "Detection Models",
            "2"
        )

    with col3:
        st.metric(
            "Runway FPS",
            "60.99"
        )

    with col4:
        st.html("""
        <div class="status-pill">
            ● SYSTEM READY
        </div>
        """)

    st.write("")
    st.divider()


    # =========================================================
    # TWO CORE MODULES
    # =========================================================

    st.html("""
    <div class="section-label">
        CORE VISION MODULES
    </div>
    """)

    st.header(
        "Aircraft intelligence, split into two missions"
    )

    col1, col2 = st.columns(2)

    with col1:

        st.html("""
        <div class="avi-card">

            <div style="font-size:2.3rem;">
                🛬
            </div>

            <h2>Landing Analysis</h2>

            <p style="color:#64748b; line-height:1.6;">
                Detect the runway from an approach image and
                evaluate runway alignment using geometric analysis.
            </p>

            <hr>

            <b>Pipeline</b>

            <p style="color:#475569;">
                YOLO Runway Detection
                → Geometry Extraction
                → Alignment Assessment
                → Landing Zone
            </p>

            <div>

                <span class="avi-tag"
                      style="background:#eff6ff;color:#1d4ed8;">
                    RUNWAY
                </span>

                <span class="avi-tag"
                      style="background:#ecfeff;color:#0e7490;">
                    ALIGNMENT
                </span>

            </div>

        </div>
        """)

    with col2:

        st.html("""
        <div class="avi-card">

            <div style="font-size:2.3rem;">
                🔧
            </div>

            <h2>Aircraft Inspection</h2>

            <p style="color:#64748b; line-height:1.6;">
                Detect visible aircraft surface defects and
                identify their location and confidence.
            </p>

            <hr>

            <b>Pipeline</b>

            <p style="color:#475569;">
                Aircraft Image
                → YOLO Damage Detection
                → Defect Classification
                → Bounding Boxes
            </p>

            <div>

                <span class="avi-tag"
                      style="background:#eff6ff;color:#1d4ed8;">
                    CRACK
                </span>

                <span class="avi-tag"
                      style="background:#eff6ff;color:#1d4ed8;">
                    DENT
                </span>

                <span class="avi-tag"
                      style="background:#ecfeff;color:#0e7490;">
                    CORROSION
                </span>

            </div>

        </div>
        """)

    st.write("")
    st.divider()


    # =========================================================
    # ARCHITECTURE
    # =========================================================

    st.html("""
    <div class="section-label">
        SYSTEM ARCHITECTURE
    </div>
    """)

    st.header(
        "One interface. Two specialized vision pipelines."
    )

    st.html("""
    <div class="avi-card">

        <div style="
            display:flex;
            align-items:center;
            justify-content:space-between;
            gap:15px;
            flex-wrap:wrap;
        ">

            <div>

                <div style="
                    font-size:0.75rem;
                    color:#64748b;
                ">
                    INPUT
                </div>

                <div style="
                    font-size:1.15rem;
                    font-weight:750;
                ">
                    Aircraft Image
                </div>

            </div>


            <div style="
                font-size:1.5rem;
                color:#38bdf8;
            ">
                →
            </div>


            <div>

                <div style="
                    font-size:0.75rem;
                    color:#64748b;
                ">
                    VISION
                </div>

                <div style="
                    font-size:1.15rem;
                    font-weight:750;
                ">
                    YOLO Detection
                </div>

            </div>


            <div style="
                font-size:1.5rem;
                color:#38bdf8;
            ">
                →
            </div>


            <div>

                <div style="
                    font-size:0.75rem;
                    color:#64748b;
                ">
                    ANALYSIS
                </div>

                <div style="
                    font-size:1.15rem;
                    font-weight:750;
                ">
                    Geometry / Defects
                </div>

            </div>


            <div style="
                font-size:1.5rem;
                color:#38bdf8;
            ">
                →
            </div>


            <div>

                <div style="
                    font-size:0.75rem;
                    color:#64748b;
                ">
                    OUTPUT
                </div>

                <div style="
                    font-size:1.15rem;
                    font-weight:750;
                ">
                    Visual Assessment
                </div>

            </div>

        </div>

    </div>
    """)

    st.write("")
    st.divider()


    # =========================================================
    # MODEL SNAPSHOT
    # =========================================================

    st.html("""
    <div class="section-label">
        MODEL SNAPSHOT
    </div>
    """)

    st.header(
        "Experimental performance"
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Runway mAP@50",
            "70.85%"
        )

    with col2:
        st.metric(
            "Runway Recall",
            "76.67%"
        )

    with col3:
        st.metric(
            "Damage mAP@50",
            "24.4%"
        )

    with col4:
        st.metric(
            "Runway FPS",
            "60.99"
        )

    st.write("")


    # =========================================================
    # FOOTER
    # =========================================================

    st.html("""
    <div style="
        text-align:center;
        padding:35px 10px 10px;
        color:#94a3b8;
        font-size:0.78rem;
    ">

        AIRCRAFT VISION · COMPUTER VISION BASED AIRCRAFT ANALYSIS

        <br>

        CA-3 Vision-Based Application

    </div>
    """)

# --------------------------------------------------
# LANDING ANALYSIS
# --------------------------------------------------

elif page == "🛬 Landing Analysis":

    st.title("🛬 Landing & Runway Analysis")

    st.write(
        """
        Upload an aircraft approach/runway image to perform
        runway detection, alignment assessment, and landing-zone analysis.
        """
    )

    st.divider()

    uploaded_file = st.file_uploader(
        "Upload Landing / Runway Image",
        type=["jpg", "jpeg", "png"],
        key="landing_upload"
    )

    if uploaded_file is not None:

        image = Image.open(uploaded_file)

        # ==================================================
        # ANALYZE BUTTON
        # ==================================================

        if st.button(
            "🛬 Analyze Landing",
            use_container_width=True,
            key="analyze_landing"
        ):

            # --------------------------------------------------
            # MEMBER 1: RUNWAY DETECTION
            # --------------------------------------------------

            runway_result = analyze_runway(image)

            if runway_result["runway_detected"]:

                detection = runway_result["detections"][0]

                # --------------------------------------------------
                # MEMBER 2: ALIGNMENT ANALYSIS
                # --------------------------------------------------

                alignment = analyze_runway_alignment(
                    image,
                    detection
                )

                # ==================================================
                # IMAGE COMPARISON
                # ==================================================

                st.subheader("🖼️ Vision Analysis")

                image_col1, image_col2 = st.columns(2)

                with image_col1:

                    st.markdown(
                        "**Original Image**"
                    )

                    st.image(
                        image,
                        use_container_width=True
                    )

                with image_col2:

                    st.markdown(
                        "**Runway Detection Result**"
                    )

                    st.image(
                        runway_result["annotated_image"],
                        use_container_width=True
                    )

                st.divider()

                # ==================================================
                # DETECTION RESULTS
                # ==================================================

                st.subheader("📊 Analysis Results")

                metric1, metric2, metric3, metric4 = st.columns(4)

                with metric1:

                    st.metric(
                        "Runway Confidence",
                        f"{detection['confidence'] * 100:.1f}%"
                    )

                with metric2:

                    st.metric(
                        "Lateral Deviation",
                        f"{alignment['lateral_deviation_normalized'] * 100:.2f}%"
                    )

                with metric3:

                    st.metric(
                        "Angular Deviation",
                        f"{alignment['angular_deviation']:.1f}°"
                    )

                with metric4:

                    status = alignment["alignment_status"]

                    if status == "GOOD":
                        status_text = "🟢 GOOD"

                    elif status == "MINOR DEVIATION":
                        status_text = "🟡 MINOR"

                    else:
                        status_text = "🔴 MISALIGNED"

                    st.metric(
                        "Alignment Status",
                        status_text
                    )

                st.write("")

                # ==================================================
                # TECHNICAL DETAILS
                # ==================================================

                detail1, detail2 = st.columns(2)

                with detail1:

                    st.markdown("### 📦 Bounding Box")

                    st.code(
                        str(detection["bbox"]),
                        language="text"
                    )

                with detail2:

                    st.markdown("### 📐 Geometry Source")

                    st.info(
                        alignment["geometry_source"]
                    )

                st.divider()

                # ==================================================
                # LANDING ZONE
                # ==================================================

                st.subheader("🛬 Landing Zone Assessment")

                landing_col1, landing_col2 = st.columns(2)

                landing_zone = alignment["landing_zone"]

                with landing_col1:

                    st.markdown(
                        "**Zone Type**"
                    )

                    st.info(
                        landing_zone["type"]
                    )

                with landing_col2:

                    st.markdown(
                        "**Assessment Region**"
                    )

                    st.info(
                        landing_zone["description"]
                    )

                st.divider()

                # ==================================================
                # FINAL ALIGNMENT VISUALIZATION
                # ==================================================

                st.subheader("🛰️ Alignment Visualization")

                st.image(
                    alignment["annotated_image"],
                    use_container_width=True
                )

            else:

                # ==================================================
                # NO RUNWAY DETECTED
                # ==================================================

                st.error(
                    "❌ No runway detected. "
                    "Please upload another runway image."
                )

# --------------------------------------------------
# DAMAGE INSPECTION
# --------------------------------------------------

elif page == "🔧 Damage Inspection":

    st.title("🔧 Aircraft Damage Inspection")

    st.write(
        "Upload an aircraft image to detect surface defects "
        "such as cracks, dents, and corrosion."
    )

    st.divider()

    uploaded_file = st.file_uploader(
        "Upload Aircraft Image",
        type=["jpg", "jpeg", "png"],
        key="damage_upload"
    )

    if uploaded_file is not None:

        image = Image.open(uploaded_file)

        # ==================================================
        # ANALYZE BUTTON
        # ==================================================

        if st.button(
            "🔍 Analyze Damage",
            use_container_width=True,
            key="analyze_damage"
        ):

            with st.spinner("Analyzing aircraft surface..."):

                result = analyze_damage(image)

            # ==================================================
            # IMAGE COMPARISON
            # ==================================================

            st.subheader("🖼️ Vision Analysis")

            image_col1, image_col2 = st.columns(2)

            with image_col1:

                st.markdown("**Original Aircraft Image**")

                st.image(
                    image,
                    use_container_width=True
                )

            with image_col2:

                st.markdown("**Damage Detection Result**")

                st.image(
                    result["annotated_image"],
                    channels="RGB",
                    use_container_width=True
                )

            st.success("✅ Analysis completed!")

            st.divider()

            # ==================================================
            # DAMAGE SUMMARY
            # ==================================================

            st.subheader("📊 Damage Summary")

            col1, col2, col3, col4 = st.columns(4)

            with col1:

                st.metric(
                    "Total Defects",
                    result["total_defects"]
                )

            with col2:

                st.metric(
                    "Cracks",
                    result["counts"]["crack"]
                )

            with col3:

                st.metric(
                    "Dents",
                    result["counts"]["dent"]
                )

            with col4:

                st.metric(
                    "Corrosion",
                    result["counts"]["corrosion"]
                )

            st.divider()

            # ==================================================
            # DETECTION DETAILS
            # ==================================================

            st.subheader("🔎 Detection Details")

            if result["detections"]:

                # Create horizontal columns for detections
                detection_columns = st.columns(
                    min(len(result["detections"]), 4)
                )

                for i, detection in enumerate(
                    result["detections"]
                ):

                    with detection_columns[
                        i % len(detection_columns)
                    ]:

                        st.html(
                            f"""
                            <div class="avi-card">

                                <h4>
                                    {detection["class"].title()}
                                </h4>

                                <p>
                                    Confidence:
                                    <strong>
                                        {detection["confidence"] * 100:.1f}%
                                    </strong>
                                </p>

                                <p>
                                    Bounding Box:
                                    <code>
                                        {detection["bbox"]}
                                    </code>
                                </p>

                            </div>
                            """,
                            
                        )

            else:

                st.info(
                    "No surface defects detected."
                )


# --------------------------------------------------
# MODEL PERFORMANCE
# --------------------------------------------------

elif page == "📊 Model Performance":

    st.title("📊 Model Performance")

    st.write(
        """
        Experimental evaluation of the computer vision models
        used in the Aircraft Vision System.
        """
    )

    st.divider()

    runway_tab, damage_tab = st.tabs(
        ["🛬 Runway Detection", "🔧 Damage Detection"]
    )

    # ==================================================
    # RUNWAY DETECTION
    # ==================================================

    with runway_tab:

        st.subheader("🛬 Runway Detection Model")

        st.write(
            """
            Final YOLO-based runway detection model evaluated
            on the held-out LARD_V2 test set.
            """
        )

        # ==================================================
        # MODEL SNAPSHOT
        # ==================================================

        st.markdown(
            '<div class="section-label">MODEL SNAPSHOT</div>',
            unsafe_allow_html=True
        )

        st.html(
            """
            <div style="
                display:grid;
                grid-template-columns:repeat(4,1fr);
                gap:14px;
                margin:12px 0 24px 0;
            ">

                <div class="avi-card">
                    <div style="font-size:12px;opacity:.65;">
                        MODEL
                    </div>
                    <div style="
                        font-size:22px;
                        font-weight:750;
                        margin-top:6px;
                    ">
                        YOLOv8n
                    </div>
                </div>

                <div class="avi-card">
                    <div style="font-size:12px;opacity:.65;">
                        INPUT SIZE
                    </div>
                    <div style="
                        font-size:22px;
                        font-weight:750;
                        margin-top:6px;
                    ">
                        640 × 640
                    </div>
                </div>

                <div class="avi-card">
                    <div style="font-size:12px;opacity:.65;">
                        TEST IMAGES
                    </div>
                    <div style="
                        font-size:22px;
                        font-weight:750;
                        margin-top:6px;
                    ">
                        3000
                    </div>
                </div>

                <div class="avi-card">
                    <div style="font-size:12px;opacity:.65;">
                        CLASSES
                    </div>
                    <div style="
                        font-size:22px;
                        font-weight:750;
                        margin-top:6px;
                    ">
                        1
                    </div>
                </div>

            </div>
            """
        )

        # ==================================================
        # PERFORMANCE
        # ==================================================

        st.markdown(
            '<div class="section-label">DETECTION PERFORMANCE</div>',
            unsafe_allow_html=True
        )

        st.html(
            """
            <div style="
                display:grid;
                grid-template-columns:repeat(4,1fr);
                gap:14px;
                margin:12px 0 14px 0;
            ">

                <div class="avi-card">
                    <div style="font-size:12px;opacity:.65;">
                        PRECISION
                    </div>
                    <div style="
                        font-size:27px;
                        font-weight:800;
                        margin-top:5px;
                    ">
                        74.55%
                    </div>
                </div>

                <div class="avi-card">
                    <div style="font-size:12px;opacity:.65;">
                        RECALL
                    </div>
                    <div style="
                        font-size:27px;
                        font-weight:800;
                        margin-top:5px;
                    ">
                        76.67%
                    </div>
                </div>

                <div class="avi-card">
                    <div style="font-size:12px;opacity:.65;">
                        mAP@50
                    </div>
                    <div style="
                        font-size:27px;
                        font-weight:800;
                        margin-top:5px;
                    ">
                        70.85%
                    </div>
                </div>

                <div class="avi-card">
                    <div style="font-size:12px;opacity:.65;">
                        FPS
                    </div>
                    <div style="
                        font-size:27px;
                        font-weight:800;
                        margin-top:5px;
                    ">
                        60.99
                    </div>
                </div>

            </div>

            <div style="
                display:grid;
                grid-template-columns:repeat(3,1fr);
                gap:14px;
                margin:0 0 24px 0;
            ">

                <div class="avi-card">
                    <div style="font-size:12px;opacity:.65;">
                        F1 SCORE
                    </div>
                    <div style="
                        font-size:25px;
                        font-weight:800;
                        margin-top:5px;
                    ">
                        75.60%
                    </div>
                </div>

                <div class="avi-card">
                    <div style="font-size:12px;opacity:.65;">
                        mAP@50:95
                    </div>
                    <div style="
                        font-size:25px;
                        font-weight:800;
                        margin-top:5px;
                    ">
                        35.26%
                    </div>
                </div>

                <div class="avi-card">
                    <div style="font-size:12px;opacity:.65;">
                        INFERENCE TIME
                    </div>
                    <div style="
                        font-size:25px;
                        font-weight:800;
                        margin-top:5px;
                    ">
                        16.4 ms
                    </div>
                </div>

            </div>
            """
        )

        # ==================================================
        # RUNWAY SUMMARY
        # ==================================================

        st.markdown(
            '<div class="section-label">EVALUATION SUMMARY</div>',
            unsafe_allow_html=True
        )

        st.subheader("📋 Runway Model Summary")

        runway_data = {
            "Metric": [
                "Precision",
                "Recall",
                "F1 Score",
                "mAP@50",
                "mAP@50:95",
                "Inference Time",
                "FPS"
            ],
            "Result": [
                "74.55%",
                "76.67%",
                "75.60%",
                "70.85%",
                "35.26%",
                "16.4 ms/image",
                "60.99"
            ]
        }

        st.table(runway_data)

        st.divider()

        # ==================================================
        # ALIGNMENT
        # ==================================================

        st.markdown(
            '<div class="section-label">POST-DETECTION ANALYSIS</div>',
            unsafe_allow_html=True
        )

        st.subheader("📐 Runway Alignment Assessment")

        st.write(
            """
            Runway alignment is a geometry-based assessment applied
            after runway detection. It is not evaluated using mAP,
            because it is not a separately trained detection model.
            """
        )

        st.html(
            """
            <div style="
                display:grid;
                grid-template-columns:repeat(3,1fr);
                gap:14px;
                margin:12px 0 18px 0;
            ">

                <div class="avi-card">
                    <div style="font-size:12px;opacity:.65;">
                        LATERAL GOOD THRESHOLD
                    </div>
                    <div style="
                        font-size:26px;
                        font-weight:800;
                        margin-top:5px;
                    ">
                        ≤ 15%
                    </div>
                </div>

                <div class="avi-card">
                    <div style="font-size:12px;opacity:.65;">
                        ANGULAR GOOD THRESHOLD
                    </div>
                    <div style="
                        font-size:26px;
                        font-weight:800;
                        margin-top:5px;
                    ">
                        ≤ 5°
                    </div>
                </div>

                <div class="avi-card">
                    <div style="font-size:12px;opacity:.65;">
                        LANDING ZONE
                    </div>
                    <div style="
                        font-size:26px;
                        font-weight:800;
                        margin-top:5px;
                    ">
                        35% – 65%
                    </div>
                </div>

            </div>
            """
        )

        st.info(
            """
            The alignment module uses the detected runway bounding box
            and geometry processing to estimate lateral deviation,
            angular deviation, alignment status, and a project-defined
            central landing-assessment zone.
            """
        )

    # ==================================================
    # DAMAGE DETECTION
    # ==================================================

    with damage_tab:

        st.subheader("🔧 Aircraft Damage Detection Model")

        st.write(
            """
            Final YOLO-based aircraft surface damage detector
            evaluated on the held-out test set.
            """
        )

        # ==================================================
        # MODEL SNAPSHOT
        # ==================================================

        st.markdown(
            '<div class="section-label">MODEL SNAPSHOT</div>',
            unsafe_allow_html=True
        )

        st.html(
            """
            <div style="
                display:grid;
                grid-template-columns:repeat(4,1fr);
                gap:14px;
                margin:12px 0 24px 0;
            ">

                <div class="avi-card">
                    <div style="font-size:12px;opacity:.65;">
                        MODEL
                    </div>
                    <div style="
                        font-size:22px;
                        font-weight:750;
                        margin-top:6px;
                    ">
                        YOLOv8s
                    </div>
                </div>

                <div class="avi-card">
                    <div style="font-size:12px;opacity:.65;">
                        INPUT SIZE
                    </div>
                    <div style="
                        font-size:22px;
                        font-weight:750;
                        margin-top:6px;
                    ">
                        640 × 640
                    </div>
                </div>

                <div class="avi-card">
                    <div style="font-size:12px;opacity:.65;">
                        TEST IMAGES
                    </div>
                    <div style="
                        font-size:22px;
                        font-weight:750;
                        margin-top:6px;
                    ">
                        169
                    </div>
                </div>

                <div class="avi-card">
                    <div style="font-size:12px;opacity:.65;">
                        DAMAGE CLASSES
                    </div>
                    <div style="
                        font-size:22px;
                        font-weight:750;
                        margin-top:6px;
                    ">
                        3
                    </div>
                </div>

            </div>
            """
        )

        st.caption(
            "Classes: Corrosion • Crack • Dent"
        )

        # ==================================================
        # OVERALL PERFORMANCE
        # ==================================================

        st.markdown(
            '<div class="section-label">OVERALL PERFORMANCE</div>',
            unsafe_allow_html=True
        )

        st.html(
            """
            <div style="
                display:grid;
                grid-template-columns:repeat(4,1fr);
                gap:14px;
                margin:12px 0 14px 0;
            ">

                <div class="avi-card">
                    <div style="font-size:12px;opacity:.65;">
                        PRECISION
                    </div>
                    <div style="
                        font-size:27px;
                        font-weight:800;
                        margin-top:5px;
                    ">
                        41.9%
                    </div>
                </div>

                <div class="avi-card">
                    <div style="font-size:12px;opacity:.65;">
                        RECALL
                    </div>
                    <div style="
                        font-size:27px;
                        font-weight:800;
                        margin-top:5px;
                    ">
                        22.1%
                    </div>
                </div>

                <div class="avi-card">
                    <div style="font-size:12px;opacity:.65;">
                        mAP@50
                    </div>
                    <div style="
                        font-size:27px;
                        font-weight:800;
                        margin-top:5px;
                    ">
                        24.4%
                    </div>
                </div>

                <div class="avi-card">
                    <div style="font-size:12px;opacity:.65;">
                        mAP@50:95
                    </div>
                    <div style="
                        font-size:27px;
                        font-weight:800;
                        margin-top:5px;
                    ">
                        11.2%
                    </div>
                </div>

            </div>

            <div style="
                display:grid;
                grid-template-columns:repeat(2,1fr);
                gap:14px;
                margin:0 0 24px 0;
            ">

                <div class="avi-card">
                    <div style="font-size:12px;opacity:.65;">
                        TEST INSTANCES
                    </div>
                    <div style="
                        font-size:25px;
                        font-weight:800;
                        margin-top:5px;
                    ">
                        358
                    </div>
                </div>

                <div class="avi-card">
                    <div style="font-size:12px;opacity:.65;">
                        INFERENCE TIME
                    </div>
                    <div style="
                        font-size:25px;
                        font-weight:800;
                        margin-top:5px;
                    ">
                        6.4 ms/image
                    </div>
                </div>

            </div>
            """
        )

        # ==================================================
        # PER CLASS
        # ==================================================

        st.markdown(
            '<div class="section-label">CLASS-LEVEL EVALUATION</div>',
            unsafe_allow_html=True
        )

        st.subheader("🔍 Per-Class Performance")

        damage_data = {
            "Class": [
                "Corrosion",
                "Crack",
                "Dent"
            ],
            "Precision": [
                "0.0%",
                "78.8%",
                "47.1%"
            ],
            "Recall": [
                "0.0%",
                "53.7%",
                "12.5%"
            ],
            "mAP@50": [
                "0.64%",
                "61.2%",
                "11.4%"
            ],
            "mAP@50:95": [
                "0.20%",
                "28.5%",
                "4.85%"
            ]
        }

        st.table(damage_data)

        st.divider()

        # ==================================================
        # OBSERVATIONS
        # ==================================================

        st.markdown(
            '<div class="section-label">EVALUATION OBSERVATIONS</div>',
            unsafe_allow_html=True
        )

        st.subheader("🧠 Model Observations")

        col1, col2, col3 = st.columns(3)

        with col1:

            st.info(
                """
                **🔎 Crack Detection**

                The model achieved the highest performance
                for crack detection, with **61.2% mAP@50**.
                """
            )

        with col2:

            st.info(
                """
                **🔧 Dent Detection**

                Dent detection showed lower recall and mAP
                compared with crack detection.
                """
            )

        with col3:

            st.info(
                """
                **⚠️ Corrosion Detection**

                Corrosion detection was very weak in the
                held-out test set.
                """
            )

        st.divider()
        


# --------------------------------------------------
# FAILURE CASES
# --------------------------------------------------

elif page == "🧪 Failure Cases":

    st.title("🧪 Failure & Challenging Cases")

    st.write(
        """
        Real examples demonstrating challenging visual conditions
        and limitations encountered by the aircraft vision models.
        """
    )

    st.divider()

    # ==================================================
    # RUNWAY CASE
    # ==================================================

    st.subheader("🛬 Runway Detection")

    runway_col1, runway_col2 = st.columns(2)

    with runway_col1:

        st.markdown("**Challenging Runway Scene**")

        st.image(
            "results/failure_cases/runway_challenging.jpg",
            use_container_width=True
        )

    with runway_col2:

        st.markdown("### ⚠️ Challenging Case")

        st.write(
            """
            This aerial scene contains a large amount of surrounding
            terrain and visual information, making runway localization
            more challenging for the vision system.
            """
        )

        st.markdown("**Why it is challenging:**")

        st.write(
            """
            • Large background region  
            • Complex terrain and ground structures  
            • Runway occupies a relatively small region  
            • Multiple visual patterns can resemble runway surfaces
            """
        )

        st.info(
            """
            **Limitation:** Performance can vary when the runway is
            distant, occupies a small portion of the image, or is
            surrounded by visually complex terrain.
            """
        )

    st.divider()

    # ==================================================
    # DAMAGE CASE
    # ==================================================

    st.subheader("🔧 Aircraft Damage Detection")

    damage_col1, damage_col2 = st.columns(2)

    with damage_col1:

        st.markdown("**Corrosion Missed by Model**")

        st.image(
            "results/failure_cases/corrosion_missed.png",
            use_container_width=True
        )

    with damage_col2:

        st.markdown("### ❌ Corrosion Not Detected")

        st.write(
            """
            Corrosion is visibly present on the aircraft surface,
            but the damage detection model did not identify it.
            """
        )

        st.markdown("**Why it is challenging:**")

        st.write(
            """
            • Corrosion regions can be small and localized  
            • Surface texture can resemble surrounding aircraft material  
            • Low visual contrast makes detection difficult  
            • Damage appearance can vary significantly
            """
        )

        st.warning(
            """
            **Observed limitation:** Corrosion detection showed very
            weak performance on the held-out test set, indicating that
            this damage class remains challenging for the experimental
            model.
            """
        )

    st.divider()

  