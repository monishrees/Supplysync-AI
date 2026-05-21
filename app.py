import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import io
import numpy as np
from utils.html_table import render_html_table
import streamlit as st
import altair as alt
from streamlit_option_menu import option_menu
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import sqlite3
import time

st.set_page_config(
    page_title="SupplySyncAI",
    layout="wide"
)

st.markdown("""
<style>
div[data-testid="stAlert"] {
    color: #000000 !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>

/* App background */
.stApp {
    background-color: #EDEDED;
    margin: 0;
    padding: 0;
}

/* Remove top spacing completely */
.block-container {
    padding-top: 0rem !important;
    margin-top: -5.5rem !important;
}

/* keep app background */
.main {
    background-color: #f0f2f6 !important;
}

/* Remove main section spacing */
section.main > div:first-child {
    padding-top: 0rem !important;
    margin-top: 0rem !important;
}
            
/* Remove extra container padding */
[data-testid="stAppViewContainer"] {
    padding-top: 0rem !important;
    margin-top: 0rem !important;
}

/*  REMOVE TOP GAP COMPLETELY */
[data-testid="stAppViewContainer"] {
    padding-top: 0rem !important;
    margin-top: 0rem !important;
}

/*  REMOVE TOP SPACER DIV */
[data-testid="stAppViewContainer"] > div:first-child {
    margin-top: 0rem !important;
    padding-top: 0rem !important;
} 
              
/* Header fix */
header[data-testid="stHeader"] {
    position: relative;
    background-color: #EDEDED !important;
}
            
header[data-testid="stHeader"] * {
    color: #000000 !important;
}

</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>

/* Block container — single source of truth */
.block-container {
    padding-left: 1rem !important;
    padding-right: 1rem !important;
    max-width: 100% !important;
    overflow-x: hidden !important;
}

section.main > div {
    padding-left: 0rem !important;
    padding-right: 0rem !important;
    max-width: 100% !important;
    overflow-x: hidden !important;
}

[data-testid="stAppViewContainer"] {
    padding-left: 0rem !important;
    padding-right: 0rem !important;
    overflow-x: hidden !important;
}

</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>

/* =========================================
   RADIO CONTAINER – FULL WIDTH
   ========================================= */
div.element-container:has(div.stRadio) {
    width: 100% !important;
}

/* =========================================
   Teal WRAP BOX – FULL PAGE WIDTH
   ========================================= */
div.stRadio > div {
    background-color:  #00D05E;
    padding: 16px 0px;
    border-radius: 8px;
    width: 100%;
    box-sizing: border-box;
    display: flex;
    justify-content: center;
}

/* =========================================
   RADIO GROUP ALIGNMENT
   ========================================= */
div[data-baseweb="radio-group"] {
    display: flex !important;
    justify-content: center !important;
    align-items: center;
    gap: 50px;
    width: 100%;
    margin: 0 auto;
}
            
div[data-baseweb="radio"] {
    display: flex;
    align-items: center;
    justify-content: center;
}

/* =========================================
   RADIO OPTION TEXT
   ========================================= */
/* RADIO LABEL TEXT – FORCE WHITE */
div[data-baseweb="radio"] label,
div[data-baseweb="radio"] label span {
    font-size: 18px !important;
    font-weight: 800 !important;
    color: #FFFFFF !important;
    white-space: nowrap;
}


/* =========================================
   SPACE BETWEEN OPTIONS
   ========================================= */
div[data-baseweb="radio"] {
    margin-right: 28px;
}

          

</style>
""", unsafe_allow_html=True)

st.markdown(""" 
 <style> /* Expander outer card */ 
    div[data-testid="stExpander"]
        { background-color: #2F75B5;
        border-radius: 20px; 
        border: 1px solid #9EDAD0; 
        overflow: hidden; /* 🔑 fixes unfinished edges */ }
    /* Hide expander header completely */
    div[data-testid="stExpander"]:nth-of-type(1)
             summary { display: none; }
    /* Inner content padding fix */
     div[data-testid="stExpander"]:nth-of-type(1) > 
            div { padding: 22px 18px; } 
            </style> """, unsafe_allow_html=True)


st.markdown(
    """
    <style>
        /* Dark blue themed button */
        div.stButton > button {
            background-color: #0B2C5D;   /* Dark blue from your header */
            color: #FFFFFF;
            border-radius: 8px;
            padding: 8px 18px;
            border: none;
            font-weight: 600;
        }

        div.stButton > button:hover {
            background-color: #08306B;   /* Slightly darker on hover */
            color: #FFFFFF;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("""
<style>

/* =========================================
   SUMMARY GRID (CENTERED, SMALL, EQUAL BOXES)
   ========================================= */
.summary-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 14px;
    margin: 6px 0 10px 0;
    justify-content: center;
    
}

/* =========================================
   SUMMARY CARD (TABLE CONTAINER)
   ========================================= */
.summary-card {
    border: 2px solid #6B7280;
    border-radius: 2px;
    background-color: #F8FAFC;
    overflow: hidden;
    text-align: center;
}

/* =========================================
   HEADER ROW (NO WRAP, SAME HEIGHT)
   ========================================= */
.summary-title {
    background-color:#1F3A5F;
    color: #ffffff;
    font-size: 14px;
    font-weight: 700;
    padding: 8px 6px;
    border-bottom: 1px solid #6B7280;

    white-space: nowrap;       /* 🔥 stop wrapping */
    overflow: hidden;
    text-overflow: ellipsis;
}

/* =========================================
   VALUE CELL (COMPACT)
   ========================================= */
.summary-value {
    font-size: 22px;
    font-weight: 600;
    color: #000000;
    padding: 1px 0;
}

</style>
""", unsafe_allow_html=True)


st.markdown(
    """
    <div style="
        background-color:#0B2C5D;
        padding:35px;
        border-radius:12px;
        color:white;
        text-align:center;
        margin:0 0 20px 0;
    ">
        <h1 style="margin:0 0 8px 0;">
            SupplySync.AI Autonomous Inventory Intelligence & Demand-Driven Retail Execution Platform
        </h1>
        <h3 style="font-weight:400; margin:0;">
            From Reactive Ordering to Autonomous Supply Intelligence
        </h3>
        <p style="font-size:17px; margin-top:15px;">
            Automatically replenish inventory using real-time demand signals, lead times, and supplier dynamics.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div style="
        background-color:#2F75B5;
        padding:28px;
        border-radius:12px;
        color:white;
        font-size:16px;
        line-height:1.6;
        margin-bottom:25px;
    ">

    <p>
    This application delivers an end-to-end <b>AI-powered demand forecasting and predictive 
    replenishment platform </b> by integrating sales transactions, inventory data, supplier 
    lead times, promotions, events, and operational signals into a unified intelligent system.
    </p>

    <p>
    Unlike traditional retail systems that rely on manual restocking and high-level forecasts, 
    this platform operates at a <b>granular SKU × Store × Time level</b>, enabling precise demand prediction 
    and automated replenishment decisions.
    It not only forecasts demand but also acts on it—triggering intelligent auto-procurement, optimizing 
    reorder quantities, and ensuring continuous product availability across the supply chain.
    </p>

    <h4 style="margin-top:22px;">Why This Matters</h4>
    
    <p>
    Retail operations are influenced by dynamic, real-world factors that go beyond historical sales. 
    This application captures and responds to:
    </p>

    <ul>
        <li>Demand patterns and seasonality trends</li>
        <li>Supplier lead times and delivery reliability</li>
        <li>Promotion and event-driven demand fluctuations</li>
        <li>Inventory levels and stock health</li>
        <li>Real-time consumption and sales velocity</li>
    </ul>

    <p style="margin-top:15px;">
        <b>The result:</b> More accurate forecasts, reduced stockouts,
        optimizing inventory, and improved profitability.
    </p>

    </div>
    """,
    unsafe_allow_html=True
)



# CENTERED SMALL PLOT FUNCTION
def show_small_plot(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=120, bbox_inches="tight")
    buf.seek(0)

    st.markdown("<div style='text-align:center;'>", unsafe_allow_html=True)
    st.image(buf, width=480)  # Half screen
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown(
    """
    <div style="
        background-color:#0B2C5D;
        padding:18px 25px;
        border-radius:10px;
        color:white;
        margin-top:20px;
        margin-bottom:10px;
    ">
        <h3 style="margin:0;">
            Data Collection & Integration (Unified Data Ingestion)
        </h3>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div style="
        background-color:#2F75B5;
        padding:28px;
        border-radius:12px;
        color:white;
        font-size:16px;
        line-height:1.6;
        margin-bottom:20px;
    ">

    <p>
    This section consolidates data from multiple enterprise sources into a single analytical model.
    </p>

    <b>Integrated Data Domains:</b>
    <ul>
        <li>Real-time stock monitoring</li>
        <li>Supplier & ERP integration</li>
        <li>Service Level Agreement (SLA) tracking and alerts</li>
        <li>Promotions & events</li>
        <li>SKU-level optimization</li>
        <li>AI-based auto-reorder triggers</li>
    </ul>

    <p>
    All data is validated and aligned using a <b>consistent dimensional model</b>
    to ensure forecasting accuracy.
    </p>

    </div>
    """,
    unsafe_allow_html=True
)

@st.cache_data
def load_data():

    conn = sqlite3.connect("database.db")

    query = "SELECT * FROM fdm_1500"

    df = pd.read_sql(query, conn)

    conn.close()

    return df

# Session state
if "df" not in st.session_state:
    st.session_state.df = None

# Button to load data
if st.button("Load Data", key="load_database_button"):

    start_time = time.time()

    st.session_state.df = load_data()

    end_time = time.time()

    load_time = round(end_time - start_time, 2)

    st.success(f"Database loaded successfully in {load_time} seconds")

df = st.session_state.df

if df is not None:

    st.markdown(f"""
        <div style="
            background-color:#0B2C5D;
            padding:15px 18px;
            border-radius:10px;
            color:white;
            margin-top:8px;
            margin-bottom:8px;    
        ">
            <h4 style="margin:0;">
                Data Preview 
            </h4>
        </div>
        """, unsafe_allow_html=True)

    render_html_table(
        df.head(20),
        max_height=260
    )

    st.markdown(f"""
        <div style="
            background-color:#2F75B5;
            padding:16px;
            border-radius:12px;
            color:white;
            font-size:16px;
            line-height:1.7;
            margin-bottom:20px;
        ">

        <p style='font-weight:600;'>
            Shape: {df.shape[0]} rows × {df.shape[1]} columns
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )

else:

    st.markdown(
        "<p style='color:#000000;'>Click the button above to load the dataset.</p>",
        unsafe_allow_html=True
    )
    
# ============================================================
# STEP 2 – DATA PRE-PROCESSING (USER-CONTROLLED PIPELINE)
# ============================================================
if "preprocess_history" not in st.session_state:
    st.session_state.preprocess_history = {
        "duplicates": None,
        "outliers": {},
        "null_replaced_cols": None,
        "null_replaced_rows": None,
        "numeric_converted": None
    }

if "preprocessing_completed" not in st.session_state:
    st.session_state.preprocessing_completed = False



st.markdown("""
<div style="
    background-color:#0B2C5D;
    padding:18px 25px;
    border-radius:10px;
    color:white;
    margin-top:25px;
    margin-bottom:12px;
">
    <h3 style="margin:0;">
        Data Pre-Processing (Data Quality & Readiness)
    </h3>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style="
    background-color:#2F75B5;
    padding:24px;
    border-radius:12px;
    color:white;
    font-size:16px;
    line-height:1.7;
    margin-bottom:20px;
">
This section ensures the dataset is <b>model-ready</b> by handling:
<ul>
    <li>Missing values & inconsistencies</li>
    <li>Outliers & anomalies</li>
    <li>Data type validation</li>
    <li>Referential integrity checks across dimensions</li>
    <li>Time alignment and granularity normalization</li>
</ul>

This step guarantees that downstream models are trained on
<b>clean, reliable, and trustworthy data.</b>
</div>
""", unsafe_allow_html=True)

# Safety check
if st.session_state.df is None:
    st.warning("⚠ Load data first.")
    st.stop()

df = st.session_state.df

# ------------------------------------------------------------
# STEP SELECTOR (SEQUENTIAL CONTROL)
# ------------------------------------------------------------
st.markdown(
    "<div style='font-size:20px; font-weight:600; color:#000000; margin-bottom:8px;'>"
    "Select a Data Pre-Processing Step"
    "</div>",
    unsafe_allow_html=True
)
st.write("")


step = st.radio(
    "",
    [
        "Remove Duplicate Rows",
        "Remove Outliers",
        "Replace Missing Values"
    ],
    index=None,
    horizontal=True,
    label_visibility="collapsed"

)

# ============================================================
# 1️⃣ REMOVE DUPLICATE ROWS
# ============================================================

