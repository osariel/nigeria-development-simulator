"""Grounded conversational routing; no external model or network is required."""
import math
import re
import pandas as pd


def money(value):
    if pd.isna(value):
        return 'Not available'
    return f'₦{value:,.0f}'


def answer(prompt, context, states, costs):
    text = prompt.lower().strip()
    context = dict(context)
    years = [int(y) for y in re.findall(r'\b20\d{2}\b', text)]
    if years:
        if len(set(years)) > 1:
            return {'text': 'Please ask about one year at a time.', 'context': context}
        if years[0] not in states.year.values:
            return {'text': 'Available budget years: ' + ', '.join(map(str, sorted(states.year.unique()))) + '.', 'context': context}
        context['year'] = years[0]
    mentioned = sorted([s for s in states.state.unique() if re.search(r'\b' + re.escape(s.lower()) + r'\b', text)], key=lambda s: text.index(s.lower()))
    if mentioned:
        context['states'] = mentioned
    year = context['year']
    selected = context.get('states', [])
    frame = states[states.year == year]
    rows = frame[frame.state.isin(selected)]
    result = {'context': context}

    def respond(message, table=None, source_rows=None):
        result['text'] = message
        if table is not None:
            result['table'] = table
        if source_rows is not None:
            result['sources'] = [dict(state=r.state, status=str(r.get('data_status', 'unknown')), budget_status=str(r.get('budget_status', 'unknown')), name=str(r.get('budget_source_name', 'Local dataset')), url=str(r.get('budget_source_url', '')), notes=str(r.get('budget_notes', ''))) for _, r in source_rows.iterrows()]
        return result

    if re.search(r'\b(help|hello|hi)\b', text):
        return respond('Ask for a state budget, compare states, rank budgets, or estimate what an amount could build. For example: “Lagos budget 2026”, “Compare Lagos and Kano”, or “What could ₦1 billion build?” Follow-ups reuse the state and year shown in the sidebar.')
    if 'capital' in text and any(w in text for w in ['what is', 'meaning', 'mean?', 'explain capital']):
        return respond('Capital spending funds assets such as roads, schools and water infrastructure. Recurrent spending covers ongoing costs such as salaries and operations. A budget is a spending plan; it does not show what was actually delivered.')

    scenario = bool(re.search(r'build|schools?|clinics?|boreholes?|roads?|health centres?|water|what if|allocate|spend|could|simulate', text))
    amount_match = re.search(r'(?:₦|ngn\s*|naira\s*)?(-?\d[\d,]*(?:\.\d+)?)\s*(trillion|billion|million|bn|mn|[bmk])\b', text)
    raw_amount = re.search(r'(?:₦|ngn\s*)(-?\d[\d,]*(?:\.\d+)?)\b', text)
    percentage = re.search(r'(-?\d+(?:\.\d+)?)\s*(?:%|percent)', text)
    if scenario or amount_match or raw_amount:
        if percentage:
            pct = float(percentage[1])
            if not 0 < pct <= 100:
                return respond('Choose a percentage greater than 0 and no more than 100.')
            if len(rows) != 1:
                return respond('Name one state for this percentage scenario, for example “What could 10% of Lagos capital budget build?”')
            column = 'capital_budget_ngn' if 'capital' in text else 'annual_budget_ngn'
            base = rows.iloc[0][column]
            if pd.isna(base):
                return respond('That budget amount is missing, so I cannot calculate this scenario.', source_rows=rows)
            amount = base * pct / 100
            basis = f'{pct:g}% of {rows.iloc[0].state}’s {year} {"capital" if "capital" in text else "total"} budget'
        elif amount_match or raw_amount:
            match = amount_match or raw_amount
            amount = float(match[1].replace(',', ''))
            if amount_match:
                amount *= {'trillion': 1e12, 'billion': 1e9, 'million': 1e6, 'bn': 1e9, 'mn': 1e6, 'b': 1e9, 'm': 1e6, 'k': 1e3}[match[2]]
            basis = 'your hypothetical allocation'
        elif 'amount' in context and not mentioned and not years:
            amount = context['amount']
            basis = 'your previous hypothetical allocation'
        else:
            return respond('Give an amount or a percentage of one state’s budget, for example “What could ₦1 billion build?” or “Allocate 10% of Lagos capital budget to schools”.')
        if not math.isfinite(amount) or amount <= 0 or amount > 1e16:
            return respond('Enter a positive allocation of no more than ₦10 quadrillion.')
        context['amount'] = amount
        aliases = {'school': 'school', 'clinic': 'health', 'health': 'health', 'borehole': 'borehole', 'road': 'road', 'water': 'water'}
        keywords = {v for k, v in aliases.items() if k in text}
        chosen = costs[costs.item.str.lower().apply(lambda item: any(k in item for k in keywords))] if keywords else costs
        table = pd.DataFrame([{'Project': r['item'], 'Unit': r.unit, 'Cost per unit': money(r.cost_ngn), 'Whole units': math.floor(amount / r.cost_ngn), 'Unspent balance': money(amount - math.floor(amount / r.cost_ngn) * r.cost_ngn)} for _, r in chosen.iterrows()])
        result['assumptions'] = chosen[['item', 'source_name', 'source_url', 'notes']].to_dict('records')
        return respond(f'**{money(amount)}** from {basis}. Each row is a separate alternative using the full allocation; do not add the rows together.\n\nThese are benchmark estimates, not procurement quotes or predictions of delivery. Local conditions, land, staffing and equipment can change costs.', table, rows if percentage else None)

    if re.search(r'rank|highest|lowest|largest|smallest|top\b', text):
        metric = 'annual_budget_per_person' if ('person' in text or 'capita' in text) else ('capital_budget_ngn' if 'capital' in text else 'annual_budget_ngn')
        ranked = frame.dropna(subset=[metric]).sort_values(metric, ascending=bool(re.search('lowest|smallest', text)))
        count = re.search(r'top\s+(\d+)', text)
        ranked = ranked.head(min(int(count[1]), 37) if count else 10)
        return respond(f'**{year} budget ranking** by {"budget per resident (population projections)" if "person" in metric else "capital budget" if "capital" in metric else "total budget"}. Missing values are excluded. This ranks spending plans, not development outcomes.', pd.DataFrame({'State': ranked.state, 'Amount': ranked[metric].map(money)}).reset_index(drop=True), ranked)
    if 'compare' in text and len(rows) < 2:
        return respond('Name at least two states, for example “Compare Lagos and Kano in 2026”.')
    if rows.empty:
        return respond('Which state would you like to explore? Try “Lagos budget 2026”, “Rank states by budget per person”, or “What could ₦1 billion build?”')
    if not (mentioned or years or re.search(r'budget|compare|capital|recurrent|person|capita|source|breakdown|money|population|and|what about', text)):
        return respond('I can look up budgets, compare or rank states, and calculate project scenarios from this dataset. Try “Show the capital budget” or “What could 10% build?”')
    table = pd.DataFrame([{'State': r.state, 'Total budget': money(r.annual_budget_ngn), 'Capital': money(r.capital_budget_ngn), 'Recurrent': money(r.recurrent_budget_ngn), 'Budget per resident': money(r.annual_budget_per_person)} for _, r in rows.iterrows()])
    return respond(f'**{year} · {", ".join(rows.state)}**\n\nCapital is planned investment in assets; recurrent is ongoing spending. Per-resident amounts use population projections. Missing figures remain unavailable. These are budget plans, not actual expenditure.', table, rows)
