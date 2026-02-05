import re

def extract_fields(text: str) -> dict:
    fields = {}

    def find(pattern):
        match = re.search(pattern, text, re.IGNORECASE)
        return match.group(1).strip() if match else None

    fields["policyNumber"] = find(r"POLICY NUMBER[:\s]*([A-Z0-9\-]+)")
    fields["policyHolder"] = find(r"NAME OF INSURED.*?\n([A-Za-z ]+)")
    fields["dateOfLoss"] = find(r"DATE OF LOSS[:\s]*([0-9/]+)")
    fields["timeOfLoss"] = find(r"TIME.*?(AM|PM)")
    fields["location"] = find(r"LOCATION OF LOSS.*?\n(.+)")
    fields["description"] = find(r"DESCRIPTION OF ACCIDENT.*?\n(.+)")
    fields["claimant"] = find(r"DRIVER'S NAME AND ADDRESS.*?\n([A-Za-z ]+)")
    fields["assetType"] = "Vehicle" if "VEHICLE" in text.upper() else None
    fields["assetId"] = find(r"V\.I\.N[:\s]*([A-Z0-9]+)")
    
    damage = find(r"ESTIMATE AMOUNT[:\s]*\$?([0-9,]+)")
    fields["estimatedDamage"] = int(damage.replace(",", "")) if damage else None

    fields["claimType"] = "injury" if "INJURED" in text.upper() else "property"

    return fields
