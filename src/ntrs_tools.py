"""Functions to read NTRS records and find sentences with experimental values.

They never write to the CSV: they only produce candidates to be checked by hand.
"""
import re

DOI_RE = re.compile(r"10\.\d{4,9}/[^\s\"'<>\\]+")
KEY_RE = re.compile(
    r"(\d+(?:\.\d+)?\s?%\s?(?:by\s+volume\s+)?(?:O2|O_2|oxygen)"
    r"|(?:O2|oxygen)[^.]{0,80}\d"
    r"|\d+(?:\.\d+)?\s?(?:atm|psia|psi|kPa|bar)\b"
    r"|\d+(?:\.\d+)?\s?cm/?\s?s\b)", re.IGNORECASE)


def find_doi(record: dict) -> str:
    """First DOI found in the record (identifier field, otherwise a search in the text)."""
    for ident in record.get("identifier", []) or []:
        if isinstance(ident, dict) and str(ident.get("type", "")).upper() == "DOI":
            return str(ident.get("value", "")).strip()
    m = DOI_RE.search(str(record.get("identifier", "")) + str(record.get("publications", "")))
    return m.group(0).rstrip(".,;)") if m else ""


def find_pdf_path(record: dict) -> str:
    """Path of the PDF in the record's downloads, or an empty string."""
    m = re.search(r"(/api/citations/\d+/downloads/[^\"'\s]+?\.pdf)", str(record.get("downloads", "")))
    return m.group(1) if m else ""


def candidate_sentences(text: str, limit: int = 12) -> list[str]:
    """Sentences that mention oxygen, pressure or flow velocity (to be checked by hand)."""
    flat = re.sub(r"\s+", " ", text)
    out = []
    for s in re.split(r"(?<=[.!?])\s+", flat):
        if 20 <= len(s) <= 400 and KEY_RE.search(s) and s not in out:
            out.append(s)
        if len(out) >= limit:
            break
    return out
