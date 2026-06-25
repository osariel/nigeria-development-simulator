import streamlit as st
import pandas as pd
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

st.set_page_config(
    page_title="Nigeria Development Simulator",
    page_icon="🇳🇬",
    layout="wide"
)
st.markdown(
    """
    <style>
    /* Main background */
    .stApp {
        background-color: #f7f9fb;
        color: #0f172a;
    }

    /* Main content area */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1200px;
        color: #0f172a;
    }

    /* Keep ordinary markdown readable without overriding widget internals */
    .block-container p {
        color: #0f172a;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #0f172a;
    }

    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] p {
        color: #ffffff;
    }

    /* Overview hero */
    .hero {
        background-color: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 16px;
        padding: 2rem;
        box-shadow: 0 4px 14px rgba(15, 23, 42, 0.06);
    }

    .hero p {
        font-size: 1.1rem;
        line-height: 1.6;
        margin-bottom: 0.75rem;
        color: #334155;
    }

    .hero-small {
        font-size: 0.95rem;
        color: #475569;
    }

    .overview-card {
        background-color: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 14px;
        padding: 1.2rem;
        min-height: 155px;
        box-shadow: 0 4px 14px rgba(15, 23, 42, 0.04);
    }

    .overview-card h3 {
        font-size: 1.05rem;
        margin-bottom: 0.5rem;
    }

    .overview-card p {
        color: #475569;
        line-height: 1.55;
        margin-bottom: 0;
    }

    .overview-cta {
        background-color: #ecfdf5;
        border: 1px solid #99f6e4;
        border-radius: 14px;
        padding: 1.2rem 1.4rem;
    }

    .overview-cta p {
        color: #134e4a;
        margin-bottom: 0;
    }

    .state-insight {
        background-color: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 14px;
        padding: 1.2rem 1.4rem;
        box-shadow: 0 4px 14px rgba(15, 23, 42, 0.04);
    }

    .state-insight p {
        color: #334155;
        line-height: 1.6;
        margin-bottom: 0.7rem;
    }

    .state-insight p:last-child {
        margin-bottom: 0;
    }

    .ranking-insight {
        background-color: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 14px;
        padding: 1.2rem 1.4rem;
        box-shadow: 0 4px 14px rgba(15, 23, 42, 0.04);
    }

    .ranking-insight p {
        color: #334155;
        line-height: 1.6;
        margin-bottom: 0;
    }

    .simulation-insight {
        background-color: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 14px;
        padding: 1.2rem 1.4rem;
        box-shadow: 0 4px 14px rgba(15, 23, 42, 0.04);
    }

    .simulation-insight p {
        color: #334155;
        line-height: 1.6;
        margin-bottom: 0;
    }

    .budget-insight {
        background-color: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 14px;
        padding: 1.2rem 1.4rem;
        box-shadow: 0 4px 14px rgba(15, 23, 42, 0.04);
    }

    .budget-insight p {
        color: #334155;
        line-height: 1.6;
        margin-bottom: 0;
    }

    /* Page titles */
    h1 {
        font-size: 2.4rem;
        font-weight: 800;
        color: #0f172a;
        letter-spacing: -0.03em;
    }

    h2, h3 {
        color: #111827;
        font-weight: 700;
    }

    /* Metric cards */
    div[data-testid="stMetric"] {
        background-color: #ffffff;
        padding: 1.2rem;
        border-radius: 16px;
        border: 1px solid #e5e7eb;
        box-shadow: 0 4px 14px rgba(15, 23, 42, 0.06);
    }

    div[data-testid="stMetric"] label,
    div[data-testid="stMetric"] div {
        color: #0f172a;
    }

    /* Info boxes */
    div[data-testid="stAlert"] {
        border-radius: 14px;
    }

    /* Dataframes */
    div[data-testid="stDataFrame"] {
        border-radius: 14px;
        overflow: hidden;
    }

    /* Buttons */
    .stButton button {
        border-radius: 10px;
        background-color: #0f766e;
        color: white;
        border: none;
    }

    /* Hide Streamlit branding bits */
    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# -----------------------------
# Load data
# -----------------------------
states = pd.read_csv(DATA_DIR / "states.csv")
project_costs = pd.read_csv(DATA_DIR / "project_costs.csv")

REQUIRED_STATE_COLUMNS = [
    "state",
    "population",
    "annual_budget_ngn",
    "capital_budget_ngn",
    "recurrent_budget_ngn"
]

REQUIRED_PROJECT_COST_COLUMNS = [
    "sector",
    "item",
    "unit_cost_ngn",
    "unit_name"
]


def validate_columns(dataframe, required_columns, file_name):
    missing_columns = [
        column for column in required_columns
        if column not in dataframe.columns
    ]

    if missing_columns:
        st.error(
            f"{file_name} is missing required column(s): "
            f"{', '.join(missing_columns)}. Please check the CSV file."
        )
        st.stop()


validate_columns(states, REQUIRED_STATE_COLUMNS, "data/states.csv")
validate_columns(project_costs, REQUIRED_PROJECT_COST_COLUMNS, "data/project_costs.csv")

# Add calculated columns
states["annual_budget_per_person"] = (
    states["annual_budget_ngn"] / states["population"]
)

states["capital_budget_per_person"] = (
    states["capital_budget_ngn"] / states["population"]
)

states["recurrent_budget_per_person"] = (
    states["recurrent_budget_ngn"] / states["population"]
)

states["capital_share_percent"] = (
    states["capital_budget_ngn"] / states["annual_budget_ngn"]
) * 100

states["recurrent_share_percent"] = (
    states["recurrent_budget_ngn"] / states["annual_budget_ngn"]
) * 100


# -----------------------------
# Sidebar navigation
# -----------------------------
st.sidebar.markdown(
    """
    # 🇳🇬 NDS

    **Nigeria Development Simulator**

    Explore state budgets, development indicators and policy scenarios.
    """
)

page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Overview",
        "🗺️ State Explorer",
        "📊 State Rankings",
        "🧪 What-if Simulator",
        "🏗️ Budget Structure",
        "🗂️ Data Sources",
        "⚙️ About the Model"
    ]
)


# -----------------------------
# Shared helper
# -----------------------------
def select_state():
    selected_state = st.selectbox(
        "Choose a state",
        states["state"].unique()
    )

    state_data = states[states["state"] == selected_state].iloc[0]

    return selected_state, state_data


# -----------------------------
# Overview page
# -----------------------------
if page == "🏠 Overview":
    total_states = len(states)
    total_population = states["population"].sum()
    total_annual_budget = states["annual_budget_ngn"].sum()
    average_capital_per_person = states["capital_budget_per_person"].mean()

    st.markdown(
    """
    <div class="hero">
        <h1>Nigeria Development Simulator</h1>
        <p>
            A public-facing tool for exploring how state budgets, population size and
            capital spending shape simple development comparisons across Nigerian states.
        </p>
        <p class="hero-small">
            Use the simulator to inspect state-level budget data, compare states and test
            basic what-if scenarios using prototype/sample values for all 36 states plus the FCT.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

    st.divider()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("States + FCT", total_states)

    with col2:
        st.metric("Prototype Population", f"{total_population:,.0f}")

    with col3:
        st.metric("Total Annual Budget", f"₦{total_annual_budget:,.0f}")

    with col4:
        st.metric(
            "Avg Capital per Person",
            f"₦{average_capital_per_person:,.0f}"
        )

    st.divider()

    st.write("### What you can explore")

    explore_col1, explore_col2 = st.columns(2)

    with explore_col1:
        st.markdown(
            """
            <div class="overview-card">
                <h3>Inspect a state</h3>
                <p>
                    Use State Explorer to view population, annual budget, capital budget,
                    recurrent budget and per-person indicators for one state at a time.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with explore_col2:
        st.markdown(
            """
            <div class="overview-card">
                <h3>Compare states</h3>
                <p>
                    Use State Rankings to compare states by capital budget per person,
                    the simulator's current simple development indicator.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    explore_col3, explore_col4 = st.columns(2)

    with explore_col3:
        st.markdown(
            """
            <div class="overview-card">
                <h3>Test scenarios</h3>
                <p>
                    Use the What-if Simulator and Budget Structure pages to explore how
                    capital and recurrent spending changes affect per-person figures.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with explore_col4:
        st.markdown(
            """
            <div class="overview-card">
                <h3>Check the data</h3>
                <p>
                    Use Data Sources to see what files power the prototype and what
                    verified sources should be added in future versions.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.divider()

    st.info(
        "Prototype dataset: this version uses prototype/sample values for all 36 states "
        "plus the FCT. The figures are not verified official data and should not be read "
        "as a complete measure of development."
    )

    st.markdown(
        """
        <div class="overview-cta">
            <p>
                <strong>Start with State Explorer</strong> to inspect one state, or use
                <strong>State Rankings</strong> to compare states in the current prototype dataset.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    with st.expander("View current prototype dataset"):
        st.dataframe(states, use_container_width=True)


# -----------------------------
# State Explorer page
# -----------------------------
elif page == "🗺️ State Explorer":
    st.title("🗺️ State Explorer")
    st.markdown(
        """
        Review one state at a time using the current budget and population fields.
        This page helps compare the size of a state's budget with the population it serves.
        """
    )

    st.divider()

    selector_left, selector_center, selector_right = st.columns([1, 2, 1])

    with selector_center:
        selected_state, state_data = select_state()

    st.write(f"## {selected_state}")

    st.caption("State-level snapshot using prototype/sample values, not verified official data.")

    st.divider()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Population", f"{state_data['population']:,.0f}")

    with col2:
        st.metric("Annual Budget", f"₦{state_data['annual_budget_ngn']:,.0f}")

    with col3:
        st.metric("Capital Budget", f"₦{state_data['capital_budget_ngn']:,.0f}")

    col4, col5 = st.columns(2)

    with col4:
        st.metric("Recurrent Budget", f"₦{state_data['recurrent_budget_ngn']:,.0f}")

    with col5:
        st.metric(
            "Annual Budget per Person",
            f"₦{state_data['annual_budget_per_person']:,.0f}"
        )

    st.write("### Per Person Detail")

    col6, col7 = st.columns(2)

    with col6:
        st.metric(
            "Capital Budget per Person",
            f"₦{state_data['capital_budget_per_person']:,.0f}"
        )

    with col7:
        st.metric(
            "Recurrent Budget per Person",
            f"₦{state_data['recurrent_budget_per_person']:,.0f}"
        )

    st.divider()

    st.write("### Interpretation")

    st.markdown(
        f"""
        <div class="state-insight">
            <p>
                <strong>{selected_state}</strong> has a total annual budget of
                <strong>₦{state_data['annual_budget_ngn']:,.0f}</strong> for a population of
                <strong>{state_data['population']:,.0f}</strong>, which works out to
                <strong>₦{state_data['annual_budget_per_person']:,.0f}</strong> per person.
            </p>
            <p>
                Capital spending is <strong>{state_data['capital_share_percent']:.1f}%</strong>
                of the budget, while recurrent spending is
                <strong>{state_data['recurrent_share_percent']:.1f}%</strong>. The current simple
                development indicator is capital budget per person:
                <strong>₦{state_data['capital_budget_per_person']:,.0f}</strong>.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.info(
        "Prototype note: these figures use prototype/sample values for all 36 states plus "
        "the FCT. They are not verified official data."
    )


# -----------------------------
# State Rankings page
# -----------------------------
elif page == "📊 State Rankings":
    st.title("📊 State Rankings")
    st.markdown(
        """
        Compare all 36 states plus the FCT using budget-per-person and budget structure
        indicators calculated from the current prototype dataset.
        """
    )

    st.divider()

    ranking_options = {
        "Annual budget per person": {
            "column": "annual_budget_per_person",
            "label": "Annual Budget per Person",
            "format": "currency",
            "description": "total annual budget divided by population"
        },
        "Capital budget per person": {
            "column": "capital_budget_per_person",
            "label": "Capital Budget per Person",
            "format": "currency",
            "description": "capital budget divided by population"
        },
        "Recurrent budget per person": {
            "column": "recurrent_budget_per_person",
            "label": "Recurrent Budget per Person",
            "format": "currency",
            "description": "recurrent budget divided by population"
        },
        "Capital budget share": {
            "column": "capital_share_percent",
            "label": "Capital Budget Share",
            "format": "percent",
            "description": "the percentage of the annual budget assigned to capital spending"
        }
    }

    selected_ranking = st.radio(
        "Rank states by",
        list(ranking_options.keys()),
        horizontal=True
    )

    ranking_config = ranking_options[selected_ranking]
    ranking_column = ranking_config["column"]

    ranking = states.sort_values(
        by=ranking_column,
        ascending=False
    ).copy()

    ranking["rank"] = range(1, len(ranking) + 1)

    display_ranking = ranking[
        [
            "rank",
            "state",
            "population",
            "annual_budget_per_person",
            "capital_budget_per_person",
            "recurrent_budget_per_person",
            "capital_share_percent"
        ]
    ].copy()

    display_ranking = display_ranking.rename(
        columns={
            "rank": "Rank",
            "state": "State",
            "population": "Population",
            "annual_budget_per_person": "Annual Budget per Person",
            "capital_budget_per_person": "Capital Budget per Person",
            "recurrent_budget_per_person": "Recurrent Budget per Person",
            "capital_share_percent": "Capital Budget Share (%)"
        }
    )

    st.dataframe(
        display_ranking,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Population": st.column_config.NumberColumn(format="%d"),
            "Annual Budget per Person": st.column_config.NumberColumn(format="₦%d"),
            "Capital Budget per Person": st.column_config.NumberColumn(format="₦%d"),
            "Recurrent Budget per Person": st.column_config.NumberColumn(format="₦%d"),
            "Capital Budget Share (%)": st.column_config.NumberColumn(format="%.1f%%")
        }
    )

    st.divider()

    st.write(f"### Ranking by {ranking_config['label']}")

    chart_data = ranking[
        ["state", ranking_column]
    ].set_index("state")

    st.bar_chart(chart_data)

    top_state = ranking.iloc[0]
    top_value = top_state[ranking_column]

    if ranking_config["format"] == "percent":
        top_value_text = f"{top_value:.1f}%"
    else:
        top_value_text = f"₦{top_value:,.0f}"

    st.write("### Interpretation")

    st.markdown(
        f"""
        <div class="ranking-insight">
            <p>
                This ranking sorts states by <strong>{ranking_config['description']}</strong>.
                In the current prototype dataset, <strong>{top_state['state']}</strong> ranks highest for
                <strong>{ranking_config['label']}</strong> at <strong>{top_value_text}</strong>.
                Higher values show stronger relative budget allocation on this specific measure,
                not a complete measure of development.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.info(
        "Prototype note: the dataset includes all 36 states plus the FCT, but the figures "
        "are prototype/sample values rather than verified official data."
    )


# -----------------------------
# What-if Simulator page
# -----------------------------
elif page == "🧪 What-if Simulator":
    st.title("🧪 What-if Simulator")
    st.markdown(
        """
        Adjust budget assumptions for one state and see how the changes affect
        per-person budget indicators. This is a simple modelling workspace using
        the current prototype/sample data.
        """
    )

    st.divider()

    selector_left, selector_center, selector_right = st.columns([1, 2, 1])

    with selector_center:
        selected_state, state_data = select_state()

    st.write(f"## {selected_state}")
    st.caption("Adjust the assumptions below to compare original and simulated figures.")

    current_capital_budget = state_data["capital_budget_ngn"]
    current_recurrent_budget = state_data["recurrent_budget_ngn"]
    current_annual_budget = state_data["annual_budget_ngn"]
    population = state_data["population"]
    current_annual_per_person = state_data["annual_budget_per_person"]
    current_capital_per_person = state_data["capital_budget_per_person"]
    current_recurrent_per_person = state_data["recurrent_budget_per_person"]

    st.divider()

    st.write("### Simulation Assumptions")

    control_col1, control_col2 = st.columns(2)

    with control_col1:
        capital_change_percent = st.slider(
            "Capital budget change (%)",
            min_value=-50,
            max_value=100,
            value=10,
            step=5
        )

    with control_col2:
        recurrent_change_percent = st.slider(
            "Recurrent budget change (%)",
            min_value=-50,
            max_value=100,
            value=0,
            step=5
        )

    simulated_capital_budget = current_capital_budget * (1 + capital_change_percent / 100)
    simulated_recurrent_budget = current_recurrent_budget * (1 + recurrent_change_percent / 100)
    simulated_annual_budget = simulated_capital_budget + simulated_recurrent_budget

    simulated_annual_per_person = simulated_annual_budget / population
    simulated_capital_per_person = simulated_capital_budget / population
    simulated_recurrent_per_person = simulated_recurrent_budget / population
    simulated_capital_budget_increase = simulated_capital_budget - current_capital_budget

    st.divider()

    st.write("### Original vs Simulated")

    before_col1, before_col2, before_col3 = st.columns(3)

    with before_col1:
        st.metric(
            "Annual Budget per Person",
            f"₦{simulated_annual_per_person:,.0f}",
            delta=f"₦{simulated_annual_per_person - current_annual_per_person:,.0f}"
        )

    with before_col2:
        st.metric(
            "Capital Budget per Person",
            f"₦{simulated_capital_per_person:,.0f}",
            delta=f"₦{simulated_capital_per_person - current_capital_per_person:,.0f}"
        )

    with before_col3:
        st.metric(
            "Recurrent Budget per Person",
            f"₦{simulated_recurrent_per_person:,.0f}",
            delta=f"₦{simulated_recurrent_per_person - current_recurrent_per_person:,.0f}"
        )

    comparison_data = pd.DataFrame({
        "Indicator": [
            "Annual Budget per Person",
            "Capital Budget per Person",
            "Recurrent Budget per Person"
        ],
        "Original": [
            current_annual_per_person,
            current_capital_per_person,
            current_recurrent_per_person
        ],
        "Simulated": [
            simulated_annual_per_person,
            simulated_capital_per_person,
            simulated_recurrent_per_person
        ]
    }).set_index("Indicator")

    st.bar_chart(comparison_data)

    with st.expander("View budget totals"):
        totals_data = pd.DataFrame({
            "Budget Type": ["Annual Budget", "Capital Budget", "Recurrent Budget"],
            "Original": [
                current_annual_budget,
                current_capital_budget,
                current_recurrent_budget
            ],
            "Simulated": [
                simulated_annual_budget,
                simulated_capital_budget,
                simulated_recurrent_budget
            ]
        })

        st.dataframe(
            totals_data,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Original": st.column_config.NumberColumn(format="₦%d"),
                "Simulated": st.column_config.NumberColumn(format="₦%d")
            }
        )

    st.divider()

    st.write("### What could this fund?")

    project_options = project_costs["item"].tolist()
    selected_project_item = st.selectbox(
        "Choose a prototype project cost assumption",
        project_options
    )

    selected_project = project_costs[
        project_costs["item"] == selected_project_item
    ].iloc[0]

    unit_cost = selected_project["unit_cost_ngn"]
    unit_name = selected_project["unit_name"]

    cost_col1, cost_col2 = st.columns(2)

    with cost_col1:
        st.metric("Additional Capital Allocation", f"₦{simulated_capital_budget_increase:,.0f}")

    with cost_col2:
        st.metric("Selected Unit Cost", f"₦{unit_cost:,.0f}")

    if simulated_capital_budget_increase <= 0:
        st.info(
            "There is no additional capital allocation to estimate project funding from. "
            "Increase the capital budget assumption above to see an illustrative project estimate."
        )
    else:
        estimated_units = simulated_capital_budget_increase / unit_cost

        st.metric(
            f"Estimated {unit_name}",
            f"{estimated_units:,.1f}"
        )

        st.write(
            f"The simulated additional capital allocation could fund approximately "
            f"{estimated_units:,.1f} {unit_name}."
        )

    st.caption(
        "These are prototype cost assumptions, not verified procurement costs. Real costs vary "
        "by location, inflation, procurement, terrain, specification, and implementation quality."
    )

    st.write("### What changed")

    st.markdown(
        f"""
        <div class="simulation-insight">
            <p>
                For <strong>{selected_state}</strong>, the simulation changes capital spending by
                <strong>{capital_change_percent}%</strong> and recurrent spending by
                <strong>{recurrent_change_percent}%</strong>. Under these assumptions, capital
                budget per person moves from <strong>₦{current_capital_per_person:,.0f}</strong>
                to <strong>₦{simulated_capital_per_person:,.0f}</strong>.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.info(
        "Prototype note: this is a modelling demonstration using prototype/sample values "
        "from states.csv. It does not include actual spending performance or wider "
        "development outcomes."
    )


# -----------------------------
# Budget Structure page
# -----------------------------
elif page == "🏗️ Budget Structure":
    st.title("🏗️ Budget Structure")
    st.markdown(
        """
        Explore how a selected state's annual budget is split between capital spending
        and recurrent spending using the current prototype dataset.
        """
    )

    st.divider()

    selector_left, selector_center, selector_right = st.columns([1, 2, 1])

    with selector_center:
        selected_state, state_data = select_state()

    st.write(f"## {selected_state}")
    st.caption("Capital and recurrent shares are calculated from the annual budget fields.")

    capital_share = state_data["capital_share_percent"]
    recurrent_share = state_data["recurrent_share_percent"]

    st.divider()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Capital Share of Budget", f"{capital_share:.1f}%")

    with col2:
        st.metric("Recurrent Share of Budget", f"{recurrent_share:.1f}%")

    with col3:
        st.metric("Capital Budget", f"₦{state_data['capital_budget_ngn']:,.0f}")

    with col4:
        st.metric("Recurrent Budget", f"₦{state_data['recurrent_budget_ngn']:,.0f}")

    st.divider()

    st.write("### Capital vs Recurrent Spending")

    budget_structure = pd.DataFrame({
        "Budget Type": ["Capital", "Recurrent"],
        "Amount": [
            state_data["capital_budget_ngn"],
            state_data["recurrent_budget_ngn"]
        ]
    }).set_index("Budget Type")

    st.bar_chart(budget_structure)

    st.write("### Interpretation")

    if capital_share > recurrent_share:
        balance_text = "leans more toward capital spending than recurrent spending"
    elif recurrent_share > capital_share:
        balance_text = "leans more toward recurrent spending than capital spending"
    else:
        balance_text = "is evenly split between capital and recurrent spending"

    st.markdown(
        f"""
        <div class="budget-insight">
            <p>
                In the current prototype dataset, <strong>{selected_state}</strong>'s budget
                <strong>{balance_text}</strong>. Capital spending accounts for
                <strong>{capital_share:.1f}%</strong> of the annual budget, while recurrent
                spending accounts for <strong>{recurrent_share:.1f}%</strong>.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.info(
        "Prototype note: these figures come from prototype/sample values in states.csv, "
        "not verified official data. Capital spending usually refers to projects and "
        "infrastructure, while recurrent spending covers ongoing government operating costs."
    )


# -----------------------------
# Archived/internal page: removed from public navigation.
# Kept in place for now so the old prototype statistics code is not lost.
# -----------------------------
elif page == "📈 M248 Statistics Lab":
    st.title("📈 M248 Statistics Lab")

    st.markdown(
        """
        This section is where your M248 statistics becomes useful.

        Later, we can use the data to explore:

        - Mean and variance of state budget indicators
        - Outliers
        - Correlation
        - Regression
        - Confidence intervals
        - Comparing groups of states
        """
    )

    st.divider()

    mean_capital_per_person = states["capital_budget_per_person"].mean()
    variance_capital_per_person = states["capital_budget_per_person"].var()
    standard_deviation_capital_per_person = states["capital_budget_per_person"].std()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Mean Capital Budget per Person",
            f"₦{mean_capital_per_person:,.0f}"
        )

    with col2:
        st.metric(
            "Variance",
            f"{variance_capital_per_person:,.0f}"
        )

    with col3:
        st.metric(
            "Standard Deviation",
            f"₦{standard_deviation_capital_per_person:,.0f}"
        )

    st.info(
        "Because the current dataset is still very small, these statistics are only illustrative. "
        "They will become more useful when we add all Nigerian states and more indicators."
    )


# -----------------------------
# About the Model page
# -----------------------------
elif page == "⚙️ About the Model":
    st.title("⚙️ About the Model")
    st.markdown(
        """
        The Nigeria Development Simulator is a prototype tool for exploring how state
        budget figures relate to population size and simple per-person indicators.
        """
    )

    st.divider()

    st.write("### Current Prototype Dataset")
    st.markdown(
        """
        The current app uses prototype/sample values for all 36 states plus the FCT
        from `states.csv`.

        It currently includes:

        - State name
        - Population
        - Annual budget
        - Capital budget
        - Recurrent budget

        The state list is complete, but the figures are not verified official data.
        The dataset is useful for testing the simulator interface and basic calculations.
        """
    )

    st.write("### Current Indicators")
    st.markdown(
        """
        The app currently calculates five simple indicators:

        - **Annual budget per person:** annual budget divided by population.
        - **Capital budget per person:** capital budget divided by population.
        - **Recurrent budget per person:** recurrent budget divided by population.
        - **Capital budget share:** capital budget as a percentage of annual budget.
        - **Recurrent budget share:** recurrent budget as a percentage of annual budget.
        """
    )

    st.write("### What the Simulator Can Currently Show")
    st.markdown(
        """
        With the current data, the simulator can:

        - Compare all 36 states plus the FCT by budget-per-person indicators.
        - Show how capital and recurrent spending are split.
        - Test simple what-if changes to capital and recurrent budgets.
        - Explain how each state looks under the current prototype calculations.
        """
    )

    st.write("### Limitations")
    st.markdown(
        """
        This prototype should be interpreted carefully.

        - The current dataset contains prototype/sample values, not verified official data.
        - Budget figures alone do not prove development outcomes.
        - Real development depends on implementation, governance, procurement, inflation,
          security, education, health, infrastructure and many other factors.
        - The app does not yet measure whether money was actually spent well or whether
          projects were completed.
        """
    )

    st.write("### Next Improvements")
    st.markdown(
        """
        Stronger future versions can add:

        - Verified official values for Nigerian states and the FCT.
        - Verified data sources.
        - Year-by-year trends.
        - Sector-level budgets.
        - Project cost assumptions.
        - Richer development indicators.
        """
    )


# -----------------------------
# Data Sources page
# -----------------------------
elif page == "🗂️ Data Sources":
    st.title("🗂️ Data Sources")
    st.markdown(
        """
        This page explains what data currently powers the prototype and what should
        be added before the simulator is treated as a verified public evidence tool.
        """
    )

    st.divider()

    st.write("### Current Prototype Files")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("States in states.csv", len(states))

    with col2:
        st.metric("Project cost items", len(project_costs))

    st.markdown(
        """
        The app currently uses two local CSV files:

        - `data/states.csv`: prototype/sample state-level budget and population values
          for all 36 states plus the FCT, used by the main simulator pages.
        - `data/project_costs.csv`: prototype project-cost assumptions used for
          illustrative development modelling in the What-if Simulator.
        """
    )

    st.write("### Prototype Status")
    st.info(
        "The current dataset contains prototype/sample values for all 36 states plus the "
        "FCT. The state list is complete, but the figures are not verified official data."
    )

    st.write("### Future Verified Sources")
    st.markdown(
        """
        Future versions should replace or validate the prototype/sample figures using
        credible public sources, such as:

        - Official state budget documents.
        - National Bureau of Statistics data.
        - Other credible public datasets from government, development institutions or
          reputable research organisations.
        """
    )

    st.write("### Data Preview")

    with st.expander("View states.csv prototype data"):
        st.dataframe(states, use_container_width=True)

    with st.expander("View project_costs.csv prototype data"):
        st.dataframe(project_costs, use_container_width=True)
