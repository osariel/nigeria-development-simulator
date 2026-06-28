# Nigeria Development Simulator Data

This folder is structured for a first real-data baseline using 2025 approved
Nigerian state budget figures where available.

## Files

- `state_budgets.csv`: state budget figures by year.
- `state_population.csv`: population figures or projections by state and year.
- `project_costs.csv`: project-cost assumptions for budget translation.
- `sources.csv`: source catalogue for source IDs used in the data files.
- `states.csv`: legacy fallback file kept for deployment compatibility.

## Budget Data Quality

Each row in `state_budgets.csv` should include:

- `state`
- `year`
- `total_budget_ngn`
- `capital_budget_ngn`
- `recurrent_budget_ngn`
- `personnel_cost_ngn`
- `overhead_cost_ngn`
- `debt_service_ngn`
- `source_id`
- `data_status`
- `notes`

Use blank cells when a value is not available yet. Do not fill gaps with
unsourced numbers.

## Population Data

The first real-data baseline should use population projections from the
National Bureau of Statistics where available. Population rows should include
source notes so users can distinguish official figures from estimates.

## Status Labels

- `Verified`: taken from an official budget document or reputable published
  dataset.
- `Estimated`: derived from available public figures or transparent
  assumptions.
- `Missing/partial`: source-backed values are not available yet, or the row
  still needs review before use in public analysis.

## Source Catalogue

`sources.csv` should document each `source_id` with:

- `source_id`
- `source_name`
- `publisher`
- `year`
- `url`
- `source_type`
- `access_date`
- `reliability_note`

The app keeps source URLs out of the main public pages, but the source fields
remain available for audit and later publication.

## OpenStates Strategy

Open Nigerian States / OpenStates is treated as the preferred public source
directory for state budget documents. Use `SRC_OPENSTATES_MAIN` for the main
portal record, and use state-specific OpenStates source IDs when a linked
approved budget document has been identified.

OpenStates entries should be treated as document-directory records until the
figures have been extracted from the linked approved budget document. Do not
replace a news-sourced or secondary figure with an OpenStates-linked figure
unless the approved document value has been checked.
