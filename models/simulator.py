"""Five-year capital planning model. All monetary inputs are nominal naira."""
from dataclasses import dataclass, asdict
import math


@dataclass(frozen=True)
class Scenario:
    state: str
    start_year: int
    budget: float
    allocations: dict
    unit_costs: dict
    inflation: float = 0.10
    cost_adjustment: float = 0.0
    delay_years: int = 0


def simulate(plan):
    sectors = set(plan.allocations)
    if not sectors or sectors != set(plan.unit_costs):
        raise ValueError('Allocations and unit costs must cover the same sectors.')
    values = [plan.budget, plan.inflation, plan.cost_adjustment, *plan.allocations.values(), *plan.unit_costs.values()]
    if not all(math.isfinite(v) for v in values):
        raise ValueError('All assumptions must be finite numbers.')
    if plan.budget <= 0 or any(v <= 0 for v in plan.unit_costs.values()):
        raise ValueError('Budget and unit costs must be positive.')
    if any(v < 0 for v in plan.allocations.values()) or not math.isclose(sum(plan.allocations.values()), 100, abs_tol=1e-8):
        raise ValueError('Allocations must be non-negative and total 100%.')
    if not 0 <= plan.inflation <= 1 or not -0.9 <= plan.cost_adjustment <= 3:
        raise ValueError('Inflation or cost adjustment is outside the supported range.')
    if type(plan.delay_years) is not int or not 0 <= plan.delay_years <= 5:
        raise ValueError('Delay must be a whole number between zero and five years.')
    rows = []
    for sector, share in plan.allocations.items():
        balance = 0.0
        completed = 0
        starts = []
        for t in range(5):
            release = plan.budget * share / 100 / 5
            balance += release
            cost = plan.unit_costs[sector] * (1 + plan.cost_adjustment) * (1 + plan.inflation) ** t
            units = math.floor(balance / cost)
            spent = units * cost
            balance -= spent
            starts.append(units)
            delivered = starts[t - plan.delay_years] if t >= plan.delay_years else 0
            completed += delivered
            rows.append(dict(year=plan.start_year + t, sector=sector, funding_ngn=release,
                             unit_cost_ngn=cost, construction_spend_ngn=spent,
                             unspent_ngn=balance, units_started=units,
                             units_completed=delivered, cumulative_completed=completed,
                             pending_units=sum(starts) - completed))
    return {'assumptions': asdict(plan), 'annual': rows}
