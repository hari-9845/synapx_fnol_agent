MANDATORY_FIELDS = [
    "policyNumber",
    "policyHolder",
    "dateOfLoss",
    "location",
    "claimType"
]

def find_missing_fields(fields: dict) -> list:
    missing = []
    for field in MANDATORY_FIELDS:
        if not fields.get(field):
            missing.append(field)
    return missing
