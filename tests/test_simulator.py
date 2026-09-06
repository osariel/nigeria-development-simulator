import unittest
from dataclasses import replace
from models.simulator import Scenario, simulate

class SimulatorTests(unittest.TestCase):
    def setUp(self):
        self.plan = Scenario('Edo', 2026, 1000, {'Schools': 100}, {'Schools': 60}, inflation=0)
    def test_cash_conservation_and_carry(self):
        rows = simulate(self.plan)['annual']
        self.assertEqual([r['units_started'] for r in rows], [3, 3, 4, 3, 3])
        for i, row in enumerate(rows):
            self.assertAlmostEqual(sum(r['construction_spend_ngn'] for r in rows[:i+1]) + row['unspent_ngn'], 200*(i+1))
            self.assertGreaterEqual(row['unspent_ngn'], 0)
    def test_delay_retains_paid_pipeline(self):
        rows = simulate(replace(self.plan, delay_years=2))['annual']
        self.assertEqual([r['units_completed'] for r in rows], [0, 0, 3, 3, 4])
        self.assertEqual(rows[-1]['pending_units'], 6)
        self.assertEqual(rows[-1]['cumulative_completed'] + rows[-1]['pending_units'], 16)
    def test_inflation_and_initial_cost_change(self):
        base = simulate(self.plan)['annual']
        expensive = simulate(replace(self.plan, inflation=.2, cost_adjustment=.2))['annual']
        self.assertAlmostEqual(expensive[-1]['unit_cost_ngn'], 60*1.2**5)
        self.assertLess(expensive[-1]['cumulative_completed'], base[-1]['cumulative_completed'])
    def test_zero_allocation(self):
        rows = simulate(replace(self.plan, allocations={'Schools':0,'Water':100},unit_costs={'Schools':60,'Water':10}))['annual']
        self.assertTrue(all(r['units_started']==0 for r in rows if r['sector']=='Schools'))
    def test_invalid_assumptions(self):
        for change in [dict(budget=-1),dict(budget=float('nan')),dict(allocations={'Schools':90}),dict(unit_costs={'Schools':0}),dict(delay_years=1.5)]:
            with self.assertRaises(ValueError):
                simulate(replace(self.plan, **change))
