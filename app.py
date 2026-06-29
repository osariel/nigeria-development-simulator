from pathlib import Path
from urllib.parse import quote

import altair as alt
import pandas as pd
import streamlit as st


BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"

BUDGET_COLUMNS = [
    "state",
    "year",
    "total_budget_ngn",
    "capital_budget_ngn",
    "recurrent_budget_ngn",
    "budget_status",
    "source_id",
    "data_status",
    "notes",
]

BUDGET_BASE_COLUMNS = [
    "state",
    "year",
    "total_budget_ngn",
]

BUDGET_OPTIONAL_COLUMNS = [
    "capital_budget_ngn",
    "recurrent_budget_ngn",
    "budget_status",
]

POPULATION_COLUMNS = [
    "state",
    "year",
    "population",
    "source_name",
    "source_url",
    "notes",
]

LEGACY_STATE_COLUMNS = [
    "state",
    "population",
    "annual_budget_ngn",
    "capital_budget_ngn",
    "recurrent_budget_ngn",
]

PROJECT_COST_COLUMNS = [
    "category",
    "item",
    "unit",
    "cost_ngn",
    "source_name",
    "source_url",
    "notes",
]

LEGACY_PROJECT_COST_COLUMNS = [
    "sector",
    "item",
    "unit_cost_ngn",
    "unit_name",
]

BUDGET_INSIGHTS_COLUMNS = [
    "state",
    "year",
    "sector",
    "theme",
    "planned_action",
    "amount_ngn",
    "source_id",
    "data_status",
    "notes",
]

FISCAL_INDICATOR_COLUMNS = [
    "state",
    "year",
    "indicator",
    "value",
    "unit",
    "source_id",
    "data_status",
    "notes",
]

BUDGET_OUTCOME_COLUMNS = [
    "state",
    "year",
    "sector",
    "outcome_metric",
    "value",
    "unit",
    "source_id",
    "data_status",
    "notes",
]

DEFAULT_PROJECT_COSTS = pd.DataFrame(
    [
        {
            "category": "Education",
            "item": "Primary school block",
            "unit": "school blocks",
            "cost_ngn": 120_000_000,
            "source_name": "Built-in fallback",
            "source_url": "",
            "notes": "Illustrative fallback assumption used only if project_costs.csv is missing or incomplete.",
        },
        {
            "category": "Healthcare",
            "item": "Primary health centre",
            "unit": "health centres",
            "cost_ngn": 250_000_000,
            "source_name": "Built-in fallback",
            "source_url": "",
            "notes": "Illustrative fallback assumption used only if project_costs.csv is missing or incomplete.",
        },
        {
            "category": "Water",
            "item": "Borehole water project",
            "unit": "boreholes",
            "cost_ngn": 15_000_000,
            "source_name": "Built-in fallback",
            "source_url": "",
            "notes": "Illustrative fallback assumption used only if project_costs.csv is missing or incomplete.",
        },
        {
            "category": "Roads",
            "item": "1 km rural road",
            "unit": "km of road",
            "cost_ngn": 500_000_000,
            "source_name": "Built-in fallback",
            "source_url": "",
            "notes": "Illustrative fallback assumption used only if project_costs.csv is missing or incomplete.",
        },
    ]
)

POPULATION_ESTIMATE_NOTE = (
    "Population figures are projection-based estimates, not new census counts."
)

PROJECT_COST_ESTIMATE_NOTE = (
    "Project costs are benchmark estimates and may vary by location, procurement "
    "method, inflation, and project specification."
)

PUBLIC_DISCLAIMER = (
    "For civic education and exploratory analysis. This tool does not provide "
    "financial, legal, or official government advice."
)

BUDGET_REVISION_POLICY_NOTE = (
    "Figures show the latest revised/supplementary approved budget where available; "
    "otherwise the original approved budget is shown. Proposed figures are clearly "
    "marked where used."
)

SOURCE_PENDING_STATUS = "source_pending"
LEGACY_PENDING_STATUS = "place" + "holder"


st.set_page_config(
    page_title="Nigeria Development Simulator",
    page_icon="NG",
    layout="centered",
)


