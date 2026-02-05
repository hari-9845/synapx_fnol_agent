import re
import pdfplumber

def extract_text(pdf_path: str) -> str:
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text


def extract_fields(text: str) -> dict:
    fields = {}

    def find(pattern):
        match = re.search(pattern, text, re.IGNORECASE)
        return match.group(1).strip() if match else None

    # Policy Info
    fields["policyNumber"] = find(r"Policy Number[:\-]\s*(.+)")
    fields["policyholderName"] = find(r"Policyholder Name[:\-]\s*(.+)")
    fields["effectiveDates"] = find(r"Effective Dates?[:\-]\s*(.+)")

    # Incident Info
    fields["incidentDate"] = find(r"Incident Date[:\-]\s*(.+)")
    fields["incidentTime"] = find(r"Incident Time[:\-]\s*(.+)")
    fields["incidentLocation"] = find(r"Location[:\-]\s*(.+)")
    fields["incidentDescription"] = find(r"Description[:\-]\s*(.+)")

    # Involved Parties
    fields["claimantName"] = find(r"Claimant[:\-]\s*(.+)")
    fields["thirdParties"] = find(r"Third Parties?[:\-]\s*(.+)")
    fields["contactDetails"] = find(r"Contact[:\-]\s*(.+)")

    # Asset Details
    fields["assetType"] = find(r"Asset Type[:\-]\s*(.+)")
    fields["assetId"] = find(r"Asset ID[:\-]\s*(.+)")

    damage = find(r"Estimated Damage[:\-]\s*₹?([\d,]+)")
    fields["estimatedDamage"] = int(damage.replace(",", "")) if damage else None

    # Mandatory Fields
    fields["claimType"] = find(r"Claim Type[:\-]\s*(.+)")
    fields["attachments"] = find(r"Attachments?[:\-]\s*(.+)")
    fields["initialEstimate"] = fields["estimatedDamage"]

    return fields


def find_missing_fields(fields: dict) -> list:
    mandatory = [
        "policyNumber",
        "incidentDate",
        "incidentDescription",
        "claimType",
        "estimatedDamage"
    ]
    return [f for f in mandatory if not fields.get(f)]
