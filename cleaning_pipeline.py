import pandas as pd

def clean_agent_data(txns, agents):
    clean_df = txns.drop_duplicates(subset="txn_id").copy()

    clean_df["txn_type"] = (
        clean_df["txn_type"].astype(str).str.strip().str.lower()
        .map({"deposit": "Deposit", "withdrawal": "Withdrawal"})
    )

    clean_df["amount"] = pd.to_numeric(
        clean_df["amount"], errors="coerce"
    )
    clean_df["amount"] = clean_df["amount"].fillna(
        clean_df["amount"].median()
    )

    clean_df["txn_date"] = pd.to_datetime(
        clean_df["txn_date"], format="mixed", errors="coerce"
    )

    q1 = clean_df["amount"].quantile(0.25)
    q3 = clean_df["amount"].quantile(0.75)
    iqr = q3 - q1

    clean_df["is_outlier"] = (
        (clean_df["amount"] < q1 - 1.5 * iqr) |
        (clean_df["amount"] > q3 + 1.5 * iqr)
    )

    clean_df = clean_df.merge(
        agents[["agent_id", "county"]],
        on="agent_id",
        how="left"
    )

    clean_df["county"] = clean_df["county"].fillna("Unknown")

    return clean_df
