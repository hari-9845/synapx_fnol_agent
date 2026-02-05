from extractor.pdf_reader import extract_text_from_pdf
from extractor.field_extractor import extract_fields
from validator.field_validator import find_missing_fields
from router.claim_router import route_claim

def process_claim(file_path: str) -> dict:
    text = extract_text_from_pdf(file_path)
    fields = extract_fields(text)
    missing_fields = find_missing_fields(fields)
    route, reason = route_claim(fields, missing_fields)

    return {
        "extractedFields": fields,
        "missingFields": missing_fields,
        "recommendedRoute": route,
        "reasoning": reason
    }

if __name__ == "__main__":
    result = process_claim("data/sample_fnol.pdf")
    print(result)