st.markdown(
    """
    <style>
    *, *::before, *::after {
        box-sizing: border-box;
    }

    .stApp {
        background: #f8fafc;
        color: #0f172a;
        font-size: clamp(0.92rem, 2.5vw, 1rem);
    }

    .block-container {
        max-width: 760px;
        width: 100%;
        padding-top: clamp(0.75rem, 3vw, 1.4rem);
        padding-bottom: clamp(1.4rem, 5vw, 2.5rem);
        padding-left: clamp(1rem, 4vw, 2.5rem);
        padding-right: clamp(1rem, 4vw, 2.5rem);
    }

    header[data-testid="stHeader"] {
        display: none;
    }

    div[data-testid="stDecoration"] {
        display: none;
    }

    div[data-testid="stAppViewContainer"] {
        padding-top: 0;
    }

    h1 {
        font-size: clamp(1.6rem, 5vw, 2.6rem);
        line-height: 1.15;
        letter-spacing: 0;
        color: #0f172a;
    }

    h2 {
        font-size: clamp(1.25rem, 4vw, 2rem);
        line-height: 1.2;
        color: #111827;
        letter-spacing: 0;
    }

    h3 {
        font-size: clamp(1.05rem, 3vw, 1.4rem);
        line-height: 1.25;
        color: #111827;
        letter-spacing: 0;
    }

    p,
    li,
    label,
    [data-testid="stMarkdownContainer"] {
        font-size: clamp(0.92rem, 2.5vw, 1rem);
        line-height: 1.55;
    }

    .hero {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        width: 100%;
        max-width: 100%;
        padding: clamp(1rem, 4vw, 1.4rem);
        box-shadow: 0 8px 22px rgba(15, 23, 42, 0.06);
    }

    .hero h1 {
        margin-bottom: 0.65rem;
    }

    .hero p,
    .plain-card p,
    .note-card p {
        color: #334155;
        line-height: 1.6;
        margin-bottom: 0;
    }

    .metric-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 14px;
        width: 100%;
        max-width: 100%;
        min-width: 0;
        padding: clamp(0.85rem, 3vw, 1rem);
        margin-bottom: 0.75rem;
        box-shadow: 0 4px 14px rgba(15, 23, 42, 0.04);
        overflow-wrap: anywhere;
    }

    .project-result-card {
        background: #f8fafc;
        border: 1px solid #cbd5e1;
        border-left: 5px solid #1f7a5c;
        border-radius: 14px;
        width: 100%;
        max-width: 100%;
        min-width: 0;
        padding: clamp(1rem, 3.5vw, 1.2rem);
        margin-bottom: 0.85rem;
        box-shadow: 0 8px 20px rgba(15, 23, 42, 0.06);
        overflow-wrap: anywhere;
    }

    .metric-label {
        color: #64748b;
        font-size: clamp(0.78rem, 2.4vw, 0.86rem);
        font-weight: 700;
        margin-bottom: 0.35rem;
    }

    .metric-value {
        color: #0f172a;
        font-size: clamp(1.02rem, 4vw, 1.28rem);
        font-weight: 800;
        line-height: 1.25;
    }

    .metric-help {
        color: #475569;
        font-size: clamp(0.84rem, 2.4vw, 0.9rem);
        line-height: 1.45;
        margin-top: 0.4rem;
    }

    .project-result-card .metric-label {
        color: #166534;
    }

    .project-result-card .metric-value {
        color: #0f172a;
        font-size: clamp(1.25rem, 5vw, 1.65rem);
    }

    .infographic-card {
        background: #ffffff;
        border: 1px solid #dbe3ec;
        border-radius: 14px;
        width: 100%;
        max-width: 100%;
        min-width: 0;
        padding: clamp(0.9rem, 3vw, 1rem);
        margin-bottom: 0.75rem;
        box-shadow: 0 5px 16px rgba(15, 23, 42, 0.05);
        overflow-wrap: anywhere;
        transition: border-color 0.18s ease, box-shadow 0.18s ease, transform 0.18s ease;
    }

    .infographic-card:hover {
        border-color: #1f7a5c;
        box-shadow: 0 10px 24px rgba(15, 23, 42, 0.08);
        transform: translateY(-1px);
    }

    .infographic-link {
        display: block;
        color: inherit;
        text-decoration: none !important;
    }

    .infographic-link:focus-visible .infographic-card {
        outline: 3px solid rgba(31, 122, 92, 0.35);
        outline-offset: 2px;
        border-color: #1f7a5c;
        box-shadow: 0 10px 24px rgba(15, 23, 42, 0.08);
    }

    .infographic-icon {
        font-size: 1.45rem;
        line-height: 1;
        margin-bottom: 0.55rem;
    }

    .infographic-title {
        color: #0f172a;
        font-size: clamp(0.98rem, 3vw, 1.08rem);
        font-weight: 800;
        line-height: 1.25;
        margin-bottom: 0.35rem;
    }

    .infographic-text {
        color: #475569;
        font-size: clamp(0.86rem, 2.5vw, 0.94rem);
        line-height: 1.45;
    }

    .hero-stat-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        width: 100%;
        max-width: 100%;
        padding: clamp(1.2rem, 5vw, 1.6rem) clamp(1rem, 4vw, 1.4rem);
        margin-bottom: 0.85rem;
        text-align: center;
        box-shadow: 0 8px 22px rgba(15, 23, 42, 0.06);
    }

    .hero-stat-lead {
        color: #475569;
        font-size: clamp(0.9rem, 2.6vw, 1rem);
        margin-bottom: 0.4rem;
    }

    .hero-stat-value {
        color: #1f7a5c;
        font-size: clamp(2.2rem, 9vw, 2.8rem);
        font-weight: 800;
        line-height: 1.1;
        margin-bottom: 0.35rem;
    }

    .hero-stat-tail {
        color: #475569;
        font-size: clamp(0.9rem, 2.6vw, 1rem);
        margin: 0;
    }

    .stat-chip-row {
        display: flex;
        gap: clamp(0.4rem, 2vw, 0.6rem);
        margin-bottom: 1.1rem;
    }

    .stat-chip {
        flex: 1;
        min-width: 0;
        border-radius: 12px;
        padding: clamp(0.6rem, 2.5vw, 0.75rem);
        text-align: center;
    }

    .stat-chip-icon {
        font-size: 1.2rem;
        line-height: 1;
        margin-bottom: 0.3rem;
    }

    .stat-chip-text {
        font-size: clamp(0.8rem, 2.3vw, 0.86rem);
        font-weight: 700;
        line-height: 1.3;
        overflow-wrap: anywhere;
    }

    .stat-chip-green {
        background: #ecfdf5;
    }

    .stat-chip-green .stat-chip-text {
        color: #065f46;
    }

    .stat-chip-blue {
        background: #eff6ff;
    }

    .stat-chip-blue .stat-chip-text {
        color: #1e40af;
    }

    .nav-grid .infographic-card {
        height: 100%;
    }

    .about-data-toggle summary {
        color: #64748b !important;
        font-size: clamp(0.84rem, 2.4vw, 0.9rem) !important;
        font-weight: 700;
    }

    .about-badge {
        display: inline-block;
        background: #e0f2fe;
        border: 1px solid #7dd3fc;
        color: #075985;
        border-radius: 999px;
        padding: 0.25rem 0.7rem;
        font-size: 0.85rem;
        font-weight: 800;
        margin: 0.35rem 0 0.75rem 0;
    }

    .plain-card,
    .note-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 14px;
        width: 100%;
        max-width: 100%;
        min-width: 0;
        padding: clamp(0.85rem, 3vw, 1rem);
        margin-bottom: 0.8rem;
        box-shadow: 0 4px 14px rgba(15, 23, 42, 0.04);
        overflow-wrap: anywhere;
    }

    .note-card {
        background: #ecfdf5;
        border-color: #99f6e4;
    }

    .note-card p {
        color: #064e3b;
    }

    .small-muted {
        color: #64748b;
        font-size: clamp(0.84rem, 2.4vw, 0.9rem);
        line-height: 1.5;
    }

    div[data-testid="stHorizontalBlock"] {
        gap: clamp(0.4rem, 2vw, 1rem);
        width: 100%;
    }

    div[data-testid="column"] {
        min-width: 0;
    }

    div[data-testid="stDataFrame"],
    div[data-testid="stTable"] {
        width: 100%;
        max-width: 100%;
        overflow-x: auto;
    }

    div[data-testid="stDataFrame"] * {
        max-width: 100%;
    }

    /* Main app widgets: keep labels readable on light backgrounds. */
    section[data-testid="stMain"] [data-testid="stWidgetLabel"] p,
    section[data-testid="stMain"] [data-testid="stRadio"] label p,
    section[data-testid="stMain"] [data-testid="stRadio"] label span,
    section[data-testid="stMain"] [data-testid="stSelectbox"] label p,
    section[data-testid="stMain"] [data-testid="stNumberInput"] label p,
    section[data-testid="stMain"] [data-testid="stSlider"] label p,
    section[data-testid="stMain"] [data-testid="stExpander"] summary p {
        color: #0f172a !important;
    }

    section[data-testid="stMain"] [role="radiogroup"] label,
    section[data-testid="stMain"] [role="radiogroup"] label p,
    section[data-testid="stMain"] [role="radiogroup"] label span,
    section[data-testid="stMain"] [data-baseweb="radio"] div {
        color: #0f172a !important;
    }

    section[data-testid="stMain"] [data-baseweb="select"] div,
    section[data-testid="stMain"] [data-baseweb="select"] span,
    section[data-testid="stMain"] input {
        color: #0f172a !important;
        background-color: #ffffff;
        max-width: 100%;
    }

    .stButton button {
        background-color: #ffffff;
        color: #0f172a;
        border: 1px solid #cbd5e1;
        min-height: 2.75rem;
        width: 100%;
        max-width: 100%;
        touch-action: manipulation;
    }

    .stButton button p,
    .stButton button span {
        color: #0f172a !important;
    }

    div[data-testid="stAlert"] {
        border-radius: 12px;
        background-color: #fffbeb;
        border: 1px solid #f59e0b;
        color: #422006;
    }

    div[data-testid="stAlert"] p,
    div[data-testid="stAlert"] li,
    div[data-testid="stAlert"] span {
        color: #422006 !important;
    }

    @media (max-width: 768px) {
        .block-container {
            padding-top: 0.75rem;
            padding-bottom: 1.5rem;
            padding-left: 1rem;
            padding-right: 1rem;
        }

        .hero {
            border-radius: 14px;
            padding: 1rem;
        }

        .metric-card,
        .plain-card,
        .note-card,
        .infographic-card {
            border-radius: 12px;
            padding: 0.9rem;
            margin-bottom: 0.65rem;
        }

        div[data-testid="stHorizontalBlock"] {
            gap: 0.5rem;
        }

        div[data-testid="stVerticalBlock"] {
            gap: 0.45rem;
        }

        section[data-testid="stMain"] [data-baseweb="select"] > div,
        section[data-testid="stMain"] [data-baseweb="input"] > div,
        section[data-testid="stMain"] [data-testid="stNumberInput"] input {
            min-height: 2.75rem;
        }
    }

    @media (max-width: 480px) {
        .block-container {
            padding-top: 0.5rem;
            padding-left: 0.85rem;
            padding-right: 0.85rem;
        }

        .hero {
            padding: 0.9rem;
            box-shadow: 0 4px 12px rgba(15, 23, 42, 0.05);
        }

        h1 {
            margin-bottom: 0.45rem;
        }

        h2,
        h3 {
            margin-top: 0.7rem;
        }

        .metric-card,
        .plain-card,
        .note-card,
        .infographic-card {
            padding: 0.85rem;
            box-shadow: 0 3px 10px rgba(15, 23, 42, 0.04);
        }

        .metric-value {
            line-height: 1.2;
        }

        div[data-testid="stDataFrame"],
        div[data-testid="stTable"] {
            font-size: 0.86rem;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def format_ngn(value, long_form=False):
    if pd.isna(value):
        return "Not available yet"

    absolute_value = abs(value)
    scales = [
        (1_000_000_000_000, "tn", "trillion"),
        (1_000_000_000, "bn", "billion"),
        (1_000_000, "m", "million"),
    ]
    for divisor, compact_suffix, long_suffix in scales:
        if absolute_value >= divisor:
            amount = value / divisor
            suffix = long_suffix if long_form else compact_suffix
            separator = " " if long_form else ""
            return f"₦{amount:,.2f}{separator}{suffix}"

    return f"₦{value:,.0f}"


def format_naira(value):
    return format_ngn(value)


def format_ngn_long(value):
    return format_ngn(value, long_form=True)


def format_number(value):
    if pd.isna(value):
        return "Not available"
    return f"{value:,.0f}"


def format_percent(value):
    if pd.isna(value):
        return "Not available yet"
    return f"{value:.1f}%"


def has_value(value):
    return not pd.isna(value)


def safe_divide(numerator, denominator):
    if pd.isna(numerator) or pd.isna(denominator) or denominator <= 0:
        return pd.NA
    return numerator / denominator


def metric_card(label, value, help_text=None):
    help_markup = f'<div class="metric-help">{help_text}</div>' if help_text else ""
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            {help_markup}
        </div>
        """,
        unsafe_allow_html=True,
    )


def project_result_card(label, value, help_text=None):
    help_markup = f'<div class="metric-help">{help_text}</div>' if help_text else ""
    st.markdown(
        f"""
        <div class="project-result-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            {help_markup}
        </div>
        """,
        unsafe_allow_html=True,
    )


