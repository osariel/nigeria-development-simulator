import unittest
import pandas as pd
from models.chat import answer

class ChatTests(unittest.TestCase):
    def setUp(self):
        self.states = pd.DataFrame([
            dict(state='Lagos', year=2026, annual_budget_ngn=1e9, capital_budget_ngn=6e8, recurrent_budget_ngn=4e8, annual_budget_per_person=100),
            dict(state='Kano', year=2026, annual_budget_ngn=5e8, capital_budget_ngn=float('nan'), recurrent_budget_ngn=2e8, annual_budget_per_person=50),
        ])
        self.costs = pd.DataFrame([dict(item='Basic school', unit='schools', cost_ngn=180e6, source_name='Benchmark', source_url='', notes='Estimate')])
        self.context = dict(year=2026, states=[])
    def ask(self, text, context=None):
        return answer(text, context or self.context, self.states, self.costs)
    def test_allocation_and_followup(self):
        r = self.ask('What could ₦1 billion build?')
        self.assertEqual(r['table'].iloc[0]['Whole units'], 5)
        self.assertEqual(r['table'].iloc[0]['Project'], 'Basic school')
        self.assertEqual(r['table'].iloc[0]['Unspent balance'], '₦100,000,000')
        self.assertEqual(self.ask('What about schools?', r['context'])['context']['amount'], 1e9)
    def test_percentage(self):
        r = self.ask('What could 50% of Lagos capital budget build?')
        self.assertEqual(r['context']['amount'], 3e8)
        self.assertEqual(r['table'].iloc[0]['Whole units'], 1)
    def test_missing_and_invalid(self):
        self.assertIn('missing', self.ask('What could 10% of Kano capital budget build?')['text'])
        self.assertIn('no more than 100', self.ask('What could 120% of Lagos budget build?')['text'])
        self.assertIn('positive', self.ask('Build schools with ₦-1 billion')['text'])
        self.assertNotIn('table', self.ask('Lagos budget 2030'))
    def test_compare_rank_and_context(self):
        r = self.ask('Compare Lagos and Kano')
        self.assertEqual(len(r['table']), 2)
        self.assertEqual(len(self.ask('Show capital budget', r['context'])['table']), 2)
        self.assertEqual(self.ask('Rank by budget per person')['table'].iloc[0]['State'], 'Lagos')
    def test_unsupported(self):
        self.assertNotIn('table', self.ask('Who won the election?', dict(year=2026, states=['Lagos'])))

if __name__ == '__main__':
    unittest.main()
