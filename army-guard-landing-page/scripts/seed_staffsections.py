"""Seed the 6 staff section tiles for the landing page.

Based on the customer's reference photo:
  COS              (Chief of Staff)
  G1               Personnel
  G2/G6/IA/ADS     Intelligence / Communication
  G3/G5/G5         Operations
  G4/G9            Logistics / Installation
  G8               Financial / Resource Mgmt

Idempotent — checks for existing rows by arng_code before creating.
"""
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from auth import get_credential, load_env  # noqa: E402

from PowerPlatform.Dataverse.client import DataverseClient  # noqa: E402

# Hex color matching the dark-blue tiles in the reference photo
TILE_COLOR = "#1F4E79"

SECTIONS = [
    {"arng_code": "COS",          "arng_name": "COS",                             "arng_displayorder": 1, "arng_color": TILE_COLOR},
    {"arng_code": "G1",           "arng_name": "G1 Personnel",                    "arng_displayorder": 2, "arng_color": TILE_COLOR},
    {"arng_code": "G2/G6/IA/ADS", "arng_name": "G2/G6/IA/ADS Intelligence / Communication", "arng_displayorder": 3, "arng_color": TILE_COLOR},
    {"arng_code": "G3/G5/G5",     "arng_name": "G3/G5/G5 Operations",             "arng_displayorder": 4, "arng_color": TILE_COLOR},
    {"arng_code": "G4/G9",        "arng_name": "G4/G9 Logistics / Installation",  "arng_displayorder": 5, "arng_color": TILE_COLOR},
    {"arng_code": "G8",           "arng_name": "G8 Financial / Resource Mgmt",    "arng_displayorder": 6, "arng_color": TILE_COLOR},
]


def main():
    load_env()
    client = DataverseClient(os.environ["DATAVERSE_URL"], get_credential())

    # Get existing codes to avoid duplicates
    existing_codes = set()
    pages = client.records.get(
        "arng_staffsection",
        select=["arng_code"],
        top=100,
    )
    for page in pages:
        for r in page:
            if r.get("arng_code"):
                existing_codes.add(r["arng_code"])

    print(f"Found {len(existing_codes)} existing staff sections: {sorted(existing_codes)}", flush=True)

    to_create = [s for s in SECTIONS if s["arng_code"] not in existing_codes]
    if not to_create:
        print("All 6 staff sections already present — nothing to do.", flush=True)
        return

    print(f"Creating {len(to_create)} new staff sections...", flush=True)
    guids = client.records.create("arng_staffsection", to_create)
    for section, guid in zip(to_create, guids):
        print(f"  [CREATE] {section['arng_code']:<14} -> {guid}", flush=True)

    print("", flush=True)
    print("DONE.", flush=True)


if __name__ == "__main__":
    main()
