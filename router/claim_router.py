def route_claim(fields: dict, missing_fields: list) -> tuple:
    description = (fields.get("description") or "").lower()
    estimated_damage = fields.get("estimatedDamage")

    if missing_fields:
        return "Manual Review", "Mandatory fields are missing"

    if any(word in description for word in ["fraud", "staged", "inconsistent"]):
        return "Investigation Flag", "Suspicious keywords found in description"

    if fields.get("claimType") == "injury":
        return "Specialist Queue", "Injury-related claim requires specialist handling"

    if estimated_damage is not None and estimated_damage < 25000:
        return "Fast-track", "Low estimated damage eligible for fast-track"

    return "Standard Processing", "Default routing applied"
