from extractor.fnol_extractor import extract_text, extract_fields, find_missing_fields


def route_claim(fields: dict, missing_fields: list):
    """
    Decide claim routing based on Synapx rules
    """
    description = (fields.get("incidentDescription") or "").lower()
    damage = fields.get("estimatedDamage")
    claim_type = (fields.get("claimType") or "").lower()

    # Rule 1: Missing mandatory fields
    if missing_fields:
        return (
            "Manual Review",
            "Mandatory fields are missing: " + ", ".join(missing_fields)
        )

    # Rule 2: Fraud indicators
    fraud_keywords = ["fraud", "staged", "inconsistent"]
    if any(word in description for word in fraud_keywords):
        return (
            "Investigation Flag",
            "Suspicious keywords detected in incident description"
        )

    # Rule 3: Injury claims
    if claim_type == "injury":
        return (
            "Specialist Queue",
            "Injury-related claims require specialist handling"
        )

    # Rule 4: Fast-track low value claims
    if damage is not None and damage < 25000:
        return (
            "Fast-track",
            "Estimated damage is below ₹25,000"
        )

    # Default fallback
    return (
        "Manual Review",
        "Claim does not meet fast-track criteria"
    )


def process_claim(pdf_path: str) -> dict:
    """
    End-to-end FNOL claim processing
    """
    # 1. Extract text
    text = extract_text(pdf_path)

    # 2. Extract fields
    extracted_fields = extract_fields(text)

    # 3. Find missing fields
    missing_fields = find_missing_fields(extracted_fields)

    # 4. Route claim
    route, reason = route_claim(extracted_fields, missing_fields)

    # 5. Final structured output
    return {
        "extractedFields": extracted_fields,
        "missingFields": missing_fields,
        "recommendedRoute": route,
        "reasoning": reason
    }


# For direct local testing (without FastAPI)
if __name__ == "__main__":
    sample_pdf = "data/sample_fnol.pdf"
    result = process_claim(sample_pdf)
    print(result)
