from pathlib import Path

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
    "personnel_cost_ngn",
    "overhead_cost_ngn",
    "debt_service_ngn",
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
    "personnel_cost_ngn",
    "overhead_cost_ngn",
    "debt_service_ngn",
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
    "This tool is for civic education and exploratory analysis. It does not provide "
    "financial, legal, or official government advice."
)


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

    section[data-testid="stSidebar"] {
        background-color: #0f172a;
    }

    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #ffffff;
    }

    section[data-testid="stSidebar"] .stMarkdown p,
    section[data-testid="stSidebar"] [role="radiogroup"] label p,
    section[data-testid="stSidebar"] [data-testid="stWidgetLabel"] p {
        color: #ffffff !important;
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
        .note-card {
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
        .note-card {
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


def note_card(text):
    st.markdown(
        f"""
        <div class="note-card">
            <p>{text}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def population_note():
    st.caption(POPULATION_ESTIMATE_NOTE)


def project_cost_note():
    st.caption(PROJECT_COST_ESTIMATE_NOTE)


def data_status_label(status):
    normalized = str(status).strip().lower()
    if normalized == "verified":
        return "Verified source"
    if normalized == "verified_breakdown":
        return "Verified breakdown"
    if normalized == "approved_total_verified":
        return "Verified total"
    if normalized == "approved_total_needs_review":
        return "Needs review"
    if normalized == "partial_verified_total":
        return "Verified total, breakdown pending"
    if normalized == "proposed_total_needs_review":
        return "Proposed / not final"
    if normalized in ["estimated", "estimate", "projection", "estimated/projection"]:
        return "Estimated/projection"
    return "Not available yet"


def data_status_caption(status):
    normalized = str(status).strip().lower()
    captions = {
        "verified_breakdown": (
            "Total, projects and running-government figures are available from a clear source."
        ),
        "approved_total_verified": (
            "Approved total is available; detailed budget breakdown is not yet extracted."
        ),
        "partial_verified_total": (
            "Total is available from a comparative source; breakdown is still pending."
        ),
        "approved_total_needs_review": (
            "A public approved-total figure is available but still needs source review."
        ),
        "proposed_total_needs_review": (
            "This appears to be a proposal or pre-final figure, not a final approved budget."
        ),
        "missing": "The budget figure has not yet been entered for this state/year.",
    }
    return captions.get(normalized, "Use this badge as a quick guide to data confidence.")


def data_status_badge(status):
    label = data_status_label(status)
    normalized = str(status).strip().lower()
    if normalized in ["verified", "verified_breakdown"]:
        background = "#dcfce7"
        border = "#86efac"
        color = "#166534"
    elif normalized in ["approved_total_verified", "partial_verified_total"]:
        background = "#dbeafe"
        border = "#93c5fd"
        color = "#1e3a8a"
    elif normalized in [
        "estimated",
        "estimate",
        "projection",
        "estimated/projection",
        "approved_total_needs_review",
        "proposed_total_needs_review",
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
    st.caption(data_status_caption(status))


def source_caption(row):
    source_id = str(row.get("source_id", "")).strip()
    source_name = str(row.get("budget_source_name", "")).strip()
    if source_id in ["", "SRC_PENDING", "unknown"] or not source_name:
        st.caption("Source pending")
    else:
        st.caption(f"Source: {source_name}")


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
            population["source_name"] = "Legacy prototype states.csv"
            population["source_url"] = ""
            population["notes"] = (
                "Fallback prototype/sample population value from data/states.csv."
            )
        else:
            population = pd.DataFrame(columns=POPULATION_COLUMNS)

        for column in BUDGET_OPTIONAL_COLUMNS:
            if column not in budgets.columns:
                budgets[column] = pd.NA
        if "source_id" not in budgets.columns:
            budgets["source_id"] = "unknown"
        if "data_status" not in budgets.columns:
            budgets["data_status"] = "Missing/partial"
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
        states["data_status"] = states["data_status"].fillna("Missing/partial")
        states["budget_notes"] = states["budget_notes"].fillna("")
        if sources_path.exists():
            sources = safe_read_csv(sources_path, "data/sources.csv")
            if {"source_id", "source_name"}.issubset(sources.columns):
                source_lookup = (
                    sources[["source_id", "source_name"]]
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
                states = states.drop(columns=["source_name"])
            else:
                states["budget_source_name"] = states["source_id"].fillna("unknown")
        else:
            states["budget_source_name"] = states["source_id"].fillna("unknown")
        states["budget_source_url"] = ""

        data_mode = "new"
    else:
        states = safe_read_csv(states_path, "data/states.csv")
        validate_columns(states, LEGACY_STATE_COLUMNS, "data/states.csv")

        if "year" not in states.columns:
            states["year"] = 2025

        states["budget_source_name"] = "Legacy prototype states.csv"
        states["budget_source_url"] = ""
        states["budget_notes"] = (
            "Fallback prototype/sample value from data/states.csv."
        )
        states["source_id"] = "legacy_states_csv"
        states["data_status"] = "Missing/partial"
        for column in ["personnel_cost_ngn", "overhead_cost_ngn", "debt_service_ngn"]:
            states[column] = pd.NA
        states["population_source_name"] = "Legacy prototype states.csv"
        states["population_source_url"] = ""
        states["population_notes"] = (
            "Fallback prototype/sample value from data/states.csv."
        )
        data_mode = "legacy"


    states["year"] = states["year"].astype(int)
    states["data_status"] = states["data_status"].fillna("Missing/partial")
    states["data_status"] = states["data_status"].where(
        states["data_status"].isin(
            [
                "Verified",
                "Estimated",
                "Estimated/projection",
                "Missing/partial",
                "missing",
                "verified_breakdown",
                "partial_verified_total",
                "approved_total_verified",
                "approved_total_needs_review",
                "proposed_total_needs_review",
            ]
        ),
        "Missing/partial",
    )

    numeric_columns = [
        "population",
        "annual_budget_ngn",
        "capital_budget_ngn",
        "recurrent_budget_ngn",
        "personnel_cost_ngn",
        "overhead_cost_ngn",
        "debt_service_ngn",
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
        costs["source_name"] = "Legacy prototype project_costs.csv"
        costs["source_url"] = ""
        costs["notes"] = (
            "Fallback-compatible prototype assumption from the older project_costs.csv format."
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
    if int(selected_year) == 2026:
        st.info(
            "2026 data is being added gradually. Approved totals are shown where "
            "verified; missing values mean the approved figure has not yet been extracted."
        )


def data_quality_summary(year_data, selected_year):
    total_rows = year_data["state"].nunique()
    rows_with_budget = year_data.loc[
        year_data["annual_budget_ngn"].notna() & (year_data["annual_budget_ngn"] > 0),
        "state",
    ].nunique()
    missing_budget = max(total_rows - rows_with_budget, 0)

    st.caption(
        f"{selected_year} coverage: {rows_with_budget} states/FCT have total budget "
        f"values; {missing_budget} are missing."
    )

    if missing_budget:
        st.warning(
            "Some states/FCT are still missing total budget values for this year."
        )

    status_counts = (
        year_data["data_status"]
        .fillna("Missing/partial")
        .map(data_status_label)
        .value_counts()
        .reset_index()
    )
    status_counts.columns = ["Status", "Count"]

    with st.expander("Data status summary"):
        st.dataframe(status_counts, hide_index=True, width="stretch")


def get_state_year_selection(year_data, selected_year, prefix=""):
    state_options = year_data["state"].drop_duplicates().sort_values().tolist()
    selected_state = st.selectbox(
        "Choose your state",
        state_options,
        key=f"{prefix}_state",
    )

    row = year_data[year_data["state"] == selected_state].iloc[0]

    return selected_state, selected_year, row


def budget_breakdown_text(row):
    capital = row["capital_share_percent"]
    recurrent = row["recurrent_share_percent"]
    if pd.isna(capital) or pd.isna(recurrent):
        return (
            "The split between projects and running government is not fully available "
            "for this row."
        )
    return (
        f"For every ₦100 in the budget, about ₦{capital:.0f} goes to "
        f"projects and development, while about ₦{recurrent:.0f} goes to "
        "running government."
    )


def partial_data_caption(row):
    missing = []
    labels = {
        "capital_budget_ngn": "projects and development",
        "recurrent_budget_ngn": "running government",
        "personnel_cost_ngn": "personnel cost",
        "overhead_cost_ngn": "overhead cost",
        "debt_service_ngn": "debt service",
    }
    for column, label in labels.items():
        if pd.isna(row.get(column)):
            missing.append(label)

    if missing:
        st.caption(
            "Partial data: "
            + ", ".join(missing)
            + " not available for this row."
        )


def has_budget_breakdown(row):
    return has_value(row.get("capital_budget_ngn")) and has_value(
        row.get("recurrent_budget_ngn")
    )


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


st.sidebar.markdown(
    """
    # Nigeria Budget

    Simple public budget explainer.
    """
)

page = st.sidebar.radio(
    "Pages",
    [
        "Home",
        "State Explorer",
        "Budget Translator",
        "Compare States",
        "About",
    ],
)

st.sidebar.markdown("### Budget year")
available_years = states["year"].drop_duplicates().sort_values(ascending=False).tolist()
selected_year = st.sidebar.selectbox(
    "Budget year",
    available_years,
    index=0,
    key="global_budget_year",
    label_visibility="collapsed",
)
selected_year_data = states[states["year"] == selected_year].copy()

if selected_year_data.empty:
    st.error(f"No budget rows are available for {selected_year}.")
    st.stop()

st.caption(f"Showing budget data for {selected_year}.")
year_update_note(selected_year)
data_quality_summary(selected_year_data, selected_year)


if page == "Home":
    st.markdown(
        """
        <div class="hero">
            <h1>Understand your state budget in simple terms.</h1>
            <p>
                Pick a Nigerian state, choose a year, and see what the budget means
                for people, projects, and everyday government spending.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")
    selected_state, selected_year, row = get_state_year_selection(
        selected_year_data, selected_year, "home"
    )
    data_status_badge(row["data_status"])

    metric_card(
        "Total Budget",
        format_naira(row["annual_budget_ngn"]),
        total_budget_help(row),
    )
    metric_card(
        "Budget per Person",
        format_naira(row["annual_budget_per_person"]),
        per_person_budget_help(row),
    )
    population_note()

    note_card(
        f"{selected_state} in {selected_year}: {budget_breakdown_text(row)}"
    )
    partial_data_caption(row)

    st.markdown("### What you can do")
    metric_card(
        "Explore your state",
        "See the big numbers first",
        "Start with total budget, projects, running government, and budget per person.",
    )
    metric_card(
        "Translate budget into projects",
        "Roads, schools, health centres, water",
        "Use simple project-cost assumptions to understand the scale of a budget.",
    )
    metric_card(
        "Compare states",
        "One simple comparison page",
        "Rank states by budget per person or by how much goes to projects.",
    )

    st.info(
        "Data note: use the badge above to see whether the selected figures are verified, "
        "estimated, or missing/partial."
    )

    st.markdown("### Current data coverage")
    coverage_data = selected_year_data.copy()
    total_states = coverage_data["state"].nunique()
    states_with_budget = coverage_data.loc[
        coverage_data["annual_budget_ngn"].notna()
        & (coverage_data["annual_budget_ngn"] > 0),
        "state",
    ].nunique()
    states_with_population = coverage_data.loc[
        coverage_data["population"].notna() & (coverage_data["population"] > 0),
        "state",
    ].nunique()
    states_with_both = coverage_data.loc[
        coverage_data["annual_budget_ngn"].notna()
        & (coverage_data["annual_budget_ngn"] > 0)
        & coverage_data["population"].notna()
        & (coverage_data["population"] > 0),
        "state",
    ].nunique()

    metric_card("States in dataset", format_number(total_states))
    metric_card("States with total budget", format_number(states_with_budget))
    metric_card("States with population", format_number(states_with_population))
    metric_card("States with both", format_number(states_with_both))

    missing_budget = coverage_data[
        coverage_data["annual_budget_ngn"].isna()
        | (coverage_data["annual_budget_ngn"] <= 0)
    ][["state", "year", "data_status", "budget_notes"]].copy()

    if missing_budget.empty:
        st.caption("All states for this year currently have a total budget value.")
    else:
        missing_budget = missing_budget.rename(
            columns={
                "state": "State",
                "year": "Year",
                "data_status": "Status",
                "budget_notes": "Notes",
            }
        )
        st.caption("States where total_budget_ngn is missing:")
        st.dataframe(missing_budget, hide_index=True, width="stretch")


elif page == "State Explorer":
    st.title("State Explorer")
    st.write("Choose a state. The page explains the selected year's budget in plain English.")

    selected_state, selected_year, row = get_state_year_selection(
        selected_year_data, selected_year, "explorer"
    )

    st.markdown(f"### {selected_state}, {selected_year}")
    data_status_badge(row["data_status"])
    source_caption(row)

    metric_card(
        "Total Budget",
        format_naira(row["annual_budget_ngn"]),
        total_budget_help(row),
    )
    if not has_budget_breakdown(row):
        st.info("Breakdown not yet available for this state.")
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
    metric_card("Population", format_number(row["population"]))
    metric_card(
        "Budget per Person",
        format_naira(row["annual_budget_per_person"]),
        per_person_budget_help(row),
    )
    metric_card(
        "Project Budget per Person",
        format_naira(row["capital_budget_per_person"]),
        project_per_person_budget_help(row),
    )
    population_note()
    metric_card("For every ₦100", budget_breakdown_text(row))
    partial_data_caption(row)

    st.markdown("### Simple explanation")
    if not has_budget_breakdown(row) and has_value(row["annual_budget_ngn"]):
        note_card(
            f"{selected_state}'s total budget is {format_ngn_long(row['annual_budget_ngn'])}. "
            "The detailed split between projects and running government is not yet available."
        )
    else:
        note_card(
            f"{selected_state}'s total budget is {format_ngn_long(row['annual_budget_ngn'])}. "
            f"Projects and development share: {format_percent(row['capital_share_percent'])}. "
            f"Running government share: {format_percent(row['recurrent_share_percent'])}."
        )

    with st.expander("Show technical details"):
        detail_data = pd.DataFrame(
            [
                {
                    "Label": "Annual budget per person",
                    "Value": format_ngn_long(row["annual_budget_per_person"]),
                },
                {
                    "Label": "Capital/project budget per person",
                    "Value": format_ngn_long(row["capital_budget_per_person"]),
                },
                {
                    "Label": "Recurrent/running government per person",
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
                {
                    "Label": "Budget source",
                    "Value": row["budget_source_name"],
                },
                {
                    "Label": "Budget data status",
                    "Value": data_status_label(row["data_status"]),
                },
                {
                    "Label": "Population source",
                    "Value": row["population_source_name"],
                },
            ]
        )
        st.dataframe(detail_data, hide_index=True, width="stretch")

    st.info(
        "Data note: use the badge above to see whether these figures are verified, "
        "estimated, or missing/partial."
    )


elif page == "Budget Translator":
    st.title("Budget Translator")
    st.write(
        "Turn a budget amount into rough project examples. These estimates are for "
        "understanding scale, not official promises."
    )

    selected_state, selected_year, row = get_state_year_selection(
        selected_year_data, selected_year, "translator"
    )
    data_status_badge(row["data_status"])
    source_caption(row)
    partial_data_caption(row)

    amount_source = st.radio(
        "What amount should we translate?",
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

    metric_card("Amount to Translate", format_naira(amount))
    project_cost_note()

    if using_default_project_costs:
        st.warning(
            "data/project_costs.csv is missing or incomplete, so the app is using safe "
            "default illustrative assumptions."
        )

    st.markdown("### Approximate project examples")
    st.warning(
        "Project translations use benchmark estimates only. They are not official "
        "promises or procurement costs."
    )

    if not has_value(amount):
        st.info("This amount is not available for the selected state and year.")
    elif amount <= 0:
        st.info("Enter an amount greater than zero to see project examples.")
    else:
        for project in project_translation(amount, project_costs):
            metric_card(
                project["item"],
                f"{project['units']:,.1f} {project['unit_name']}",
                f"Assumed unit cost: {format_ngn_long(project['unit_cost'])}",
            )

    st.caption(
        "Project costs are benchmark estimates and may vary by location, procurement "
        "method, inflation, and project specification."
    )

    with st.expander("Show project-cost assumptions"):
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


elif page == "Compare States":
    st.title("Compare States")
    st.write("Choose the states you want to compare for the selected year.")
    st.caption("Each selected state shows its own budget data status.")

    year_data = selected_year_data.copy()

    state_options = year_data["state"].sort_values().tolist()
    useful_defaults = [
        state for state in ["Lagos", "Edo", "Rivers", "Kano", "FCT"]
        if state in state_options
    ]

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
            chart_data = comparison.dropna(subset=[column]).set_index("state")[[column]]
            if chart_data.empty:
                st.info(empty_message)
                return

            st.markdown(f"#### {title}")
            st.bar_chart(chart_data.rename(columns={column: title}))

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
            "Budget per person",
            "annual_budget_per_person",
            "Budget per person is not available for the selected states.",
        )
        population_note()
        st.caption(
            "Charts exclude states where the selected figure is not available yet. "
            "Data confidence is shown in the table below."
        )

        st.markdown("### Comparison table")
        display = comparison[
            [
                "state",
                "annual_budget_ngn",
                "capital_budget_ngn",
                "recurrent_budget_ngn",
                "annual_budget_per_person",
                "data_status",
            ]
        ].copy()
        display["annual_budget_ngn"] = display["annual_budget_ngn"].map(format_naira)
        display["capital_budget_ngn"] = display["capital_budget_ngn"].map(format_naira)
        display["recurrent_budget_ngn"] = display["recurrent_budget_ngn"].map(format_naira)
        display["annual_budget_per_person"] = display[
            "annual_budget_per_person"
        ].map(format_naira)
        display["data_status"] = display["data_status"].map(data_status_label)
        display = display.rename(
            columns={
                "state": "State",
                "annual_budget_ngn": "Total budget",
                "capital_budget_ngn": "Capital budget",
                "recurrent_budget_ngn": "Recurrent budget",
                "annual_budget_per_person": "Budget per person",
                "data_status": "Data confidence",
            }
        )
        st.dataframe(display, hide_index=True, width="stretch")

        if len(selected_states) == 1:
            note_card(
                "You selected one state. Add more states above if you want a side-by-side comparison."
            )
        else:
            note_card(
                "This comparison shows budget size and per-person figures. It does not prove "
                "which state delivers better development outcomes."
            )

    with st.expander("See top states ranking"):
        data_status_badge("approved_total_verified")
        ranking_options = {
            "Total Budget": "annual_budget_ngn",
            "Budget per Person": "annual_budget_per_person",
            "Project Budget per Person": "capital_budget_per_person",
            "Project Share": "capital_share_percent",
        }
        selected_ranking = st.radio(
            "Rank by",
            list(ranking_options.keys()),
            key="top_states_ranking_metric",
        )
        if selected_ranking in [
            "Budget per Person",
            "Project Budget per Person",
        ]:
            population_note()
        ranking_column = ranking_options[selected_ranking]
        ranked = year_data.dropna(subset=[ranking_column]).sort_values(
            ranking_column,
            ascending=False,
        ).head(10)
        if ranked.empty:
            st.info(f"{selected_ranking} is not available for ranking.")
        else:
            if selected_ranking == "Total Budget":
                st.caption(
                    "Rankings currently cover only states with verified/pilot total budget values."
                )
            display = ranked[
                [
                    "state",
                    ranking_column,
                    "data_status",
                ]
            ].copy()
            if ranking_column == "capital_share_percent":
                display[ranking_column] = display[ranking_column].map(format_percent)
            else:
                display[ranking_column] = display[ranking_column].map(format_ngn_long)
            display["data_status"] = display["data_status"].map(data_status_label)
            display = display.rename(
                columns={
                    "state": "State",
                    "annual_budget_ngn": "Total Budget",
                    "annual_budget_per_person": "Budget per Person",
                    "capital_budget_per_person": "Project Budget per Person",
                    "capital_share_percent": "Project Share",
                    "data_status": "Status",
                }
            )
            st.dataframe(display, hide_index=True, width="stretch")

    st.info(
        "Data note: comparison rows may mix verified, estimated, and missing/partial data."
    )


# Hidden internal page: source-handling code is kept intact, but this page is
# currently not linked from the public sidebar menu.
elif page == "Data Sources":
    st.title("Data Sources")
    st.write(
        "This prototype uses local CSV files. It now prefers separate budget, population "
        "and source files when they exist, while keeping the old states.csv fallback for deployment safety."
    )

    metric_card("State rows", format_number(len(states)))
    metric_card("Project-cost assumptions", format_number(len(project_costs)))

    st.markdown("### Current files")
    metric_card(
        "data/state_budgets.csv",
        "Preferred budget file",
        "Columns include budget amounts, personnel/overhead/debt fields, source_id, data_status and notes.",
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
        "Documents source_id, publisher, year, URL, source type, access date and reliability notes.",
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
        "Current rows are still prototype/sample values unless source_id, data_status "
        "and notes are replaced with verified source details."
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
        "Prototype only",
        "Prototype data that should not be relied upon for public decisions.",
    )

    with st.expander("Preview normalized state data"):
        preview_columns = [
            "state",
            "year",
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
    st.title("About")
    data_status_badge("Missing/partial")
    st.write(
        "Nigeria Development Simulator is a public budget explainer. It is designed "
        "to help people understand state budgets quickly on a phone."
    )

    st.markdown("### What it can explain")
    metric_card("Total Budget", "How much the state plans to spend")
    metric_card("Projects and Development", "Money usually linked to capital projects")
    metric_card("Running Government", "Money for salaries and day-to-day operations")
    metric_card("For every ₦100", "A simple split between projects and running government")

    st.markdown("### Important limits")
    note_card(
        "Budget figures alone do not prove development. Real outcomes depend on "
        "implementation, governance, procurement, inflation, security, education, health, "
        "infrastructure and many other factors."
    )
    note_card(
        "Rows may be verified, estimated/projection, or missing/partial. Project "
        "translations are illustrative estimates, not official promises."
    )

    with st.expander("Technical notes"):
        st.write(
            "The app calculates budget per person, project budget per person, recurrent "
            "budget per person, and the percentage split between capital and recurrent budgets."
        )


st.markdown("---")
st.caption(
    PUBLIC_DISCLAIMER
    + "\n\n"
    "© 2026 Nigeria Development Simulator. All Rights Reserved.\n\n"
    "Original analysis, design and presentation are protected. Source data remains "
    "the property of the original publishers.\n\n"
    "For civic education and exploratory analysis only."
)