if step == "Remove Duplicate Rows":

    st.markdown(
    "<h3 style='color:#000000;'>Remove Duplicate Rows</h3>",
    unsafe_allow_html=True
)
    st.write("")

    st.markdown("""
<div style="
    background-color:#2F75B5;
    padding:28px;
    border-radius:12px;
    color:white;
    font-size:16px;
        line-height:1.6;
        margin-bottom:20px;
">
<b>What this does:</b>
This step identifies and removes <b>exact duplicate records</b> from the dataset.<br>

<b>Duplicate rows often occur due to:</b>
<ul>
    <li>Multiple data ingestion runs</li>
    <li>System retries or sync issues</li>
    <li>Manual data merges</li>
</ul><br>

<b>Why this is important:</b>
<ul>
    <li>Prevents <b>double counting of sales, customers, or inventory</b></li>
    <li>Ensures <b>accurate aggregates and trends</b></li>
    <li>Avoids biased model training caused by repeated observations</li>
</ul><br>

<b>How it helps forecasting:</b><br>
Demand models rely on <b>true historical patterns</b>.<br>
Duplicates distort demand signals and inflate sales volumes,
leading to <b>over-forecasting</b>.
</div>
""", unsafe_allow_html=True)

    # --------------------------------------------------
    # DUPLICATE REMOVAL – FIXED BEFORE / AFTER LOGIC
    # --------------------------------------------------

    # Init session keys (SAFE)
    if "dup_before_df" not in st.session_state:
        st.session_state.dup_before_df = None
    if "dup_after_df" not in st.session_state:
        st.session_state.dup_after_df = None
    if "dup_removed_df" not in st.session_state:
        st.session_state.dup_removed_df = None


    if st.button("Apply Duplicate Row Removal"):
        st.write("")
        st.write("")
        # Prevent re-run
        if st.session_state.dup_removed_df is not None:
            st.markdown(
                "<h3 style='color:#000000;'>Duplicate rows were already removed earlier.</h3>",
                unsafe_allow_html=True
            )

        else:
            # 🔒 SNAPSHOT BEFORE (CRITICAL)
            before_df = st.session_state.df.copy()

            # Detect duplicates from BEFORE snapshot
            pk_col = "id"  # change if your PK name is different

            cols_to_check = [col for col in before_df.columns if col != pk_col]

            dup_mask = before_df.duplicated(subset=cols_to_check)
            dup_rows = before_df[dup_mask]

            if dup_rows.empty:
                st.markdown(
                    "<h3 style='color:#000000;'>No duplicate rows found.</h3>",
                    unsafe_allow_html=True
                )
            else:
                # Cleaned version
                after_df = before_df.drop_duplicates(subset=cols_to_check).reset_index(drop=True)


                # ✅ STORE ALL THREE STATES (IMMUTABLE)
                st.session_state.dup_before_df = before_df
                st.session_state.dup_removed_df = dup_rows
                st.session_state.dup_after_df = after_df

                # ✅ UPDATE WORKING DF ONLY ONCE
                st.session_state.df = after_df
                st.session_state.preprocessing_completed = True

                st.success("✔ Duplicate rows removed")


    # --------------------------------------------------
    # OUTPUT SECTION – ALWAYS USE SNAPSHOTS
    # --------------------------------------------------

    if st.session_state.dup_removed_df is not None:

        before_df = st.session_state.dup_before_df   # 🔒 frozen
        after_df = st.session_state.dup_after_df     # 🔒 frozen
        removed_df = st.session_state.dup_removed_df     
        st.markdown(
                    "<h3 style='color:#000000;'>##### Duplicate Removal Summary #####</h3>",
                    unsafe_allow_html=True
                )
        st.write("")
        st.markdown("""
        <div class="summary-grid">
            <div class="summary-card">
                <div class="summary-title">Rows Before</div>
                <div class="summary-value">{}</div>
            </div>
            <div class="summary-card">
                <div class="summary-title">Rows After</div>
                <div class="summary-value">{}</div>
            </div>
            <div class="summary-card">
                <div class="summary-title">Duplicates Removed</div>
                <div class="summary-value">{}</div>
            </div>
        </div>
        """.format(
            before_df.shape[0],
            after_df.shape[0],
            removed_df.shape[0]
        ), unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        # ===== BEFORE =====
        st.markdown(
            f"<h4 style='color:#000000;'>Before Duplicate Removal ({before_df.shape[0]} Rows)</h4>",
            unsafe_allow_html=True
        )
        st.write("")
        render_html_table(
            before_df,
            title=None,
            max_height=300
        )

        st.markdown("<br>", unsafe_allow_html=True)

        # ===== AFTER =====
        st.markdown(
        f"<h4 style='color:#000000;'>After Duplicate Removal ({after_df.shape[0]} Rows)</h4>",
        unsafe_allow_html=True
        )
        st.write("")
        render_html_table(
            after_df,
            title=None,
            max_height=300
        )

        st.markdown("<br>", unsafe_allow_html=True)

        # ===== REMOVED =====
        st.markdown(
            f"<h4 style='color:#000000;'>Removed Duplicates ({removed_df.shape[0]} Rows)</h4>",
            unsafe_allow_html=True
        )
        st.write("")
        render_html_table(
            removed_df,
            title=None,
            max_height=300  # smaller is fine here
        )
    # ============================================================
    # OUTLIER DETECTION (IQR-BASED – FLAG ONLY)
    # ============================================================
if step == "Remove Outliers":

    st.markdown(
    "<h3 style='color:#000000;'>Remove Outliers</h3>",
    unsafe_allow_html=True
)
    st.write("")

    st.markdown("""
    <div style="
        background-color:#2F75B5;
        padding:24px;
        border-radius:12px;
        color:white;
        font-size:16px;
        line-height:1.7;
        margin-bottom:20px;
    ">
    <b>What this does:</b><br>
    This step identifies and handles <b>statistical outliers</b> in numeric fields using a
    <b>robust IQR-based method</b>.

    Outlier handling is performed <b>internally</b> and follows a <b>two-level strategy</b>:
    <ul>
        <li><b>Mild anomalies</b> are <b>capped</b> to safe bounds (no row deletion)</li>
        <li><b>Extreme anomalies</b> in <b>critical columns</b> are <b>removed</b></li>
    </ul>

    <br>

    <b>Why this is important:</b>
    <ul>
        <li>Prevents extreme values from <b>skewing averages and distributions</b></li>
        <li>Reduces noise without discarding valuable data</li>
        <li>Ensures numeric stability for downstream models</li>
        <li>Avoids over-cleaning by deleting only <b>truly abnormal records</b></li>
    </ul>
    <br>

    <b>How it helps forecasting:</b>
    <li>
    Demand forecasting models are highly sensitive to extreme numeric values.
    By controlling these extremes, the model learns from realistic historical behavior
    rather than rare or erroneous spikes.
    </li>

    <li>
    This improves forecasting by preserving <b>true demand signals</b>, reducing noise,
    preventing overreaction to anomalies, and ensuring forecasts remain
    <b>stable, generalizable, and business-relevant</b> across time, products, and stores.
    </li>


    </div>
    """, unsafe_allow_html=True)

    

    df = st.session_state.df

    # --------------------------------------------------
    # NUMERIC COLUMN DETECTION
    # --------------------------------------------------
    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()

    if not numeric_cols:
        st.info("No numeric columns available for outlier detection.")
        st.stop()

    # --------------------------------------------------
    # BASE COLUMNS (MOST TRUSTWORTHY FOR DELETION)
    # --------------------------------------------------
    DELETE_COLS = ["quantity_sold", "unit_price"]

    # --------------------------------------------------
    # INIT SESSION KEYS
    # --------------------------------------------------
    if "out_before_df" not in st.session_state:
        st.session_state.out_before_df = None
    if "out_after_df" not in st.session_state:
        st.session_state.out_after_df = None
    if "out_removed_df" not in st.session_state:
        st.session_state.out_removed_df = None

    # --------------------------------------------------
    # APPLY AGGRESSIVE OUTLIER HANDLING
    # --------------------------------------------------
    if st.button("Apply Outlier Removal"):

        if st.session_state.out_removed_df is not None:
            st.markdown(
                "<h3 style='color:#000000;'>Outliers were already handled earlier.</h3>",
                unsafe_allow_html=True
            )

        else:
            before_df = df.copy()
            after_df = before_df.copy()

            # Count how many columns flag each row
            outlier_count = pd.Series(0, index=before_df.index)

            for col in numeric_cols:
                Q1 = before_df[col].quantile(0.25)
                Q3 = before_df[col].quantile(0.75)
                IQR = Q3 - Q1

                mild_lower = Q1 - 1.5 * IQR
                mild_upper = Q3 + 1.5 * IQR

                # More aggressive extreme bounds
                extreme_lower = Q1 - 2.0 * IQR
                extreme_upper = Q3 + 2.0 * IQR

                # Count mild outliers
                is_mild = (
                    (before_df[col] < mild_lower) |
                    (before_df[col] > mild_upper)
                )

                outlier_count += is_mild.astype(int)

                # Hard delete if base column is extreme
                if col in DELETE_COLS:
                    outlier_count += (
                        (before_df[col] < extreme_lower) |
                        (before_df[col] > extreme_upper)
                    ).astype(int) * 2  # heavier weight

                # Cap all numeric columns
                after_df[col] = after_df[col].clip(mild_lower, mild_upper)

            # 🔥 DELETE RULE (AGGRESSIVE BUT LOGICAL)
            # Remove rows flagged in 3+ signals
            extreme_mask = outlier_count >= 4

            removed_df = before_df[extreme_mask]
            after_df = after_df[~extreme_mask].reset_index(drop=True)

            # Save snapshots
            st.session_state.out_before_df = before_df
            st.session_state.out_removed_df = removed_df
            st.session_state.out_after_df = after_df

            st.session_state.df = after_df
            st.session_state.preprocessing_completed = True

            st.success("Outliers handled successfully")
    # --------------------------------------------------
    # OUTPUT SECTION (UNCHANGED)
    # --------------------------------------------------
    if st.session_state.out_removed_df is not None:

        before_df = st.session_state.out_before_df
        after_df = st.session_state.out_after_df
        removed_df = st.session_state.out_removed_df

        st.markdown(
            "<h3 style='color:#000000;'>####  Outlier Removal Summary</h3>",
            unsafe_allow_html=True
        )
        st.write("")
        st.markdown("""
        <div class="summary-grid">
            <div class="summary-card">
                <div class="summary-title">Rows Before</div>
                <div class="summary-value">{}</div>
            </div>
            <div class="summary-card">
                <div class="summary-title">Rows After</div>
                <div class="summary-value">{}</div>
            </div>
            <div class="summary-card">
                <div class="summary-title">Outliers Removed</div>
                <div class="summary-value">{}</div>
            </div>
        </div>
        """.format(
            before_df.shape[0],
            after_df.shape[0],
            removed_df.shape[0]
        ), unsafe_allow_html=True)
        st.write("")
            # ===== BEFORE =====
        st.markdown(
            f"<h4 style='color:#000000;'>Before Outlier Handling ({before_df.shape[0]} Rows)</h4>",
            unsafe_allow_html=True
        )
        st.write("")
        render_html_table(before_df, max_height=300)
        st.write("")

        # ===== AFTER =====
        st.markdown(
            f"<h4 style='color:#000000;'>After Outlier Handling ({after_df.shape[0]} Rows)</h4>",
            unsafe_allow_html=True
        )
        st.write("")
        render_html_table(after_df, max_height=300)
        

        st.markdown("<br>", unsafe_allow_html=True)

        # ===== REMOVED =====
        st.markdown(
            f"<h4 style='color:#000000;'>Removed Outliers ({removed_df.shape[0]} Rows)</h4>",
            unsafe_allow_html=True
        )
        st.write("")
        render_html_table(removed_df, max_height=300)




# ============================================================
# 3️⃣ REPLACE NULL VALUES WITH "UNKNOWN"
# ============================================================

elif step == "Replace Missing Values":

    st.markdown(
    "<h3 style='color:#000000;'>Replace Missing Values</h3>",
    unsafe_allow_html=True
)
    st.write("")

    st.markdown(
    """
    <div style="
        background-color:#2F75B5;
        padding:28px;
        border-radius:12px;
        color:white;
        font-size:16px;
        line-height:1.6;
        margin-bottom:20px;
    ">

    <b>What this does:<br>

    For non-critical categorical fields, missing values are replaced with a placeholder like:<br>
    “<b>Unknown</b>”<br>

    <b>Examples:</b>

    <li> Product Name</li>
    <li> Supplier Type</li>
    <li> Event Name</li>
    <li> Platform Type</li><br>

    <b>Why this is important:<br>

    <li>Preserves valuable records instead of discarding them</li>
    <li> Keeps categorical columns consistent</li>
    <li> Allows models to learn from “unknown” patterns rather than losing data</li><br>

        
    <b>Modelling advantage:</b>

    Many ML models can handle a distinct “<b>Unknown</b>” category better than missing values.<br>

    This improves:<br>

    <li>Model stability</li>
    <li>Feature completeness</li>
    <li>Interpretability</li>

    </div>
    """,
    unsafe_allow_html=True
)


    # ============================================================
    # NULL VALUE REPLACEMENT (STATEFUL + AFFECTED ROWS ONLY)
    # ============================================================

    df = st.session_state.df

    # ------------------------------------------------------------
    # INIT SESSION KEYS
    # ------------------------------------------------------------
    if "null_before_rows" not in st.session_state:
        st.session_state.null_before_rows = None
    if "null_after_rows" not in st.session_state:
        st.session_state.null_after_rows = None
    if "null_replaced_cols" not in st.session_state:
        st.session_state.null_replaced_cols = None


    # ------------------------------------------------------------
    # DETECT NULLS (CURRENT DF)
    # ------------------------------------------------------------
    null_mask = df.isnull()
    affected_rows_before = df[null_mask.any(axis=1)]
    null_counts = null_mask.sum()
    null_counts = null_counts[null_counts > 0]


    # ------------------------------------------------------------
    # APPLY NULL REPLACEMENT
    # ------------------------------------------------------------
    if st.button("Apply NULL Replacement"):

        if null_counts.empty:
            st.markdown(
                "<h3 style='color:#000000;'>NULL values were already handled earlier.</h3>",
                unsafe_allow_html=True
            )

        else:
            # 🔒 SNAPSHOT ONLY AFFECTED ROWS (BEFORE)
            st.session_state.null_before_rows = affected_rows_before.copy()

            # SAVE COLUMN IMPACT
            st.session_state.null_replaced_cols = (
                null_counts.to_frame("NULL Count")
            )

            # APPLY REPLACEMENT
            df_updated = df.fillna("Unknown")
            st.session_state.df = df_updated
            st.session_state.preprocessing_completed = True

            # 🔒 SNAPSHOT SAME ROWS AFTER REPLACEMENT
            st.session_state.null_after_rows = df_updated.loc[
                affected_rows_before.index
            ].copy()

            st.success(" NULL values replaced with 'Unknown'")


    # ------------------------------------------------------------
    # OUTPUT SECTION – AFFECTED ROWS ONLY
    # ------------------------------------------------------------
    if (
    st.session_state.null_before_rows is not None and
    st.session_state.null_after_rows is not None and
    st.session_state.null_replaced_cols is not None
):


        before_rows = st.session_state.null_before_rows
        after_rows = st.session_state.null_after_rows
        replaced_cols = st.session_state.null_replaced_cols
        # ===================== COLUMNS =====================
        st.markdown(
            "<h3 style='color:#000000;'>####  Columns Where NULL Values Were Replaced</h3>",
            unsafe_allow_html=True
        )
        st.write("")

        if not replaced_cols.empty:
            value_col = replaced_cols.columns[0]

            html_cards = "".join(
                f"""
                <div class="summary-card">
                    <div class="summary-title">{str(idx).replace('_', ' ').title()}</div>
                    <div class="summary-value">{row[value_col]}</div>
                </div>
                """
                for idx, row in replaced_cols.iterrows()
            )

            st.markdown(
                f"""
                <div class="summary-grid">
                
                    {html_cards}
                </div>
                """,
                unsafe_allow_html=True   # 🔥 THIS IS CRITICAL
            )
        else:
            st.markdown(
                "<h3 style='color:#000000;'>No NULL values were replaced.</h3>",
                unsafe_allow_html=True
            )

        st.write("")
        # ===================== BEFORE =====================
        st.markdown(
            f"<h4 style='color:#000000;'>Rows Before Missing Values Replacement ({before_rows.shape[0]} Rows)</h4>",
            unsafe_allow_html=True
        )
        st.write("")
        render_html_table(before_rows)
        
        # ===================== AFTER =====================
        st.markdown(
            f"<h4 style='color:#000000;'>Rows After Missing Values Replacement ({after_rows.shape[0]} Rows)</h4>",
            unsafe_allow_html=True
        )
        st.write("")
        render_html_table(after_rows)



st.markdown("""
<style>

/* =====================================================
   GLOBAL / COMMON STYLES
   ===================================================== */

/* Clean report-style table (used across EDA) */
.clean-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 13.5px;
}

.clean-table th {
    background-color: #F4F6F7;
    padding: 8px;
    text-align: left;
    font-weight: 600;
    border-bottom: 1px solid #D6DBDF;
    color: #34495E;
}

.clean-table td {
    padding: 7px 8px;
    border-bottom: 1px solid #ECF0F1;
    color: #2C3E50;
}

.clean-table tr:hover {
    background-color: #F8F9F9;
}



/* =====================================================
   DATA QUALITY – LAYOUT (FINAL, CLEAN)
   ===================================================== */

/* Horizontal row for 3 cards */
.quality-row {
    display: flex;
    gap: 16px;
    margin-bottom: 48px;   /* clear gap between rows */
}

/* Individual card */
.quality-card {
    flex: 1;
    background-color: white;
    border-radius: 12px;
    padding: 16px 18px;
    box-shadow: 0px 2px 8px rgba(0,0,0,0.06);
    border-left: 5px solid #2F75B5;
    margin-bottom: 48px;   /* ~5 line gap between sections */
}

/* Section title with light blue band (AS PER IMAGE) */
.quality-title {
    font-size: 15px;
    font-weight: 600;
    color: #ffffff;
    background-color:#123A72;
    padding: 10px 14px;
    border-radius: 6px;
    margin-bottom: 18px;
}

/* Scrollable content inside card */
.table-scroll {
    max-height: 260px;
    overflow-y: auto;
}
            

            
/* ===============================
   TABLE APPEARANCE (NO RENAMES)
   =============================== */

.quality-card table {
    width: 100%;
    border-collapse: collapse;
    background-color: #FFFFFF;
    font-size: 14px;
}

/* Table header */
.quality-card th {
    background-color: #E5ECF4;   /* slightly darker */
    color: #1F2937;
    font-weight: 600;
    text-align: left;
    padding: 10px 12px;
    border-bottom: 1px solid #D6DEE8;
}

/* Table cells */
.quality-card td {
    padding: 9px 12px;
    color: #111827;
    border-bottom: 1px solid #EEF2F7;
}

/* Zebra rows (LIKE IMAGE) */
.quality-card tr:nth-child(even) td {
    background-color: #FFFFFF;
}

.quality-card tr:nth-child(odd) td {
    background-color: #F3F6FA;
}

/* Subtle hover */
.quality-card tr:hover td {
    background-color: #E9F1FF;
}


/* =====================================================
   REPORT / CARD STYLE (used for future EDA sections)
   ===================================================== */

.report-card {
    background-color: #FFFFFF;
    border-radius: 14px;
    padding: 18px 20px;
    margin-bottom: 22px;
    box-shadow: 0px 2px 8px rgba(0,0,0,0.06);
    border-left: 6px solid #2F75B5;
}

.report-title {
    font-size: 16px;
    font-weight: 600;
    margin-bottom: 12px;
    color: #2C3E50;
}

.metric-pill {
    display: inline-block;
    background-color: #EBF5FB;
    color: #1F618D;
    padding: 6px 12px;
    border-radius: 20px;
    font-size: 13px;
    font-weight: 600;
    margin-right: 8px;
}

</style>
""", unsafe_allow_html=True)

# Global transparent theme
def transparent_theme():
    return {
        "config": {
            "background": "transparent",
            "view": {
                "fill": "transparent",
                "stroke": "transparent"
            },
            "axis": {
                "labelColor": "rgba(255,255,255,0.8)",
                "titleColor": "rgba(255,255,255,0.9)",
                "gridColor": "rgba(255,255,255,0.25)",
                "domainColor": "rgba(255,255,255,0.4)"
            },
            "text": {"color": "white"}
        }
    }

alt.themes.register("transparent_theme", transparent_theme)
alt.themes.enable("transparent_theme")


# ============================================================
# STEP 3 – EDA (LOCKED UNTIL PREPROCESSING)
# ============================================================

if not st.session_state.preprocessing_completed:
    st.info("ℹ Please apply at least one data pre-processing step to unlock EDA.")
    st.stop()


df = st.session_state.get("df", None)

if df is None:
    st.warning("⚠ No dataset available.")
    st.stop()

if "eda_completed" not in st.session_state:
    st.session_state.eda_completed = False


 # ---------------- EDA HEADER ----------------
st.markdown(
    """
    <div style="
        background-color:#0B2C5D;
        padding:18px 25px;
        border-radius:10px;
        color:white;
        margin-top:20px;
        margin-bottom:10px;
    ">
        <h3 style="margin:0;">Exploratory Data Analysis (EDA)</h3>
    </div>
    """,
    unsafe_allow_html=True
)
st.write("")
st.info(f"Dataset Loaded: **{df.shape[0]} rows × {df.shape[1]} columns**")
st.write("")
# ---------------- EDA INTRO CARD ----------------
st.markdown(
    """
    <div style="
        background-color:#2F75B5;
        padding:28px;
        border-radius:12px;
        color:white;
        font-size:16px;
        line-height:1.6;
        margin-bottom:20px;
    ">

    <b>Exploratory Data Analysis (EDA)</b><br><br>

    Provides <b>high-level insights</b> to understand data behavior before model engineering.<br><br>

    <b>Key Insights Generated:</b>
    <ul>
        <li>Sales and revenue trends across products and categories</li>
        <li>Fast-moving and slow-moving SKU identification</li>
        <li>Stock availability, overstock, and understock analysis</li>
        <li>Reorder planning and stockout risk monitoring</li>
        <li>Supplier lead time and delivery performance evaluation</li>
        <li>Procurement cost and purchasing behavior analysis</li>
        <li>Weather, events, and social trends impact on demand</li>
        <li>Store-wise and city-wise sales performance comparison</li>
    </ul>

    This section focuses on <b>interpretability</b>, not deep statistical modeling.

    </div>
    """,
    unsafe_allow_html=True
)

# ============================================================
# COLUMN MAPPING (SAFE & SIMPLE)
# ============================================================

def map_col(candidates):
    for c in candidates:
        if c in df.columns:
            return c
    return None

col_rev     = map_col(["Sales_Revenue"])
col_qty     = map_col(["Quantity_Sold"])
col_price   = map_col(["Unit_Price"])
col_date    = map_col(["Date"])
col_product = map_col(["Product_ID"])
col_store   = map_col(["Store_ID"])
col_channel = map_col(["Payment_Type"])
col_event   = map_col(["Event_ID"])
col_promo   = map_col(["Promo_ID"])
col_Transaction = map_col(["Transaction_ID"])

num_df = df.select_dtypes(include=np.number)

# ============================================================
# EDA NAVIGATION
# ============================================================
# =========================
# EDA NAVIGATION – ACTIVE BUTTON HIGHLIGHT (SAFE)
# =========================

# =========================
# EDA NAVIGATION (INSTANT COLOR CHANGE)
# =========================

st.markdown(
    "<h3 style='color:black;'>List of Analytics</h3>",
    unsafe_allow_html=True
)
st.markdown(
    "<div style='margin-top:6px'></div>",
    unsafe_allow_html=True
)



if "eda_option" not in st.session_state:
    st.session_state.eda_option = None


def nav_button(label, value):
    
    """Instant active highlight + no size change"""
    if st.session_state.eda_option == value:
        st.markdown(
            f"""
            <div style="
                background-color:#4F97EE
;
                color:white;
                padding:14px;
                border-radius:10px;
                font-weight:600;
                text-align:center;
                margin-bottom:12px;
            ">
                {label}
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        if st.button(label, use_container_width=True):
            st.session_state.eda_option = value
            st.rerun() 

with st.expander(" ", expanded=True):
    row1 = st.columns(5)
    row2 = st.columns(4)

    with row1[0]:
        nav_button("Data Quality Overview", "Data Quality Overview")
    with row1[1]:
        nav_button("Sales Overview", "Sales Overview")
    with row1[2]:
        nav_button("Demand Forecasting Analysis", "Demand Forecasting Analysis")
    with row1[3]:
        nav_button("Inventory & Stock Analysis", "Inventory & Stock Analysis")
    with row1[4]:
        nav_button("Predictive Replenishment Analysis", "Predictive Replenishment Analysis")

    with row2[0]:
        nav_button("Supplier & Lead Time Analysis", "Supplier & Lead Time Analysis")
    with row2[1]:
        nav_button("Store-Level Analysis", "Store-Level Analysis")
    with row2[2]:
        nav_button("External Factors Impact Analysis", "External Factors Impact Analysis")
    with row2[3]:
        nav_button("Summary Report", "Summary Report")


eda_option = st.session_state.eda_option
if eda_option is not None:
    st.session_state.eda_completed = True
st.markdown(
    "<div style='margin-top:6px'></div>",
    unsafe_allow_html=True
)

if eda_option is None:
    st.info("Select an analysis to view insights.")

# ============================================================
# EDA ROUTER (⚠️ DO NOT BREAK THIS STRUCTURE)
# ============================================================

if eda_option == "Data Quality Overview":

    st.markdown(
        """
        <div style="
            background-color:#2F75B5;
            padding:28px;
            border-radius:12px;
            color:white;
            font-size:16px;
            line-height:1.6;
            margin-bottom:20px;
        ">

        <b>What this section does:</b>

        This section provides a <b>high-level health check</b> of the dataset before any modeling or forecasting is attempted.

        It evaluates:
        <ul>
            <li>Missing values</li>
            <li>Duplicate records</li>
            <li>Data type consistency</li>
            <li>Overall row and column completeness</li>
        </ul>

        <b>Why this matters:</b>

        Demand forecasting models are highly sensitive to <b>poor data quality</b>.
        Even small inconsistencies (missing prices, invalid quantities, duplicate transactions)
        can significantly distort predictions.<br>

        <b>Key insights users get:</b>
        <ul>
            <li>Whether the dataset is <b>model-ready</b></li>
            <li>Which columns require cleaning or transformation</li>
            <li>Confidence in the reliability of downstream analysis</li>
        </ul>

        </div>
        """,
        unsafe_allow_html=True
    )

    # =========================
    # PREPARE DATA
    # =========================
    rows_count = df.shape[0]
    cols_count = df.shape[1]
    
    dup_count = df.duplicated().sum()
    dtype_counts = df.dtypes.value_counts()

    mv = (df.isnull().mean() * 100).round(2).sort_values(ascending=False)

    # =========================
    # DATASET SHAPE
    # =========================
    st.markdown(
        f"""
        <div class="quality-card">
            <div class="quality-title">Dataset Shape</div>
            <table class="clean-table">
                <tr><th>Metric</th><th>Value</th></tr>
                <tr><td>Total Rows</td><td>{rows_count}</td></tr>
                <tr><td>Total Columns</td><td>{cols_count}</td></tr>
            </table>
        </div>
        """,
        unsafe_allow_html=True
    )

    # =========================
    # MISSING VALUE ANALYSIS
    # =========================
    st.markdown(
        f"""
        <div class="quality-card">
            <div class="quality-title">Missing Value Analysis (%)</div>
            <div class="table-scroll">
                <table class="clean-table">
                    <tr><th>Column Name</th><th>Missing (%)</th></tr>
                    {''.join([f"<tr><td>{c}</td><td>{v}%</td></tr>" for c, v in mv.items()])}
                </table>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # =========================
    # DUPLICATE ANALYSIS
    # =========================
    st.markdown(
        f"""
        <div class="quality-card">
            <div class="quality-title">Duplicate Analysis</div>
            <table class="clean-table">
                <tr><th>Metric</th><th>Value</th></tr>
                <tr><td>Total Duplicate Rows</td><td>{dup_count}</td></tr>
            </table>
        </div>
        """,
        unsafe_allow_html=True
    )

    # =========================
    # DATA TYPES SUMMARY
    # =========================
    st.markdown(
        f"""
        <div class="quality-card">
            <div class="quality-title">Data Types Summary</div>
            <table class="clean-table">
                <tr><th>Data Type</th><th>Column Count</th></tr>
                {''.join([f"<tr><td>{d}</td><td>{c}</td></tr>" for d, c in dtype_counts.items()])}
            </table>
        </div>
        """,
        unsafe_allow_html=True
    )
    
elif eda_option == "Sales Overview":
    st.markdown(
    """
    <div style="
        background-color:#2F75B5;
        padding:28px;
        border-radius:12px;
        color:white;
        font-size:16px;
        line-height:1.6;
        margin-bottom:20px;
    ">

    <b>What this section does:</b>

    This provides a <b>macro-level snapshot of sales performance</b>


    It typically highlights:
    <ul>
        <li>Total revenue</li>
        <li>Total units sold</li>
        <li>Average order value</li>
        <li>Sales trends over time</li>
    </ul><br>

    <b>Why this matters:</b>

    Before diving into granular analysis, it’s important to understand:
    <ul>
        <li>Overall business scale</li>
        <li>Growth or decline patterns</li>
        <li>Presence of seasonality or anomalies</li>
    </ul><br>

    <b>Key insights users get:</b>
    <ul>
        <li>Baseline sales behavior</li>
        <li>Early signals of trends or volatility</li>
        <li>Context for all deeper analyses</li>
    </ul>

    </div>
    """,
    unsafe_allow_html=True
)
    st.markdown("###  Sales Overview")
           # ---------- ROW 1 ----------
    st.markdown(
        """
        <div class="summary-grid">
            <div class="summary-card">
                <div class="summary-title">Total Revenue</div>
                <div class="summary-value">{}</div>
            </div>
            <div class="summary-card">
                <div class="summary-title">Average Order Value</div>
                <div class="summary-value">{}</div>
            </div>
            <div class="summary-card">
                <div class="summary-title">Maximum Order Value</div>
                <div class="summary-value">{}</div>
            </div>
        </div>
        """.format(
            f"${df[col_rev].sum():,.2f}" if col_rev else "NA",
            f"${df[col_rev].mean():,.2f}" if col_rev else "NA",
            f"${df[col_rev].max():,.2f}" if col_rev else "NA",
        ),
        unsafe_allow_html=True
        )

        # ---------- ROW 2 ----------
    st.markdown(
        """
        <div class="summary-grid">
            <div class="summary-card">
                <div class="summary-title">Total Sales</div>
                <div class="summary-value">{}</div>
            </div>
            <div class="summary-card">
                <div class="summary-title">Total Units Sold</div>
                <div class="summary-value">{}</div>
            </div>
            <div class="summary-card">
                <div class="summary-title">Average Units / Transaction</div>
                <div class="summary-value">{}</div>
            </div>
        </div>
        """.format(
            f"${(df[col_qty] * df[col_price]).sum():,.2f}" if col_qty and col_price else "NA",
            f"{df[col_qty].sum():,}" if col_qty else "NA",
            f"{df[col_qty].mean():.2f}" if col_qty else "NA",
        ),
        unsafe_allow_html=True
        )

    st.write("")
    st.write("")

    # ================= ROW 1 =================
    col1, col2 = st.columns(2)

    with col1: 
        if "Date" in df.columns and col_rev:
            st.markdown(
            """
            <div style="
                background-color:#2F75B5;
                padding:18px 25px;
                border-radius:10px;
                font-size:20px;
                color:white;
                margin-top:20px;
                margin-bottom:10px;
                text-align:center;
            ">
                <b>Sales By Year</b>
            </div>
            """,
            unsafe_allow_html=True
        )
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
        df = df.dropna(subset=["Date"])

        df["Year"] = df["Date"].dt.year
        df["Quarter"] = df["Date"].dt.to_period("Q").astype(str)
        df["Month"] = df["Date"].dt.to_period("M").astype(str)

        sales_by_year = (
            df.groupby("Year")[col_rev]
            .sum()
            .sort_index()
        )
        
        chart=(
                alt.Chart(sales_by_year.reset_index())
                .mark_bar(color="#001F5C",cornerRadiusEnd=6)
                .encode(
                    x=alt.X("Year:O", title="Year"),
                    y=alt.Y(f"{col_rev}:Q", title="Revenue",scale=alt.Scale(padding=10)),
                    tooltip=["Year", col_rev]
                )
                .properties(
                    height=380,
                    background="#00D05E",
                    padding={"top": 10, "left": 10, "right": 10, "bottom": 10}
                )
                .configure_view(
                    fill="#00D05E",
                    strokeOpacity=0
                )
                .configure_axis(
                    labelColor="#000000",
                    titleColor="#000000",
                    gridColor="rgba(0,0,0,0.2)",
                    domainColor="rgba(0,0,0,0.3)"
                )
            )

        st.altair_chart(chart, use_container_width=True)
   
    
    with col2:
        st.markdown(
            """
            <div style="
                background-color:#2F75B5;
                padding:18px 25px;
                border-radius:10px;
                font-size:20px;
                color:white;
                margin-top:20px;
                margin-bottom:10px;
                text-align:center;
            ">
                <b>Sales By Quaters</b>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Aggregate revenue by quarter
        sales_by_quarter = (
            df.groupby("Quarter")[col_rev]
            .sum()
            .sort_index()
        )

        # Altair chart with SAME layout/template as yearly chart
        chart_quarter = (
            alt.Chart(sales_by_quarter.reset_index())
            .mark_bar(color="#001F5C", cornerRadiusEnd=6)
            .encode(
                x=alt.X("Quarter:O", title="Quarter"),
                y=alt.Y(f"{col_rev}:Q", title="Revenue", scale=alt.Scale(padding=10)),
                tooltip=["Quarter", col_rev]
            )
            .properties(
                height=380,
                background="#00D05E",
                padding={"top": 10, "left": 10, "right": 10, "bottom": 10}
            )
            .configure_view(
                fill="#00D05E",
                strokeOpacity=0
            )
            .configure_axis(
                labelColor="#000000",
                titleColor="#000000",
                gridColor="rgba(0,0,0,0.2)",
                domainColor="rgba(0,0,0,0.3)"
            )
        )

        st.altair_chart(chart_quarter, use_container_width=True)

# ================= ROW 2 =================

    col3, col4 = st.columns(2)
    with col3:
        st.markdown(
            """
            <div style="
                background-color:#2F75B5;
                padding:18px 25px;
                border-radius:10px;
                font-size:20px;
                color:white;
                margin-top:20px;
                margin-bottom:10px;
                text-align:center;
            ">
                <b>Sales By Month</b>
            </div>
            """,
            unsafe_allow_html=True
        )
        # Aggregate revenue by month
        sales_by_month = (
            df.groupby("Month")[col_rev]
            .sum()
            .sort_index()
        )

        # Altair chart with SAME layout/template
        chart_month = (
            alt.Chart(sales_by_month.reset_index())
            .mark_bar(color="#001F5C", cornerRadiusEnd=6)
            .encode(
                x=alt.X("Month:O", title="Month"),
                y=alt.Y(f"{col_rev}:Q", title="Revenue", scale=alt.Scale(padding=10)),
                tooltip=["Month", col_rev]
            )
            .properties(
                height=380,
                background="#00D05E",
                padding={"top": 10, "left": 10, "right": 10, "bottom": 10}
            )
            .configure_view(
                fill="#00D05E",
                strokeOpacity=0
            )
            .configure_axis(
                labelColor="#000000",
                titleColor="#000000",
                gridColor="rgba(0,0,0,0.2)",
                domainColor="rgba(0,0,0,0.3)"
            )
        )

        st.altair_chart(chart_month, use_container_width=True)

    with col4:
        st.markdown(
            """
            <div style="
                background-color:#2F75B5;
                padding:18px 25px;
                border-radius:10px;
                font-size:20px;
                color:white;
                margin-top:20px;
                margin-bottom:10px;
                text-align:center;
            ">
                <b>Sales By Day</b>
            </div>
            """,
            unsafe_allow_html=True
        )
        # Aggregate revenue by Date
        sales_by_Date = (
            df.groupby("Date")[col_rev]
            .sum()
            .sort_index()
        )

        # Altair chart with SAME layout/template
        chart_Date = (
            alt.Chart(sales_by_Date.reset_index())
            .mark_bar(color="#001F5C", cornerRadiusEnd=6)
            .encode(
                x=alt.X("Date:T", title="Date", axis=alt.Axis(format="%Y-%m-%d")),
                y=alt.Y(f"{col_rev}:Q", title="Revenue", scale=alt.Scale(padding=10)),
                tooltip=["Date", col_rev]
            )
            .properties(
                height=380,
                background="#00D05E",
                padding={"top": 10, "left": 10, "right": 10, "bottom": 10}
            )
            .configure_view(
                fill="#00D05E",
                strokeOpacity=0
            )
            .configure_axis(
                labelColor="#000000",
                titleColor="#000000",
                gridColor="rgba(0,0,0,0.2)",
                domainColor="rgba(0,0,0,0.3)"
            )
        )

        st.altair_chart(chart_Date, use_container_width=True)

# ================= ROW 3 =================
    col5, col6 = st.columns(2)

    with col5:
        if col_store and col_rev:
            st.markdown(
            """
            <div style="
                background-color:#2F75B5;
                padding:18px 25px;
                border-radius:10px;
                font-size:20px;
                color:white;
                margin-top:20px;
                margin-bottom:10px;
                text-align:center;
            ">
                <b>Sales By Store</b>
            </div>
            """,
            unsafe_allow_html=True
        )
        # Aggregate revenue by store
        sales_store = (
            df.groupby(col_store)[col_rev]
            .sum()
            .sort_values(ascending=False)
        )

        # Altair chart with SAME layout/template
        chart_store = (
            alt.Chart(sales_store.reset_index())
            .mark_bar(color="#001F5C", cornerRadiusEnd=6)
            .encode(
                x=alt.X(f"{col_store}:O", title="Store"),
                y=alt.Y(f"{col_rev}:Q", title="Revenue", scale=alt.Scale(padding=10)),
                tooltip=[col_store, col_rev]
            )
            .properties(
                height=380,
                background="#00D05E",
                padding={"top": 10, "left": 10, "right": 10, "bottom": 10}
            )
            .configure_view(
                fill="#00D05E",
                strokeOpacity=0
            )
            .configure_axis(
                labelColor="#000000",
                titleColor="#000000",
                gridColor="rgba(0,0,0,0.2)",
                domainColor="rgba(0,0,0,0.3)"
            )
        )

        st.altair_chart(chart_store, use_container_width=True)

    with col6:
        if col_channel and col_rev:
                st.markdown(
            """
            <div style="
                background-color:#2F75B5;
                padding:18px 25px;
                border-radius:10px;
                font-size:20px;
                color:white;
                margin-top:20px;
                margin-bottom:10px;
                text-align:center;
            ">
                <b>Sales By Sales Channels</b>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Aggregate revenue by channel
        sales_channel = (
            df.groupby(col_channel)[col_rev]
            .sum()
            .sort_values(ascending=False)
        )

        # Altair chart with SAME layout/template
        chart_channel = (
            alt.Chart(sales_channel.reset_index())
            .mark_bar(color="#001F5C", cornerRadiusEnd=6)
            .encode(
                x=alt.X(f"{col_channel}:O", title="Channel"),
                y=alt.Y(f"{col_rev}:Q", title="Revenue", scale=alt.Scale(padding=10)),
                tooltip=[col_channel, col_rev]
            )
            .properties(
                height=380,
                background="#00D05E",
                padding={"top": 10, "left": 10, "right": 10, "bottom": 10}
            )
            .configure_view(
                fill="#00D05E",
                strokeOpacity=0
            )
            .configure_axis(
                labelColor="#000000",
                titleColor="#000000",
                gridColor="rgba(0,0,0,0.2)",
                domainColor="rgba(0,0,0,0.3)"
            )
        )

        st.altair_chart(chart_channel, use_container_width=True)

    
elif eda_option == "Demand Forecasting Analysis":

    st.markdown(
    """
    <div style="
        background-color:#2F75B5;
        padding:28px;
        border-radius:12px;
        color:white;
        font-size:16px;
        line-height:1.6;
        margin-bottom:20px;
    ">

    <b>What this section does:</b>

    This section analyzes <b>customer demand patterns</b> across products,
    categories, and seasons to support demand forecasting and inventory planning.

    It helps identify:
    <ul>
        <li>Fast-moving products</li>
        <li>High-demand categories</li>
        <li>Seasonal demand fluctuations</li>
        <li>Monthly demand behavior</li>
    </ul><br>

    <b>Why this matters:</b>

    Understanding demand patterns helps businesses:
    <ul>
        <li>Optimize inventory replenishment</li>
        <li>Prevent stock shortages</li>
        <li>Improve forecasting accuracy</li>
        <li>Plan for seasonal demand spikes</li>
    </ul><br>

    <b>Key insights users get:</b>
    <ul>
        <li>Best-selling products</li>
        <li>Season-wise demand trends</li>
        <li>Category-wise demand distribution</li>
    </ul>

    </div>
    """,
    unsafe_allow_html=True
    )

    st.markdown("### Demand Analysis")

    # =========================================================
    # ROW 1 → PRODUCT DEMAND ANALYSIS
    # =========================================================

    col1, col2 = st.columns(2)

    # ---------------------------------------------------------
    # TOP PRODUCTS
    # ---------------------------------------------------------
    with col1:

        st.markdown(
            """
            <div style="
                background-color:#2F75B5;
                padding:18px 25px;
                border-radius:10px;
                font-size:20px;
                color:white;
                margin-top:20px;
                margin-bottom:10px;
                text-align:center;
            ">
                <b>High-Demand Categories</b>
            </div>
            """,
            unsafe_allow_html=True
        )
    
        # Remove invalid categories like \N
        clean_df = df[
            (df["Category"].notna()) &
            (df["Category"] != r"\N") &
            (df["Category"].str.strip() != "")
        ]

        top_categories = (
            clean_df.groupby("Category")["Quantity_Sold"]
            .sum()
            .sort_values(ascending=False)
            .head(10)
            .reset_index()
        )

        chart_categories = (
            alt.Chart(top_categories)
            .mark_bar(color="#001F5C", cornerRadiusEnd=6)
            .encode(
                y=alt.Y(
                    "Category:N",
                    sort='-x',
                    title="Category"
                ),
                x=alt.X(
                    "Quantity_Sold:Q",
                    title="Quantity Sold"
                ),
                tooltip=["Category", "Quantity_Sold"]
            )
            .properties(
                height=400,
                background="#00D05E",
                padding={"top": 10, "left": 10, "right": 10, "bottom": 10}
            )
            .configure_view(
                fill="#00D05E",
                strokeOpacity=0
            )
            .configure_axis(
                labelColor="#000000",
                titleColor="#000000",
                gridColor="rgba(0,0,0,0.2)",
                domainColor="rgba(0,0,0,0.3)"
            )
        )

        st.altair_chart(chart_categories, use_container_width=True)

    # ---------------------------------------------------------
    # TOP CATEGORIES
    # ---------------------------------------------------------
    with col2:

        st.markdown(
            """
            <div style="
                background-color:#2F75B5;
                padding:18px 25px;
                border-radius:10px;
                font-size:20px;
                color:white;
                margin-top:20px;
                margin-bottom:10px;
                text-align:center;
            ">
                <b>Top High-Demand Products</b>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Remove invalid categories like \N
        clean_df = df[
            (df["Category"].notna()) &
            (df["Category"] != r"\N") &
            (df["Category"].str.strip() != "")
        ]

        top_products = (
            clean_df.groupby("Product Name")["Quantity_Sold"]
            .sum()
            .sort_values(ascending=False)
            .head(10)
            .reset_index()
        )

        chart_products = (
            alt.Chart(top_products)
            .mark_bar(color="#001F5C", cornerRadiusEnd=6)
            .encode(
                y=alt.Y(
                    "Product Name:N",
                    sort='-x',
                    title="Product"
                ),
                x=alt.X(
                    "Quantity_Sold:Q",
                    title="Quantity Sold"
                ),
                tooltip=["Product Name", "Quantity_Sold"]
            )
            .properties(
                height=400,
                background="#00D05E",
                padding={"top": 10, "left": 10, "right": 10, "bottom": 10}
            )
            .configure_view(
                fill="#00D05E",
                strokeOpacity=0
            )
            .configure_axis(
                labelColor="#000000",
                titleColor="#000000",
                gridColor="rgba(0,0,0,0.2)",
                domainColor="rgba(0,0,0,0.3)"
            )
        )

        st.altair_chart(chart_products, use_container_width=True)

    # =========================================================
    # ROW 2 → SEASONAL DEMAND ANALYSIS
    # =========================================================

    col3, col4 = st.columns(2)

    # ---------------------------------------------------------
    # SEASON-WISE DEMAND
    # ---------------------------------------------------------
    with col3:

        st.markdown(
            """
            <div style="
                background-color:#2F75B5;
                padding:18px 25px;
                border-radius:10px;
                font-size:20px;
                color:white;
                margin-top:20px;
                margin-bottom:10px;
                text-align:center;
            ">
                <b>Season-wise Demand Analysis</b>
            </div>
            """,
            unsafe_allow_html=True
        )

        season_demand = (
            df.groupby("Season")["Quantity_Sold"]
            .sum()
            .reset_index()
        )

        chart_season = (
            alt.Chart(season_demand)
            .mark_bar(color="#001F5C", cornerRadiusEnd=6)
            .encode(
                x=alt.X("Season:N", title="Season"),
                y=alt.Y("Quantity_Sold:Q", title="Quantity Sold"),
                tooltip=["Season", "Quantity_Sold"]
            )
            .properties(
                height=400,
                background="#00D05E",
                padding={"top": 10, "left": 10, "right": 10, "bottom": 10}
            )
            .configure_view(
                fill="#00D05E",
                strokeOpacity=0
            )
            .configure_axis(
                labelColor="#000000",
                titleColor="#000000",
                gridColor="rgba(0,0,0,0.2)",
                domainColor="rgba(0,0,0,0.3)"
            )
        )

        st.altair_chart(chart_season, use_container_width=True)

    # ---------------------------------------------------------
    # MONTHLY DEMAND TREND
    # ---------------------------------------------------------
    with col4:

        st.markdown(
            """
            <div style="
                background-color:#2F75B5;
                padding:18px 25px;
                border-radius:10px;
                font-size:20px;
                color:white;
                margin-top:20px;
                margin-bottom:10px;
                text-align:center;
            ">
                <b>Monthly Seasonal Demand Trend</b>
            </div>
            """,
            unsafe_allow_html=True
        )

        month_order = [
            "January", "February", "March", "April",
            "May", "June", "July", "August",
            "September", "October", "November", "December"
        ]

        monthly_demand = (
            df.groupby("Month")["Quantity_Sold"]
            .sum()
            .reset_index()
        )

        monthly_demand["Month"] = pd.Categorical(
            monthly_demand["Month"],
            categories=month_order,
            ordered=True
        )

        monthly_demand = monthly_demand.sort_values("Month")

        chart_monthly = (
            alt.Chart(monthly_demand)
            .mark_line(
                color="#001F5C",
                strokeWidth=4,
                point=True
            )
            .encode(
                x=alt.X("Month:N", title="Months" , sort=month_order),
                y=alt.Y("Quantity_Sold:Q", title="Quantity Sold"),
                tooltip=["Month", "Quantity_Sold"]
            )
            .properties(
                height=400,
                background="#00D05E",
                padding={"top": 10, "left": 10, "right": 10, "bottom": 10}
            )
            .configure_view(
                fill="#00D05E",
                strokeOpacity=0
            )
            .configure_axis(
                labelColor="#000000",
                titleColor="#000000",
                gridColor="rgba(0,0,0,0.2)",
                domainColor="rgba(0,0,0,0.3)"
            )
        )

        st.altair_chart(chart_monthly, use_container_width=True)

        # =========================================================
    # ROW 3 → MOVING AVERAGE & FUTURE FORECAST
    # =========================================================

    st.write("")
    st.write("")

    col5, col6 = st.columns(2)

    # =========================================================
    # MOVING AVERAGE DEMAND TREND
    # =========================================================

    with col5:

        st.markdown(
            """
            <div style="
                background-color:#2F75B5;
                padding:18px 25px;
                border-radius:10px;
                font-size:20px;
                color:white;
                margin-top:20px;
                margin-bottom:10px;
                text-align:center;
            ">
                <b>Moving Average Demand Trend</b>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Convert Date column
        df["Date"] = pd.to_datetime(
            df["Date"],
            errors="coerce"
        )

        # Remove null dates
        df = df.dropna(subset=["Date"])

        # Aggregate Daily Demand
        moving_avg_df = (
            df.groupby("Date")["Quantity_Sold"]
            .sum()
            .reset_index()
            .sort_values("Date")
        )

        # Calculate 7-Day Moving Average
        moving_avg_df["7_Day_MA"] = (
            moving_avg_df["Quantity_Sold"]
            .rolling(window=7)
            .mean()
        )

        # Altair Chart
        moving_chart = (
            alt.Chart(moving_avg_df)
            .mark_line(
                color="#001F5C",
                strokeWidth=4
            )
            .encode(
                x=alt.X(
                    "Date:T",
                    title="Date"
                ),
                y=alt.Y(
                    "7_Day_MA:Q",
                    title="7-Day Moving Average"
                ),
                tooltip=[
                    alt.Tooltip("Date:T", title="Date"),
                    alt.Tooltip("7_Day_MA:Q", title="Moving Avg")
                ]
            )
            .properties(
                height=400,
                background="#00D05E",
                padding={
                    "top": 10,
                    "left": 10,
                    "right": 10,
                    "bottom": 10
                }
            )
            .configure_view(
                fill="#00D05E",
                strokeOpacity=0
            )
            .configure_axis(
                labelColor="#000000",
                titleColor="#000000",
                gridColor="rgba(0,0,0,0.2)",
                domainColor="rgba(0,0,0,0.3)"
            )
        )

        st.altair_chart(moving_chart, use_container_width=True)

    # =========================================================
    # FUTURE DEMAND FORECAST (2025–2026 MANUAL PREDICTION)
    # =========================================================

    with col6:

        st.markdown(
            """
            <div style="
                background-color:#2F75B5;
                padding:18px 25px;
                border-radius:10px;
                font-size:20px;
                color:white;
                margin-top:20px;
                margin-bottom:10px;
                text-align:center;
            ">
                <b>Future Demand Forecast</b>
            </div>
            """,
            unsafe_allow_html=True
        )

        # -----------------------------------------------------
        # PREPARE DATA
        # -----------------------------------------------------

        df["Date"] = pd.to_datetime(
            df["Date"],
            errors="coerce"
        )

        df = df.dropna(subset=["Date"])

        # Aggregate yearly demand
        yearly_demand = (
            df.groupby(df["Date"].dt.year)["Quantity_Sold"]
            .sum()
            .reset_index()
        )

        yearly_demand.columns = [
            "Year",
            "Demand"
        ]

        # -----------------------------------------------------
        # CREATE FUTURE FORECAST
        # -----------------------------------------------------

        # Simple growth forecasting
        latest_demand = yearly_demand["Demand"].iloc[-1]

        # Example growth percentages
        forecast_2025 = latest_demand * 1.10
        forecast_2026 = forecast_2025 * 1.12

        # Forecast dataframe
        forecast_df = pd.DataFrame({
            "Year": [2025, 2026],
            "Demand": [
                forecast_2025,
                forecast_2026
            ],
            "Type": [
                "Forecast",
                "Forecast"
            ]
        })

        # Historical dataframe
        historical_df = yearly_demand.copy()
        historical_df["Type"] = "Historical"

        # Combine
        final_df = pd.concat(
            [historical_df, forecast_df],
            ignore_index=True
        )

        # -----------------------------------------------------
        # FORECAST CHART
        # -----------------------------------------------------

        forecast_chart = (
            alt.Chart(final_df)
            .mark_line(
                point=True,
                strokeWidth=4
            )
            .encode(

                x=alt.X(
                    "Year:O",
                    title="Year"
                ),

                y=alt.Y(
                    "Demand:Q",
                    title="Demand Quantity"
                ),

                color=alt.Color(
                    "Type:N",
                    scale=alt.Scale(
                        domain=[
                            "Historical",
                            "Forecast"
                        ],
                        range=[
                            "#001F5C",
                            "#FF6B00"
                        ]
                    ),
                    title="Demand Type"
                ),

                tooltip=[
                    alt.Tooltip("Date:T", title="Date"),
                    alt.Tooltip("Demand_Type:N", title="Type"),
                    alt.Tooltip("Quantity:Q", title="Quantity")
                ]
            )
            .properties(
                height=400,
                background="#00D05E",
                padding={
                    "top": 10,
                    "left": 10,
                    "right": 10,
                    "bottom": 10
                }
            )
            .configure_view(
                fill="#00D05E",
                strokeOpacity=0
            )
            .configure_axis(
                labelColor="#000000",
                titleColor="#000000",
                gridColor="rgba(0,0,0,0.2)",
                domainColor="rgba(0,0,0,0.3)"
            )
        )

        st.altair_chart(forecast_chart, use_container_width=True)


# =========================================================
# 4. INVENTORY & STOCK ANALYSIS
# =========================================================

elif eda_option == "Inventory & Stock Analysis":

    st.markdown(
    """
    <div style="
        background-color:#2F75B5;
        padding:28px;
        border-radius:12px;
        color:white;
        font-size:16px;
        line-height:1.6;
        margin-bottom:20px;
    ">

    <b>What this section does:</b>

    This section analyzes inventory health, stock movement, warehouse usage, and stock risks.

    <b>Why this matters:</b>

    Helps businesses:
    <ul>
        <li>Avoid stockouts</li>
        <li>Reduce overstocking</li>
        <li>Optimize warehouse space</li>
        <li>Improve replenishment planning</li>
    </ul>

    <br>

    <b>Key insights users get:</b>
    <ul>
        <li>Fast-moving products</li>
        <li>Dead stock detection</li>
        <li>Inventory shortages</li>
        <li>Warehouse efficiency</li>
        <li>Inventory aging risks</li>
    </ul>

    </div>
    """,
    unsafe_allow_html=True
)

    st.markdown("### Inventory & Stock Analysis")

    # =====================================================
    # ROW 1
    # =====================================================

    col1, col2 = st.columns(2)

    # =====================================================
    # 1. STOCK LEVEL BY CATEGORY
    # =====================================================

    with col1:

        st.markdown(
            """
            <div style="
                background-color:#2F75B5;
                padding:18px 25px;
                border-radius:10px;
                font-size:20px;
                color:white;
                margin-top:20px;
                margin-bottom:10px;
                text-align:center;
            ">
                <b>Stock Level by Product Category</b>
            </div>
            """,
            unsafe_allow_html=True
        )

        clean_df = df[
            (df["Category"].notna()) &
            (df["Category"] != r"\N") &
            (df["Category"].str.strip() != "") &
            (df["Stock_On_Hand"].notna())
        ].copy()

          # Convert stock column to numeric
        clean_df["Stock_On_Hand"] = pd.to_numeric(
            clean_df["Stock_On_Hand"],
            errors="coerce"
        )

        # Remove invalid stock values
        clean_df = clean_df.dropna(
            subset=["Stock_On_Hand"]
        )

        stock_by_category = (
            clean_df.groupby("Category")["Stock_On_Hand"]
            .sum()
            .reset_index()
        )

        # Sort descending
        stock_by_category = (
            stock_by_category.sort_values(
                by="Stock_On_Hand",
                ascending=False
            )
            .head(10)
        )

        chart_stock = (
            alt.Chart(stock_by_category)
            .mark_bar(
                color="#001F5C",
                cornerRadiusEnd=6
            )
            .encode(
                x=alt.X(
                    "Category:N",
                    sort='-y',
                    title="Product Category"
                ),

                y=alt.Y(
                    "Stock_On_Hand:Q",
                    title="Available Stock"
                ),

                tooltip=[
                    alt.Tooltip(
                        "Category:N",
                        title="Category"
                    ),

                    alt.Tooltip(
                        "Stock_On_Hand:Q",
                        title="Stock Quantity",
                        format=",.0f"
                    )
                ]
            )
            .properties(
                height=400,
                background="#00D05E"
            )
            .configure_view(
                fill="#00D05E",
                strokeOpacity=0
            )
        )

        st.altair_chart(
            chart_stock,
            use_container_width=True
        )

    # =====================================================
    # 2. INVENTORY TURNOVER ANALYSIS
    # =====================================================

    with col2:

        st.markdown(
            """
            <div style="
                background-color:#2F75B5;
                padding:18px 25px;
                border-radius:10px;
                font-size:20px;
                color:white;
                margin-top:20px;
                margin-bottom:10px;
                text-align:center;
            ">
                <b>Inventory Turnover Analysis</b>
            </div>
            """,
            unsafe_allow_html=True
        )

        clean_df = df[
            (df["Product Name"].notna()) &
            (df["Current_Stock"].notna()) &
            (df["Quantity_Sold"].notna()) &
            (df["Category"].notna()) &
            (df["Category"] != r"\N") &
            (df["Category"].str.strip() != "")
        ]


        # -------------------------------------------------
        # CALCULATE TOTAL SALES & STOCK
        # -------------------------------------------------

        inventory_df = (
            clean_df.groupby("Product Name")
            .agg({
                "Quantity_Sold": "sum",
                "Current_Stock": "mean"
            })
            .reset_index()
        )

        # -------------------------------------------------
        # AVERAGE DAILY SALES
        # -------------------------------------------------

        # Assuming dataset contains one year of sales
        inventory_df["Avg_Daily_Sales"] = (
            inventory_df["Quantity_Sold"] / 365
        )

        inventory_df["Avg_Daily_Sales"] = (
            inventory_df["Avg_Daily_Sales"]
            .replace(0, 1)
        )

        inventory_df["Days_To_Sell"] = (
            inventory_df["Current_Stock"] /
            inventory_df["Avg_Daily_Sales"]
        )

        inventory_df = (
            inventory_df.sort_values(
                "Days_To_Sell",
                ascending=True
            )
            .head(10)
        )

        chart_inventory = (
            alt.Chart(inventory_df)
            .mark_bar(
                color="#001F5C",
                cornerRadiusEnd=6
            )
            .encode(

                y=alt.Y(
                    "Product Name:N",
                    sort='x',
                    title="Product"
                ),

                x=alt.X(
                    "Days_To_Sell:Q",
                    title="Days to Sell Inventory"
                ),

                tooltip=[

                    alt.Tooltip(
                        "Product Name:N",
                        title="Product"
                    ),

                    alt.Tooltip(
                        "Current_Stock:Q",
                        title="Current Stock",
                        format=",.0f"
                    ),

                    alt.Tooltip(
                        "Quantity_Sold:Q",
                        title="Total Sold",
                        format=",.0f"
                    ),

                    alt.Tooltip(
                        "Days_To_Sell:Q",
                        title="Days Remaining",
                        format=".1f"
                    )
                ]
            )
            .properties(
                height=400,
                background="#00D05E"
            )
            .configure_view(
                fill="#00D05E",
                strokeOpacity=0
            )
            .configure_axis(
                labelColor="#000000",
                titleColor="#000000",
                gridColor="rgba(0,0,0,0.2)",
                domainColor="rgba(0,0,0,0.3)"
            )
        )
        st.altair_chart(
            chart_inventory,
            use_container_width=True
        )

    # =====================================================
    # ROW 2
    # =====================================================

    col3, col4 = st.columns(2)

    # =====================================================
    # 3. STOCK-OUT FREQUENCY TREND
    # =====================================================

    with col3:

        st.markdown(
            """
            <div style="
                background-color:#2F75B5;
                padding:18px 25px;
                border-radius:10px;
                font-size:20px;
                color:white;
                margin-top:20px;
                margin-bottom:10px;
                text-align:center;
            ">
                <b>Stock-Out Frequency Trend</b>
            </div>
            """,
            unsafe_allow_html=True
        )

        clean_df = df.copy()

        clean_df["Date"] = pd.to_datetime(
            clean_df["Date"],
            errors="coerce"
        )

        clean_df["Stock_On_Hand"] = pd.to_numeric(
            clean_df["Stock_On_Hand"],
            errors="coerce"
        )

        clean_df = clean_df.dropna(
            subset=["Date", "Stock_On_Hand"]
        )

        # =====================================================
        # CREATE STOCK-OUT FLAG
        # =====================================================

        # =====================================================

        clean_df["Stock_Out_Flag"] = (
            clean_df["Stock_On_Hand"] <= 0
        ).astype(int)

        # =====================================================
        # MONTHLY STOCK-OUT COUNT
        # =====================================================

        clean_df["Month"] = (
            clean_df["Date"]
            .dt.strftime("%Y-%m")
        )

        stockout_df = (
            clean_df.groupby("Month")["Stock_Out_Flag"]
            .sum()
            .reset_index()
        )

        stockout_df.columns = [
            "Month",
            "Stockout_Count"
        ]
            
        chart_stockout = (
            alt.Chart(stockout_df)
            .mark_line(
                color="#001F5C",
                point={
                    "filled": True,
                    "size": 80
                },
                strokeWidth=4
            )
            .encode(

                x=alt.X(
                    "Month:N",
                    title="Month",
                    sort=list(stockout_df["Month"]),
                    axis=alt.Axis(labelAngle=-35)
                ),

                y=alt.Y(
                    "Stockout_Count:Q",
                    title="Number of Stock-Outs"
                ),
                tooltip=[

                    alt.Tooltip(
                        "Month:N",
                        title="Month"
                    ),

                    alt.Tooltip(
                        "Stockout_Count:Q",
                        title="Stock-Out Count"
                    )
                ]
            )
            .properties(
                height=400,
                background="#00D05E"
            )
            .configure_view(
                fill="#00D05E",
                strokeOpacity=0
            )
            .configure_axis(
                labelColor="#000000",
                titleColor="#000000",
                gridColor="rgba(0,0,0,0.2)",
                domainColor="rgba(0,0,0,0.3)"
            )
        )   
        st.altair_chart(
            chart_stockout,
            use_container_width=True
        )    

    # =====================================================
    # 4. DEAD STOCK ANALYSIS
    # =====================================================

    with col4:

        st.markdown(
            """
            <div style="
                background-color:#2F75B5;
                padding:18px 25px;
                border-radius:10px;
                font-size:20px;
                color:white;
                margin-top:20px;
                margin-bottom:10px;
                text-align:center;
            ">
                <b>Slow-Moving Products</b>
            </div>
            """,
            unsafe_allow_html=True
        )

        # =====================================================
        # CLEAN DATA
        # =====================================================

        clean_df = df[
            (df["Category"].notna()) &
            (df["Category"] != r"\N") &
            (df["Category"].astype(str).str.strip() != "")
        ].copy()

        # Remove \n from Product Name
        clean_df["Product Name"] = (
            clean_df["Product Name"]
            .astype(str)
            .str.replace(r"\\n", " ", regex=True)
            .str.replace(r"\n", " ", regex=True)
            .str.replace(r"\r", " ", regex=True)
            .str.strip()
        )

        # Remove empty product names
        clean_df = clean_df[
            clean_df["Product Name"].str.strip() != ""
        ]

        clean_df["Stock_On_Hand"] = pd.to_numeric(
            clean_df["Stock_On_Hand"],
            errors="coerce"
        ).fillna(0)

        clean_df["Quantity_Sold"] = pd.to_numeric(
            clean_df["Quantity_Sold"],
            errors="coerce"
        ).fillna(0)
        # =====================================================
        # DEAD STOCK DATA
        # =====================================================

        dead_stock = (
            clean_df.groupby("Product Name")
            .agg({
                "Stock_On_Hand": "sum",
                "Quantity_Sold": "sum"
            })
            .reset_index()
        )

        dead_stock = dead_stock.sort_values(
            by=["Stock_On_Hand", "Quantity_Sold"],
            ascending=[False, True]
        ).head(10)

        # =====================================================
        # BAR CHART
        # =====================================================

        chart_dead = (
            alt.Chart(dead_stock)
            .mark_bar(
                color="#001F5C",
                cornerRadiusEnd=6
            )
            .encode(

                y=alt.Y(
                    "Product Name:N",
                    sort='-x',
                    title="Product"
                ),

                x=alt.X(
                    "Stock_On_Hand:Q",
                    title="Remaining Stock"
                ),

                tooltip=[

                    alt.Tooltip(
                        "Product Name:N",
                        title="Product"
                    ),

                    alt.Tooltip(
                        "Stock_On_Hand:Q",
                        title="Remaining Stock"
                    ),

                    alt.Tooltip(
                        "Quantity_Sold:Q",
                        title="Quantity Sold"
                    )
                ]
            )
            .properties(
                height=400,
                background="#00D05E"
            )
            .configure_view(
                fill="#00D05E",
                strokeOpacity=0
            )
            .configure_axis(
                labelColor="#000000",
                titleColor="#000000",
                gridColor="rgba(0,0,0,0.2)",
                domainColor="rgba(0,0,0,0.3)"
            )
        )

        st.altair_chart(
            chart_dead,
            use_container_width=True
        )
    # =====================================================
    # ROW 3
    # =====================================================

    col5, col6 = st.columns(2)

    # =====================================================
    # 5. WAREHOUSE UTILIZATION
    # =====================================================

    with col5:

        st.markdown(
            """
            <div style="
                background-color:#2F75B5;
                padding:18px 25px;
                border-radius:10px;
                font-size:20px;
                color:white;
                margin-top:20px;
                margin-bottom:10px;
                text-align:center;
            ">
                <b>Warehouse Utilization Analysis</b>
            </div>
            """,
            unsafe_allow_html=True
        )

        used_capacity = df["WH_Quantity_On_Hand"].sum()
        total_capacity = df["Capacity"].sum()

        utilization_df = pd.DataFrame({
            "Type": [
                "Used Capacity",
                "Available Capacity"
            ],
            "Value": [
                used_capacity,
                max(total_capacity - used_capacity, 0)
            ]
        })

        chart_utilization = (
            alt.Chart(utilization_df)
            .mark_arc(innerRadius=80)
            .encode(
                theta="Value:Q",
                color="Type:N",
                tooltip=[
                    "Type",
                    "Value"
                ]
            )
            .properties(
                height=400,
                background="#00D05E"
            )
        )

        st.altair_chart(
            chart_utilization,
            use_container_width=True
        )

    # =====================================================
    # 6. INVENTORY AGING ANALYSIS
    # =====================================================

    with col6:

        st.markdown(
            """
            <div style="
                background-color:#2F75B5;
                padding:18px 25px;
                border-radius:10px;
                font-size:20px;
                color:white;
                margin-top:20px;
                margin-bottom:10px;
                text-align:center;
            ">
                <b>Inventory Aging Analysis</b>
            </div>
            """,
            unsafe_allow_html=True
        )

        # =====================================================
        # REMOVE \n COMPLETELY FROM CATEGORY
        # =====================================================

        df = df[
            (df["Category"].notna()) &
            (df["Category"] != r"\N") &
            (df["Category"].str.strip() != "")
        ]

        # Convert date column
        df["Last_Updated"] = pd.to_datetime(
            df["Last_Updated"],
            errors="coerce"
        )

        # Current date
        today = pd.Timestamp.today()

        # Calculate aging days
        df["Inventory_Age_Days"] = (
            today - df["Last_Updated"]
        ).dt.days

        # Average aging by category
        aging_df = (
            df.groupby("Category")["Inventory_Age_Days"]
            .mean()
            .reset_index()
        )

        # Sort values
        aging_df = aging_df.sort_values(
            by="Inventory_Age_Days",
            ascending=False
        )

        # =====================================================
        # BAR CHART
        # =====================================================

        chart_aging = (
            alt.Chart(aging_df)
            .mark_bar(
                color="#001F5C",
                cornerRadiusEnd=6
            )
            .encode(

                y=alt.Y(
                    "Category:N",
                    sort='-x',
                    title="Category"
                ),

                x=alt.X(
                    "Inventory_Age_Days:Q",
                    title="Average Aging Days"
                ),

                tooltip=[

                    alt.Tooltip(
                        "Category:N",
                        title="Category"
                    ),

                    alt.Tooltip(
                        "Inventory_Age_Days:Q",
                        title="Avg Aging Days",
                        format=".1f"
                    )
                ]
            )
            .properties(
                height=400,
                background="#00D05E"
            )
            .configure_view(
                fill="#00D05E",
                strokeOpacity=0
            )
            .configure_axis(
                labelColor="#000000",
                titleColor="#000000",
                gridColor="rgba(0,0,0,0.2)",
                domainColor="rgba(0,0,0,0.3)"
            )
        )

        st.altair_chart(
            chart_aging,
            use_container_width=True
        )

# =========================================================
# Predictive REPLENISHMENT ANALYSIS
# =========================================================

elif eda_option == "Predictive Replenishment Analysis":

    st.markdown(
    """
    <div style="
        background-color:#2F75B5;
        padding:28px;
        border-radius:12px;
        color:white;
        font-size:16px;
        line-height:1.7;
        margin-bottom:20px;
    ">

    <b>What this section does:</b><br>

    This section focuses on inventory risk monitoring,
    replenishment planning, and smart procurement decisions.

    <ul>
        <li>Stock risk analysis</li>
        <li>Reorder monitoring</li>
        <li>Safety stock tracking</li>
        <li>Inventory replenishment prioritization</li>
    </ul>

    <b>Why this matters:</b>
    <ul>
        <li>Prevents stock-outs</li>
        <li>Improves inventory planning</li>
        <li>Supports AI-based replenishment</li>
        <li>Optimizes procurement efficiency</li>
    </ul>

    <b>Business Value:</b>
    <ul>
        <li>Reduces inventory shortages</li>
        <li>Improves warehouse availability</li>
        <li>Automates replenishment decisions</li>
        <li>Enhances operational efficiency</li>
    </ul>

    </div>
    """,
    unsafe_allow_html=True
)

    # =====================================================
    # DATA CLEANING
    # =====================================================

    numeric_cols = [
        "Current_Stock",
        "Reorder_Point",
        "Recommended_Order_Quantity",
        "Safety_Stock_Level",
        "Stockout_Risk"
    ]

    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # =====================================================
    # CREATE RISK CATEGORY
    # =====================================================

    def risk_category(x):
        if pd.isna(x):
            return "Unknown"
        elif x >= 70:
            return "High Risk"
        elif x >= 40:
            return "Medium Risk"
        else:
            return "Low Risk"

    df["Risk_Category"] = df["Stockout_Risk"].apply(risk_category)

    # =====================================================
    # ROW 1
    # =====================================================

    col1, col2 = st.columns(2)

    # =====================================================
    # 1. STOCK VS REORDER POINT
    # =====================================================

    with col1:

        st.markdown(
        """
        <div style="
            background-color:#2F75B5;
            padding:18px 25px;
            border-radius:10px;
            font-size:20px;
            color:white;
            margin-top:20px;
            margin-bottom:10px;
            text-align:center;
        ">
            <b>Stock vs Reorder Point</b>
        </div>
        """,
        unsafe_allow_html=True
    )

        stock_compare = (
            df.groupby("SKU_ID")[[
                "Current_Stock",
                "Reorder_Point"
            ]]
            .mean()
            .reset_index()
            .head(15)
        )

        stock_compare_melt = stock_compare.melt(
            id_vars="SKU_ID",
            var_name="Metric",
            value_name="Value"
        )

        chart_stock = (
            alt.Chart(stock_compare_melt)
            .mark_bar()
            .encode(
                x=alt.X("SKU_ID:N", title="SKU"),
                y=alt.Y("Value:Q", title="Stock Level"),
                color="Metric:N",
                xOffset="Metric:N",
                tooltip=["SKU_ID", "Metric", "Value"]
            )
            .properties(
                height=400,
                background="#00D05E"
            )
            .configure_view(
                fill="#00D05E",
                strokeOpacity=0
            )
        )

        st.altair_chart(chart_stock, use_container_width=True)

    # =====================================================
    # 2. RECOMMENDED REORDER QUANTITY
    # =====================================================

    with col2:

        st.markdown(
        """
        <div style="
            background-color:#2F75B5;
            padding:18px 25px;
            border-radius:10px;
            font-size:20px;
            color:white;
            margin-top:20px;
            margin-bottom:10px;
            text-align:center;
        ">
            <b>Recommended Reorder Quantity</b>
        </div>
        """,
        unsafe_allow_html=True
    )

        # =====================================================
        # CLEAN DATA
        # =====================================================

        df = df[
            (df["Category"].notna()) &
            (df["Category"] != r"\N") &
            (df["Category"].astype(str).str.strip() != "")
        ].copy()

        # Remove \n from Product Name
        df["Product Name"] = (
            df["Product Name"]
            .astype(str)
            .str.replace(r"\\n", " ", regex=True)
            .str.replace(r"\n", " ", regex=True)
            .str.replace(r"\r", " ", regex=True)
            .str.strip()
        )

        # Convert reorder quantity to numeric
        df["Recommended_Order_Quantity"] = pd.to_numeric(
            df["Recommended_Order_Quantity"],
            errors="coerce"
        ).fillna(0)

        # =====================================================
        # REORDER DATA
        # =====================================================

        reorder_qty = (
            df.groupby("Product Name")["Recommended_Order_Quantity"]
            .mean()
            .sort_values(ascending=False)
            .head(15)
            .reset_index()
        )

        # =====================================================
        # BAR CHART
        # =====================================================

        chart_reorder = (
            alt.Chart(reorder_qty)
            .mark_bar(
                color="#001F5C",
                cornerRadiusEnd=6
            )
            .encode(

                y=alt.Y(
                    "Product Name:N",
                    sort='-x',
                    title="Product"
                ),

                x=alt.X(
                    "Recommended_Order_Quantity:Q",
                    title="Recommended Quantity"
                ),

                tooltip=[

                    alt.Tooltip(
                        "Product Name:N",
                        title="Product"
                    ),

                    alt.Tooltip(
                        "Recommended_Order_Quantity:Q",
                        title="Recommended Quantity",
                        format=".1f"
                    )
                ]
            )
            .properties(
                height=400,
                background="#00D05E"
            )
            .configure_view(
                fill="#00D05E",
                strokeOpacity=0
            )
            .configure_axis(
                labelColor="#000000",
                titleColor="#000000",
                gridColor="rgba(0,0,0,0.2)",
                domainColor="rgba(0,0,0,0.3)"
            )
        )

        st.altair_chart(
            chart_reorder,
            use_container_width=True
        )
    # =====================================================
    # ROW 2
    # =====================================================

    col3, col4 = st.columns(2)
    # =====================================================
    # 3. SAFETY STOCK COMPARISON
    # =====================================================

    with col3:

        st.markdown(
        """
        <div style="
            background-color:#2F75B5;
            padding:18px 25px;
            border-radius:10px;
            font-size:20px;
            color:white;
            margin-top:20px;
            margin-bottom:10px;
            text-align:center;
        ">
            <b>Safety Stock Comparison</b>
        </div>
        """,
        unsafe_allow_html=True
    )

        safety_stock = (
            df.groupby("SKU_ID")[[
                "Current_Stock",
                "Safety_Stock_Level"
            ]]
            .mean()
            .reset_index()
            .head(15)
        )

        safety_stock_melt = safety_stock.melt(
            id_vars="SKU_ID",
            var_name="Metric",
            value_name="Value"
        )

        chart_safety = (
            alt.Chart(safety_stock_melt)
            .mark_bar()
            .encode(
                x=alt.X("SKU_ID:N", title="SKU"),
                y=alt.Y("Value:Q", title="Stock Level"),
                color="Metric:N",
                xOffset="Metric:N",
                tooltip=["SKU_ID", "Metric", "Value"]
            )
            .properties(
                height=400,
                background="#00D05E"
            )
            .configure_view(
                fill="#00D05E",
                strokeOpacity=0
            )
        )

        st.altair_chart(chart_safety, use_container_width=True)

    # =====================================================
    # 4. REPLENISHMENT PRIORITY HEATMAP
    # =====================================================

    with col4:

        st.markdown(
        """
        <div style="
            background-color:#2F75B5;
            padding:18px 25px;
            border-radius:10px;
            font-size:20px;
            color:white;
            margin-top:20px;
            margin-bottom:10px;
            text-align:center;
        ">
            <b>Replenishment Priority Heatmap</b>
        </div>
        """,
        unsafe_allow_html=True
    )

        # =====================================================
        # CLEAN DATA
        # =====================================================

        clean_df = df.copy()

        # Remove invalid categories
        clean_df = clean_df[
            (clean_df["Category"].notna()) &
            (clean_df["Category"] != r"\N") &
            (clean_df["Category"].astype(str).str.strip() != "")
        ]

        # Clean Product Name
        clean_df["Product Name"] = (
            clean_df["Product Name"]
            .astype(str)
            .str.replace(r"\\n", " ", regex=True)
            .str.replace(r"\n", " ", regex=True)
            .str.replace(r"\r", " ", regex=True)
            .str.strip()
        )

        # =====================================================
        # NUMERIC CONVERSION
        # =====================================================

        clean_df["Recommended_Order_Quantity"] = pd.to_numeric(
            clean_df["Recommended_Order_Quantity"],
            errors="coerce"
        ).fillna(1)

        clean_df["Stockout_Risk"] = pd.to_numeric(
            clean_df["Stockout_Risk"],
            errors="coerce"
        ).fillna(1)

        # =====================================================
        # CREATE PRIORITY DATA
        # =====================================================

        priority_df = (
            clean_df.groupby([
                "Category",
                "Product Name"
            ])
            .agg({
                "Recommended_Order_Quantity": "mean",
                "Stockout_Risk": "mean"
            })
            .reset_index()
        )

        # =====================================================
        # PRIORITY SCORE
        # =====================================================

        priority_df["Priority_Score"] = (
            priority_df["Recommended_Order_Quantity"] +
            priority_df["Stockout_Risk"]
        )

        # Remove invalid values
        priority_df = priority_df.dropna(
            subset=["Priority_Score"]
        )

        # Keep top products
        priority_df = priority_df.sort_values(
            by="Priority_Score",
            ascending=False
        ).head(20)

        # =====================================================
        # HEATMAP
        # =====================================================

        chart_priority = (
            alt.Chart(priority_df)
            .mark_rect()
            .encode(

                x=alt.X(
                    "Category:N",
                    title="Category"
                ),

                y=alt.Y(
                    "Product Name:N",
                    title="Product",
                    sort='-x'
                ),

                color=alt.Color(
                    "Priority_Score:Q",
                    title="Priority Score",
                    scale=alt.Scale(scheme="reds")
                ),

                tooltip=[

                    alt.Tooltip(
                        "Category:N",
                        title="Category"
                    ),

                    alt.Tooltip(
                        "Product Name:N",
                        title="Product"
                    ),

                    alt.Tooltip(
                        "Priority_Score:Q",
                        title="Priority Score",
                        format=".2f"
                    ),

                    alt.Tooltip(
                        "Recommended_Order_Quantity:Q",
                        title="Recommended Quantity",
                        format=".2f"
                    ),

                    alt.Tooltip(
                        "Stockout_Risk:Q",
                        title="Stockout Risk",
                        format=".2f"
                    )
                ]
            )
            .properties(
                height=400,
                background="#00D05E"
            )
            .configure_view(
                fill="#00D05E",
                strokeOpacity=0
            )
            .configure_axis(
                labelColor="#000000",
                titleColor="#000000",
                labelFontSize=10,
                titleFontSize=12,
                grid=False
            )
        )

        st.altair_chart(
            chart_priority,
            use_container_width=True
        )
# =========================================================
# SUPPLIER & LEAD TIME ANALYSIS
# =========================================================

elif eda_option == "Supplier & Lead Time Analysis":

    st.markdown(
    """
    <div style="
        background-color:#2F75B5;
        padding:28px;
        border-radius:12px;
        color:white;
        font-size:16px;
        line-height:1.7;
        margin-bottom:20px;
    ">

    <b>What this section does:</b><br>

    This section evaluates supplier reliability, procurement efficiency,
    and delivery performance.

    <ul>
        <li>Lead time analysis</li>
        <li>Delivery performance monitoring</li>
        <li>Supplier benchmarking</li>
        <li>Procurement delay tracking</li>
    </ul>

    <b>Why this matters:</b>
    <ul>
        <li>Prevents replenishment delays</li>
        <li>Improves supplier selection</li>
        <li>Reduces stock-out risks</li>
        <li>Optimizes procurement planning</li>
    </ul>

    <b>Business Value:</b>
    <ul>
        <li>Better supplier management</li>
        <li>Faster inventory replenishment</li>
        <li>Improved supply chain stability</li>
        <li>Supports AI procurement optimization</li>
    </ul>

    </div>
    """,
    unsafe_allow_html=True
)

    # =====================================================
    # DATA CLEANING
    # =====================================================

    df["Lead_Time_Days"] = pd.to_numeric(df["Lead_Time_Days"], errors="coerce")
    df["Delivery_Delay_Days"] = pd.to_numeric(df["Delivery_Delay_Days"], errors="coerce")
    df["Supplier_Rating"] = pd.to_numeric(df["Supplier_Rating"], errors="coerce")
    df["On_Time_Delivery_Rate"] = pd.to_numeric(df["On_Time_Delivery_Rate"], errors="coerce")
    df["Unit_Cost"] = pd.to_numeric(df["Unit_Cost"], errors="coerce")
    df["Reliability_Score"] = pd.to_numeric(df["Reliability_Score"], errors="coerce")

    # =====================================================
    # ROW 1
    # =====================================================

    col1, col2 = st.columns(2)

    # =====================================================
    # 1. LEAD TIME BY SUPPLIER
    # =====================================================

    with col1:

        st.markdown(
        """
        <div style="
            background-color:#2F75B5;
            padding:18px 25px;
            border-radius:10px;
            font-size:20px;
            color:white;
            margin-top:20px;
            margin-bottom:10px;
            text-align:center;
        ">
            <b>Lead Time by Supplier</b>
        </div>
        """,
        unsafe_allow_html=True
    )

        lead_time = (
            df.groupby("Supplier_Name")["Lead_Time_Days"]
            .mean()
            .sort_values(ascending=False)
            .head(10)
            .reset_index()
        )

        chart_lead = (
            alt.Chart(lead_time)
            .mark_bar(color="#001F5C", cornerRadiusEnd=6)
            .encode(
                y=alt.Y(
                    "Supplier_Name:N",
                    sort='-x',
                    title="Supplier"
                ),
                x=alt.X(
                    "Lead_Time_Days:Q",
                    title="Average Lead Time"
                ),
                tooltip=["Supplier_Name", "Lead_Time_Days"]
            )
            .properties(
                height=400,
                background="#00D05E"
            )
            .configure_view(
                fill="#00D05E",
                strokeOpacity=0
            )
        )

        st.altair_chart(chart_lead, use_container_width=True)

    # =====================================================
    # 2. ON-TIME DELIVERY RATE
    # =====================================================

    with col2:

        st.markdown(
        """
        <div style="
            background-color:#2F75B5;
            padding:18px 25px;
            border-radius:10px;
            font-size:20px;
            color:white;
            margin-top:20px;
            margin-bottom:10px;
            text-align:center;
        ">
            <b>On-Time Delivery Rate</b>
        </div>
        """,
        unsafe_allow_html=True
    )

        # =====================================================
        # DELIVERY DATA
        # =====================================================

        delivery_status = (
            df["On_Time_Delivery_Flag"]
            .value_counts()
            .reset_index()
        )

        delivery_status.columns = [
            "Delivery_Status",
            "Count"
        ]

        # =====================================================
        # PERCENTAGE
        # =====================================================

        total = delivery_status["Count"].sum()

        delivery_status["Percentage"] = (
            delivery_status["Count"] / total * 100
        ).round(1)

        # =====================================================
        # DONUT CHART
        # =====================================================

        chart_delivery = (
            alt.Chart(delivery_status)
            .mark_arc(
                innerRadius=80
            )
            .encode(

                theta=alt.Theta(
                    "Count:Q"
                ),

                color=alt.Color(
                    "Delivery_Status:N",
                    title="Delivery Status"
                ),

                tooltip=[

                    alt.Tooltip(
                        "Delivery_Status:N",
                        title="Delivery Status"
                    ),

                    alt.Tooltip(
                        "Count:Q",
                        title="Count"
                    ),

                    alt.Tooltip(
                        "Percentage:Q",
                        title="Percentage (%)",
                        format=".1f"
                    )
                ]
            )
            .properties(
                height=400,
                background="#00D05E"
            )
            .configure_view(
                fill="#00D05E",
                strokeOpacity=0
            )
        )

        st.altair_chart(
            chart_delivery,
            use_container_width=True
        )

    # =====================================================
    # ROW 2
    # =====================================================

    col3, col4 = st.columns(2)

    # =====================================================
    # 3. DELIVERY DELAY ANALYSIS
    # =====================================================

    with col3:

        st.markdown(
        """
        <div style="
            background-color:#2F75B5;
            padding:18px 25px;
            border-radius:10px;
            font-size:20px;
            color:white;
            margin-top:20px;
            margin-bottom:10px;
            text-align:center;
        ">
            <b>Delivery Delay Analysis</b>
        </div>
        """,
        unsafe_allow_html=True
    )

        # =====================================================
        # CLEAN DATA
        # =====================================================

        delay_df = df.copy()

        delay_df["Delivery_Delay_Days"] = pd.to_numeric(
            delay_df["Delivery_Delay_Days"],
            errors="coerce"
        ).fillna(0)

        # =====================================================
        # CREATE DELAY CATEGORIES
        # =====================================================

        def classify_delay(days):

            if days <= 0:
                return "On Time"

            elif days <= 3:
                return "Minor Delay"

            elif days <= 7:
                return "Moderate Delay"

            else:
                return "Severe Delay"

        delay_df["Delay_Category"] = (
            delay_df["Delivery_Delay_Days"]
            .apply(classify_delay)
        )

        # =====================================================
        # COUNT CATEGORIES
        # =====================================================

        delay_summary = (
            delay_df["Delay_Category"]
            .value_counts()
            .reset_index()
        )

        delay_summary.columns = [
            "Delay_Category",
            "Count"
        ]

        # =====================================================
        # BAR CHART
        # =====================================================

        chart_delay = (
            alt.Chart(delay_summary)
            .mark_bar(
                color="#001F5C",
                cornerRadiusEnd=6
            )
            .encode(

                y=alt.Y(
                    "Delay_Category:N",
                    sort=[
                        "On Time",
                        "Minor Delay",
                        "Moderate Delay",
                        "Severe Delay"
                    ],
                    title="Delivery Status"
                ),

                x=alt.X(
                    "Count:Q",
                    title="Number of Deliveries"
                ),

                tooltip=[

                    alt.Tooltip(
                        "Delay_Category:N",
                        title="Category"
                    ),

                    alt.Tooltip(
                        "Count:Q",
                        title="Deliveries"
                    )
                ]
            )
            .properties(
                height=400,
                background="#00D05E"
            )
            .configure_view(
                fill="#00D05E",
                strokeOpacity=0
            )
            .configure_axis(
                labelColor="#000000",
                titleColor="#000000",
                gridColor="rgba(0,0,0,0.2)",
                domainColor="rgba(0,0,0,0.3)"
            )
        )

        st.altair_chart(
            chart_delay,
            use_container_width=True
        )
    # =====================================================
    # 4. SUPPLIER PERFORMANCE COMPARISON
    # =====================================================

    with col4:

        st.markdown(
        """
        <div style="
            background-color:#2F75B5;
            padding:18px 25px;
            border-radius:10px;
            font-size:20px;
            color:white;
            margin-top:20px;
            margin-bottom:10px;
            text-align:center;
        ">
            <b>Supplier Performance Comparison</b>
        </div>
        """,
        unsafe_allow_html=True
    )

        # =====================================================
        # CLEAN DATA
        # =====================================================

        supplier_df = df.copy()

        numeric_cols = [
            "On_Time_Delivery_Rate",
            "Lead_Time_Days",
            "Supplier_Rating"
        ]

        for col in numeric_cols:

            supplier_df[col] = pd.to_numeric(
                supplier_df[col],
                errors="coerce"
            ).fillna(0)

        # =====================================================
        # CONVERT METRICS TO SCORE OUT OF 10
        # =====================================================

        # On-Time Delivery Score out of 10
        supplier_df["Delivery_Score_10"] = (
            supplier_df["On_Time_Delivery_Rate"] * 10
        ).clip(0, 10)

        # Supplier Rating out of 10
        supplier_df["Supplier_Rating_10"] = (
            supplier_df["Supplier_Rating"]
        ).clip(0, 10)

        # Lower lead time is better
        max_lead = supplier_df["Lead_Time_Days"].max()

        supplier_df["Lead_Time_Score_10"] = (
            (1 - (supplier_df["Lead_Time_Days"] / max_lead)) * 10
        ).clip(0, 10)

        # =====================================================
        # SUPPLIER PERFORMANCE DATA
        # =====================================================

        supplier_perf = (
            supplier_df.groupby("Supplier_Name")[[
                "Delivery_Score_10",
                "Lead_Time_Score_10",
                "Supplier_Rating_10"
            ]]
            .mean()
            .reset_index()
            .head(8)
        )

        # Rename columns
        supplier_perf.columns = [
            "Supplier_Name",
            "On-Time Delivery",
            "Lead Time",
            "Supplier Rating"
        ]

        # =====================================================
        # MELT DATA
        # =====================================================

        supplier_perf_melt = supplier_perf.melt(
            id_vars="Supplier_Name",
            var_name="Metric",
            value_name="Score"
        )

        # =====================================================
        # GROUPED BAR CHART
        # =====================================================

        chart_perf = (
            alt.Chart(supplier_perf_melt)
            .mark_bar(cornerRadiusTopRight=4,
                    cornerRadiusTopLeft=4)
            .encode(

                x=alt.X(
                    "Supplier_Name:N",
                    title="Supplier"
                ),

                y=alt.Y(
                    "Score:Q",
                    title="Performance Score (Out of 10)",
                    scale=alt.Scale(domain=[0, 10])
                ),

                color=alt.Color(
                    "Metric:N",
                    title="Performance Metric"
                ),

                xOffset="Metric:N",

                tooltip=[

                    alt.Tooltip(
                        "Supplier_Name:N",
                        title="Supplier"
                    ),

                    alt.Tooltip(
                        "Metric:N",
                        title="Metric"
                    ),

                    alt.Tooltip(
                        "Score:Q",
                        title="Score",
                        format=".1f"
                    )
                ]
            )
            .properties(
                height=400,
                background="#00D05E"
            )
            .configure_view(
                fill="#00D05E",
                strokeOpacity=0
            )
            .configure_axis(
                labelColor="#000000",
                titleColor="#000000",
                gridColor="rgba(0,0,0,0.2)",
                domainColor="rgba(0,0,0,0.3)"
            )
        )

        st.altair_chart(
            chart_perf,
            use_container_width=True
        )
        

# =========================================================
# STORE-LEVEL ANALYSIS
# =========================================================

elif eda_option == "Store-Level Analysis":

    st.markdown(
    """
    <div style="
        background-color:#2F75B5;
        padding:28px;
        border-radius:12px;
        color:white;
        font-size:16px;
        line-height:1.7;
        margin-bottom:20px;
    ">

    <b>What this section does:</b><br>

    This section analyzes how each store/location performs in terms of:
    <ul>
        <li>Sales performance</li>
        <li>Demand behavior</li>
        <li>Inventory availability</li>
        <li>Operational efficiency</li>
    </ul>

    <b>Why this matters:</b>
    <ul>
        <li>Identify high-performing stores</li>
        <li>Detect low-stock locations</li>
        <li>Understand regional demand</li>
        <li>Optimize replenishment strategy</li>
    </ul>

    <b>Business Value:</b>
    <ul>
        <li>Improves store-level forecasting</li>
        <li>Reduces stock-outs</li>
        <li>Supports regional inventory planning</li>
        <li>Enhances operational efficiency</li>
    </ul>

    </div>
    """,
    unsafe_allow_html=True
)

    # =====================================================
    # CLEANING
    # =====================================================

    df["Sales_Revenue"] = pd.to_numeric(df["Sales_Revenue"], errors="coerce")
    df["Quantity_Sold"] = pd.to_numeric(df["Quantity_Sold"], errors="coerce")
    df["Stock_On_Hand"] = pd.to_numeric(df["Stock_On_Hand"], errors="coerce")
    df["Area_sqft"] = pd.to_numeric(df["Area_sqft"], errors="coerce")
    df["On_Time_Delivery_Rate"] = pd.to_numeric(df["On_Time_Delivery_Rate"], errors="coerce")

    # =====================================================
    # ROW 1
    # =====================================================

    col1, col2 = st.columns(2)

    # =====================================================
    # 1. STORE TYPE PERFORMANCE
    # =====================================================

    with col1:

        st.markdown(
        """
        <div style="
            background-color:#2F75B5;
            padding:18px 25px;
            border-radius:10px;
            font-size:20px;
            color:white;
            margin-top:20px;
            margin-bottom:10px;
            text-align:center;
        ">
            <b>Store Type Performance</b>
        </div>
        """,
        unsafe_allow_html=True
    )

        type_sales = (
            df.groupby("Store_Type")["Sales_Revenue"]
            .sum()
            .sort_values(ascending=False)
            .reset_index()
        )

        chart_type = (
            alt.Chart(type_sales)
            .mark_bar(color="#001F5C", cornerRadiusEnd=6)
            .encode(
                x=alt.X("Store_Type:N", title="Store Type"),
                y=alt.Y("Sales_Revenue:Q", title="Revenue"),
                tooltip=["Store_Type", "Sales_Revenue"]
            )
            .properties(
                height=400,
                background="#00D05E"
            )
            .configure_view(
                fill="#00D05E",
                strokeOpacity=0
            )
        )

        st.altair_chart(chart_type, use_container_width=True)

    # =====================================================
    # 2. STORE-WISE SALES PERFORMANCE
    # =====================================================

    with col2:

        st.markdown(
        """
        <div style="
            background-color:#2F75B5;
            padding:18px 25px;
            border-radius:10px;
            font-size:20px;
            color:white;
            margin-top:20px;
            margin-bottom:10px;
            text-align:center;
        ">
            <b>Store-Wise Sales Performance</b>
        </div>
        """,
        unsafe_allow_html=True
    )

        store_sales = (
            df.groupby("Store_Name")["Sales_Revenue"]
            .sum()
            .sort_values(ascending=False)
            .head(10)
            .reset_index()
        )

        chart_store_sales = (
            alt.Chart(store_sales)
            .mark_bar(color="#001F5C", cornerRadiusEnd=6)
            .encode(
                x=alt.X(
                    "Store_Name:N",
                    sort='-y',
                    title="Store"
                ),
                y=alt.Y(
                    "Sales_Revenue:Q",
                    title="Revenue"
                ),
                tooltip=["Store_Name", "Sales_Revenue"]
            )
            .properties(
                height=400,
                background="#00D05E"
            )
            .configure_view(
                fill="#00D05E",
                strokeOpacity=0
            )
        )

        st.altair_chart(chart_store_sales, use_container_width=True)
    
    # =====================================================
    # ROW 2
    # =====================================================

    col3, col4 = st.columns(2)

    # =====================================================
    # 3. CITY-WISE SALES
    # =====================================================

    with col3:

        st.markdown(
        """
        <div style="
            background-color:#2F75B5;
            padding:18px 25px;
            border-radius:10px;
            font-size:20px;
            color:white;
            margin-top:20px;
            margin-bottom:10px;
            text-align:center;
        ">
            <b>City-Wise Sales</b>
        </div>
        """,
        unsafe_allow_html=True
    )

        city_sales = (
            df.groupby("City")["Sales_Revenue"]
            .sum()
            .sort_values(ascending=False)
            .head(10)
            .reset_index()
        )

        chart_city = (
            alt.Chart(city_sales)
            .mark_bar(color="#001F5C", cornerRadiusEnd=6)
            .encode(
                y=alt.Y(
                    "City:N",
                    sort='-x',
                    title="City"
                ),
                x=alt.X(
                    "Sales_Revenue:Q",
                    title="Revenue"
                ),
                tooltip=["City", "Sales_Revenue"]
            )
            .properties(
                height=400,
                background="#00D05E"
            )
            .configure_view(
                fill="#00D05E",
                strokeOpacity=0
            )
        )

        st.altair_chart(chart_city, use_container_width=True)

    # =====================================================
    # 4. STORE AREA VS SALES
    # =====================================================

    with col4:

        st.markdown(
        """
        <div style="
            background-color:#2F75B5;
            padding:18px 25px;
            border-radius:10px;
            font-size:20px;
            color:white;
            margin-top:20px;
            margin-bottom:10px;
            text-align:center;
        ">
            <b>Top Store Sales Analysis</b>
        </div>
        """,
        unsafe_allow_html=True
    )

        # =====================================================
        # CLEAN DATA
        # =====================================================

        store_df = df.copy()

        store_df["Area_sqft"] = pd.to_numeric(
            store_df["Area_sqft"],
            errors="coerce"
        ).fillna(0)

        store_df["Sales_Revenue"] = pd.to_numeric(
            store_df["Sales_Revenue"],
            errors="coerce"
        ).fillna(0)

        # =====================================================
        # STORE SUMMARY
        # =====================================================

        sales_df = (
            store_df.groupby("Store_Name")[[
                "Area_sqft",
                "Sales_Revenue"
            ]]
            .mean()
            .reset_index()
        )

        # Top stores by sales
        sales_df = sales_df.sort_values(
            by="Sales_Revenue",
            ascending=False
        ).head(15)

        # =====================================================
        # BAR CHART
        # =====================================================

        chart_area_sales = (
            alt.Chart(sales_df)
            .mark_bar(
                color="#001F5C",
                cornerRadiusEnd=6
            )
            .encode(

                y=alt.Y(
                    "Store_Name:N",
                    sort='-x',
                    title="Store"
                ),

                x=alt.X(
                    "Sales_Revenue:Q",
                    title="Average Sales Revenue"
                ),

                tooltip=[

                    alt.Tooltip(
                        "Store_Name:N",
                        title="Store"
                    ),

                    alt.Tooltip(
                        "Sales_Revenue:Q",
                        title="Sales Revenue",
                        format=".2f"
                    ),

                    alt.Tooltip(
                        "Area_sqft:Q",
                        title="Store Area (sqft)",
                        format=".0f"
                    )
                ]
            )
            .properties(
                height=400,
                background="#00D05E"
            )
            .configure_view(
                fill="#00D05E",
                strokeOpacity=0
            )
            .configure_axis(
                labelColor="#000000",
                titleColor="#000000",
                gridColor="rgba(0,0,0,0.2)",
                domainColor="rgba(0,0,0,0.3)"
            )
        )

        st.altair_chart(
            chart_area_sales,
            use_container_width=True
        )
    # =====================================================
    # ROW 3
    # =====================================================

    col5, col6 = st.columns(2)

    # =====================================================
    # 5. STORE INVENTORY AVAILABILITY
    # =====================================================

    with col5:

        st.markdown(
        """
        <div style="
            background-color:#2F75B5;
            padding:18px 25px;
            border-radius:10px;
            font-size:20px;
            color:white;
            margin-top:20px;
            margin-bottom:10px;
            text-align:center;
        ">
            <b>Store Inventory Availability</b>
        </div>
        """,
        unsafe_allow_html=True
    )

        inventory_store = (
            df.groupby("Store_Name")["Stock_On_Hand"]
            .sum()
            .sort_values(ascending=False)
            .head(10)
            .reset_index()
        )

        chart_inventory = (
            alt.Chart(inventory_store)
            .mark_bar(color="#001F5C", cornerRadiusEnd=6)
            .encode(
                x=alt.X("Store_Name:N", sort='-y', title="Store"),
                y=alt.Y("Stock_On_Hand:Q", title="Available Stock"),
                tooltip=["Store_Name", "Stock_On_Hand"]
            )
            .properties(
                height=400,
                background="#00D05E"
            )
            .configure_view(
                fill="#00D05E",
                strokeOpacity=0
            )
        )

        st.altair_chart(chart_inventory, use_container_width=True)

    # =====================================================
    # 6. STORE REPLENISHMENT EFFICIENCY
    # =====================================================

    with col6:

        st.markdown(
        """
        <div style="
            background-color:#2F75B5;
            padding:18px 25px;
            border-radius:10px;
            font-size:20px;
            color:white;
            margin-top:20px;
            margin-bottom:10px;
            text-align:center;
        ">
            <b>Store Replenishment Efficiency</b>
        </div>
        """,
        unsafe_allow_html=True
    )

        replenishment = (
            df.groupby("Store_Name")["On_Time_Delivery_Rate"]
            .mean()
            .sort_values(ascending=False)
            .head(10)
            .reset_index()
        )

        chart_replenishment = (
            alt.Chart(replenishment)
            .mark_bar(color="#001F5C", cornerRadiusEnd=6)
            .encode(
                y=alt.Y(
                    "Store_Name:N",
                    sort='-x',
                    title="Store"
                ),
                x=alt.X(
                    "On_Time_Delivery_Rate:Q",
                    title="Delivery Rate"
                ),
                tooltip=[
                    "Store_Name",
                    "On_Time_Delivery_Rate"
                ]
            )
            .properties(
                height=400,
                background="#00D05E"
            )
            .configure_view(
                fill="#00D05E",
                strokeOpacity=0
            )
        )

        st.altair_chart(chart_replenishment, use_container_width=True)

# =========================================================
# EXTERNAL FACTORS IMPACT ANALYSIS
# =========================================================

elif eda_option == "External Factors Impact Analysis":

    st.markdown(
    """
    <div style="
        background-color:#2F75B5;
        padding:28px;
        border-radius:12px;
        color:white;
        font-size:16px;
        line-height:1.6;
        margin-bottom:20px;
    ">

    <b>What this section does:</b>

    Analyzes how external factors influence product demand,
    sales behavior, and replenishment planning.

    <b>External factors include:</b>
    <ul>
        <li>Weather conditions</li>
        <li>Festivals & events</li>
        <li>Promotions & discounts</li>
        <li>Price changes</li>
        <li>Social media trends</li>
        <li>Customer sentiment</li>
    </ul>

    <br>

    <b>Business Value:</b>
    <ul>
        <li>Improve demand forecasting</li>
        <li>Prepare inventory proactively</li>
        <li>Optimize promotional planning</li>
        <li>Reduce stockouts</li>
        <li>Enable trend-based replenishment</li>
    </ul>

    </div>
    """,
    unsafe_allow_html=True
)

    st.markdown("### External Factors Impact Analysis")

    # =====================================================
    # CLEANING NUMERIC COLUMNS
    # =====================================================

    numeric_cols = [
        "Temperature",
        "Quantity_Sold",
        "Sales_Revenue",
        "Discount_Percent",
        "Unit_Price",
        "Trend_Velocity",
        "Engagement_Score",
        "Mention_Count",
        "Sentiment_Score"
    ]

    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(
                df[col],
                errors="coerce"
            )

    # =====================================================
    # ROW 1
    # =====================================================

    col1, col2 = st.columns(2)

    # =====================================================
    # 1. WEATHER VS PRODUCT CATEGORY DEMAND
    # =====================================================

    with col1:

        st.markdown(
            """
            <div style="
                background-color:#2F75B5;
                padding:18px 25px;
                border-radius:10px;
                font-size:20px;
                color:white;
                margin-top:20px;
                margin-bottom:10px;
                text-align:center;
            ">
                <b>Weather vs Product Category Demand</b>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Clean category values
        clean_df = df.copy()

        clean_df = clean_df[
            (clean_df["Category"].notna()) &
            (clean_df["Category"] != r"\N") &
            (clean_df["Category"].astype(str).str.strip() != "")
        ]

        # Aggregate sales
        weather_category = (
            clean_df.groupby(
                ["Weather_Condition", "Category"]
            )["Quantity_Sold"]
            .sum()
            .reset_index()
        )

        chart_weather = (
            alt.Chart(weather_category)
            .mark_bar()
            .encode(

                x=alt.X(
                    "Weather_Condition:N",
                    title="Weather Condition"
                ),

                y=alt.Y(
                    "Quantity_Sold:Q",
                    title="Total Quantity Sold"
                ),

                xOffset="Category:N",

                color=alt.value("#001F5C"),

                tooltip=[
                    alt.Tooltip(
                        "Weather_Condition:N",
                        title="Weather"
                    ),

                    alt.Tooltip(
                        "Category:N",
                        title="Category"
                    ),

                    alt.Tooltip(
                        "Quantity_Sold:Q",
                        title="Quantity Sold"
                    )
                ]
            )
            .properties(
                height=400,
                background="#00D05E"
            )
            .configure_view(
                fill="#00D05E",
                strokeOpacity=0
            )
        )

        st.altair_chart(
            chart_weather,
            use_container_width=True
        )

    # =====================================================
    # 2. FESTIVAL / EVENT DEMAND IMPACT
    # =====================================================

    with col2:

        st.markdown(
            """
            <div style="
                background-color:#2F75B5;
                padding:18px 25px;
                border-radius:10px;
                font-size:20px;
                color:white;
                margin-top:20px;
                margin-bottom:10px;
                text-align:center;
            ">
                <b>Festival / Event Demand Impact</b>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Remove invalid category values
        clean_df = df.copy()

        clean_df = clean_df[
            (clean_df["Category"].notna()) &
            (clean_df["Category"] != r"\N") &
            (clean_df["Category"].astype(str).str.strip() != "")
        ]

        # Remove invalid event names
        clean_df = clean_df[
            (clean_df["Event_Name"].notna()) &
            (clean_df["Event_Name"] != r"\N") &
            (clean_df["Event_Name"].astype(str).str.strip() != "")
        ]

        festival_df = (
            clean_df.groupby("Event_Name")["Quantity_Sold"]
            .sum()
            .sort_values(ascending=False)
            .head(10)
            .reset_index()
        )

        chart_festival = (
            alt.Chart(festival_df)
            .mark_bar(
                color="#001F5C",
                cornerRadiusEnd=6
            )
            .encode(

                x=alt.X(
                    "Event_Name:N",
                    sort='-y',
                    title="Event"
                ),

                y=alt.Y(
                    "Quantity_Sold:Q",
                    title="Quantity Sold"
                ),

                tooltip=[
                    alt.Tooltip(
                        "Event_Name:N",
                        title="Event"
                    ),

                    alt.Tooltip(
                        "Quantity_Sold:Q",
                        title="Quantity Sold"
                    )
                ]
            )
            .properties(
                height=400,
                background="#00D05E"
            )
            .configure_view(
                fill="#00D05E",
                strokeOpacity=0
            )
        )

        st.altair_chart(
            chart_festival,
            use_container_width=True
        )

    # =====================================================
    # ROW 2
    # =====================================================

    col3, col4 = st.columns(2)

    # =====================================================
    # 3. PROMOTION EFFECTIVENESS ANALYSIS
    # =====================================================

    with col3:

        st.markdown(
            """
            <div style="
                background-color:#2F75B5;
                padding:18px 25px;
                border-radius:10px;
                font-size:20px;
                color:white;
                margin-top:20px;
                margin-bottom:10px;
                text-align:center;
            ">
                <b>Promotion Effectiveness Analysis</b>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Remove invalid category values
        clean_df = df.copy()

        clean_df = clean_df[
            (clean_df["Category"].notna()) &
            (clean_df["Category"] != r"\N") &
            (clean_df["Category"].astype(str).str.strip() != "")
        ]

        promo_df = (
            clean_df.groupby("Promotion_Name")
            .agg({
                "Sales_Revenue": "sum",
                "Quantity_Sold": "sum"
            })
            .sort_values(
                by="Sales_Revenue",
                ascending=False
            )
            .head(10)
            .reset_index()
        )

        chart_promo = (
            alt.Chart(promo_df)
            .mark_bar(
                color="#001F5C",
                cornerRadiusEnd=6
            )
            .encode(

                x=alt.X(
                    "Promotion_Name:N",
                    sort='-y',
                    title="Promotion"
                ),

                y=alt.Y(
                    "Sales_Revenue:Q",
                    title="Revenue"
                ),

                tooltip=[

                    alt.Tooltip(
                        "Promotion_Name:N",
                        title="Promotion"
                    ),

                    alt.Tooltip(
                        "Sales_Revenue:Q",
                        title="Revenue",
                        format=",.2f"
                    ),

                    alt.Tooltip(
                        "Quantity_Sold:Q",
                        title="Quantity Sold"
                    )
                ]
            )
            .properties(
                height=400,
                background="#00D05E"
            )
            .configure_view(
                fill="#00D05E",
                strokeOpacity=0
            )
        )

        st.altair_chart(
            chart_promo,
            use_container_width=True
        )
    # =====================================================
    # 4. SOCIAL TREND INFLUENCE
    # =====================================================

    with col4:

        st.markdown(
            """
            <div style="
                background-color:#2F75B5;
                padding:18px 25px;
                border-radius:10px;
                font-size:20px;
                color:white;
                margin-top:20px;
                margin-bottom:10px;
                text-align:center;
            ">
                <b>Social Trend Influence on Demand</b>
            </div>
            """,
            unsafe_allow_html=True
        )

        social_df = (
            df.groupby("Platform_Name")["Quantity_Sold"]
            .sum()
            .sort_values(ascending=False)
            .reset_index()
        )

        chart_social = (
            alt.Chart(social_df)
            .mark_bar(
                color="#001F5C",
                cornerRadiusEnd=6
            )
            .encode(

                x=alt.X(
                    "Platform_Name:N",
                    sort="-y",
                    title="Social Media Platform"
                ),

                y=alt.Y(
                    "Quantity_Sold:Q",
                    title="Quantity Sold"
                ),

                tooltip=[

                    alt.Tooltip(
                        "Platform_Name:N",
                        title="Platform"
                    ),

                    alt.Tooltip(
                        "Quantity_Sold:Q",
                        title="Quantity Sold"
                    )
                ]
            )
            .properties(
                height=400,
                background="#00D05E"
            )
            .configure_view(
                fill="#00D05E",
                strokeOpacity=0
            )
        )

        st.altair_chart(
            chart_social,
            use_container_width=True
        )

elif eda_option == "Summary Report":
    # =========================
    # SUMMARY REPORT – INTRO
    # =========================
    st.markdown(
        """
        <div style="
            background-color:#2F75B5;
            padding:28px;
            border-radius:12px;
            color:white;
            font-size:16px;
            line-height:1.6;
            margin-bottom:25px;">

        <b>What this section does:</b>

        This provides a <b>consolidated narrative summary</b> of all EDA findings.

        It highlights:
        <ul>
            <li>Key demand patterns</li>
            <li>Major influencing factors</li>
            <li>Data readiness for modelling</li>
        </ul>

        <b>Why this matters:</b>

        Not all stakeholders want charts.<br>
        This section translates analysis into <b>actionable understanding</b>.


        <b>Key insights users get:</b>
        <ul>
            <li>A single, clear view of data insights</li>
            <li>Business-ready conclusions</li>
            <li>Readiness assessment for model engineering</li>
        </ul>

        </div>
        """,
        unsafe_allow_html=True
    )

    # =========================
    # FINAL EDA SUMMARY NARRATIVE (FULLY GROUNDED IN OUTPUTS)
    # =========================
    st.markdown(
        """
        <div style="
            background-color:#0B2C5D;
            padding:30px;
            border-radius:12px;
            color:white;
            font-size:15px;
            line-height:1.7;
        ">

        <h4>Data Health & Readiness</h4>
        <ul>
            <li>The dataset consists of <b>1,513 rows and 209 columns</b>, providing extensive coverage across inventory, suppliers, stores, demand, replenishment, and external factors.</li>
            <li>A total of <b>14 duplicate records</b> were identified and removed, improving data consistency and reliability.</li>
            <li>Most critical operational and transactional columns contain <b>minimal missing values</b>, ensuring high analytical quality.</li>
            <li>The dataset includes a balanced combination of <b>categorical, numerical, and datetime features</b>, making it suitable for forecasting and AI-driven analytics.</li>
            <li>Columns such as <b>Lead Time Adjustment</b> contain partial missing values, indicating selective procurement adjustment gaps.</li>
        </ul>

        <h4>Overall Sales Performance</h4>
        <ul>
            <li>Sales trends exhibit <b>strong fluctuations and demand spikes</b>, especially during promotions and seasonal events.</li>
            <li>Revenue contribution is highly concentrated among a subset of products and stores.</li>
            <li>Store-wise and category-wise sales confirm the presence of <b>high-performing entities driving overall revenue</b>.</li>
            <li>Demand behavior varies significantly across time periods, indicating <b>seasonal and event-driven purchasing patterns</b>.</li>
        </ul>

        <h4> Demand Forecasting Analysis</h4>
        <ul>
            <li>Historical demand patterns reveal recurring seasonal trends and periodic demand spikes.</li>
            <li>Moving average analysis successfully smooths short-term fluctuations and exposes <b>long-term demand direction</b>.</li>
            <li>Future demand forecasting identifies upcoming high-demand periods and potential inventory pressure zones.</li>
            <li>Forecast trends indicate that <b>AI-based replenishment planning</b> can significantly reduce stock shortages.</li>
            <li>Demand forecasting supports proactive procurement and improves inventory planning efficiency.</li>
        </ul>

        <h4> Inventory & Stock Analysis</h4>
        <ul>
            <li>Inventory distribution varies widely across categories, with certain products showing <b>overstock and understock situations</b>.</li>
            <li>Inventory turnover analysis clearly separates <b>fast-moving and slow-moving products</b>.</li>
            <li>Stock-out trend analysis reveals recurring shortage periods affecting sales continuity.</li>
            <li>Dead stock analysis identifies products with <b>high inventory but low sales movement</b>.</li>
            <li>Inventory aging patterns indicate prolonged storage duration for selected SKUs, increasing holding costs.</li>
            <li>Warehouse utilization analysis highlights opportunities for improving storage efficiency.</li>
        </ul>

        <h4> Predictive Replenishment Analysis</h4>
        <ul>
            <li>Reorder analysis identifies products approaching <b>critical stock thresholds</b>.</li>
            <li>Recommended reorder quantity analysis supports smarter procurement decisions and auto-restocking.</li>
            <li>Safety stock comparison highlights products operating below ideal inventory buffers.</li>
            <li>Replenishment priority analysis ranks products based on <b>stock urgency and demand pressure</b>.</li>
            <li>Inventory risk heatmaps reveal high-risk products and locations vulnerable to stock-outs.</li>
            <li>The analysis strongly supports <b>AI-driven replenishment automation</b>.</li>
        </ul>

        <h4>Supplier & Lead Time Analysis</h4>
        <ul>
            <li>Supplier lead times vary significantly, directly impacting replenishment speed and inventory availability.</li>
            <li>Delivery delay analysis reveals recurring procurement bottlenecks and shipment instability.</li>
            <li>On-time delivery rates differ considerably among suppliers, indicating reliability gaps.</li>
            <li>Supplier benchmarking highlights clear differences in <b>lead time, consistency, and operational efficiency</b>.</li>
            <li>Procurement cycle trends indicate periods of increasing procurement delays.</li>
            <li>Supplier risk scoring identifies vendors with elevated operational and replenishment risks.</li>
        </ul>

        <h4> Store-Level Analysis</h4>
        <ul>
            <li>Revenue generation is concentrated among selected stores and regions.</li>
            <li>Store inventory analysis reveals uneven stock availability across branches.</li>
            <li>Regional demand comparison confirms strong <b>location-specific purchasing behavior</b>.</li>
            <li>Store replenishment efficiency varies significantly between operational units.</li>
            <li>Top-selling products differ across stores, indicating localized customer preferences.</li>
            <li>Inter-store stock transfer analysis highlights opportunities for better stock balancing.</li>
        </ul>

        <h4>External Factors Impact Analysis</h4>
        <ul>
            <li>Weather conditions show noticeable influence on demand for multiple product categories.</li>
            <li>Festivals and promotional events generate <b>significant sales uplift and demand spikes</b>.</li>
            <li>Promotion effectiveness analysis confirms that not all discounts improve profitability.</li>
            <li>Price sensitivity analysis reveals direct relationships between pricing changes and customer demand.</li>
            <li>Social trend influence analysis identifies products experiencing trend-driven demand surges.</li>
            <li>Sentiment analysis indicates that positive customer sentiment often correlates with higher sales demand.</li>
        </ul>

        <h4> Cross-Dimensional Insights</h4>
        <ul>
            <li>Revenue, demand, and inventory risks are concentrated across selected products, stores, and suppliers.</li>
            <li>Stock-outs, overstocking, delayed procurement, and inefficient promotions act as <b>hidden operational leakages</b>.</li>
            <li>External factors such as weather, promotions, pricing, and events introduce strong non-linear demand behavior.</li>
            <li>Forecasting accuracy improves significantly when combining <b>SKU × Store × Supplier × Promotion × Event</b> dimensions.</li>
        </ul>

        <h4> Final Takeaway</h4>
        <ul>
            <li>The dataset is <b>clean, scalable, and enterprise-ready</b> for advanced analytics and AI modeling.</li>
            <li>Clear demand drivers, supplier inefficiencies, and inventory risks are observable across multiple operational dimensions.</li>
            <li>The EDA strongly validates downstream use cases in <b>demand forecasting, smart replenishment, inventory optimization, supplier intelligence, and promotion analytics</b>.</li>
            <li>The overall analytical framework provides a strong foundation for building <b>SupplySync AI – Predictive Replenishment & Auto-Procurement System</b>.</li>
        </ul>

        </div>
        """,
        unsafe_allow_html=True
    )

st.write("")
# ============================================================
# FOOTER
# ============================================================

st.markdown("""
    <br><br>
    <div style="
        background-color:#2E86C1;
        padding:12px;
        text-align:center;
        color:white;
        border-radius:6px;
        font-size:14px;">
        © 2025 SupplySyncAI – Predictive Replenishment & Auto-Procurement
    </div>
""", unsafe_allow_html=True)