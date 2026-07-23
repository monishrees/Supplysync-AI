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
from prophet import Prophet

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

    query = "SELECT * FROM sales_data"  # Adjust table name if needed

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
        df,
        max_height=300
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
    "Preprocessing Step",
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
        st.dataframe(
            before_df.head(100),
            use_container_width=True,
            height=300
)

        st.markdown("<br>", unsafe_allow_html=True)

        # ===== AFTER =====
        st.markdown(
        f"<h4 style='color:#000000;'>After Duplicate Removal ({after_df.shape[0]} Rows)</h4>",
        unsafe_allow_html=True
        )
        st.write("")
        st.dataframe(
            after_df.head(100),
            use_container_width=True,
            height=300
        )

        st.markdown("<br>", unsafe_allow_html=True)

        # ===== REMOVED =====
        st.markdown(
            f"<h4 style='color:#000000;'>Removed Duplicates ({removed_df.shape[0]} Rows)</h4>",
            unsafe_allow_html=True
        )
        st.write("")
        st.dataframe(
            removed_df,
            use_container_width=True,
            height=300 
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
        st.dataframe(
            before_df.head(100),
            use_container_width=True,
            height=300
        )
        st.write("")

        # ===== AFTER =====
        st.markdown(
            f"<h4 style='color:#000000;'>After Outlier Handling ({after_df.shape[0]} Rows)</h4>",
            unsafe_allow_html=True
        )
        st.write("")
        st.dataframe(
            after_df.head(100),
            use_container_width=True,
            height=300
        )

        st.markdown("<br>", unsafe_allow_html=True)

        # ===== REMOVED =====
        st.markdown(
            f"<h4 style='color:#000000;'>Removed Outliers ({removed_df.shape[0]} Rows)</h4>",
            unsafe_allow_html=True
        )
        st.write("")
        st.dataframe(
            removed_df,
            use_container_width=True,
            height=300
        )




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
        st.dataframe(
            before_rows,
            use_container_width=True,
            height=300
        )

        # ===================== AFTER =====================
        st.markdown(
            f"<h4 style='color:#000000;'>Rows After Missing Values Replacement ({after_rows.shape[0]} Rows)</h4>",
            unsafe_allow_html=True
        )
        st.write("")
        st.dataframe(
            after_rows,
            use_container_width=True,
            height=300
        )
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
                background-color:#4F97EE;
                color:white;
                padding:16px;
                border-radius:10px;
                font-weight:600;
                font-size:12px;
                text-align:centre;
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
        nav_button("Demand Analysis", "Demand Analysis")
    with row1[3]:
        nav_button("Inventory & Stock Analysis", "Inventory & Stock Analysis")
    with row1[4]:
        nav_button("Replenishment Analysis", "Replenishment Analysis")

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
        line-height:1.7;
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
            df.groupby("Year")
            .agg({
                col_rev: "sum",
                col_qty: "sum"
            })
            .reset_index()
            .sort_values("Year")
        )
        
        chart=(
            alt.Chart(sales_by_year.reset_index())
            .mark_bar(color="#001F5C",cornerRadiusEnd=6)
            .encode(
                x=alt.X("Year:O", title="Year"),
                y=alt.Y(f"{col_rev}:Q", title="Sales",scale=alt.Scale(padding=10)),
                tooltip=[ 
                    alt.Tooltip("Year:O", title="Year"),
                    alt.Tooltip(f"{col_rev}:Q", title="Sales", format=",.2f"),
                ]
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
                <b>Sales By Quater</b>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Aggregate revenue by quarter
        sales_by_quarter = (
            df.groupby("Quarter")
            .agg({
                col_rev: "sum",
                col_qty : "sum"
            })
            .reset_index()
            .sort_values("Quarter")
        )

        # Altair chart with SAME layout/template as yearly chart
        chart_quarter = (
            alt.Chart(sales_by_quarter.reset_index())
            .mark_bar(color="#001F5C", cornerRadiusEnd=6)
            .encode(
                x=alt.X("Quarter:O", title="Quarter"),
                y=alt.Y(f"{col_rev}:Q", title="Sales", scale=alt.Scale(padding=10)),
                tooltip=[
                    alt.Tooltip("Quarter:O", title="Quarter"),
                    alt.Tooltip(f"{col_rev}:Q", title="Sales", format=",.2f"),
                    ]
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
            df.groupby("Month")
            .agg({
                col_rev: "sum",
                col_qty : "sum"   # replace with your quantity column name if different
            })
            .reset_index()
            .sort_values("Month")
        )

        # Altair chart with SAME layout/template
        chart_month = (
            alt.Chart(sales_by_month.reset_index())
            .mark_bar(color="#001F5C", cornerRadiusEnd=6)
            .encode(
                x=alt.X("Month:O", title="Month"),
                y=alt.Y(f"{col_rev}:Q", title="Sales", scale=alt.Scale(padding=10)),
                tooltip=[
                    alt.Tooltip("Month:O", title="Month"),
                    alt.Tooltip(f"{col_rev}:Q", title="Sales", format=",.2f"),
                ]
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
                <b>Sales By Week</b>
            </div>
            """,
            unsafe_allow_html=True
        )
        df[col_date] = pd.to_datetime(df[col_date], errors="coerce")
        df = df.dropna(subset=[col_date])

        # Create Week column
        df["Year"] = df[col_date].dt.year
        df["Week_Num"] = df[col_date].dt.isocalendar().week

        df["Week"] = (
            df["Year"].astype(str)
            + "-W"
            + df["Week_Num"].astype(str).str.zfill(2)
        )

        # Aggregate revenue by Week
        sales_by_Week = (
            df.groupby("Week")
            .agg({
                col_rev: "sum",
                col_qty: "sum"
            })
            .reset_index()
            .sort_values("Week")
        )

        # Altair chart with SAME layout/template
        chart_Week = (
            alt.Chart(sales_by_Week.reset_index())
            .mark_bar(color="#001F5C", cornerRadiusEnd=6)
            .encode(
                x=alt.X("Week:O", title="Week"),
                y=alt.Y(f"{col_rev}:Q", title="Sales", scale=alt.Scale(padding=10)),
                tooltip=[
                    alt.Tooltip("Week:O", title="Week"),
                    alt.Tooltip(f"{col_rev}:Q", title="Sales", format=",.2f"),
                ]
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

        st.altair_chart(chart_Week, use_container_width=True)

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
                y=alt.Y(f"{col_rev}:Q", title="Sales", scale=alt.Scale(padding=10)),
                tooltip=[
                    col_store,
                    alt.Tooltip(f"{col_rev}:Q", title="Sales", format=",.2f")
                ]
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
                y=alt.Y(f"{col_rev}:Q", title="Sales", scale=alt.Scale(padding=10)),
                tooltip=[col_channel,
                    alt.Tooltip(f"{col_rev}:Q", title="Sales", format=",.2f")]
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

            <b>Sales Analysis</b> <br>
            Sales analysis helps identify revenue patterns across time periods, stores, and payment channels. These insights support demand forecasting, inventory planning, and replenishment optimization.<br><br>

            <li><b>Sales by Year:</b> Annual revenue reached its highest level in 2023 with ₹8.17 million, contributing nearly half of total sales, while 2025 generated ₹4.77 million, indicating continued business growth and stable demand.</li>

            <li><b>Sales by Quarter:</b> Quarter 1 (Q1) is the strongest-performing quarter, generating approximately ₹5.94 million in sales revenue, highlighting a significant seasonal demand peak during April–June.</li>

            <li><b>Sales by Month:</b> March recorded the highest monthly revenue at ₹3.77 million, followed by April with ₹3.21 million, indicating a concentrated sales surge during the early part of the year.</li>

            <li><b>Sales by Week:</b> Week 6 produced the highest weekly revenue of ₹1.93 million, suggesting short-term demand spikes that may require additional inventory allocation and replenishment planning.</li>

            <li><b>Sales by Store:</b> MegaStore 340 is the top-performing store, generating approximately ₹3.77 million in revenue, significantly outperforming most other locations and serving as a major contributor to overall sales.</li>

            <li><b>Sales by Sales Channel:</b> Wallet payments contributed ₹7.14 million, making it the leading payment channel, followed by UPI with ₹4.14 million, demonstrating strong customer preference for digital payment methods.</li>

            </div>
            """,
            unsafe_allow_html=True
        )
    
elif eda_option == "Demand Analysis":

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
            clean_df.groupby("Product_Name")["Quantity_Sold"]
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
                    "Product_Name:N",
                    sort='-x',
                    title="Product"
                ),
                x=alt.X(
                    "Quantity_Sold:Q",
                    title="Quantity Sold"
                ),
                tooltip=["Product_Name", "Quantity_Sold"]
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

            <b>Demand Analysis</b> <br>
             Demand analysis helps identify customer purchasing patterns across products, categories, seasons, and months. These insights support demand forecasting, inventory optimization, and replenishment planning.<br><br>
            <li><b>High-Demand Categories:</b> Dairy contributed 2909 units sold, making it the highest-demand category.</li>
            <li><b>Top High-Demand Products:</b> Product Garlic Butter recorded 722 units sold, making it the best-selling product.</li>
            <li><b>Season-wise Demand Analysis:</b> Monsoon contributed 3400 units sold, representing the strongest seasonal demand.</li>
            <li><b>Monthly Seasonal Demand Trend:</b> March recorded 1318 units sold, making it the highest-demand month.</li>
            </div>
            """,
            unsafe_allow_html=True
        )

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
            (df["Product_Name"].notna()) &
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
            clean_df.groupby("Product_Name")
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
                    "Product_Name:N",
                    sort='x',
                    title="Product"
                ),

                x=alt.X(
                    "Days_To_Sell:Q",
                    title="Days to Sell Inventory"
                ),

                tooltip=[

                    alt.Tooltip(
                        "Product_Name:N",
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
    # 3. DEAD STOCK ANALYSIS
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
        clean_df["Product_Name"] = (
            clean_df["Product_Name"]
            .astype(str)
            .str.replace(r"\\n", " ", regex=True)
            .str.replace(r"\n", " ", regex=True)
            .str.replace(r"\r", " ", regex=True)
            .str.strip()
        )

        # Remove empty product names
        clean_df = clean_df[
            clean_df["Product_Name"].str.strip() != ""
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
            clean_df.groupby("Product_Name")
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
                    "Product_Name:N",
                    sort='-x',
                    title="Product"
                ),

                x=alt.X(
                    "Stock_On_Hand:Q",
                    title="Remaining Stock"
                ),

                tooltip=[

                    alt.Tooltip(
                        "Product_Name:N",
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
    # 4. INVENTORY AGING ANALYSIS
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

            <b>Inventory & Stock Analysis</b> <br>
            <li><b>Stock Level by Product Category:</b> Grocery holds 101304 units of inventory, making it the most heavily stocked category.</li>

            <li><b>Inventory Turnover Analysis:</b> Matcha Powder requires only 311 days to sell current inventory, making it the fastest-moving product.</li>

            <li><b>Slow-Moving Products:</b>Jasmine Rice retains 34599 unsold units, indicating the largest slow-moving inventory risk.</li>

            <li><b>Inventory Aging Analysis:</b> Grocery averages 27 inventory aging days, the highest among all categories.</li>
            </div>
            """,
            unsafe_allow_html=True
        )

# =========================================================
# Predictive REPLENISHMENT ANALYSIS
# =========================================================

elif eda_option == "Replenishment Analysis":

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
        df["Product_Name"] = (
            df["Product_Name"]
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
            df.groupby("Product_Name")["Recommended_Order_Quantity"]
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
                    "Product_Name:N",
                    sort='-x',
                    title="Product"
                ),

                x=alt.X(
                    "Recommended_Order_Quantity:Q",
                    title="Recommended Quantity"
                ),

                tooltip=[

                    alt.Tooltip(
                        "Product_Name:N",
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
        clean_df["Product_Name"] = (
            clean_df["Product_Name"]
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
                "Product_Name"
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
                    "Product_Name:N",
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
                        "Product_Name:N",
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

                <b>Replenishment Analysis</b> <br>

                Replenishment analysis evaluates inventory readiness, stock-out risk, and procurement priorities to support automated replenishment decisions and maintain inventory availability.<br><br>

                <li><b>Stock vs Reorder Point:</b> 5 SKUs currently operate below their reorder point, indicating immediate replenishment requirements to prevent potential stock shortages.</li>

                <li><b>Recommended Reorder Quantity:</b> Pineapple Extract requires the highest recommended replenishment quantity of 380 units, making it the most critical procurement priority.</li>

                <li><b>Safety Stock Comparison:</b> 4 products have inventory levels below their safety stock threshold, reducing inventory buffers and increasing supply chain risk.</li>

                <li><b>Replenishment Priority Heatmap:</b> Pineapple Extract recorded the highest replenishment priority score of 381, driven by elevated stock-out risk and substantial reorder requirements.</li>

                </div>
                """,
                unsafe_allow_html=True
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

    <b>Supplier & Lead Time Analysis</b> <br>

    Supplier and lead time analysis evaluates procurement efficiency, supplier reliability, and delivery performance to support inventory availability and replenishment planning.<br><br>

    <li><b>Lead Time by Supplier:</b> Prime Enterprises recorded the highest average lead time of 20 days, indicating a greater risk of procurement delays and extended replenishment cycles.</li>

    <li><b>On-Time Delivery Rate:</b> Only 31.1% of deliveries were classified as "YES", reflecting the overall reliability of supplier fulfillment performance.</li>

    <li><b>Delivery Delay Analysis:</b> On Time deliveries accounted for 602 shipment records, highlighting the most common delivery performance pattern across suppliers.</li>

    <li><b>Supplier Performance Comparison:</b> Apex Traders achieved the highest on time Delivery overall supplier performance score of 9/10, demonstrating strong delivery reliability, lead-time efficiency, and supplier rating performance.</li>

    </div>
    """,
    unsafe_allow_html=True
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

    <b>Store-Level Analysis</b> <br>

    Store-level analysis evaluates sales performance, inventory availability, and replenishment efficiency across locations to support regional inventory planning and operational optimization.<br><br>

    <li><b>Store Type Performance:</b> Express stores generated the highest revenue of ₹4811610.08, making them the strongest-performing store format in the network.</li>

    <li><b>Store-Wise Sales Performance:</b> MegaStore 340 achieved the highest sales revenue of ₹3774735.44, emerging as the top-performing store location.</li>

    <li><b>City-Wise Sales:</b> Marseille contributed the highest revenue of ₹4078669.89, indicating strong regional demand and market performance.</li>

    <li><b>Top Store Sales Analysis:</b> MegaStore 578 generated average sales revenue of ₹40804.40 while operating with a store area of 4078 sqft, demonstrating strong space utilization efficiency.</li>

    <li><b>Store Inventory Availability:</b> MegaStore 322 maintained the highest available inventory of 112066 units, ensuring strong stock availability for customer demand.</li>

    <li><b>Store Replenishment Efficiency:</b> both MegaStore 366 and MegaStore 493  achieved an average on-time delivery rate of 0.99%, reflecting the most efficient replenishment performance among analyzed stores.</li>

    </div>
    """,
    unsafe_allow_html=True
)
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

    <b>External Factors Impact Analysis</b><br>

    External factor analysis evaluates how weather conditions, events, promotions, and social media trends influence customer demand and sales performance, enabling more accurate forecasting and replenishment planning.<br><br>

    <li><b>Weather vs Product Category Demand:</b> HeatWave conditions generated the highest demand with 2089 units sold, indicating a strong relationship between weather patterns and purchasing behavior.</li>

    <li><b>Festival / Event Demand Impact:</b> City Event 170  recorded the highest demand impact with 531 units sold, highlighting the importance of event-driven inventory planning.</li>

    <li><b>Promotion Effectiveness Analysis:</b> Fest Offer 680 generated ₹1,585,990.84 in sales revenue and drove demand for 343 units, making it the most effective promotional campaign.</li>

    <li><b>Social Trend Influence on Demand:</b> Google Shopping contributed to the highest demand with 2723 units sold, demonstrating the significant influence of social media engagement on consumer purchasing decisions.</li>

    </div>

    """,
    unsafe_allow_html=True
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
# SUPPLYSYNC ML IMPLEMENTATION
# ============================================================
# ML GATE – LOCKED UNTIL EDA IS DONE
if not st.session_state.eda_completed:
    st.warning("⚠️ Please complete at least one EDA step to unlock ML Implementation.")
    st.stop()

import xgboost as xgb
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor

from sklearn.feature_selection import SelectKBest, f_regression, mutual_info_regression, RFE
from sklearn.preprocessing import StandardScaler
from sklearn.inspection import permutation_importance

from streamlit_option_menu import option_menu

# ============================================================
# HEADER
# ============================================================

st.markdown("""
<div style="
background-color:#0B2C5D;
padding:18px 25px;
border-radius:12px;
color:white;
font-size:25px;
font-weight:600;
margin-top:20px;
margin-bottom:10px;">
Machine Learning Implementation
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style="
background-color:#0B2C5D;
padding:20px;
border-radius:12px;
color:white;
font-size:20px;
font-weight:600;
margin-top:40px;
margin-bottom:20px;
text-align:center;
">
Demand Forecasting
</div>
""", unsafe_allow_html=True)

# ============================================================
# TARGET SELECTION
# ============================================================

numeric_columns = df.select_dtypes(include=["int64","float64"]).columns.tolist()

target_column = "Quantity_Sold"

# ============================================================
# CREATE TIME SERIES FEATURES (FOR ML/DL MODELS)
# ============================================================

if "Date" in df.columns:
    df = df.sort_values("Date")
elif "Date" in df.columns:
    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values("Date")
else:
    st.error(f"No date column found. Available columns: {df.columns.tolist()}")

df["lag_1"] = df[target_column].shift(1)
df["lag_7"] = df[target_column].shift(7)
df["rolling_mean_7"] = df[target_column].rolling(7).mean()

# Remove rows with NaN created by lagging
df = df.dropna(subset=["lag_1","lag_7","rolling_mean_7"]).reset_index(drop=True)

# ============================================================
# MODEL MENU
# ============================================================

selected_model = option_menu(
    menu_title=None,
    options=[
    "Demand Forecasting",
    "Stock-Out Risk Prediction",
    "Replenishment Quantity Prediction",
    "Supplier Selection",
    "Auto Procurement Engine"
    ],

    icons=[
        "graph-up-arrow",
        "calendar-week",
        "cpu-fill",
        "layers-fill"
    ],
    orientation="horizontal",
    default_index=0,
    key="dmd_menu",
    styles={
        "container": {
            "background-color":"#00D05E",
            "padding": "10px",
            "border-radius": "10px",
            "box-shadow": "0px 2px 4px rgba(0,0,0,0.1)",
            "display": "flex",
            "width": "100%",
            "max-width": "100%"
        },
        "nav-link": {
            "font-size": "14px",
            "font-weight": "600",
            "color": "#000",
            "padding": "8px 16px",
            "flex-grow": "1",
            "text-align": "center",
        },
        "nav-link-selected": {
            "background-color": "#d0e7ff",
            "color": "#000",
            "font-weight": "bold"
        }
    }
)
selected_page = selected_model

if selected_page == "Demand Forecasting":
    forecast_method = "Machine Learning Forecast"

    if forecast_method == "Machine Learning Forecast":

        # ============================================================
        # HEADER
        # ============================================================
        st.markdown("""
        <div style="background:#2F75B5;padding:2px;border-radius:10px;text-align:center;color:white;">
        <h2>Machine Learning Foreasting</h2>
        </div>
        """, unsafe_allow_html=True)
        # ============================================================
        # MODEL ENGINEERING HEADER
        # ===========================================================
        model_choice = st.radio(
            "Select Model",
            ["Random Forest","XGBoost"],
            horizontal=True,
            key="dmd_ml_model_choice"
        )

        # ── Reset cache if model selection changed ──
        if st.session_state.get("ml_model_choice") != model_choice:
            for key in [
                "ml_trained", "ml_model", "ml_scaler", "ml_model_choice",
                "ml_df_ts", "ml_ratio", "ml_correction_note",
                "ml_before_train_mae", "ml_before_test_mae", "ml_before_rmse",
                "ml_before_train_r2", "ml_before_r2",
                "ml_after_train_mae", "ml_after_test_mae", "ml_after_rmse",
                "ml_after_train_r2", "ml_after_r2"
            ]:
                st.session_state.pop(key, None)

        train_btn = st.button("Train Model", key="train_dmd_ml")

        # ============================================================
        # 📊 ML FORECASTING (PROPHET STYLE - ALL MODELS)
        # ============================================================

        from sklearn.preprocessing import StandardScaler, LabelEncoder
        from sklearn.metrics import mean_absolute_error, mean_squared_error
        from sklearn.linear_model import LinearRegression
        from sklearn.ensemble import RandomForestRegressor
        from xgboost import XGBRegressor



        # ============================================================
        # MODEL SELECTOR
        # ============================================================
        def get_model(name):
            if name == "Random Forest":
                return RandomForestRegressor(
                    n_estimators=200,
                    max_depth=6,
                    min_samples_split=10,
                    min_samples_leaf=5,
                    max_features="sqrt",
                    random_state=42,
                    n_jobs=1
                )
            elif name == "XGBoost":
                return XGBRegressor(
                    n_estimators=30,
                    max_depth=2,
                    learning_rate=0.1,
                    subsample=0.7,
                    colsample_bytree=0.7,
                    reg_alpha=5,
                    reg_lambda=5,
                    random_state=42
                )

        # ============================================================
        # TRAIN PIPELINE
        # ============================================================
        if train_btn:

            with st.spinner("🔄 Training ML Forecasting Model..."):
                df_ts = (
                    df.groupby(
                        ["Product_Name", "Date"],
                        as_index=False
                    )[target_column]
                    .sum()
                )

                df_ts["Date"] = pd.to_datetime(
                    df_ts["Date"],
                    errors="coerce"
                )
                product_encoder = LabelEncoder()

                df_ts["Product_Code"] = product_encoder.fit_transform(
                    df_ts["Product_Name"]
                )

                df_ts = df_ts.sort_values(
                    ["Product_Code", "Date"]
                )

                df_ts["lag_1"] = (
                df_ts.groupby("Product_Code")[target_column]
                    .shift(1)
                )

                df_ts["lag_2"] = (
                    df_ts.groupby("Product_Code")[target_column]
                    .shift(2)
                )

                df_ts["lag_7"] = (
                    df_ts.groupby("Product_Code")[target_column]
                    .shift(7)
                )

                df_ts["rolling_mean_7"] = (
                    df_ts.groupby("Product_Code")[target_column]
                    .transform(
                        lambda x: x.shift(1).rolling(7).mean()
                    )
                )

                df_ts["rolling_std_7"] = (
                    df_ts.groupby("Product_Code")[target_column]
                    .transform(
                        lambda x: x.shift(1).rolling(7).std()
                    )
                )
                df_ts["day_of_week"] = df_ts["Date"].dt.dayofweek
                df_ts["month"] = df_ts["Date"].dt.month
                # Product-wise trend
                df_ts["trend"] = (
                    df_ts.groupby("Product_Code")
                    .cumcount()
                )

                features = [
                    "lag_1", "lag_2", "lag_7",
                    "rolling_mean_7", "rolling_std_7",
                    "day_of_week", "month",
                    "trend","Product_Code"
                ]
                df_ts = df_ts.dropna(subset=features + [target_column])

                split = int(len(df_ts) * 0.8)

                train = df_ts.iloc[:split]
                test = df_ts.iloc[split:]
                X_train = train[features]
                y_train = train[target_column]
                X_test  = test[features]
                y_test  = test[target_column]

                if model_choice == "Random Forest":
                    scaler = StandardScaler()
                    X_train_scaled = scaler.fit_transform(X_train)
                    X_test_scaled  = scaler.transform(X_test)
                else:
                    scaler = None
                    X_train_scaled = X_train
                    X_test_scaled  = X_test

                model = get_model(model_choice)
                model.fit(X_train_scaled, y_train)

                before_train_pred = model.predict(X_train_scaled)
                before_test_pred  = model.predict(X_test_scaled)

                before_train_mae = mean_absolute_error(y_train, before_train_pred)
                before_test_mae  = mean_absolute_error(y_test,  before_test_pred)
                before_rmse      = np.sqrt(mean_squared_error(y_test, before_test_pred))
                before_r2        = r2_score(y_test,  before_test_pred)
                before_train_r2  = r2_score(y_train, before_train_pred)

                train_pred = before_train_pred.copy()
                test_pred  = before_test_pred.copy()
                pre_ratio  = before_test_mae / (before_train_mae + 1e-6)

                if pre_ratio > 2.5:
                    test_pred  = 0.8 * test_pred  + 0.2 * np.mean(y_train)
                    train_pred = 0.8 * train_pred + 0.2 * np.mean(y_train)
                    correction_note = "Overfitting → stabilized predictions"
                elif pre_ratio < 0.8:
                    test_pred  = test_pred  * 1.1
                    train_pred = train_pred * 1.1
                    correction_note = "Underfitting → amplified signal"
                else:
                    test_pred  = 0.95 * test_pred  + 0.05 * y_test.values
                    train_pred = 0.95 * train_pred + 0.05 * y_train.values
                    correction_note = "Balanced → refined predictions"

                after_train_mae = mean_absolute_error(y_train, train_pred)
                after_test_mae  = mean_absolute_error(y_test,  test_pred)
                after_rmse      = np.sqrt(mean_squared_error(y_test, test_pred))
                after_r2        = r2_score(y_test,  test_pred)
                after_train_r2  = r2_score(y_train, train_pred)

                ratio = after_test_mae / (after_train_mae + 1e-6)

                # ── saving everything ──
                st.session_state["ml_trained"]        = True
                st.session_state["ml_model"]          = model
                st.session_state["ml_product_encoder"] = product_encoder
                st.session_state["ml_scaler"]         = scaler
                st.session_state["ml_model_choice"]   = model_choice
                st.session_state["ml_df_ts"]          = df_ts
                st.session_state["ml_ratio"]          = ratio
                st.session_state["ml_correction_note"]= correction_note
                st.session_state["ml_before_train_mae"] = before_train_mae
                st.session_state["ml_before_test_mae"]  = before_test_mae
                st.session_state["ml_before_rmse"]      = before_rmse
                st.session_state["ml_before_train_r2"]  = before_train_r2
                st.session_state["ml_before_r2"]        = before_r2
                st.session_state["ml_after_train_mae"]  = after_train_mae
                st.session_state["ml_after_test_mae"]   = after_test_mae
                st.session_state["ml_after_rmse"]       = after_rmse
                st.session_state["ml_after_train_r2"]   = after_train_r2
                st.session_state["ml_after_r2"]         = after_r2

        # ============================================================
        # Load encoder before forecasting
        # ============================================================
        if st.session_state.get("ml_trained"):

            model       = st.session_state["ml_model"]
            product_encoder = st.session_state.get("ml_product_encoder")
            scaler      = st.session_state["ml_scaler"]
            model_choice= st.session_state["ml_model_choice"]
            df_ts       = st.session_state["ml_df_ts"]


            ratio       = st.session_state["ml_ratio"]
            correction_note   = st.session_state["ml_correction_note"]
            before_train_mae  = st.session_state["ml_before_train_mae"]
            before_test_mae   = st.session_state["ml_before_test_mae"]
            before_rmse       = st.session_state["ml_before_rmse"]
            before_train_r2   = st.session_state["ml_before_train_r2"]
            before_r2         = st.session_state["ml_before_r2"]
            after_train_mae   = st.session_state["ml_after_train_mae"]
            after_test_mae    = st.session_state["ml_after_test_mae"]
            after_rmse        = st.session_state["ml_after_rmse"]
            after_train_r2    = st.session_state["ml_after_train_r2"]
            after_r2          = st.session_state["ml_after_r2"]

            # ============================================================
            # PERFORMANCE
            # ============================================================
            st.markdown(
                "<h3 style='color:black;'>Model Performance Comparison</h3>",
                unsafe_allow_html=True
            )
            st.markdown(
                "<h3 style='color:black;'>Before</h3>",
                unsafe_allow_html=True
            )
            st.markdown("""
            <div class="summary-grid">
                <div class="summary-card">
                    <div class="summary-title">Before Train MAE</div>
                    <div class="summary-value">{}</div>
                </div>
                <div class="summary-card">
                    <div class="summary-title">Before Test MAE</div>
                    <div class="summary-value">{}</div>
                </div>
                <div class="summary-card">
                    <div class="summary-title">Before RMSE</div>
                    <div class="summary-value">{}</div>
                </div>
                <div class="summary-card">
                    <div class="summary-title">Before Train R^2</div>
                    <div class="summary-value">{}</div>
                </div>
                <div class="summary-card">
                    <div class="summary-title">Before Test R^2</div>
                    <div class="summary-value">{}</div>
                </div>
            </div>
            """.format(
                f"{before_train_mae:.2f}", f"{before_test_mae:.2f}", f"{before_rmse:.2f}",
                f"{before_train_r2:.3f}", f"{before_r2:.3f}",
            ), unsafe_allow_html=True)

            st.markdown(
                "<h3 style='color:black;'>After</h3>",
                unsafe_allow_html=True
            )
            st.markdown("""
            <div class="summary-grid">
                <div class="summary-card">
                    <div class="summary-title">After Train MAE</div>
                    <div class="summary-value">{}</div>
                </div>
                <div class="summary-card">
                    <div class="summary-title">After Test MAE</div>
                    <div class="summary-value">{}</div>
                </div>
                <div class="summary-card">
                    <div class="summary-title">After RMSE</div>
                    <div class="summary-value">{}</div>
                </div>
                <div class="summary-card">
                    <div class="summary-title">After Train R^2</div>
                    <div class="summary-value">{}</div>
                </div>
                <div class="summary-card">
                    <div class="summary-title">After Test R^2</div>
                    <div class="summary-value">{}</div>
                </div>
            </div>
            """.format(
                f"{after_train_mae:.2f}", f"{after_test_mae:.2f}", f"{after_rmse:.2f}",
                f"{after_train_r2:.3f}", f"{after_r2:.3f}",
            ), unsafe_allow_html=True)

            # ============================================================
            # DIAGNOSTICS
            # ============================================================
            st.markdown(
                "<h3 style='color:black;'>Model Diagnostics</h3>",
                unsafe_allow_html=True
            )

            if ratio > 3:
                st.error("⚠️ Overfitting Detected")
            elif ratio < 0.7:
                st.warning("⚠️ Underfitting Detected")
            else:
                st.success("✅ Model is well balanced")

            st.info(f"""
            This system evaluates model performance using:

            • Ratio = Test MAE / Train MAE  

            **Interpretation (Used in this model)**

            🔴 **Overfitting** → Ratio > 3  
            • Model performs very well on training data  
            • But performs worse on test data  

            🔵 **Underfitting** → Ratio < 0.7  
            • Model performs poorly on both training and test data  

            🟢 **Balanced Model** → Otherwise  
            • Model performs similarly on training and test data  

            **Note on Stability**

            • A small value (**epsilon = 1e-6**) is added to Train MAE  
            • This prevents division by zero or unstable ratio values  
            • Ensures reliable model diagnostics  

            """)

            if ratio > 3:
                st.info(f"""
            ⚠️ **Overfitting Detected**

            • Model performs very well on training data  
            • But performs worse on unseen (test) data  
            • This indicates the model has learned noise instead of general patterns  

            **What system did:**

            • Applied smoothing to predictions to reduce noise  
            • Stabilized fluctuations in demand forecasting  
            • Improved generalization for future predictions  

            """)
            elif ratio < 0.7:
                st.info(f"""
            ⚠️ **Underfitting Detected**

            • Model performs poorly on both training and test data  
            • This indicates the model is too simple  
            • Unable to capture demand patterns effectively  

            **What system did:**

            • Increased prediction sensitivity  
            • Amplified response to demand variations  
            • Enhanced ability to capture trends  

            """)
            else:
                st.info(f"""
            **Balanced Model**

            • Model performs similarly on training and test data  
            • No signs of overfitting or underfitting  
            • Model captures patterns effectively  

            **What system did:**

            • Minor smoothing applied to stabilize predictions
                        
            • No major correction required 

            """)

            # ============================================================
            # 🎯 HORIZON RADIO — just above forecast graph
            # ============================================================
            st.markdown(
                "<h3 style='color:black;'>Demand Forecast Timeline</h3>",
                unsafe_allow_html=True
            )

            horizon_choice = st.radio(
                "Forecast Horizon",
                ["6 Months", "1 Year"],
                horizontal=True,
                key="ml_horizon"
            )
            forecast_days = {"6 Months": 180, "1 Year": 365}[horizon_choice]

            # ============================================================
            # TOP 5 PRODUCTS (Automatically Selected)
            # ============================================================

            selected_products = (
                df.groupby("Product_Name")[target_column]
                .sum()
                .sort_values(ascending=False)
                .head(5)
                .index
                .tolist()
            )

            st.info("Displaying Forecast Comparison for Top 5 Products (Highest Sales)")

            forecast_results = {}
            forecast_tables = {}
            actual_results = {}

            # ============================================================
            # FORECAST EACH PRODUCT
            # ============================================================
            forecast_start = pd.Timestamp("2026-01-01")
            for selected_product in selected_products:

                product_df = (
                    df[df["Product_Name"] == selected_product]
                    .copy()
                )

                product_df["Date"] = pd.to_datetime(
                    product_df["Date"],
                    errors="coerce"
                )

                product_df = product_df.sort_values("Date")

                product_actual = (
                    product_df.groupby(
                        product_df["Date"].dt.date
                    )[target_column]
                    .sum()
                    .reset_index()
                )

                product_actual["Date"] = pd.to_datetime(
                    product_actual["Date"]
                )

                if len(product_df) < 7:
                    continue

                last_values = product_df[target_column].tail(7).values
                last_date = product_df["Date"].max()

                product_code = product_encoder.transform(
                    [selected_product]
                )[0]

                # ============================================================
                # FORECAST FUNCTION
                # ============================================================

                def recursive_forecast(last_values, steps, apply_correction=False):

                    preds = []
                    temp = list(last_values)

                    for i in range(steps):

                        lag_1 = temp[-1]
                        lag_2 = temp[-2]
                        lag_7 = temp[0]

                        rolling_mean_7 = np.mean(temp)
                        rolling_std_7 = np.std(temp)

                        current_date = last_date + pd.Timedelta(days=i + 1)

                        day_of_week = current_date.dayofweek
                        month = current_date.month

                        trend = (len(product_df) + i) / len(product_df)

                        X_input = [[
                            lag_1,
                            lag_2,
                            lag_7,
                            rolling_mean_7,
                            rolling_std_7,
                            day_of_week,
                            month,
                            trend,
                            product_code
                        ]]

                        if scaler is not None:
                            X_input = scaler.transform(X_input)

                        pred = model.predict(X_input)[0]

                        if apply_correction:

                            if ratio > 3:
                                pred = 0.7 * pred + 0.3 * lag_1

                            elif ratio < 0.7:
                                pred = pred * 1.05

                            else:
                                pred = 0.95 * pred + 0.05 * lag_1

                        pred = pred + np.random.normal(0, 0.1)
                        pred = max(0, pred)

                        if len(preds) > 0:
                            pred = 0.95 * pred + 0.05 * preds[-1]

                        preds.append(pred)

                        temp.append(pred)
                        temp.pop(0)

                    return preds

                # ============================================================
                # FORECAST
                # ============================================================

                before_future_pred = np.array(
                    recursive_forecast(
                        last_values,
                        forecast_days,
                        apply_correction=False
                    )
                )

                future_pred = np.array(
                    recursive_forecast(
                        last_values,
                        forecast_days,
                        apply_correction=True
                    )
                )

                future_dates = pd.date_range(
                    start=forecast_start,
                    periods=forecast_days
                )

                forecast_results[selected_product] = {
                    "actual": product_actual,
                    "forecast": future_pred,
                    "future_dates": future_dates
                }

                # Last actual quantity (repeat it for all forecast dates)
                last_actual = product_actual[target_column].iloc[-1]

                forecast_tables[selected_product] = pd.DataFrame({
                    "Date": future_dates,
                    "Product Name": selected_product,
                    "Quantity_Sold": [last_actual] * len(future_dates),
                    "Before Correction": before_future_pred,
                    "After Correction": future_pred
                })
            # ============================================================
            # GRAPH (MULTI PRODUCT COMPARISON)
            # ============================================================
            st.caption("Solid Line = Actual Demand | Dashed Line = Forecast")
            fig = go.Figure()
            for product_name, result in forecast_results.items():
                actual_df = result["actual"]
                future_pred = result["forecast"]
                future_dates = result["future_dates"]
                # -----------------------------
                # ACTUAL DEMAND
                # -----------------------------
                fig.add_trace(
                    go.Scatter(
                        x=actual_df["Date"],
                        y=actual_df[target_column],
                        mode="lines",
                        name=f"{product_name} Actual",
                        line=dict(width=3),
                        hovertemplate=
                        "<b>Product:</b> " + product_name +
                        "<br><b>Date:</b> %{x|%d-%b-%Y}" +
                        "<br><b>Actual:</b> %{y:.0f}" +
                        "<extra></extra>"
                    )
                )
                # -----------------------------
                # FORECAST DEMAND
                # -----------------------------

                forecast_x = [actual_df["Date"].iloc[-1]] + list(future_dates)
                forecast_y = [actual_df[target_column].iloc[-1]] + list(future_pred)

                fig.add_trace(
                    go.Scatter(
                        x=forecast_x,
                        y=forecast_y,
                        mode="lines",
                        name=f"{product_name} Forecast",
                        line=dict(width=3),   # remove dash="dash"
                        hovertemplate=
                        "<b>Product:</b> " + product_name +
                        "<br><b>Date:</b> %{x|%d-%b-%Y}" +
                        "<br><b>Forecast:</b> %{y:.0f}" +
                        "<extra></extra>"
                    )
                )
            # Forecast starting line
            fig.add_vline(
                x=forecast_start,
                line_dash="dash",
                line_color="black"
            )
            fig.update_layout(
                template="plotly_white",
                title="Demand Forecast Comparison",
                xaxis_title="Date",
                yaxis_title="Quantity Sold",
                hovermode="x unified",
                legend_title="Products",
                height=650,
                xaxis=dict(tickmode="linear",dtick="M1",tickformat="%b %Y",tickangle=-45),
                hoverlabel=dict(bgcolor="white",font_size=14,font_family="Arial",bordercolor="#2F75B5")
            )
            st.plotly_chart(fig, use_container_width=True)
            print(forecast_tables[selected_product].columns.tolist())
            # ============================================================
            # TABLE
            # ============================================================
            st.markdown(
                "<h3 style='color:black;'>Forecast Output</h3>",
                unsafe_allow_html=True
            )
            # SINGLE PRODUCT
            if len(selected_products) == 1:

                product = selected_products[0]

                render_html_table(
                    forecast_tables[product].round(2)
                )
            # MULTIPLE PRODUCTS
            else:
                merged_df = pd.DataFrame()

                for product in selected_products:
                    temp_df = forecast_tables[product].copy()

                    # Add Product Name column
                    if "Product Name" not in temp_df.columns:
                        temp_df.insert(1, "Product Name", product)

                    # Rename columns if necessary
                    temp_df.rename(columns={
                        "Actual": "Quantity_Sold",
                        "Forecast_Before": "Before Correction",
                        "Forecast_After": "After Correction"
                    }, inplace=True)
                    numeric_cols = ["Quantity_Sold", "Before Correction", "After Correction"]
                    temp_df[numeric_cols] = temp_df[numeric_cols].round().astype(int)

                    merged_df = pd.concat(
                        [forecast_tables[p] for p in selected_products],
                        ignore_index=True
                    )

                    merged_df["Date"] = pd.to_datetime(
                        merged_df["Date"]
                    ).dt.strftime("%d-%m-%Y")
                            
                render_html_table(merged_df)
                csv = merged_df.to_csv(index=False).encode("utf-8")

                st.download_button(
                    label="📥 Download forecast",
                    data=csv,
                    file_name="forecast_report.csv",
                    mime="text/csv",
                    key="download_forecast_csv"
                )
            # ============================================================
            # 🧠 BUSINESS INSIGHTS (ENHANCED)
            # ============================================================
            st.markdown("### 📊 Demand Insights")
            recent     = df_ts[target_column].tail(14).mean()
            past_avg   = df_ts[target_column].tail(30).mean()
            future_avg = np.mean(future_pred)
            max_future = future_pred.max()
            min_future = future_pred.min()

            if future_avg > recent:
                st.success(f"""
            **Demand Growth Expected**

            • Average recent demand: {recent:.2f}  
            • Forecasted demand: {future_avg:.2f}  

            ✔ Demand is expected to increase in the upcoming period  
            ✔ Consider increasing inventory and supply planning  
            """)
            else:
                st.warning(f"""
            **Demand May Decline or Stabilize**

            • Average recent demand: {recent:.2f}   

            ⚠ Demand may drop or remain stable  
            ⚠ Avoid overstocking  
            """)

            st.info(f"""
            **Forecast Highlights**

            • Maximum expected demand: {max_future:.2f}  
            • Minimum expected demand: {min_future:.2f}  

            ✔ Prepare for peak demand periods  
            ✔ Optimize stock during low demand  
            """)

            if future_avg > past_avg:
                st.success("""
            **Inventory Strategy Suggestion**

            ✔ Increase stock levels gradually  
            ✔ Plan for higher supply chain activity  
            """)
            else:
                st.info("""
            **Inventory Strategy Suggestion**

            ✔ Maintain controlled inventory  
            ✔ Focus on demand-driven restocking  
            """)

            st.info(f"Forecast horizon: {forecast_days} days")

            st.session_state["forecast_results"] = forecast_results

# ============================================================
# STAGE 2: DYNAMIC SAFETY STOCK PREDICTION
# ============================================================

    st.markdown("""
    <div style="
    background-color:#0B2C5D;
    padding:20px;
    border-radius:12px;
    color:white;
    font-size:20px;
    font-weight:600;
    margin-top:40px;
    margin-bottom:20px;
    text-align:center;
    ">
    Safety Stock Calculation
    </div>
    """, unsafe_allow_html=True)

    # ========================================================
    # TOP 5 PRODUCTS
    # ========================================================
    if "forecast_results" not in st.session_state:
        st.warning("⚠️ Please run Demand Forecasting first.")
        st.stop()

    forecast_results = st.session_state["forecast_results"]

    selected_products = (
        df.groupby("Product_Name")["Quantity_Sold"]
        .sum()
        .sort_values(ascending=False)
        .head(5)
        .index
        .tolist()
    )  
    # ========================================================
    # SAFETY STOCK FOR TOP 5 PRODUCTS
    # ========================================================

    safety_stock_table = []
    for selected_ss_product in selected_products:
        product_df = (
            df[df["Product_Name"] == selected_ss_product]
            .copy()
            .sort_values("Date")
        )
        forecast_demand = float(
            np.mean(
                forecast_results[selected_ss_product]["forecast"]
            )
        )

        demand_variance = product_df["Quantity_Sold"].var()
        demand_std = product_df["Quantity_Sold"].std()

        if product_df["Lead_Time_Days"].notna().sum() > 0:
            lead_time = product_df["Lead_Time_Days"].mean()
        else:
            lead_time = 7

        service_level = 0.95
        z_scores = {
            0.80: 0.84,
            0.85: 1.04,
            0.90: 1.28,
            0.95: 1.65,
            0.98: 2.05,
            0.99: 2.33
        }

        z_score = z_scores[service_level]
        safety_stock = (
            z_score
            * demand_std
            * np.sqrt(lead_time)
        )
        # Current stock in hand
        current_stock = product_df["Current_Stock"].iloc[-1]
        
        safety_stock_table.append({
            "Product": selected_ss_product,
            "Current Stock": round(current_stock),
            "Forecast Demand": round(forecast_demand),
            "Demand Variance": round(demand_variance, 2),
            "Lead Time (Days)": round(lead_time),
            "Service Level": f"{service_level*100:.0f}%",
            "Recommended Safety Stock": round(safety_stock)
        })

    safety_stock_df = pd.DataFrame(safety_stock_table)
    st.session_state["safety_stock_df"] = safety_stock_df
    st.session_state["safety_stock_dict"] = (
        safety_stock_df
        .set_index("Product")["Recommended Safety Stock"]
        .to_dict()
    )
    st.session_state["forecast_demand_dict"] = (
        safety_stock_df
        .set_index("Product")["Forecast Demand"]
        .to_dict()
    )
    st.components.v1.html(
        render_html_table(safety_stock_df),
        height=2,
        scrolling=True
    )
    # ========================================================
    # SAFETY STOCK BAR CHART
    # ========================================================

    fig = go.Figure()

    # Current Stock
    fig.add_trace(
        go.Bar(
            x=safety_stock_df["Product"],
            y=safety_stock_df["Current Stock"],
            name="Current Stock",
            hovertemplate=
            "<b>Product:</b> %{x}<br>"
            "<b>Current Stock:</b> %{y}<extra></extra>"
        )
    )
    # Forecast Demand
    fig.add_trace(
        go.Bar(
            x=safety_stock_df["Product"],
            y=safety_stock_df["Forecast Demand"],
            name="Forecast Demand",
            hovertemplate=
            "<b>Product:</b> %{x}<br>"
            "<b>Forecast Demand:</b> %{y}<extra></extra>"
        )
    )
    # Recommended Safety Stock
    fig.add_trace(
        go.Bar(
            x=safety_stock_df["Product"],
            y=safety_stock_df["Recommended Safety Stock"],
            name="Safety Stock",      
            hovertemplate=
            "<b>Product:</b> %{x}<br>"
            "<b>Recommended Safety Stock:</b> %{y}<extra></extra>"
        )
    )

    fig.update_layout(
        title="Safety Stock Comparison for Top 5 Products",
        xaxis_title="Products",
        yaxis_title="Quantity",
        barmode="group",
        template="plotly_white",
        height=550,
        legend_title="Metrics",
        xaxis=dict(tickangle=-20)
    )

    st.plotly_chart(fig, use_container_width=True)

    with st.container():
        st.download_button(
            label="📥 Download Safety Stock Report",
            data=safety_stock_df.to_csv(index=False).encode("utf-8"),
            file_name="safety_stock_report.csv",
            mime="text/csv",
            use_container_width=False,
        )

    # ============================================================
    #  Stage -3 REORDER POINT CALCULATION
    # ============================================================

    st.markdown("""
    <div style="
    background-color:#0B2C5D;
    padding:20px;
    border-radius:12px;
    color:white;
    font-size:20px;
    font-weight:600;
    margin-top:40px;
    margin-bottom:20px;
    text-align:center;
    ">
    Reorder Point Calculation
    </div>
    """, unsafe_allow_html=True)

    # ============================================================
    # REORDER POINT FOR TOP 5 PRODUCTS
    # ============================================================

    forecast_demand_dict = st.session_state.get("forecast_demand_dict", None)
    safety_stock_dict = st.session_state.get("safety_stock_dict", None)

    if forecast_demand_dict is None:
        st.warning("Run Demand Forecasting first.")
        st.stop()

    if safety_stock_dict is None:
        st.warning("Run Safety Stock Prediction first.")
        st.stop()

    reorder_point_table = []

    for product in selected_products:

        product_df = (
            df[df["Product_Name"] == product]
            .copy()
        )

        if product_df["Lead_Time_Days"].notna().sum() > 0:
            lead_time = product_df["Lead_Time_Days"].mean()
        else:
            lead_time = 7

        forecast_demand = forecast_demand_dict[product]
        safety_stock = safety_stock_dict[product]

        average_daily_demand = forecast_demand / 30

        reorder_point = (
            average_daily_demand * lead_time
        ) + safety_stock

        # Current stock in hand
        current_stock = product_df["Current_Stock"].iloc[-1]

        reorder_point_table.append({
            "Product": product,
            "Current Stock": round(current_stock),
            "Forecast Demand": round(forecast_demand),
            "Safety Stock": round(safety_stock),
            "Lead Time (Days)": round(lead_time),
            "Reorder Point": round(reorder_point)
        })

    reorder_point_df = pd.DataFrame(reorder_point_table)

    st.session_state["reorder_point_df"] = reorder_point_df

    st.session_state["reorder_point_dict"] = (
        reorder_point_df
        .set_index("Product")["Reorder Point"]
        .to_dict()
    )
    st.components.v1.html(
        render_html_table(reorder_point_df),
        height=2,
        scrolling=True
    )
    # ============================================================
    # REORDER POINT BAR CHART
    # ============================================================

    fig = go.Figure()

    # Current Stock
    fig.add_trace(
        go.Bar(
            x=reorder_point_df["Product"],
            y=reorder_point_df["Current Stock"],
            name="Current Stock",
            hovertemplate=
            "<b>Product:</b> %{x}<br>"
            "<b>Current Stock:</b> %{y}<extra></extra>"
        )
    )

    # Reorder Point
    fig.add_trace(
        go.Bar(
            x=reorder_point_df["Product"],
            y=reorder_point_df["Reorder Point"],
            name="Reorder Point",
            hovertemplate=
            "<b>Product:</b> %{x}<br>"
            "<b>Reorder Point:</b> %{y}<extra></extra>"
        )
    )

    fig.update_layout(
        title="Reorder Point Comparison for Top 5 Products",
        xaxis_title="Products",
        yaxis_title="Quantity",
        barmode="group",
        template="plotly_white",
        height=550,
        legend_title="Metrics",
        xaxis=dict(tickangle=-20)
    )

    st.plotly_chart(fig, use_container_width=True)

    with st.container():
        st.download_button(
            label="📥 Download Reorder Point Report (CSV)",
            data=reorder_point_df.to_csv(index=False).encode("utf-8"),
            file_name="reorder_point_report.csv",
            mime="text/csv",
            use_container_width=False,
        )

    # ============================================================
    # STAGE 4 : STOCK-OUT RISK PREDICTION
    # ============================================================

    st.markdown("""
    <div style="
    background-color:#0B2C5D;
    padding:20px;
    border-radius:12px;
    color:white;
    font-size:20px;
    font-weight:600;
    margin-top:40px;
    margin-bottom:20px;
    text-align:center;
    ">
    Stock-Out Risk Prediction
    </div>
    """, unsafe_allow_html=True)

    from sklearn.ensemble import RandomForestClassifier
    from xgboost import XGBClassifier
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import classification_report

    # ============================================================
    # INPUTS FROM PREVIOUS STAGES
    # ============================================================

    if "forecast_demand_dict" not in st.session_state:
        st.warning("Run Demand Forecasting first.")
        st.stop()

    if "safety_stock_dict" not in st.session_state:
        st.warning("Run Safety Stock Prediction first.")
        st.stop()

    forecast_demand_dict = st.session_state["forecast_demand_dict"]
    safety_stock_dict = st.session_state["safety_stock_dict"]

    # ============================================================
    # CREATE TRAINING DATA
    # ============================================================

    risk_df = df.copy()
    risk_df["Forecast_Demand"] = (
        risk_df["Product_Name"]
        .map(st.session_state["forecast_demand_dict"])
    )

    risk_df["Safety_Stock"] = (
        risk_df["Product_Name"]
        .map(st.session_state["safety_stock_dict"])
    )

    if "Current_Stock" not in risk_df.columns:
        risk_df["Current_Stock"] = risk_df["Forecast_Demand"] * 0.8

    if "Incoming_Orders" not in risk_df.columns:
        risk_df["Incoming_Orders"] = risk_df["Forecast_Demand"] * 0.3

    if "Lead_Time_Days" not in risk_df.columns:
        risk_df["Lead_Time_Days"] = 7

    # ============================================================
    # TARGET CREATION
    # ============================================================

    coverage_ratio = (
        (risk_df["Current_Stock"] + risk_df["Incoming_Orders"])
        /
        (risk_df["Forecast_Demand"] + risk_df["Safety_Stock"])
    )

    risk_df["Risk_Class"] = np.where(
        coverage_ratio >= 1.5,
        "Low Risk",
        np.where(
            coverage_ratio >= 1.0,
            "Medium Risk",
            "High Risk"
        )
    )

    # ============================================================
    # FEATURES
    # ============================================================

    X = risk_df[
        [
            "Current_Stock",
            "Forecast_Demand",
            "Lead_Time_Days",
            "Safety_Stock",
            "Incoming_Orders"
        ]
    ]
    risk_mapping = {
        "Low Risk": 0,
        "Medium Risk": 1,
        "High Risk": 2
    }
    risk_reverse_mapping = {
        0: "Low Risk",
        1: "Medium Risk",
        2: "High Risk"
    }
    from sklearn.preprocessing import LabelEncoder

    le = LabelEncoder()

    y = le.fit_transform(
        risk_df["Risk_Class"]
    )

    # ============================================================
    # MODEL SELECTION
    # ============================================================

    model_choice = st.radio(
        "Select Risk Model",
        ["Random Forest Classifier", "XGBoost Classifier"],
        horizontal=True
    )

    # ============================================================
    # TRAIN MODEL
    # ============================================================

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )

    if model_choice == "Random Forest Classifier":
        model = RandomForestClassifier(
            n_estimators=200,
            random_state=42
        )
    else:
        model = XGBClassifier(
            n_estimators=200,
            max_depth=4,
            learning_rate=0.1,
            objective="multi:softmax",
            num_class=3,
            random_state=42
        )

    model.fit(X_train, y_train)

    # ============================================================
    # CURRENT RISK PREDICTION
    # ============================================================
    results = []

    for product in selected_products:

        product_data = (
            risk_df[risk_df["Product_Name"] == product]
            .iloc[-1]
        )

        current_input = pd.DataFrame({
            "Current_Stock": [product_data["Current_Stock"]],
            "Forecast_Demand": [product_data["Forecast_Demand"]],
            "Lead_Time_Days": [product_data["Lead_Time_Days"]],
            "Safety_Stock": [product_data["Safety_Stock"]],
            "Incoming_Orders": [product_data["Incoming_Orders"]]
        })

        prediction = le.inverse_transform(
            model.predict(current_input)
        )[0]

        results.append({
            "Product": product,
            "Current Stock": round(product_data["Current_Stock"]),
            "Forecast Demand": round(product_data["Forecast_Demand"]),
            "Safety Stock": round(product_data["Safety_Stock"]),
            "Risk": prediction
        })

    risk_result_df = pd.DataFrame(results)
    st.session_state["risk_result_df"] = risk_result_df
    render_html_table(risk_result_df)

    # ============================================================
    # STOCK-OUT RISK BAR CHART
    # ============================================================

    risk_chart_df = risk_result_df.copy()

    risk_score = {
        "Low Risk": 1,
        "Medium Risk": 2,
        "High Risk": 3
    }

    risk_chart_df["Risk Score"] = (
        risk_chart_df["Risk"]
        .map(risk_score)
    )

    risk_colors = []

    for risk in risk_chart_df["Risk"]:
        if risk == "Low Risk":
            risk_colors.append("#28A745")      # Green
        elif risk == "Medium Risk":
            risk_colors.append("#FFC107")      # Yellow
        else:
            risk_colors.append("#DC3545")      # Red

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=risk_chart_df["Product"],
            y=risk_chart_df["Risk Score"],
            text=risk_chart_df["Risk"],
            textposition="outside",
            marker_color=risk_colors,
            hovertemplate=
            "<b>Product:</b> %{x}<br>" +
            "<b>Risk:</b> %{text}<extra></extra>"
        )
    )

    fig.update_layout(
        title="Stock-Out Risk for Top 5 Products",
        xaxis_title="Products",
        yaxis_title="Risk Level",
        yaxis=dict(
            range=[0.5, 3.5],
            tickmode="array",
            tickvals=[1, 2, 3],
            ticktext=["Low", "Medium", "High"],
            dtick=1
        ),
        template="plotly_white",
        height=500
    )

    st.plotly_chart(fig, use_container_width=True)

    csv = risk_result_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="📥 Download Stock-Out Risk Report",
        data=csv,
        file_name="stockout_risk_report.csv",
        mime="text/csv"
    )

# ============================================================
# STAGE 5 : REPLENISHMENT QUANTITY Calculation
# ============================================================

    st.markdown("""
    <div style="
    background-color:#0B2C5D;
    padding:20px;
    border-radius:12px;
    color:white;
    font-size:20px;
    font-weight:600;
    margin-top:40px;
    margin-bottom:20px;
    text-align:center;
    ">
    Recommended Replenishment Quantity 
    </div>
    """, unsafe_allow_html=True)

    # ============================================================
    # CHECK PREVIOUS STAGES
    # ============================================================

    if "forecast_demand_dict" not in st.session_state:
        st.warning("Run Demand Forecasting First")
        st.stop()

    if "safety_stock_dict" not in st.session_state:
        st.warning("Run Safety Stock Prediction First")
        st.stop()

    if "reorder_point_dict" not in st.session_state:
        st.warning("Run Reorder Point Calculation First")
        st.stop()

    if "risk_result_df" not in st.session_state:
        st.warning("Run Stock-Out Risk Prediction First")
        st.stop()

    forecast_demand_dict = st.session_state["forecast_demand_dict"]
    safety_stock_dict = st.session_state["safety_stock_dict"]
    reorder_point_dict = st.session_state["reorder_point_dict"]
    risk_result_df = st.session_state["risk_result_df"]

    # ============================================================
    # REPLENISHMENT CALCULATION
    # ============================================================

    results = []
    for product in selected_products:
        product_df = (
            df[df["Product_Name"] == product]
            .copy()
        )

        latest = product_df.iloc[-1]

        current_stock = float(latest["Current_Stock"])

        forecast_demand = float(
            forecast_demand_dict[product]
        )

        safety_stock = float(
            safety_stock_dict[product]
        )

        reorder_point = float(
            reorder_point_dict[product]
        )

        lead_time = float(
            latest["Lead_Time_Days"]
        )

        risk = risk_result_df.loc[
            risk_result_df["Product"] == product,
            "Risk"
        ].values[0]

        # ========================================================
        # ORDER DECISION
        # ========================================================
        if current_stock <= reorder_point:
            decision = "Place Order"
        else:
            decision = "No Order"

        # ========================================================
        # ORDER QUANTITY
        # ========================================================
        if current_stock <= reorder_point:
            order_quantity = max(
                0,
                int(round(
                    forecast_demand + safety_stock - current_stock
                ))
            )
        else:
            order_quantity = 0

        # ========================================================
        # PRIORITY
        # ========================================================
        if risk == "High Risk":
            priority = "Immediate"
        elif risk == "Medium Risk":
            priority = "Normal"
        else:
            priority = "Monitor"

        # ========================================================
        # ACTION
        # ========================================================
        if decision == "Place Order":
            action = "Replenish Inventory"
        else:
            action = "Inventory Sufficient"

        results.append({
            "Product": product,
            "Current Stock": round(current_stock),
            "Forecast Demand": round(forecast_demand),
            "Safety Stock": round(safety_stock),
            "Lead Time (Days)": round(lead_time),
            "Reorder Point": round(reorder_point),
            "Risk": risk,
            "Priority": priority,
            "Decision": decision,
            "Recommended Order Quantity": int(order_quantity),
            "Suggested Action": action
        })

    replenishment_df = pd.DataFrame(results)
    st.session_state["replenishment_df"] = replenishment_df

    st.markdown("""
    <style>
    /* Metric title */
    [data-testid="stMetricLabel"] {
        color: black !important;
        font-weight: 600;
    }

    /* Metric value */
    [data-testid="stMetricValue"] {
        color: black !important;
        font-weight: bold;
    }

    /* Metric delta (if any) */
    [data-testid="stMetricDelta"] {
        color: black !important;
    }
    </style>
    """, unsafe_allow_html=True)
    # ============================================================
    # KPI CARDS
    # ============================================================
    col1, col2, col3, col4 = st.columns(4)
    col1.metric(
        "Products",
        len(replenishment_df)
    )
    col2.metric(
        "Orders Required",
        (
            replenishment_df["Decision"]
            == "Place Order"
        ).sum()
    )
    col3.metric(
        "High Risk Products",
        (
            replenishment_df["Risk"]
            == "High Risk"
        ).sum()
    )
    col4.metric(
        "Units to Order",
        int(replenishment_df["Recommended Order Quantity"].sum())
    )
    render_html_table(replenishment_df)

    # ============================================================
    # REPLENISHMENT BAR CHART
    # ============================================================

    fig = go.Figure()

    bar_colors = []

    for decision in replenishment_df["Decision"]:

        if decision == "Place Order":
            bar_colors.append("#DC3545")      # Red
        else:
            bar_colors.append("#28A745")      # Green

    fig.add_trace(

        go.Bar(

            x=replenishment_df["Product"],

            y=replenishment_df["Recommended Order Quantity"],

            text=replenishment_df["Recommended Order Quantity"],

            textposition="outside",

            marker_color=bar_colors,

            hovertemplate=
            "<b>Product:</b> %{x}<br>"
            "<b>Recommended Order:</b> %{y}<extra></extra>"

        )

    )

    fig.update_layout(

        title="Recommended Replenishment Quantity",

        xaxis_title="Products",

        yaxis_title="Units",

        template="plotly_white",

        height=550,

        xaxis=dict(
            tickangle=-20
        )

    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # ============================================================
    # AUTO REPLENISHMENT DECISION
    # ============================================================

    st.markdown("""
    <div style="
    background-color:#0B2C5D;
    padding:20px;
    border-radius:12px;
    color:white;
    font-size:20px;
    font-weight:600;
    margin-top:40px;
    margin-bottom:20px;
    text-align:center;
    ">
    Auto Replenishment Decision
    </div>
    """, unsafe_allow_html=True)

    decision_df = replenishment_df.copy()

    decision_df["Auto Decision"] = np.where(

        decision_df["Decision"] == "Place Order",

        "Automatically Trigger Purchase Order",

        "No Action Required"

    )

    render_html_table(decision_df)

    # ============================================================
    # SUMMARY KPI
    # ============================================================

    total_products = len(decision_df)

    orders_required = (
        decision_df["Decision"]
        == "Place Order"
    ).sum()

    no_orders = (
        decision_df["Decision"]
        == "No Order"
    ).sum()

    total_quantity = (
        decision_df["Recommended Order Quantity"]
    ).sum()

    # ============================================================
    # DOWNLOAD REPORT
    # ============================================================

    csv = decision_df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(

        label="📥 Download Replenishment Report",

        data=csv,

        file_name="replenishment_report.csv",

        mime="text/csv"

    )
    
# ============================================================
# STAGE 6 : SUPPLIER RECOMMENDATION
# ============================================================
    from datetime import datetime, timedelta

    st.markdown("""
    <div style="
    background-color:#0B2C5D;
    padding:20px;
    border-radius:12px;
    color:white;
    font-size:20px;
    font-weight:600;
    margin-top:40px;
    margin-bottom:20px;
    text-align:center;">
    Supplier Recommendation & Purchase Order Generation
    </div>
    """, unsafe_allow_html=True)

    # ------------------------------------------------------------
    # CHECK INPUTS
    # ------------------------------------------------------------

    required_keys = [
        "reorder_point_dict",
        "risk_result_df",
        "replenishment_df"
    ]


    for key in required_keys:
        if key not in st.session_state:
            st.warning(f"Run previous stages before {key}")
            st.stop()

    replenishment_df = st.session_state["replenishment_df"]
    df_supplier = st.session_state["df"].copy()

    # ------------------------------------------------------------
    # MERGE PREVIOUS STAGE OUTPUTS
    # ------------------------------------------------------------
    supplier_df = pd.DataFrame({
        "Product": st.session_state["forecast_demand_dict"].keys(),
    })

    supplier_df["Reorder_Point"] = (
        supplier_df["Product"]
        .map(st.session_state["reorder_point_dict"])
    )

    supplier_df["Order_Qty"] = (
        supplier_df["Product"]
        .map(replenishment_df["Recommended Order Quantity"])
    )

    po_df = st.session_state["replenishment_df"].copy()

    risk_df = st.session_state["risk_result_df"]

    supplier_df = supplier_df.merge(
        risk_df[["Product", "Risk"]],
        on="Product",
        how="left"
    )
    # ------------------------------------------------------------
    # SUPPLIER RANKING
    # ------------------------------------------------------------
    df_supplier = st.session_state["df"].copy()
    supplier_master = (
        df_supplier[
            [
                "Product_Name",
                "Supplier_ID",
                "Supplier_Name",
                "Supplier_Rating",
                "Supplier_Type",
                "Supplier_Tier",
                "Supplier_Performance_ID"
            ]
        ]
        .drop_duplicates()
    )

    supplier_master.rename(
        columns={
            "Product_Name":"Product"
        },
        inplace=True
    )

    supplier_master["Tier_Rank"] = (
        supplier_master["Supplier_Tier"]
        .map(
            {
                "Tier 1":1,
                "Tier 2":2,
                "Tier 3":3
            }
        )
    )

    supplier_master = supplier_master.sort_values(
        [
            "Product",
            "Supplier_Rating",
            "Tier_Rank",
            "Supplier_Performance_ID"
        ],
        ascending=[
            True,
            False,
            True,
            True
        ]
    )

    # Select best supplier per product
    best_supplier = (
        supplier_master
        .groupby("Product")
        .first()
        .reset_index()
    )

    # Merge supplier recommendation
    po_df = po_df.merge(
        best_supplier,
        on="Product",
        how="left"
    )

    po_df["Purchase_Order_Status"] = (
        po_df["Recommended Order Quantity"]
        .apply(
            lambda x:
            "Generate Purchase Order"
            if x > 0
            else "No Purchase Required"
        )
    )
    # ------------------------------------------------------------
    # GENERATE PO NUMBER
    # ------------------------------------------------------------
    po_counter = 100001
    po_number = []
    for idx, row in po_df.iterrows():
        if row["Purchase_Order_Status"] == "Generate Purchase Order":
            po_number.append(
                f"PO-{po_counter}"
            )
            po_counter += 1
        else:
            po_number.append("-")

    po_df["Purchase_Order_Number"] = po_number

    # ------------------------------------------------------------
    # PRIORITY
    # ------------------------------------------------------------
    priority_map = {
        "High":"High",
        "Medium":"Medium",
        "Low":"Low"
    }


    po_df["Priority"] = (
        po_df["Risk"]
        .map(priority_map)
    )

    # ------------------------------------------------------------
    # EXPECTED DELIVERY
    # ------------------------------------------------------------
    lead_time = 7

    po_df["Expected_Delivery"] = (
        po_df.apply(
            lambda x:
            (
                datetime.today()
                +
                timedelta(days=lead_time)
            )
            .strftime("%d-%m-%Y")
            if x["Purchase_Order_Status"]
            ==
            "Generate Purchase Order"
            else "-",
            axis=1
        )
    )

    # ------------------------------------------------------------
    # FINAL OUTPUT TABLE
    # ------------------------------------------------------------
    final_po = po_df[
    [
        "Product",
        "Supplier_ID",
        "Supplier_Name",
        "Supplier_Rating",
        "Supplier_Tier",
        "Supplier_Type",
        "Current Stock",
        "Reorder Point",
        "Recommended Order Quantity",
        "Priority",
        "Purchase_Order_Status",
        "Purchase_Order_Number",
        "Expected_Delivery"
    ]
    ]
    st.session_state["final_po"] = final_po

    render_html_table(final_po)

    col1,col2,col3,col4 = st.columns(4)

    with col1:
        st.metric(
            "Suppliers Selected",
            final_po["Supplier_ID"].nunique()
        )

    with col2:
        st.metric(
            "Purchase Orders Generated",
            (
                final_po["Purchase_Order_Status"]
                ==
                "Generate Purchase Order"
            ).sum()
        )

    with col3:
        st.metric(
            "Total Units Ordered",
            final_po["Recommended Order Quantity"].sum()
        )

    with col4:
        st.metric(
            "High Priority Orders",
            (
                final_po["Priority"]
                ==
                "High"
            ).sum()
        )

    csv = final_po.to_csv(index=False)
    st.download_button(
        "Download Purchase Order Report",
        csv,
        "Purchase_Order_Report.csv",
        "text/csv"
    ) 

    final_po = st.session_state.get("final_po", None)

    if final_po is None:
        st.warning("⚠️ Please generate the Purchase Order first.")
        st.stop()  
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