def infographic_card(icon, title, text):
    st.markdown(
        f"""
        <div class="infographic-card">
            <div class="infographic-icon">{icon}</div>
            <div class="infographic-title">{title}</div>
            <div class="infographic-text">{text}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def clickable_infographic_card(icon, title, text, target_page):
    page_param = quote(target_page)
    st.markdown(
        f"""
        <a class="infographic-link" href="?page={page_param}" aria-label="Open {title}">
            <div class="infographic-card">
                <div class="infographic-icon">{icon}</div>
                <div class="infographic-title">{title}</div>
                <div class="infographic-text">{text}</div>
            </div>
        </a>
        """,
        unsafe_allow_html=True,
    )


def hero_money_stat(lead_text, value, tail_text):
    st.markdown(
        f"""
        <div class="hero-stat-card">
            <p class="hero-stat-lead">{lead_text}</p>
            <p class="hero-stat-value">{value}</p>
            <p class="hero-stat-tail">{tail_text}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def stat_chip_row(chips):
    chip_markup = "".join(
        f'<div class="stat-chip stat-chip-{color}">'
        f'<div class="stat-chip-icon">{icon}</div>'
        f'<div class="stat-chip-text">{text}</div>'
        f"</div>"
        for icon, text, color in chips
    )
    st.markdown(f'<div class="stat-chip-row">{chip_markup}</div>', unsafe_allow_html=True)


def note_card(text):
    st.markdown(
        f"""
        <div class="note-card">
            <p>{text}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def budget_source_note(selected_year):
    if int(selected_year) == 2025:
        st.caption(
            "2025 state budget figures are sourced from BudgIT’s comparative analysis "
            "of approved budgets for Nigeria’s 36 states. FCT 2025 is not included "
            "in that source."
        )


def population_note():
    st.caption(POPULATION_ESTIMATE_NOTE)


def project_cost_note():
    st.caption(PROJECT_COST_ESTIMATE_NOTE)


def budget_101():
    with st.expander("Budget 101: what these words mean"):
        st.write(
            "Total budget is the full amount the state plans to spend in the selected year."
        )
        st.write(
            "Capital budget means money for projects and development, such as roads, "
            "schools, hospitals, water, power and equipment."
        )
        st.write(
            "Recurrent budget means money for running government day to day, including "
            "salaries, offices and regular services."
        )
        st.write(
            "Budget per resident is the total budget divided by the estimated population. "
            "It is an approximate way to understand scale."
        )


def format_optional_text(value):
    if pd.isna(value):
        return "Not available yet"
    text = str(value).strip()
    return text if text else "Not available yet"


def filter_state_year(dataframe, state, year):
    if dataframe.empty:
        return dataframe.copy()

    rows = dataframe.copy()
    return rows[
        (rows["state"].fillna("").astype(str).str.strip() == state)
        & (pd.to_numeric(rows["year"], errors="coerce") == int(year))
    ].copy()


def format_indicator_value(row):
    unit = str(row.get("unit", "")).strip().upper()
    value = row.get("value")
    if unit == "NGN":
        return format_ngn_long(value)
    return format_optional_text(value)


def data_status_label(status):
    normalized = str(status).strip().lower()
    if normalized == "verified":
        return "Verified from approved budget source"
    if normalized == "missing_split":
        return "Total budget verified; capital/recurrent split still pending"
    if normalized == "needs_review":
        return "This figure is awaiting source verification"
    if normalized in [SOURCE_PENDING_STATUS, LEGACY_PENDING_STATUS]:
        return "Source pending"
    if normalized == "verified_breakdown":
        return "Verified from approved budget source"
    if normalized == "revised_total_verified":
        return "Revised budget"
    if normalized == "revised_total_needs_review":
        return "Revised budget, source check pending"
    if normalized == "approved_total_verified":
        return "Original approved budget"
    if normalized == "approved_total_needs_review":
        return "Source check pending"
    if normalized == "partial_verified_total":
        return "Verified total, breakdown pending"
    if normalized == "proposed_total_needs_review":
        return "Proposed / not final"
    if normalized == "needs_extraction":
        return "Needs extraction"
    if normalized in ["estimated", "estimate", "projection", "estimated/projection"]:
        return "Estimated/projection"
    return "Not available yet"


def display_status_label(status, year=None, budget_status=None, state=None):
    normalized_status = str(status).strip().lower()
    normalized_budget_status = str(budget_status).strip().lower()
    normalized_state = str(state).strip().lower()
    numeric_year = pd.to_numeric(year, errors="coerce")

    if (
        pd.notna(numeric_year)
        and int(numeric_year) == 2025
        and normalized_budget_status == "missing"
        and normalized_state == "fct"
    ):
        return "No 2025 FCT value entered yet"
    if (
        pd.notna(numeric_year)
        and int(numeric_year) == 2025
        and normalized_status == "needs_review"
    ):
        return "Awaiting official-document review"
    return data_status_label(status)


def data_status_caption(status):
    normalized = str(status).strip().lower()
    if normalized in [SOURCE_PENDING_STATUS, LEGACY_PENDING_STATUS]:
        return "A source-backed figure is not available yet for this item."

    captions = {
        "verified": (
            "This figure has been extracted from an approved budget source."
        ),
        "missing_split": (
            "The total budget has a source, but the capital/recurrent split still needs extraction."
        ),
        "needs_review": (
            "This figure is awaiting source verification against an approved budget source."
        ),
        "verified_breakdown": (
            "Total, projects and running-government figures are available from a clear source."
        ),
        "revised_total_verified": (
            "The latest revised or supplementary approved total is available from a clear source."
        ),
        "revised_total_needs_review": (
            "This figure is from a public source and is being checked against official budget documents."
        ),
        "approved_total_verified": (
            "The original approved budget total is available; revised/supplementary status still depends on source extraction."
        ),
        "partial_verified_total": (
            "Total is available from a comparative source; breakdown is still pending."
        ),
        "approved_total_needs_review": (
            "This figure is from a public source and is being checked against official budget documents."
        ),
        "proposed_total_needs_review": (
            "This appears to be a proposal or pre-final figure, not a final approved budget."
        ),
        "needs_review": "A source has been identified, but the figure still needs review.",
        "needs_extraction": "The source has been identified, but detailed extraction is still pending.",
        "missing": "The budget figure has not yet been entered for this state/year.",
    }
    return captions.get(normalized, "Use this badge as a quick guide to data confidence.")


def display_status_caption(status, year=None, budget_status=None, state=None):
    normalized_status = str(status).strip().lower()
    normalized_budget_status = str(budget_status).strip().lower()
    normalized_state = str(state).strip().lower()
    numeric_year = pd.to_numeric(year, errors="coerce")

    if (
        pd.notna(numeric_year)
        and int(numeric_year) == 2025
        and normalized_budget_status == "missing"
        and normalized_state == "fct"
    ):
        return "The 2025 FCT budget figure has not yet been entered."
    if (
        pd.notna(numeric_year)
        and int(numeric_year) == 2025
        and normalized_status == "needs_review"
    ):
        return "This 2025 baseline figure is awaiting review against official state budget documents."
    return data_status_caption(status)


def row_status_label(row):
    return display_status_label(
        row.get("data_status"),
        row.get("year"),
        row.get("budget_status"),
        row.get("state"),
    )


def data_status_badge(status, year=None, budget_status=None, state=None):
    label = display_status_label(status, year, budget_status, state)
    normalized = str(status).strip().lower()
    if normalized in ["verified", "verified_breakdown"]:
        background = "#dcfce7"
        border = "#86efac"
        color = "#166534"
    elif normalized in ["missing_split", "approved_total_verified", "partial_verified_total"]:
        background = "#dbeafe"
        border = "#93c5fd"
        color = "#1e3a8a"
    elif normalized == "revised_total_verified":
        background = "#ede9fe"
        border = "#c4b5fd"
        color = "#4c1d95"
    elif normalized in [
        "estimated",
        "estimate",
        "projection",
        "estimated/projection",
        "needs_review",
        "approved_total_needs_review",
        "proposed_total_needs_review",
        "revised_total_needs_review",
    ]:
        background = "#fef9c3"
        border = "#fde047"
        color = "#854d0e"
    else:
        background = "#f1f5f9"
        border = "#cbd5e1"
        color = "#334155"

    st.markdown(
        f"""
        <div style="
            display:inline-block;
            background:{background};
            border:1px solid {border};
            color:{color};
            border-radius:999px;
            padding:0.25rem 0.7rem;
            font-size:0.85rem;
            font-weight:700;
            margin:0.35rem 0 0.75rem 0;">
            {label}
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.caption(display_status_caption(status, year, budget_status, state))


def source_caption(row):
    source_id = str(row.get("source_id", "")).strip()
    source_name = str(row.get("budget_source_name", "")).strip()
    publisher = str(row.get("budget_source_publisher", "")).strip()
    source_type = str(row.get("budget_source_type", "")).strip()
    stage = display_status_label(
        row.get("data_status", "missing"),
        row.get("year"),
        row.get("budget_status"),
        row.get("state"),
    )

    if source_id in ["", "SRC_PENDING", "unknown"] or not source_name:
        st.caption(f"Budget stage: {stage} | Source pending")
    else:
        parts = [f"Budget stage: {stage}", f"Source: {source_name}"]
        if publisher:
            parts.append(f"Publisher: {publisher}")
        if source_type:
            parts.append(f"Type: {source_type}")
        st.caption(" | ".join(parts))


def source_display_name(row):
    source_id = str(row.get("source_id", "")).strip()
    source_name = str(row.get("budget_source_name", "")).strip()
    if source_id in ["", "SRC_PENDING", "unknown"] or not source_name:
        return "Source pending"
    return source_name


def validate_columns(dataframe, required_columns, file_name):
    missing = [column for column in required_columns if column not in dataframe.columns]
    if missing:
        st.error(
            f"{file_name} is missing required column(s): {', '.join(missing)}. "
            "Please check the deployment data file."
        )
        st.stop()


def safe_read_csv(path, file_name):
    try:
        return pd.read_csv(path)
    except Exception:
        st.error(
            f"{file_name} could not be loaded. Please check the deployment data file."
        )
        st.stop()


def empty_dataframe(columns):
    return pd.DataFrame(columns=columns)


def load_optional_csv(path, expected_columns):
    if not path.exists():
        return empty_dataframe(expected_columns)

    try:
        dataframe = pd.read_csv(path)
    except Exception:
        return empty_dataframe(expected_columns)

    if not set(expected_columns).issubset(dataframe.columns):
        return empty_dataframe(expected_columns)

    return dataframe[expected_columns].copy()


@st.cache_data
def load_states():
    budgets_path = DATA_DIR / "state_budgets.csv"
    population_path = DATA_DIR / "state_population.csv"
    states_path = DATA_DIR / "states.csv"
    sources_path = DATA_DIR / "sources.csv"

    if budgets_path.exists():
        budgets = safe_read_csv(budgets_path, "data/state_budgets.csv")
        validate_columns(budgets, BUDGET_BASE_COLUMNS, "data/state_budgets.csv")

        if population_path.exists():
            population = safe_read_csv(population_path, "data/state_population.csv")
            validate_columns(population, POPULATION_COLUMNS, "data/state_population.csv")
            population = population[POPULATION_COLUMNS].copy()
        elif states_path.exists():
            population = safe_read_csv(states_path, "data/states.csv")
            validate_columns(population, LEGACY_STATE_COLUMNS, "data/states.csv")
            if "year" not in population.columns:
                population["year"] = 2025
            population = population[["state", "year", "population"]].copy()
            population["source_name"] = "Legacy states.csv fallback"
            population["source_url"] = ""
            population["notes"] = (
                "Fallback population value from data/states.csv."
            )
        else:
            population = pd.DataFrame(columns=POPULATION_COLUMNS)

        for column in BUDGET_OPTIONAL_COLUMNS:
            if column not in budgets.columns:
                budgets[column] = pd.NA
        if "budget_status" not in budgets.columns:
            budgets["budget_status"] = "missing"
        if "source_id" not in budgets.columns:
            budgets["source_id"] = "unknown"
        if "data_status" not in budgets.columns:
            budgets["data_status"] = SOURCE_PENDING_STATUS
        if "notes" not in budgets.columns:
            budgets["notes"] = ""

        budgets = budgets[BUDGET_COLUMNS].copy()

        budgets["year"] = budgets["year"].astype(int)
        population["year"] = population["year"].astype(int)

        budgets = budgets.rename(
            columns={
                "total_budget_ngn": "annual_budget_ngn",
                "notes": "budget_notes",
            }
        )
        population = population.rename(
            columns={
                "source_name": "population_source_name",
                "source_url": "population_source_url",
                "notes": "population_notes",
            }
        )

        states = budgets.merge(
            population,
            on=["state", "year"],
            how="outer",
            validate="one_to_one",
        )

        if states.empty:
            st.error(
                "No budget rows were found in data/state_budgets.csv. Please check "
                "the deployment data file."
            )
            st.stop()

        states["source_id"] = states["source_id"].fillna("unknown")
        states["data_status"] = states["data_status"].fillna(SOURCE_PENDING_STATUS)
        states["budget_notes"] = states["budget_notes"].fillna("")
        if sources_path.exists():
            sources = safe_read_csv(sources_path, "data/sources.csv")
            source_columns = [
                "source_id",
                "source_name",
                "source_url",
                "budget_type",
                "document_title",
                "extraction_status",
            ]
            if set(source_columns).issubset(sources.columns):
                source_lookup = (
                    sources[source_columns]
                    .dropna(subset=["source_id"])
                    .drop_duplicates(subset=["source_id"], keep="last")
                )
                states = states.merge(
                    source_lookup,
                    on="source_id",
                    how="left",
                    validate="many_to_one",
                )
                states["budget_source_name"] = states["source_name"].fillna(
                    states["source_id"]
                )
                states["budget_source_publisher"] = ""
                states["budget_source_type"] = states["budget_type"].fillna("")
                states["budget_source_url"] = states["source_url"].fillna("")
                states["budget_document_title"] = states["document_title"].fillna("")
                states["budget_extraction_status"] = states[
                    "extraction_status"
                ].fillna("")
                states = states.drop(
                    columns=[
                        "source_name",
                        "source_url",
                        "budget_type",
                        "document_title",
                        "extraction_status",
                    ]
                )
            else:
                states["budget_source_name"] = states["source_id"].fillna("unknown")
                states["budget_source_publisher"] = ""
                states["budget_source_type"] = ""
                states["budget_source_url"] = ""
                states["budget_document_title"] = ""
                states["budget_extraction_status"] = ""
        else:
            states["budget_source_name"] = states["source_id"].fillna("unknown")
            states["budget_source_publisher"] = ""
            states["budget_source_type"] = ""
            states["budget_source_url"] = ""
            states["budget_document_title"] = ""
            states["budget_extraction_status"] = ""

        data_mode = "new"
    else:
        states = safe_read_csv(states_path, "data/states.csv")
        validate_columns(states, LEGACY_STATE_COLUMNS, "data/states.csv")

        if "year" not in states.columns:
            states["year"] = 2025

        states["budget_source_name"] = "Legacy states.csv fallback"
        states["budget_source_publisher"] = ""
        states["budget_source_type"] = "Legacy fallback CSV"
        states["budget_source_url"] = ""
        states["budget_notes"] = (
            "Fallback budget value from data/states.csv."
        )
        states["source_id"] = "legacy_states_csv"
        states["data_status"] = SOURCE_PENDING_STATUS
        states["budget_status"] = SOURCE_PENDING_STATUS
        states["population_source_name"] = "Legacy states.csv fallback"
        states["population_source_url"] = ""
        states["population_notes"] = (
            "Fallback population value from data/states.csv."
        )
        data_mode = "legacy"


    states["year"] = states["year"].astype(int)
    states["data_status"] = states["data_status"].fillna(SOURCE_PENDING_STATUS)
    states["data_status"] = states["data_status"].where(
        states["data_status"].isin(
            [
                "verified",
                "missing_split",
                "needs_review",
                SOURCE_PENDING_STATUS,
                LEGACY_PENDING_STATUS,
                "Verified",
                "Estimated",
                "Estimated/projection",
                "Missing/partial",
                "missing",
                "verified_breakdown",
                "revised_total_verified",
                "revised_total_needs_review",
                "partial_verified_total",
                "approved_total_verified",
                "approved_total_needs_review",
                "proposed_total_needs_review",
            ]
        ),
        SOURCE_PENDING_STATUS,
    )

    numeric_columns = [
        "population",
        "annual_budget_ngn",
        "capital_budget_ngn",
        "recurrent_budget_ngn",
    ]
    for column in numeric_columns:
        states[column] = pd.to_numeric(states[column], errors="coerce")

    states["state"] = states["state"].fillna("").astype(str).str.strip()
    states["usable_for_core_metrics"] = (
        (states["state"] != "")
        & (states["population"] > 0)
        & (states["annual_budget_ngn"] > 0)
    )

    if not states["usable_for_core_metrics"].any():
        st.error(
            "No usable state budget rows were found. At least one row must have "
            "state, positive population, and positive total budget."
        )
        st.stop()

    states["annual_budget_per_person"] = states.apply(
        lambda row: safe_divide(row["annual_budget_ngn"], row["population"]),
        axis=1,
    )
    states["capital_budget_per_person"] = states.apply(
        lambda row: safe_divide(row["capital_budget_ngn"], row["population"]),
        axis=1,
    )
    states["recurrent_budget_per_person"] = states.apply(
        lambda row: safe_divide(row["recurrent_budget_ngn"], row["population"]),
        axis=1,
    )
    states["capital_share_percent"] = states.apply(
        lambda row: (
            safe_divide(row["capital_budget_ngn"], row["annual_budget_ngn"]) * 100
            if has_value(safe_divide(row["capital_budget_ngn"], row["annual_budget_ngn"]))
            else pd.NA
        ),
        axis=1,
    )
    states["recurrent_share_percent"] = states.apply(
        lambda row: (
            safe_divide(row["recurrent_budget_ngn"], row["annual_budget_ngn"]) * 100
            if has_value(safe_divide(row["recurrent_budget_ngn"], row["annual_budget_ngn"]))
            else pd.NA
        ),
        axis=1,
    )

    return (
        states.sort_values(["state", "year"]).reset_index(drop=True),
        data_mode,
    )


@st.cache_data
def load_project_costs():
    costs_path = DATA_DIR / "project_costs.csv"

    if not costs_path.exists():
        return DEFAULT_PROJECT_COSTS.copy(), True

    costs = safe_read_csv(costs_path, "data/project_costs.csv")

    if all(column in costs.columns for column in PROJECT_COST_COLUMNS):
        costs = costs[PROJECT_COST_COLUMNS].copy()
    elif all(column in costs.columns for column in LEGACY_PROJECT_COST_COLUMNS):
        costs = costs[LEGACY_PROJECT_COST_COLUMNS].copy()
        costs = costs.rename(
            columns={
                "sector": "category",
                "unit_name": "unit",
                "unit_cost_ngn": "cost_ngn",
            }
        )
        costs["source_name"] = "Legacy project_costs.csv fallback"
        costs["source_url"] = ""
        costs["notes"] = (
            "Fallback-compatible assumption from the older project_costs.csv format."
        )
    else:
        return DEFAULT_PROJECT_COSTS.copy(), True

    costs["cost_ngn"] = pd.to_numeric(costs["cost_ngn"], errors="coerce")
    costs = costs.dropna(subset=["category", "item", "unit", "cost_ngn"])
    costs = costs[costs["cost_ngn"] > 0]
    costs[["source_name", "source_url", "notes"]] = costs[
        ["source_name", "source_url", "notes"]
    ].fillna("")

    if costs.empty:
        return DEFAULT_PROJECT_COSTS.copy(), True

    return costs.reset_index(drop=True), False


@st.cache_data
def load_budget_insights_data():
    budget_insights = load_optional_csv(
        DATA_DIR / "state_budget_insights.csv",
        BUDGET_INSIGHTS_COLUMNS,
    )
    fiscal_indicators = load_optional_csv(
        DATA_DIR / "state_fiscal_indicators.csv",
        FISCAL_INDICATOR_COLUMNS,
    )
    budget_outcomes = load_optional_csv(
        DATA_DIR / "state_budget_outcomes.csv",
        BUDGET_OUTCOME_COLUMNS,
    )

    for dataframe in [budget_insights, fiscal_indicators, budget_outcomes]:
        if "year" in dataframe.columns:
            dataframe["year"] = pd.to_numeric(dataframe["year"], errors="coerce")

    if "amount_ngn" in budget_insights.columns:
        budget_insights["amount_ngn"] = pd.to_numeric(
            budget_insights["amount_ngn"],
            errors="coerce",
        )
    if "value" in fiscal_indicators.columns:
        fiscal_indicators["value"] = pd.to_numeric(
            fiscal_indicators["value"],
            errors="coerce",
        )
    if "value" in budget_outcomes.columns:
        budget_outcomes["value"] = pd.to_numeric(
            budget_outcomes["value"],
            errors="coerce",
        )

    return budget_insights, fiscal_indicators, budget_outcomes


states, state_data_mode = load_states()
project_costs, using_default_project_costs = load_project_costs()
budget_insights, fiscal_indicators, budget_outcomes = load_budget_insights_data()


def year_update_note(selected_year):
    if int(selected_year) == 2025:
        budget_source_note(selected_year)
    if int(selected_year) == 2026:
        st.info(
            "2026 data is being added gradually. Revised/supplementary or original "
            "approved totals are shown where available; missing values mean the "
            "approved figure has not yet been extracted."
        )


def year_data_notes(selected_year):
    with st.expander("Data notes for this year"):
        st.caption(f"Showing budget data for {selected_year}.")
        st.caption(BUDGET_REVISION_POLICY_NOTE)
        year_update_note(selected_year)


def _data_quality_summary_body(year_data, selected_year):
    total_rows = year_data["state"].nunique()
    rows_with_budget = year_data.loc[
        year_data["annual_budget_ngn"].notna() & (year_data["annual_budget_ngn"] > 0),
        "state",
    ].nunique()
    missing_budget = max(total_rows - rows_with_budget, 0)
    status_counts_raw = year_data["data_status"].fillna(SOURCE_PENDING_STATUS).astype(str)
    verified_rows = int((status_counts_raw == "verified").sum())
    missing_split_rows = int((status_counts_raw == "missing_split").sum())
    needs_review_rows = int((status_counts_raw == "needs_review").sum())

    st.caption(
        f"For {selected_year}, {rows_with_budget} states/FCT have budget figures "
        f"available and {missing_budget} are not available yet."
    )
    metric_card("States in dataset", format_number(total_rows))
    metric_card("States with budget figures", format_number(rows_with_budget))
    if int(selected_year) == 2026:
        metric_card("Verified rows", format_number(verified_rows))
        metric_card("Missing split rows", format_number(missing_split_rows))
        metric_card("Needs review rows", format_number(needs_review_rows))
        st.caption(
            "2026 data currently covers all 36 states and FCT. Rows marked verified "
            "have source-backed totals and splits. Rows marked missing_split have a "
            "reported or approved total but the capital/recurrent split is still being "
            "reconciled. Rows marked needs_review should be treated as provisional."
        )

    if missing_budget:
        missing_states = (
            year_data.loc[
                year_data["annual_budget_ngn"].isna()
                | (year_data["annual_budget_ngn"] <= 0),
                "state",
            ]
            .dropna()
            .astype(str)
            .sort_values()
            .tolist()
        )
        st.warning(
            "Some states/FCT are still missing budget figures for this year."
        )
        st.caption("States where budget figures are not available yet:")
        st.write(", ".join(missing_states))
    else:
        st.caption("All states/FCT for this year currently have budget figures.")

    status_counts = (
        year_data.apply(row_status_label, axis=1)
        .value_counts()
        .reset_index()
    )
    status_counts.columns = ["Status", "Count"]
    st.caption("Source status summary")
    st.dataframe(status_counts, hide_index=True, width="stretch")


def data_quality_summary(year_data, selected_year):
    with st.expander("See data coverage"):
        _data_quality_summary_body(year_data, selected_year)


def about_this_data(year_data, selected_year):
    st.markdown('<div class="about-data-toggle">', unsafe_allow_html=True)
    with st.expander("About this data"):
        st.caption(f"Showing budget data for {selected_year}.")
        st.caption(BUDGET_REVISION_POLICY_NOTE)
        year_update_note(selected_year)
        st.caption(POPULATION_ESTIMATE_NOTE)
        st.write("")
        _data_quality_summary_body(year_data, selected_year)
    st.markdown("</div>", unsafe_allow_html=True)


def get_state_year_selection(year_data, selected_year, prefix=""):
    state_options = year_data["state"].drop_duplicates().sort_values().tolist()
    selected_state = st.session_state.get("selected_state")
    if selected_state not in state_options:
        selected_state = state_options[0]

    row = year_data[year_data["state"] == selected_state].iloc[0]

    return selected_state, selected_year, row


def budget_breakdown_text(row):
    capital = row["capital_share_percent"]
    recurrent = row["recurrent_share_percent"]
    if pd.isna(capital) or pd.isna(recurrent):
        state = format_optional_text(row.get("state"))
        year = format_optional_text(row.get("year"))
        if has_value(row.get("annual_budget_ngn")):
            return (
                f"For {state} in {year}, we have the total budget, but not yet "
                "the full breakdown between projects and day-to-day government costs."
            )
        return f"For {state} in {year}, the budget figure is not available yet."
    return (
        f"For every ₦100 in the budget, about ₦{capital:.0f} goes to "
        f"projects and development, while about ₦{recurrent:.0f} goes to "
        "running government."
    )


def budget_split_chart(row):
    split_data = pd.DataFrame(
        [
            {
                "Category": "Projects and development",
                "Amount": row.get("capital_budget_ngn"),
            },
            {
                "Category": "Running government",
                "Amount": row.get("recurrent_budget_ngn"),
            },
        ]
    ).dropna(subset=["Amount"])
    split_data = split_data[split_data["Amount"] > 0]

    if split_data.empty:
        st.info("The projects/running-government split is not available yet.")
        return

    chart = (
        alt.Chart(split_data)
        .mark_bar(cornerRadiusEnd=4, color="#1f7a5c")
        .encode(
            y=alt.Y(
                "Category:N",
                sort="-x",
                title=None,
                axis=alt.Axis(labelLimit=220, labelFontSize=13),
            ),
            x=alt.X(
                "Amount:Q",
                title="Amount",
                axis=naira_axis(),
            ),
            tooltip=[
                alt.Tooltip("Category:N", title="Category"),
                alt.Tooltip("AmountLabel:N", title="Amount"),
            ],
        )
        .transform_calculate(
            AmountLabel=(
                "datum.Amount >= 1000000000000 ? '₦' + format(datum.Amount / 1000000000000, '.2f') + 'tn' : "
                "datum.Amount >= 1000000000 ? '₦' + format(datum.Amount / 1000000000, '.2f') + 'bn' : "
                "datum.Amount >= 1000000 ? '₦' + format(datum.Amount / 1000000, '.2f') + 'm' : "
                "'₦' + format(datum.Amount, ',.0f')"
            )
        )
        .properties(height=220)
    )
    st.altair_chart(chart, width="stretch")


def naira_axis():
    return alt.Axis(
        labelExpr=(
            "datum.value >= 1000000000000 ? '₦' + format(datum.value / 1000000000000, '.0f') + 'tn' : "
            "datum.value >= 1000000000 ? '₦' + format(datum.value / 1000000000, '.0f') + 'bn' : "
            "datum.value >= 1000000 ? '₦' + format(datum.value / 1000000, '.0f') + 'm' : "
            "'₦' + format(datum.value, ',.0f')"
        ),
        labelFontSize=12,
    )


def horizontal_budget_chart(data, value_column, title, status_column=None):
    chart_columns = ["state", "year", "budget_status", value_column]
    if status_column:
        chart_columns.append(status_column)
    chart_data = data[chart_columns].copy()
    chart_data = chart_data.dropna(subset=[value_column])
    if chart_data.empty:
        return None

    chart_data["Formatted value"] = chart_data[value_column].map(format_naira)
    if status_column:
        chart_data["Data confidence"] = chart_data.apply(row_status_label, axis=1)

    chart_height = max(240, min(520, 42 * len(chart_data)))
    tooltips = [
        alt.Tooltip("state:N", title="State"),
        alt.Tooltip("Formatted value:N", title=title),
    ]
    if status_column:
        tooltips.append(alt.Tooltip("Data confidence:N", title="Data confidence"))

    return (
        alt.Chart(chart_data)
        .mark_bar(cornerRadiusEnd=4, color="#1f7a5c")
        .encode(
            y=alt.Y(
                "state:N",
                sort="-x",
                title=None,
                axis=alt.Axis(labelLimit=180, labelFontSize=13),
            ),
            x=alt.X(
                f"{value_column}:Q",
                title=title,
                axis=naira_axis(),
            ),
            tooltip=tooltips,
        )
        .properties(height=chart_height)
    )


def ranking_bar_chart(ranked, ranking_column, selected_ranking):
    chart_data = ranked[
        ["state", "year", "budget_status", ranking_column, "data_status"]
    ].copy()
    chart_data["Formatted value"] = (
        chart_data[ranking_column].map(format_percent)
        if ranking_column == "capital_share_percent"
        else chart_data[ranking_column].map(format_naira)
    )
    chart_data["Data confidence"] = chart_data.apply(row_status_label, axis=1)
    chart_height = max(260, min(520, 42 * len(chart_data)))

    value_axis = (
        alt.Axis(labelExpr="format(datum.value, '.0f') + '%'", labelFontSize=12)
        if ranking_column == "capital_share_percent"
        else naira_axis()
    )

    chart = (
        alt.Chart(chart_data)
        .mark_bar(cornerRadiusEnd=4, color="#1f7a5c")
        .encode(
            y=alt.Y(
                "state:N",
                sort="-x",
                title=None,
                axis=alt.Axis(labelLimit=180, labelFontSize=13),
            ),
            x=alt.X(
                f"{ranking_column}:Q",
                title=selected_ranking,
                axis=value_axis,
            ),
            tooltip=[
                alt.Tooltip("state:N", title="State"),
                alt.Tooltip("Formatted value:N", title=selected_ranking),
                alt.Tooltip("Data confidence:N", title="Data confidence"),
            ],
        )
        .properties(height=chart_height)
    )
    st.altair_chart(chart, width="stretch")


def partial_data_caption(row):
    missing = []
    labels = {
        "capital_budget_ngn": "projects and development",
        "recurrent_budget_ngn": "running government",
    }
    for column, label in labels.items():
        if pd.isna(row.get(column)):
            missing.append(label)

    if missing:
        st.caption(
            "Partial data: "
            + ", ".join(missing)
            + " not available for this state/year."
        )


def has_budget_breakdown(row):
    return has_value(row.get("capital_budget_ngn")) and has_value(
        row.get("recurrent_budget_ngn")
    )


def has_pending_split(row):
    return has_value(row.get("annual_budget_ngn")) and not has_budget_breakdown(row)


def total_budget_help(row):
    if not has_value(row.get("annual_budget_ngn")):
        return "This total budget figure has not yet been extracted for this state/year."
    if not has_budget_breakdown(row):
        return "The approved total is available; the projects/running-government split is still pending."
    return "This is the approved spending envelope recorded for the selected year."


def capital_budget_help(row):
    if not has_value(row.get("capital_budget_ngn")):
        return "The projects and development figure has not yet been extracted."
    return "This is the portion usually linked to infrastructure and development projects."


def recurrent_budget_help(row):
    if not has_value(row.get("recurrent_budget_ngn")):
        return "The running-government figure has not yet been extracted."
    return "This is the portion usually linked to salaries and day-to-day government costs."


def per_person_budget_help(row):
    if not has_value(row.get("annual_budget_per_person")):
        return "This cannot be calculated until both total budget and population are available."
    return "Approximate amount per resident, using projection-based population figures."


def project_per_person_budget_help(row):
    if not has_value(row.get("capital_budget_per_person")):
        return "This cannot be calculated until the projects budget is available."
    return "Approximate projects budget per resident, using projection-based population figures."


def project_translation(amount, costs):
    rows = []
    for _, project in costs.iterrows():
        units = amount / project["cost_ngn"]
        rows.append(
            {
                "item": project["item"],
                "unit_name": project["unit"],
                "unit_cost": project["cost_ngn"],
                "units": units,
            }
        )
    return rows


def public_project_label(item):
    item_text = str(item).lower()
    if "school" in item_text:
        return "Schools"
    if "health" in item_text or "hospital" in item_text or "clinic" in item_text:
        return "Health centres"
    if "borehole" in item_text or "water" in item_text:
        return "Boreholes"
    if "road" in item_text:
        return "Roads"
    return str(item).title()


PUBLIC_PAGES = [
    "Home",
    "My State",
    "What Could This Build?",
    "Compare States",
    "Rankings",
    "Where The Money Goes",
    "About",
]


query_page = st.query_params.get("page")
if query_page in PUBLIC_PAGES:
    st.session_state["page"] = query_page
    del st.query_params["page"]

if st.session_state.get("page") not in PUBLIC_PAGES:
    st.session_state["page"] = "Home"

available_years = states["year"].drop_duplicates().sort_values(ascending=False).tolist()
if st.session_state.get("selected_year") not in available_years:
    st.session_state["selected_year"] = available_years[0]


def year_data_for(year):
    return states[states["year"] == year].copy()


def state_options_for(year):
    return year_data_for(year)["state"].drop_duplicates().sort_values().tolist()


def ensure_selected_state_for_year(year):
    state_options = state_options_for(year)
    if not state_options:
        st.error(f"No states are available for {year}.")
        st.stop()

    preferred_state = st.session_state.get("selected_state")
    if preferred_state not in state_options:
        st.session_state["selected_state"] = (
            "Lagos" if "Lagos" in state_options else state_options[0]
        )
    return state_options


ensure_selected_state_for_year(st.session_state["selected_year"])


def render_exploration_controls(title="Choose what to explore", helper_text=None):
    if title:
        st.markdown(f"### {title}")
    if helper_text:
        st.caption(helper_text)

    if st.session_state.get("selected_year_control") not in available_years:
        st.session_state["selected_year_control"] = st.session_state["selected_year"]
    year_col, state_col = st.columns(2)
    with year_col:
        selected_year = st.selectbox(
            "Select budget year",
            available_years,
            key="selected_year_control",
        )
    st.session_state["selected_year"] = selected_year

    state_options = ensure_selected_state_for_year(selected_year)
    if st.session_state.get("selected_state_control") not in state_options:
        st.session_state["selected_state_control"] = st.session_state["selected_state"]
    with state_col:
        selected_state = st.selectbox(
            "Select state",
            state_options,
            key="selected_state_control",
        )
    st.session_state["selected_state"] = selected_state

    selected_year = st.session_state["selected_year"]
    selected_year_data = year_data_for(selected_year)
    if selected_year_data.empty:
        st.error(f"No budget rows are available for {selected_year}.")
        st.stop()
    return selected_year, selected_year_data


def render_back_to_home():
    st.markdown(
        '<a href="?page=Home" aria-label="Back to Home">← Back to Home</a>',
        unsafe_allow_html=True,
    )


selected_year = st.session_state["selected_year"]
selected_year_data = year_data_for(selected_year)
if selected_year_data.empty:
    st.error(f"No budget rows are available for {selected_year}.")
    st.stop()


page = st.session_state["page"]

if page == "Home":
    st.markdown(
        """
        <div class="hero">
            <h1>Our States' Budgets</h1>
            <h3>Explore how Nigerian states plan, compare, and spend public money.</h3>
            <p>
                Government budgets are public documents, but they're written for accountants,
                not citizens. This tool turns the numbers in your state's budget into plain
                language, so you can see what your government plans to spend and what that
                could mean for you.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.caption(
        "The aim is to make public budget information easier to understand, compare, and discuss."
    )

    st.markdown("### How it works")
    note_card(
        "Say you pick Edo state. You'd see that in 2026 it plans to spend about "
        "₦940bn in total, around ₦210,000 for every person in the state. Tap "
        "\"What it could build\" and that same money turns into things you can picture, "
        "like schools, clinics, and boreholes. Tap \"Compare states\" to see how Edo "
        "stacks up against its neighbours."
    )

    st.markdown("### Start exploring")
    grid_left, grid_right = st.columns(2)
    with grid_left:
        clickable_infographic_card(
            "🧾",
            "Where it goes",
            "Projects vs. running costs.",
            "Where The Money Goes",
        )
        clickable_infographic_card(
            "⚖️",
            "Compare states",
            "See states side by side.",
            "Compare States",
        )
    with grid_right:
        clickable_infographic_card(
            "🧮",
            "What it could build",
            "Schools, clinics, roads.",
            "What Could This Build?",
        )
        clickable_infographic_card(
            "🏆",
            "Rankings",
            "Who spends most per person.",
            "Rankings",
        )


elif page == "My State":
    render_back_to_home()
    selected_year, selected_year_data = render_exploration_controls(
        helper_text="You can change these selections here, or return Home to choose a different starting point."
    )

    selected_state, selected_year, row = get_state_year_selection(
        selected_year_data, selected_year, "explorer"
    )

    per_person = (
        format_naira(row["annual_budget_per_person"])
        if has_value(row["annual_budget_per_person"])
        else "Not available yet"
    )
    hero_money_stat(
        f"This year, {selected_state} state's government plans to spend",
        per_person,
        "on every person in the state",
    )

    chips = []
    if has_value(row["annual_budget_ngn"]):
        chips.append(("🏦", f"Total budget: {format_naira(row['annual_budget_ngn'])}", "green"))
    if has_value(row["population"]):
        chips.append(("👥", f"{format_number(row['population'])} people", "blue"))
    if chips:
        stat_chip_row(chips)

    if has_budget_breakdown(row):
        metric_card(
            "Projects and Development",
            format_naira(row["capital_budget_ngn"]),
            capital_budget_help(row),
        )
        metric_card(
            "Running Government",
            format_naira(row["recurrent_budget_ngn"]),
            recurrent_budget_help(row),
        )
        if has_value(row["capital_budget_per_person"]):
            metric_card(
                "Project Budget per Resident",
                format_naira(row["capital_budget_per_person"]),
                project_per_person_budget_help(row),
            )

    if has_budget_breakdown(row):
        st.markdown("### Where the money goes")
        budget_split_chart(row)
        metric_card("For every ₦100", budget_breakdown_text(row))

    st.markdown("### What this means")
    if not has_budget_breakdown(row):
        note_card(
            f"We have the total budget for {selected_state} in {selected_year}. "
            "Capital/recurrent split pending."
        )
    else:
        note_card(
            f"{selected_state}'s total budget is {format_ngn_long(row['annual_budget_ngn'])}. "
            f"Projects and development share: {format_percent(row['capital_share_percent'])}. "
            f"Running government share: {format_percent(row['recurrent_share_percent'])}."
        )

    budget_101()

    with st.expander("See source details"):
        data_status_badge(
            row["data_status"],
            row.get("year"),
            row.get("budget_status"),
            row.get("state"),
        )
        source_caption(row)

    with st.expander("See detailed data"):
        details = [
            {
                "Label": "Annual budget per resident",
                "Value": format_ngn_long(row["annual_budget_per_person"]),
            },
            {
                "Label": "Budget data status",
                "Value": row_status_label(row),
            },
            {
                "Label": "Population source",
                "Value": row["population_source_name"],
            },
        ]
        if has_budget_breakdown(row):
            details.extend(
                [
                    {
                        "Label": "Capital/project budget per resident",
                        "Value": format_ngn_long(row["capital_budget_per_person"]),
                    },
                    {
                        "Label": "Recurrent/running government per resident",
                        "Value": format_ngn_long(row["recurrent_budget_per_person"]),
                    },
                    {
                        "Label": "Projects and development share",
                        "Value": format_percent(row["capital_share_percent"]),
                    },
                    {
                        "Label": "Running government share",
                        "Value": format_percent(row["recurrent_share_percent"]),
                    },
                ]
            )
        detail_data = pd.DataFrame(details)
        st.dataframe(detail_data, hide_index=True, width="stretch")

    about_this_data(selected_year_data, selected_year)


elif page == "What Could This Build?":
    render_back_to_home()
    selected_year, selected_year_data = render_exploration_controls(
        "What it could build",
        helper_text="You can change these selections here, or return Home to choose a different starting point.",
    )

    selected_state, selected_year, row = get_state_year_selection(
        selected_year_data, selected_year, "translator"
    )

    amount_source = st.radio(
        f"What should {selected_state} spend on?",
        [
            "Total budget",
            "Projects and development budget",
            "Custom amount",
        ],
    )

    if amount_source == "Total budget":
        amount = float(row["annual_budget_ngn"]) if has_value(row["annual_budget_ngn"]) else pd.NA
    elif amount_source == "Projects and development budget":
        if has_value(row["capital_budget_ngn"]):
            amount = float(row["capital_budget_ngn"])
        elif has_value(row["annual_budget_ngn"]):
            amount = float(row["annual_budget_ngn"])
            st.warning(
                "Using total budget as temporary simulator baseline because capital "
                "budget breakdown is not yet available."
            )
        else:
            amount = pd.NA
    else:
        amount = float(
            st.number_input(
                "Enter custom amount in naira",
                min_value=0,
                value=1_000_000_000,
                step=100_000_000,
            )
        )

    hero_money_stat(
        f"{selected_state} could spend this on real things",
        format_naira(amount) if has_value(amount) else "Not available yet",
        f"in {selected_year}",
    )

    st.markdown("### This could build")

    if not has_value(amount):
        st.info("This amount is not available for the selected state and year.")
    elif amount <= 0:
        st.info("Enter an amount greater than zero to see project examples.")
    else:
        for project in project_translation(amount, project_costs):
            project_result_card(
                public_project_label(project["item"]),
                f"{project['units']:,.1f} {project['unit_name']}",
                f"Assumed unit cost: {format_ngn_long(project['unit_cost'])}",
            )

    with st.expander("Important note about these estimates"):
        st.write(
            "Project translations use benchmark estimates only. They are not official "
            "promises or procurement costs."
        )
        project_cost_note()
        if using_default_project_costs:
            st.warning(
                "data/project_costs.csv is missing or incomplete, so the app is using safe "
                "default illustrative assumptions."
            )

    with st.expander("See source details"):
        data_status_badge(
            row["data_status"],
            row.get("year"),
            row.get("budget_status"),
            row.get("state"),
        )
        source_caption(row)
        partial_data_caption(row)

    with st.expander("See detailed data"):
        assumptions = project_costs.copy()
        assumptions["cost_ngn"] = assumptions["cost_ngn"].map(format_ngn_long)
        assumptions = assumptions.rename(
            columns={
                "category": "Category",
                "item": "Project",
                "unit": "Unit",
                "cost_ngn": "Assumed Unit Cost",
                "source_name": "Source",
                "notes": "Notes",
            }
        )
        assumptions = assumptions.drop(columns=["source_url"], errors="ignore")
        st.dataframe(assumptions, hide_index=True, width="stretch")

    about_this_data(selected_year_data, selected_year)


elif page == "Where The Money Goes":
    render_back_to_home()
    selected_year, selected_year_data = render_exploration_controls(
        "Where it goes",
        helper_text="You can change these selections here, or return Home to choose a different starting point.",
    )

    selected_state, selected_year, row = get_state_year_selection(
        selected_year_data,
        selected_year,
        "money_goes",
    )

    if not has_budget_breakdown(row):
        hero_money_stat(
            f"For {selected_state} in {selected_year}, we have the total budget",
            format_naira(row["annual_budget_ngn"]),
            "but the projects vs. running-costs split isn't ready yet",
        )
        st.caption("Try another state or year to see the split.")
    else:
        capital_share = row["capital_share_percent"]
        recurrent_share = row["recurrent_share_percent"]
        if has_value(capital_share) and has_value(recurrent_share) and capital_share >= recurrent_share:
            lead = f"For every ₦100 {selected_state} spends, this much goes to projects like roads and schools"
            value = format_percent(capital_share)
        else:
            lead = f"For every ₦100 {selected_state} spends, this much goes to running government day to day"
            value = format_percent(recurrent_share)
        hero_money_stat(lead, value, "the rest covers the other side of the budget")

        chips = [
            ("🏗️", f"Projects: {format_naira(row['capital_budget_ngn'])}", "green"),
            ("🏛️", f"Running costs: {format_naira(row['recurrent_budget_ngn'])}", "blue"),
        ]
        stat_chip_row(chips)

        st.markdown("### Budget split")
        budget_split_chart(row)

    budget_101()

    with st.expander("See source details"):
        data_status_badge(
            row["data_status"],
            row.get("year"),
            row.get("budget_status"),
            row.get("state"),
        )
        source_caption(row)

    with st.expander("See detailed data"):
        detail_data = pd.DataFrame(
            [
                {
                    "Label": "Total budget",
                    "Value": format_ngn_long(row["annual_budget_ngn"]),
                },
                {
                    "Label": "Projects and development",
                    "Value": format_ngn_long(row["capital_budget_ngn"]),
                },
                {
                    "Label": "Running government",
                    "Value": format_ngn_long(row["recurrent_budget_ngn"]),
                },
                {
                    "Label": "Projects share",
                    "Value": format_percent(row["capital_share_percent"]),
                },
                {
                    "Label": "Running government share",
                    "Value": format_percent(row["recurrent_share_percent"]),
                },
            ]
        )
        st.dataframe(detail_data, hide_index=True, width="stretch")

    about_this_data(selected_year_data, selected_year)


elif page == "Compare States":
    render_back_to_home()
    selected_year, selected_year_data = render_exploration_controls(
        "Compare states",
        helper_text="The selected state from Home is included by default. Add or remove states below.",
    )

    year_data = selected_year_data.copy()

    state_options = year_data["state"].sort_values().tolist()
    global_selected_state = st.session_state.get("selected_state")
    useful_defaults = [
        state for state in ["Lagos", "Edo", "Rivers", "Kano", "FCT"]
        if state in state_options
    ]
    if global_selected_state in state_options and global_selected_state not in useful_defaults:
        useful_defaults.insert(0, global_selected_state)

    selected_states = st.multiselect(
        "Select states to compare",
        state_options,
        default=useful_defaults,
    )

    if not selected_states:
        st.info("Select one or more states to compare.")
    else:
        comparison = year_data[
            year_data["state"].isin(selected_states)
        ].sort_values("state")

        st.markdown("### Budget comparison")

        def comparison_chart(title, column, empty_message):
            chart = horizontal_budget_chart(
                comparison,
                column,
                title,
                status_column="data_status",
            )
            if chart is None:
                st.info(empty_message)
                return

            st.markdown(f"#### {title}")
            st.altair_chart(chart, width="stretch")

        comparison_chart(
            "Total budget",
            "annual_budget_ngn",
            "Total budget is not available for the selected states.",
        )
        comparison_chart(
            "Capital budget",
            "capital_budget_ngn",
            "Capital budget is not available for the selected states.",
        )
        comparison_chart(
            "Recurrent budget",
            "recurrent_budget_ngn",
            "Recurrent budget is not available for the selected states.",
        )
        comparison_chart(
            "Budget per resident",
            "annual_budget_per_person",
            "Budget per resident is not available for the selected states.",
        )
        st.caption("Charts skip states where a figure isn't available yet.")

        with st.expander("See detailed data"):
            display = comparison[
                [
                    "state",
                    "annual_budget_ngn",
                    "capital_budget_ngn",
                    "recurrent_budget_ngn",
                    "annual_budget_per_person",
                    "year",
                    "budget_status",
                    "data_status",
                    "source_id",
                    "budget_source_name",
                    "budget_source_publisher",
                    "budget_source_type",
                ]
            ].copy()
            display["annual_budget_ngn"] = display["annual_budget_ngn"].map(format_ngn_long)
            display["capital_budget_ngn"] = display["capital_budget_ngn"].map(format_ngn_long)
            display["recurrent_budget_ngn"] = display["recurrent_budget_ngn"].map(format_ngn_long)
            display["annual_budget_per_person"] = display[
                "annual_budget_per_person"
            ].map(format_ngn_long)
            display["data_status"] = display.apply(row_status_label, axis=1)
            display["budget_source_name"] = display.apply(source_display_name, axis=1)
            display["budget_source_publisher"] = display[
                "budget_source_publisher"
            ].map(format_optional_text)
            display["budget_source_type"] = display["budget_source_type"].map(
                format_optional_text
            )
            display = display.drop(columns=["source_id", "year", "budget_status"])
            display = display.rename(
                columns={
                    "state": "State",
                    "annual_budget_ngn": "Total budget",
                    "capital_budget_ngn": "Capital budget",
                    "recurrent_budget_ngn": "Recurrent budget",
                    "annual_budget_per_person": "Budget per resident",
                    "data_status": "Data confidence",
                    "budget_source_name": "Source",
                    "budget_source_publisher": "Publisher",
                    "budget_source_type": "Source type",
                }
            )
            st.dataframe(display, hide_index=True, width="stretch")

        if len(selected_states) == 1:
            note_card(
                "You selected one state. Add more states above if you want a side-by-side comparison."
            )
        else:
            note_card(
                "This comparison shows budget size and per-resident figures. It does not prove "
                "which state delivers better development outcomes."
            )

    about_this_data(selected_year_data, selected_year)


elif page == "Rankings":
    render_back_to_home()
    selected_year, selected_year_data = render_exploration_controls(
        "Rankings",
        helper_text="Rankings use the selected budget year. The selected state is highlighted when its data is available.",
    )
    ranking_options = {
        "Total Budget": "annual_budget_ngn",
        "Budget per Resident": "annual_budget_per_person",
        "Project Budget per Resident": "capital_budget_per_person",
        "Project Share": "capital_share_percent",
    }
    selected_ranking = st.radio(
        "Rank by",
        list(ranking_options.keys()),
        key="rankings_metric",
    )
    ranking_column = ranking_options[selected_ranking]
    ranked = selected_year_data.dropna(subset=[ranking_column]).sort_values(
        ranking_column,
        ascending=False,
    ).head(10)
    global_selected_state = st.session_state.get("selected_state")

    if ranked.empty:
        st.info(f"{selected_ranking} is not available for ranking.")
    else:
        top_row = ranked.iloc[0]
        top_value = (
            format_percent(top_row[ranking_column])
            if ranking_column == "capital_share_percent"
            else format_naira(top_row[ranking_column])
        )
        hero_money_stat(
            f"#1 for {selected_ranking.lower()} in {selected_year}",
            top_row["state"],
            top_value,
        )
        st.caption("A bigger budget doesn't always mean better services.")
        ranking_bar_chart(ranked, ranking_column, selected_ranking)

        selected_state_rank_data = selected_year_data.dropna(subset=[ranking_column]).sort_values(
            ranking_column,
            ascending=False,
        ).reset_index(drop=True)
        if global_selected_state in selected_state_rank_data["state"].tolist():
            selected_position = (
                selected_state_rank_data.index[
                    selected_state_rank_data["state"] == global_selected_state
                ][0]
                + 1
            )
            st.caption(
                f"Selected state: {global_selected_state} is #{selected_position} "
                f"for {selected_ranking.lower()} in {selected_year}."
            )
        else:
            st.caption(
                f"Selected state: {global_selected_state} does not have this figure available for {selected_year}."
            )

        with st.expander("See detailed data"):
            display = ranked[
                [
                    "state",
                    "year",
                    "budget_status",
                    ranking_column,
                    "data_status",
                    "budget_source_name",
                ]
            ].copy()
            if ranking_column == "capital_share_percent":
                display[ranking_column] = display[ranking_column].map(format_percent)
            else:
                display[ranking_column] = display[ranking_column].map(format_ngn_long)
            display["data_status"] = display.apply(row_status_label, axis=1)
            display["budget_source_name"] = display["budget_source_name"].map(
                format_optional_text
            )
            display = display.drop(columns=["year", "budget_status"])
            display = display.rename(
                columns={
                    "state": "State",
                    "annual_budget_ngn": "Total Budget",
                    "annual_budget_per_person": "Budget per Resident",
                    "capital_budget_per_person": "Project Budget per Resident",
                    "capital_share_percent": "Project Share",
                    "data_status": "Status",
                    "budget_source_name": "Source",
                }
            )
            st.dataframe(display, hide_index=True, width="stretch")

    budget_101()
    about_this_data(selected_year_data, selected_year)


elif page == "Budget Insights":
    st.title("Budget Insights")
    st.write(
        "This page summarises budget priorities, fiscal indicators, and available "
        "outcome evidence from public budget sources."
    )

    selected_state, selected_year, budget_row = get_state_year_selection(
        selected_year_data,
        selected_year,
        "budget_insights",
    )
    source_caption(budget_row)

    selected_insights = filter_state_year(
        budget_insights,
        selected_state,
        selected_year,
    )
    selected_indicators = filter_state_year(
        fiscal_indicators,
        selected_state,
        selected_year,
    )
    selected_outcomes = filter_state_year(
        budget_outcomes,
        selected_state,
        selected_year,
    )

    st.info(
        "2026 mostly shows planned priorities because implementation evidence is "
        "not yet available. 2025 may later include observed outcomes where reliable "
        "implementation evidence exists."
    )

    st.markdown("### Planned priorities")
    if selected_insights.empty:
        st.info(
            "Budget priority extraction has not been completed for this state/year yet."
        )
    else:
        display = selected_insights[
            [
                "sector",
                "theme",
                "planned_action",
                "amount_ngn",
                "data_status",
            ]
        ].copy()
        display["sector"] = display["sector"].map(format_optional_text)
        display["theme"] = display["theme"].map(format_optional_text)
        display["planned_action"] = display["planned_action"].map(format_optional_text)
        display["amount_ngn"] = display["amount_ngn"].map(format_ngn_long)
        display["data_status"] = display["data_status"].map(data_status_label)
        display = display.rename(
            columns={
                "sector": "Sector",
                "theme": "Theme",
                "planned_action": "Planned action",
                "amount_ngn": "Amount",
                "data_status": "Data confidence",
            }
        )
        st.dataframe(display, hide_index=True, width="stretch")

    st.markdown("### Fiscal indicators")
    if selected_indicators.empty:
        st.info(
            "Fiscal indicator extraction has not been completed for this state/year yet."
        )
    else:
        display = selected_indicators[
            [
                "indicator",
                "value",
                "unit",
                "data_status",
            ]
        ].copy()
        display["indicator"] = display["indicator"].map(format_optional_text)
        display["value"] = display.apply(format_indicator_value, axis=1)
        display["unit"] = display["unit"].map(format_optional_text)
        display["data_status"] = display["data_status"].map(data_status_label)
        display = display.rename(
            columns={
                "indicator": "Indicator",
                "value": "Value",
                "unit": "Unit",
                "data_status": "Data confidence",
            }
        )
        st.dataframe(display, hide_index=True, width="stretch")

    st.markdown("### Observed outcomes")
    if selected_outcomes.empty:
        st.info(
            "Observed outcome evidence has not been added for this state/year yet."
        )
    else:
        display = selected_outcomes[
            [
                "sector",
                "outcome_metric",
                "value",
                "unit",
                "data_status",
            ]
        ].copy()
        display["sector"] = display["sector"].map(format_optional_text)
        display["outcome_metric"] = display["outcome_metric"].map(format_optional_text)
        display["value"] = display["value"].map(format_optional_text)
        display["unit"] = display["unit"].map(format_optional_text)
        display["data_status"] = display["data_status"].map(data_status_label)
        display = display.rename(
            columns={
                "sector": "Sector",
                "outcome_metric": "Outcome metric",
                "value": "Value",
                "unit": "Unit",
                "data_status": "Data confidence",
            }
        )
        st.dataframe(display, hide_index=True, width="stretch")


# Hidden internal page: source-handling code is kept intact, but this page is
# currently not linked from the public sidebar menu.
elif page == "Data Sources":
    st.title("Data Sources")
    st.write(
        "This app uses local CSV files. It prefers separate budget, population "
        "and source files when they exist, while keeping the old states.csv fallback for deployment safety."
    )

    metric_card("State rows", format_number(len(states)))
    metric_card("Project-cost assumptions", format_number(len(project_costs)))

    st.markdown("### Current files")
    metric_card(
        "data/state_budgets.csv",
        "Preferred budget file",
        "Columns include budget amounts, budget_status, data_status, source_id and notes.",
    )
    metric_card(
        "data/state_population.csv",
        "Preferred population file",
        "Columns: state, year, population, source_name, source_url, notes.",
    )
    metric_card(
        "data/project_costs.csv",
        "Illustrative project-cost assumptions",
        "Columns: category, item, unit, cost_ngn, source_name, source_url, notes. If missing or incomplete, safe default assumptions are used.",
    )
    metric_card(
        "data/sources.csv",
        "Source catalogue",
        "Documents source_id, state, year, budget type, source URL, extraction status and extracted figures.",
    )

    if state_data_mode == "legacy":
        st.warning(
            "The app is currently using the legacy data/states.csv fallback because the "
            "separate state_budgets.csv and state_population.csv files are not both available."
        )
    else:
        st.info(
            "The app is currently using the separated budget and population files."
        )

    st.markdown("### What should be added later")
    note_card(
        "Future public versions should use verified sources such as official state "
        "budget documents, National Bureau of Statistics data and other credible public datasets."
    )

    st.markdown("### Source notes")
    note_card(
        "Rows should be interpreted using source_id, data_status and notes. Some rows "
        "may still be awaiting source review or detailed extraction."
    )

    st.markdown("### Data status")
    metric_card(
        "Verified source",
        "Official or reputable",
        "Taken from an official budget document or a reputable published dataset.",
    )
    metric_card(
        "Estimated/projection",
        "Derived or assumed",
        "Derived from available public figures or transparent assumptions.",
    )
    metric_card(
        "Missing/partial",
        "Source pending",
        "A source-backed figure is not available yet, or the row still needs review.",
    )

    with st.expander("Preview normalized state data"):
        preview_columns = [
            "state",
            "year",
            "budget_status",
            "data_status",
            "annual_budget_ngn",
            "capital_budget_ngn",
            "recurrent_budget_ngn",
            "population",
            "budget_source_name",
            "population_source_name",
        ]
        st.dataframe(states[preview_columns].head(37), hide_index=True, width="stretch")

    with st.expander("Preview project_costs.csv"):
        st.dataframe(project_costs, hide_index=True, width="stretch")

    sources_path = DATA_DIR / "sources.csv"
    if sources_path.exists():
        with st.expander("Preview sources.csv"):
            sources = safe_read_csv(sources_path, "data/sources.csv")
            st.dataframe(sources, hide_index=True, width="stretch")


elif page == "About":
    render_back_to_home()
    st.title("About")
    st.markdown(
        '<div class="about-badge">Independent civic education tool</div>',
        unsafe_allow_html=True,
    )
    st.write(
        "Nigeria Development Simulator is a public budget explainer. It helps people "
        "understand and compare Nigerian state budgets, population figures, spending "
        "priorities, and simple development scenarios."
    )
    note_card(
        "This is an independent civic education tool. It is not an official government "
        "website. Budget figures are based on public sources where available, and some "
        "figures may still be marked for review where source details are incomplete."
    )

    st.markdown("### What it can explain")
    metric_card("Total Budget", "How much a state plans to spend in a selected year")
    metric_card("Projects and Development", "Capital spending for public projects and infrastructure")
    metric_card("Running Government", "Recurrent spending for salaries and day-to-day operations")
    metric_card("For every ₦100", "A simple way to understand the spending split")

    st.markdown("### Important limits")
    note_card(
        "Budget figures alone do not prove development. Real outcomes depend on "
        "implementation, governance, procurement, inflation, security, education, health, "
        "infrastructure and many other factors."
    )
    note_card(
        "Some figures are verified from public sources, while others may still be awaiting "
        "source review or a detailed spending split. Project translations are illustrative "
        "estimates, not official promises."
    )

    with st.expander("Technical notes"):
        st.write(
            "The app calculates budget per resident, project budget per resident, recurrent "
            "budget per resident, and the percentage split between capital and recurrent budgets."
        )

    year_data_notes(selected_year)


st.markdown("---")
st.caption(
    PUBLIC_DISCLAIMER
    + "\n\n"
    "© 2026 Nigeria Development Simulator. All Rights Reserved.\n\n"
    "Original analysis, design and presentation are protected. Source data remains "
    "the property of the original publishers."
)
