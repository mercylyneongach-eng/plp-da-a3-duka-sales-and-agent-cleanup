import pandas as pd

def clean_agent_data(txns, agents):
    """
    Clean mobile-money transaction data and merge agent information.

    Returns:
        clean_df: cleaned transaction DataFrame.
        log: DataFrame documenting data-quality issues and affected rows.
    """
    clean_df = txns.copy()
    log_entries = []

    duplicates = clean_df["txn_id"].duplicated().sum()
    clean_df = clean_df.drop_duplicates(
        subset="txn_id", keep="first"
    ).copy()

    log_entries.append({
        "issue": "Duplicate transaction IDs",
        "dimension": "Uniqueness",
        "column": "txn_id",
        "rows_affected": int(duplicates)
    })

    clean_df["txn_type"] = (
        clean_df["txn_type"].astype(str).str.strip().str.lower()
        .map({"deposit": "Deposit", "withdrawal": "Withdrawal"})
    )

    log_entries.append({
        "issue": "Invalid transaction types",
        "dimension": "Consistency",
        "column": "txn_type",
        "rows_affected": int(clean_df["txn_type"].isna().sum())
    })

    clean_df["amount"] = pd.to_numeric(
        clean_df["amount"], errors="coerce"
    )
    clean_df["amount_imputed"] = clean_df["amount"].isna()

    missing = int(clean_df["amount"].isna().sum())

    log_entries.append({
        "issue": "Missing or invalid amounts",
        "dimension": "Completeness",
        "column": "amount",
        "rows_affected": missing
    })

    clean_df["amount"] = clean_df["amount"].fillna(
        clean_df["amount"].median()
    )

    clean_df["txn_date"] = pd.to_datetime(
        clean_df["txn_date"], format="mixed", errors="coerce"
    )

    log_entries.append({
        "issue": "Invalid transaction dates",
        "dimension": "Validity",
        "column": "txn_date",
        "rows_affected": int(clean_df["txn_date"].isna().sum())
    })

    q1 = clean_df["amount"].quantile(0.25)
    q3 = clean_df["amount"].quantile(0.75)
    iqr = q3 - q1

    clean_df["is_outlier"] = (
        (clean_df["amount"] < q1 - 1.5 * iqr) |
        (clean_df["amount"] > q3 + 1.5 * iqr)
    )

    log_entries.append({
        "issue": "Outliers flagged",
        "dimension": "Accuracy",
        "column": "amount",
        "rows_affected": int(clean_df["is_outlier"].sum())
    })

    clean_df = clean_df.merge(
        agents[["agent_id", "county"]],
        on="agent_id",
        how="left"
    )

    unknown = int(clean_df["county"].isna().sum())

    log_entries.append({
        "issue": "Unknown agent IDs",
        "dimension": "Referential integrity",
        "column": "agent_id",
        "rows_affected": unknown
    })

    clean_df["county"] = clean_df["county"].fillna("Unknown")

    log = pd.DataFrame(log_entries)

    return clean_df, log
