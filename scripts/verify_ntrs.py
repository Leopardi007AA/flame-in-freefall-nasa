"""Controlla gli articoli di data/papers.json sull'API ufficiale NTRS e cerca i valori sperimentali.

Uso (dalla cartella del progetto, con l'ambiente attivo, rete aperta):
    pip install pypdf          # solo per leggere i PDF
    python scripts/verify_ntrs.py

Scrive data/ntrs_check.json e un riepilogo in data/ntrs_check.md. NON modifica il CSV:
le frasi trovate vanno lette e, se giuste, copiate a mano in investigations.csv con la citazione.
"""
import io
import json
import sys
import time
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from src.ntrs_tools import candidate_sentences, find_doi, find_pdf_path  # noqa: E402

BASE = "https://ntrs.nasa.gov"


def pdf_text(url: str, max_pages: int = 25) -> str:
    try:
        from pypdf import PdfReader
    except ImportError:
        return ""
    try:
        r = requests.get(url, timeout=60)
        r.raise_for_status()
        reader = PdfReader(io.BytesIO(r.content))
        return " ".join((p.extract_text() or "") for p in reader.pages[:max_pages])
    except Exception as e:
        print(f"   PDF non letto: {type(e).__name__}")
        return ""


def main() -> int:
    papers = json.loads((ROOT / "data" / "papers.json").read_text(encoding="utf-8"))
    seen, results = set(), []
    for p in papers:
        nid = p.get("ntrs_id")
        if not nid or nid in seen:
            continue
        seen.add(nid)
        print(f"{p.get('psi_id')} {p.get('esperimento')} - NTRS {nid}")
        try:
            r = requests.get(f"{BASE}/api/citations/{nid}", timeout=30)
            r.raise_for_status()
            rec = r.json()
        except Exception as e:
            print(f"   ERRORE: {type(e).__name__}: {str(e)[:120]}")
            results.append({"psi_id": p.get("psi_id"), "ntrs_id": nid, "errore": str(e)[:200]})
            continue
        pdf = find_pdf_path(rec)
        text = pdf_text(BASE + pdf) if pdf else ""
        results.append({
            "psi_id": p.get("psi_id"), "esperimento": p.get("esperimento"), "ntrs_id": nid,
            "titolo_api": rec.get("title"), "titolo_papers": p.get("titolo"),
            "titolo_coincide": (rec.get("title") or "").strip().lower() == (p.get("titolo") or "").strip().lower(),
            "doi_api": find_doi(rec), "data": rec.get("distributionDate") or rec.get("created") or "",
            "pdf": BASE + pdf if pdf else "", "frasi_candidate": candidate_sentences(text),
        })
        time.sleep(0.5)
    (ROOT / "data" / "ntrs_check.json").write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    lines = ["# Controllo NTRS (generato da scripts/verify_ntrs.py)", "",
             "Le frasi sono CANDIDATE: vanno lette sul PDF prima di usarle.", ""]
    for x in results:
        lines += [f"## {x.get('psi_id')} {x.get('esperimento', '')} - NTRS {x['ntrs_id']}",
                  f"- Titolo (API): {x.get('titolo_api', x.get('errore'))}",
                  f"- DOI (API): {x.get('doi_api') or 'non presente nel record'}",
                  f"- Data: {x.get('data', '')}", f"- PDF: {x.get('pdf') or 'non trovato'}"]
        lines += [f"  - \"{s}\"" for s in x.get("frasi_candidate", [])]
        lines.append("")
    (ROOT / "data" / "ntrs_check.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"\nFatto: {len(results)} articoli. Apri data/ntrs_check.md.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
