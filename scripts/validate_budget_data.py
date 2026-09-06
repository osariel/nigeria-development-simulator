from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"

STATE_BUDGET_COLUMNS = [
    "state",
    "year",
    "total_budget_ngn",
    "capital_budget_ngn",
    "recurrent_budget_ngn",
    "budget_status",
    "data_status",
    "source_id",
    "notes",
]

SOURCE_COLUMNS = [
    "source_id",
    "state",
    "year",
    "budget_type",
    "source_name",
    "source_url",
    "document_title",
    "document_date",
    "extracted_total_ngn",
    "extracted_capital_ngn",
    "extracted_recurrent_ngn",
    "extraction_status",
    "last_checked",
    "notes",
]

NUMERIC_COLUMNS = [
    "total_budget_ngn",
    "capital_budget_ngn",
    "recurrent_budget_ngn",
]

SOURCE_NUMERIC_COLUMNS = [
    "extracted_total_ngn",
    "extracted_capital_ngn",
    "extracted_recurrent_ngn",
]

TOLERANCE_NGN = 1_000


def read_csv(path):
    if not path.exists():
        raise FileNotFoundError(f"Missing required file: {path}")
    return pd.read_csv(path, keep_default_na=False)


def require_columns(dataframe, required_columns, label):
    missing = [column for column in required_columns if column not in dataframe.columns]
    if missing:
        return [f"{label} is missing required column(s): {', '.join(missing)}"]
    return []


def coerce_numeric(dataframe, columns, label):
    errors = []
    converted = dataframe.copy()
    for column in columns:
        non_blank = converted[column].astype(str).str.strip() != ""
        numeric = pd.to_numeric(converted[column], errors="coerce")
        invalid = converted.loc[non_blank & numeric.isna()]
        if not invalid.empty:
            rows = ", ".join(str(index + 2) for index in invalid.index[:10])
            errors.append(f"{label}.{column} has non-numeric values on row(s): {rows}")
        converted[column] = numeric
    return converted, errors


def validate():
    errors = []
    budgets = read_csv(DATA_DIR / "state_budgets.csv")
    sources = read_csv(DATA_DIR / "sources.csv")

    errors.extend(require_columns(budgets, STATE_BUDGET_COLUMNS, "state_budgets.csv"))
    errors.extend(require_columns(sources, SOURCE_COLUMNS, "sources.csv"))
    if errors:
        return errors

    budgets = budgets[STATE_BUDGET_COLUMNS].copy()
    sources = sources[SOURCE_COLUMNS].copy()

    budgets_numeric, numeric_errors = coerce_numeric(
        budgets, NUMERIC_COLUMNS, "state_budgets.csv"
    )
    sources_numeric, source_numeric_errors = coerce_numeric(
        sources, SOURCE_NUMERIC_COLUMNS, "sources.csv"
    )
    errors.extend(numeric_errors)
    errors.extend(source_numeric_errors)

    present_total = budgets_numeric["total_budget_ngn"].notna()
    non_positive_total = budgets_numeric.loc[
        present_total & (budgets_numeric["total_budget_ngn"] <= 0)
    ]
    if not non_positive_total.empty:
        rows = ", ".join(str(index + 2) for index in non_positive_total.index[:10])
        errors.append(f"total_budget_ngn must be positive where present. Row(s): {rows}")

    has_split = (
        budgets_numeric["capital_budget_ngn"].notna()
        & budgets_numeric["recurrent_budget_ngn"].notna()
        & budgets_numeric["total_budget_ngn"].notna()
    )
    split_delta = (
        budgets_numeric.loc[has_split, "capital_budget_ngn"]
        + budgets_numeric.loc[has_split, "recurrent_budget_ngn"]
        - budgets_numeric.loc[has_split, "total_budget_ngn"]
    ).abs()
    bad_split = split_delta[split_delta > TOLERANCE_NGN]
    if not bad_split.empty:
        rows = ", ".join(str(index + 2) for index in bad_split.index[:10])
        errors.append(
            "capital_budget_ngn + recurrent_budget_ngn must equal total_budget_ngn "
            f"within ₦{TOLERANCE_NGN:,}. Row(s): {rows}"
        )

    budget_source_ids = set(
        budgets["source_id"].astype(str).str.strip().replace("", pd.NA).dropna()
    )
    source_ids = set(
        sources["source_id"].astype(str).str.strip().replace("", pd.NA).dropna()
    )
    missing_sources = sorted(budget_source_ids - source_ids)
    if missing_sources:
        errors.append(
            "Every source_id in state_budgets.csv must exist in sources.csv. "
            f"Missing: {', '.join(missing_sources[:20])}"
        )

    duplicates = budgets[
        budgets.duplicated(subset=["state", "year", "budget_status"], keep=False)
    ]
    if not duplicates.empty:
        examples = duplicates[["state", "year", "budget_status"]].head(10)
        errors.append(
            "Duplicate state/year/budget_status rows found: "
            + examples.to_dict(orient="records").__repr__()
        )

    source_lookup = sources.set_index("source_id")["source_url"].to_dict()
    verified_rows = budgets[budgets["data_status"].astype(str).str.lower() == "verified"]
    missing_verified_source = []
    for index, row in verified_rows.iterrows():
        source_id = str(row["source_id"]).strip()
        source_url = str(source_lookup.get(source_id, "")).strip()
        if not source_id or source_id == "SRC_PENDING" or not source_url:
            missing_verified_source.append(str(index + 2))
    if missing_verified_source:
        errors.append(
            "Rows marked verified must have a non-pending source_id and source_url. "
            f"Row(s): {', '.join(missing_verified_source[:20])}"
        )

    placeholder_rows = budgets[
        budgets["data_status"].astype(str).str.lower() == "placeholder"
    ]
    bad_placeholder = placeholder_rows[
        placeholder_rows["budget_status"]
        .astype(str)
        .str.lower()
        .isin(["approved", "revised", "verified"])
    ]
    if not bad_placeholder.empty:
        rows = ", ".join(str(index + 2) for index in bad_placeholder.index[:10])
        errors.append(
            "Rows marked placeholder must not display as approved/verified. "
            f"Row(s): {rows}"
        )

    return errors


def main():
    errors = validate()
    if errors:
        print("Budget data validation failed:")
        for error in errors:
            print(f"- {error}")
        raise SystemExit(1)

    print("Budget data validation passed.")


if __name__ == "__main__":
    main()
