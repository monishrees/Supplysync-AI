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
    
    chart = (
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