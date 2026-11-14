# scripts/fetch_ntrs.py
import json
import time
import requests

URL = "https://ntrs.nasa.gov/api/citations/search"

# Generiamo le query in modo dinamico per tutte le 20 investigazioni del nostro CSV
INVESTIGATIONS = [
    ("PSI-25", "BASS-II", "BASS-II microgravity solid fuel flammability"),
    ("PSI-26", "BASS", "BASS microgravity combustion cotton fiberglass"),
    ("PSI-69", "FLEX", "FLEX flame extinguishment experiment droplet"),
    ("PSI-68", "FLEX-2", "FLEX-2 droplet combustion microgravity"),
    ("PSI-39", "CFI", "Cool Flames Investigation droplet high pressure MDCA"),
    ("PSI-20", "ACME BRE", "ACME burner quiescent flammability microgravity"),
    ("PSI-21", "ACME CLD Flame", "ACME coflow laminar diffusion flame soot"),
    ("PSI-22", "ACME E-FIELD", "ACME electric fields laminar diffusion flames"),
    ("PSI-23", "ACME s-Flame", "ACME spherical diffusion flame porous burner"),
    ("PSI-10", "ACME Flame Design", "ACME flame design soot limits microgravity"),
    ("PSI-159", "ACME CFI-G", "ACME gaseous cool flames propane butane"),
    ("PSI-98", "Saffire-I", "Saffire large scale spacecraft fire experiment Cygnus"),
    ("PSI-99", "Saffire-II", "Saffire II spacecraft fire experiment Cygnus"),
    ("PSI-100", "Saffire-III", "Saffire III spacecraft fire experiment Cygnus"),
    ("PSI-102", "SAME", "Spacecraft Aerosol Measurement Equipment smoke"),
    ("PSI-101", "SAME-R", "SAME repeat smoke aerosol measurement Pyrell"),
    ("PSI-107", "SPICE", "SPICE coflow smoke point microgravity"),
    ("PSI-106", "SLICE", "Structure and Lift-Off in Combustion Experiment SLICE"),
    ("PSI-47", "DAFT", "Dust and Aerosol Measurement Feasibility Test P-Trak"),
    ("PSI-142", "Fiamme fredde", "counterflow cool flames extinction oxygen stretch")
]

def search(q, size=5):
    try:
        r = requests.post(URL, json={"q": q, "page": {"size": size, "from": 0}}, timeout=30)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print(f"Errore nella ricerca per '{q}': {e}")
        return {}

out = []
for psi_id, name, query_str in INVESTIGATIONS:
    print(f"Cerco pubblicazioni per {psi_id} - {name}...")
    data = search(query_str)
    for item in data.get("results", []):
        doi = None
        for id_obj in item.get("identifier", []):
            if isinstance(id_obj, dict) and id_obj.get("type") == "DOI":
                doi = id_obj.get("value")
            elif isinstance(id_obj, str) and "10." in id_obj:
                doi = id_obj
                
        out.append({
            "psi_id": psi_id,
            "esperimento": name,
            "ntrs_id": item.get("id"),
            "titolo": item.get("title"),
            "abstract": item.get("abstract"),
            "url": f"https://ntrs.nasa.gov/citations/{item.get('id')}",
            "doi": doi,
            "da_controllare": True
        })
    time.sleep(0.5)

with open("data/papers.json", "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=2)

print(f"Salvati {len(out)} record in data/papers.json con successo per tutte le investigazioni!")