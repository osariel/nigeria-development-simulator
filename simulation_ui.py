"""Interactive controls, comparison and portable scenario reports."""
import io
import json
import zipfile
import pandas as pd
import streamlit as st
from models.simulator import Scenario, simulate

SECTORS = {'Schools': 'Basic school infrastructure package',
           'Health centres': 'Basic primary health centre construction or major upgrade',
           'Boreholes': 'Community borehole water point'}


def report_bundle(results, benchmarks):
    output = io.BytesIO()
    with zipfile.ZipFile(output, 'w', zipfile.ZIP_DEFLATED) as archive:
        archive.writestr('scenarios.json', json.dumps(results, indent=2))
        archive.writestr('cost_sources.csv', benchmarks.to_csv(index=False))
        archive.writestr('README.txt', 'Five-year investment planning estimates. Funding is released evenly each year. Unspent cash carries forward within each sector, with no interest. Unit costs are user assumptions in start-year naira, inflated annually. Whole project packages are fully paid when started. Completion occurs after the selected delay. Pending projects have been paid for but finish outside the horizon. No additional delay costs are assumed. Excludes operating costs, land and other benchmark exclusions. State selection labels the scenario; costs are national benchmarks, not state-specific rates. No prediction of jobs, poverty or service quality.\n')
        for name, result in results.items():
            archive.writestr(name + '_annual.csv', pd.DataFrame(result['annual']).to_csv(index=False))
    return output.getvalue()


def render_simulation(states, costs):
    st.title('Build a five-year investment plan')
    st.write('Allocate funding. Explore cost pressures. Compare what two plans could deliver.')
    names = sorted(states.state.unique())
    c1, c2, c3 = st.columns(3)
    state = c1.selectbox('State', names, index=names.index('Edo') if 'Edo' in names else 0)
    year = c2.number_input('Start year', min_value=2026, max_value=2050, value=2026, step=1)
    budget = c3.number_input('Total five-year funding (₦ billion)', min_value=0.01, max_value=100000.0, value=50.0)
    reference = states[(states.state == state) & (states.year == year)]
    if not reference.empty and pd.notna(reference.iloc[0].annual_budget_ngn):
        st.caption(f"Dataset reference: {state} {year} total annual budget ₦{reference.iloc[0].annual_budget_ngn / 1e9:,.1f}bn. Your five-year allocation is hypothetical and is not deducted from this budget.")
    selected = costs[costs['item'].isin(SECTORS.values())].copy()
    if len(selected) != len(SECTORS):
        st.error('A required project benchmark is missing. Restore the school, health centre and borehole cost rows to run the model.')
        return
    with st.expander('Project costs and model assumptions'):
        st.write('Set unit costs in start-year naira. Defaults use the existing national planning benchmarks; they are not current local quotes. Schools and health centres mean the packages described below.')
        unit_costs = {}
        for sector, item in SECTORS.items():
            row = selected[selected['item'] == item].iloc[0]
            unit_costs[sector] = st.number_input(f'{sector}: cost per package (₦ million)', min_value=0.01, value=float(row.cost_ngn / 1e6), key='unit_' + sector) * 1e6
            st.caption(row.notes)
            if str(row.source_url).startswith(('https://', 'http://')):
                st.link_button(str(row.source_name), row.source_url)
        st.write('Funding arrives in five equal annual instalments. Unspent money stays in its sector. Whole packages are fully paid at the year’s cost when started. Delay shifts completion only; it adds no separate cost. Running costs, staffing and broader economic impacts are excluded.')
    results = {}
    columns = st.columns(2)
    for col, name, defaults in zip(columns, ['Plan A', 'Plan B'], [(40, 35, 25), (25, 50, 25)]):
        with col:
            st.subheader(name)
            allocation = {sector: st.number_input(f'{sector} allocation (%)', min_value=0, max_value=100, value=default, key=name + sector) for sector, default in zip(SECTORS, defaults)}
            inflation = st.slider('Annual construction inflation (%)', 0, 50, 10, key=name + 'inflation')
            adjustment = st.slider('Initial cost adjustment (%)', -50, 100, 0, key=name + 'adjustment')
            delay = st.slider('Completion delay (years)', 0, 5, 0, key=name + 'delay')
            if sum(allocation.values()) != 100:
                st.warning(f"Allocations total {sum(allocation.values())}%. Adjust them to 100% to calculate this plan.")
                continue
            result = simulate(Scenario(state, int(year), budget * 1e9, allocation, unit_costs, inflation / 100, adjustment / 100, delay))
            results[name] = result
            frame = pd.DataFrame(result['annual'])
            final = frame[frame.year == year + 4]
            st.metric('Unspent after five years', f"₦{final.unspent_ngn.sum() / 1e9:,.2f}bn")
            st.dataframe(final[['sector', 'cumulative_completed', 'pending_units']].rename(columns={'sector': 'Project package', 'cumulative_completed': 'Completed', 'pending_units': 'Due after year five'}), hide_index=True, width='stretch')
    if len(results) == 2:
        st.subheader('Compare delivery over time')
        sector = st.selectbox('Project type to compare', list(SECTORS))
        combined = pd.concat([pd.DataFrame(r['annual']).assign(plan=n) for n, r in results.items()])
        chart = combined[combined.sector == sector].pivot(index='year', columns='plan', values='cumulative_completed')
        st.line_chart(chart, x_label='Year', y_label='Cumulative completed packages')
        final = combined[combined.year == year + 4]
        comparison = final.pivot(index='sector', columns='plan', values='cumulative_completed')
        comparison['B minus A'] = comparison['Plan B'] - comparison['Plan A']
        st.dataframe(comparison, width='stretch')
        st.caption('Comparisons count completed packages, not people served or improvements in outcomes. Paid projects due after year five are shown above.')
    if results:
        with st.expander('Annual funding and delivery details'):
            for name, result in results.items():
                st.write(name)
                st.dataframe(pd.DataFrame(result['annual']), hide_index=True, width='stretch')
        st.download_button('Download plans, annual results and assumptions', report_bundle(results, selected), 'investment-plans.zip', 'application/zip')
        st.caption('The download preserves both plans and their assumptions. Controls remain available during this session; there is no account-based saving yet.')
