import pandas as pd


def load_transactions(file_path):
    df = pd.read_csv(file_path)

    
    df.columns = [str(col).strip().lower() for col in df.columns]

    if {"date", "description", "amount"}.issubset(df.columns):

        result = df[["date", "description", "amount"]].copy()

        result["date"] = pd.to_datetime(
            result["date"],
            dayfirst=True,
            errors="coerce"
        )

        result["amount"] = pd.to_numeric(
            result["amount"],
            errors="coerce"
        )

    # ---------------------------------------------------------
    # FORMAT 2: Bank statement
    # date, DrCr, amount, balance, mode, name, ...
    # ---------------------------------------------------------
    elif {"date", "drcr", "amount", "name"}.issubset(df.columns):

        # Keep only debit transactions
        result = df[
            df["drcr"]
            .astype(str)
            .str.strip()
            .str.lower()
            .isin(["db", "debit", "dr"])
        ].copy()

        result = result[["date", "name", "amount"]]

        result.rename(
            columns={"name": "description"},
            inplace=True
        )

        result["date"] = pd.to_datetime(
            result["date"],
            dayfirst=True,
            errors="coerce"
        )

        result["amount"] = pd.to_numeric(
            result["amount"],
            errors="coerce"
        )

    else:
        raise ValueError(
            "Unsupported CSV format. Required columns: "
            "date, description, amount OR "
            "date, DrCr, amount, name"
        )

    # Remove invalid transactions
    result.dropna(
        subset=["date", "description", "amount"],
        inplace=True
    )

    # Ignore zero/negative amounts
    result = result[result["amount"] > 0]

    # Clean description
    result["description"] = (
        result["description"]
        .astype(str)
        .str.strip()
    )

    # Sort by date
    result.sort_values("date", inplace=True)

    # Reset index
    result.reset_index(drop=True, inplace=True)

    return result