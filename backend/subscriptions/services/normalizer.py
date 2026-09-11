import re


MERCHANT_ALIASES = {

    # Entertainment
    "netflix": "Netflix",
    "spotify": "Spotify",
    "prime video": "Amazon Prime",
    "amazon prime": "Amazon Prime",

    # Software
    "adobe": "Adobe",
    "canva": "Canva",
    "microsoft 365": "Microsoft 365",
    "office 365": "Microsoft 365",

    # Cloud
    "google one": "Google One",

    # Shopping
    "amazon": "Amazon",
    "flipkart": "Flipkart",

    # Food
    "swiggy": "Swiggy",
    "zomato": "Zomato",
    "dominos": "Dominos",

    # Transport
    "uber": "Uber",
    "ola": "Ola",
}


# These are payment methods/banks,
# not actual merchants.
IGNORE_MERCHANTS = {
    "phonepe",
    "paytm",
    "googlepay",
    "gpay",
    "hdfcbank",
    "statebank",
    "sbi",
}


def normalize_merchant(description):

    if not description:
        return "Unknown"

    text = str(description).lower().strip()

    # Check ignored payment providers
    for item in IGNORE_MERCHANTS:

        if item in text:
            return "Other"

    # Known merchant matching
    for keyword, merchant in MERCHANT_ALIASES.items():

        if keyword in text:
            return merchant

    # Remove UPI/card prefixes
    text = re.sub(
        r"^(upi|pos|card|debit card)[/\-\s]*",
        "",
        text
    )

    # Remove special characters
    text = re.sub(
        r"[^a-zA-Z0-9\s]",
        " ",
        text
    )

    # Remove extra spaces
    text = re.sub(
        r"\s+",
        " ",
        text
    ).strip()

    if not text:
        return "Other"

    return text.title()