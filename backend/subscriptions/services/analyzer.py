FREQUENCY_MULTIPLIER = {
    "weekly": 52,
    "monthly": 12,
    "quarterly": 4,
    "yearly": 1,
}


MERCHANT_INFO = {

    "Netflix": {
        "category": "Entertainment",
        "type": "Streaming"
    },

    "Spotify": {
        "category": "Entertainment",
        "type": "Music"
    },

    "Amazon Prime": {
        "category": "Entertainment",
        "type": "Streaming"
    },

    "Adobe": {
        "category": "Software",
        "type": "SaaS"
    },

    "Canva": {
        "category": "Software",
        "type": "Design"
    },

    "Microsoft 365": {
        "category": "Software",
        "type": "Productivity"
    },

    "Google One": {
        "category": "Software",
        "type": "Cloud Storage"
    },

    "Amazon": {
        "category": "Shopping",
        "type": "E-commerce"
    },

    "Flipkart": {
        "category": "Shopping",
        "type": "E-commerce"
    },

    "Swiggy": {
        "category": "Food",
        "type": "Food Delivery"
    },

    "Zomato": {
        "category": "Food",
        "type": "Food Delivery"
    },

    "Uber": {
        "category": "Transport",
        "type": "Transport"
    },

    "Ola": {
        "category": "Transport",
        "type": "Transport"
    },

    "Dominos": {
        "category": "Food",
        "type": "Food Delivery"
    },
}


def analyze_subscriptions(subscriptions):

    results = []

    for subscription in subscriptions:

        merchant = subscription["merchant"]

        frequency = subscription["frequency"]

        amount = subscription["average_amount"]

        multiplier = FREQUENCY_MULTIPLIER.get(
            frequency,
            0
        )

        annual_cost = amount * multiplier

        monthly_cost = annual_cost / 12

        info = MERCHANT_INFO.get(
            merchant,
            {
                "category": "Other",
                "type": "Recurring Payment"
            }
        )

        results.append({

            **subscription,

            "category": info["category"],

            "type": info["type"],

            "monthly_cost": round(
                monthly_cost,
                2
            ),

            "annual_cost": round(
                annual_cost,
                2
            ),
        })

    return results