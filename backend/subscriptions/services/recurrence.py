import pandas as pd


FREQUENCY_RANGES = {
    "weekly": (5, 9),
    "monthly": (25, 35),
    "quarterly": (80, 100),
    "yearly": (330, 400),
}


def detect_frequency_from_intervals(intervals):
    """
    Determine the most common recurring frequency.
    """

    if not intervals:
        return None, 0

    frequency_scores = {}

    for frequency, (minimum, maximum) in FREQUENCY_RANGES.items():

        matches = [
            days
            for days in intervals
            if minimum <= days <= maximum
        ]

        frequency_scores[frequency] = len(matches)

    best_frequency = max(
        frequency_scores,
        key=frequency_scores.get
    )

    best_matches = frequency_scores[best_frequency]

    if best_matches == 0:
        return None, 0

    confidence = (
        best_matches / len(intervals)
    ) * 100

    return best_frequency, round(confidence)


def detect_recurring(df):

    subscriptions = []

    if df.empty:
        return subscriptions

    grouped = df.groupby("merchant")

    for merchant, group in grouped:

        # At least 3 transactions
        if len(group) < 2:
            continue

        group = group.sort_values("date").copy()

        # Remove duplicate transactions on same day
        group = group.drop_duplicates(
            subset=["date", "amount"]
        )

        if len(group) < 3:
            continue

        dates = pd.to_datetime(group["date"])

        intervals = (
            dates.diff()
            .dt.days
            .dropna()
            .tolist()
        )

        if len(intervals) < 2:
            continue

        frequency, confidence = detect_frequency_from_intervals(
            intervals
        )

        if not frequency:
            continue

        # Require reasonable confidence
        if confidence < 40:
            continue

        amounts = group["amount"].astype(float)

        average_amount = amounts.mean()

        # Check price consistency
        amount_std = amounts.std()

        if pd.isna(amount_std):
            amount_std = 0

        # Price stability score
        if average_amount == 0:
            price_score = 0
        else:
            variation = (
                amount_std / average_amount
            ) * 100

            price_score = max(
                0,
                100 - variation
            )

        # Combined confidence
        final_confidence = round(
            (confidence * 0.7) +
            (price_score * 0.3)
        )

        subscriptions.append({

            "merchant": merchant,

            "frequency": frequency,

            "average_amount": round(
                float(average_amount),
                2
            ),

            "latest_amount": round(
                float(amounts.iloc[-1]),
                2
            ),

            "average_interval_days": round(
                sum(intervals) / len(intervals),
                1
            ),

            "transaction_count": len(group),

            "confidence": final_confidence,

            "price_changed": (
                len(set(amounts)) > 1
            ),
        })

    # Highest confidence first
    subscriptions.sort(
        key=lambda x: x["confidence"],
        reverse=True
    )

    return subscriptions