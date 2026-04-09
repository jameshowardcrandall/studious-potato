"""Seed sample products and productlinks so the landing canvas app has data to display.

Creates 2 products per staff section (12 total) with 3 links each (36 total).
URLs are realistic placeholders on example.com so they're obviously swappable.
Idempotent: checks if rows already exist before inserting.
"""
import json
import os
import sys
import urllib.parse
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from auth import get_token, load_env  # noqa: E402

# Link type choice values (from arng_linktype OptionSet)
LT_DASHBOARD = 100000000
LT_MODEL_DRIVEN = 100000001
LT_CANVAS = 100000002

# section_code -> list of products.
# Each product is (name, description, [(link_name, link_type, url, sort), ...])
SAMPLE = {
    "COS": [
        ("Executive Dashboard", "Top-level KPIs and org health", [
            ("Dashboard", LT_DASHBOARD, "https://example.com/cos/exec-dashboard", 1),
            ("Open in MDA", LT_MODEL_DRIVEN, "https://example.com/cos/exec-mda", 2),
            ("Canvas App", LT_CANVAS, "https://example.com/cos/exec-canvas", 3),
        ]),
        ("Staff Directory", "Chief of Staff rosters and contacts", [
            ("Dashboard", LT_DASHBOARD, "https://example.com/cos/staff-dashboard", 1),
            ("Open in MDA", LT_MODEL_DRIVEN, "https://example.com/cos/staff-mda", 2),
            ("Canvas App", LT_CANVAS, "https://example.com/cos/staff-canvas", 3),
        ]),
    ],
    "G1": [
        ("Recruiting System", "Candidate pipeline and enlistment tracking", [
            ("Dashboard", LT_DASHBOARD, "https://example.com/g1/recruiting-dashboard", 1),
            ("Open in MDA", LT_MODEL_DRIVEN, "https://example.com/g1/recruiting-mda", 2),
            ("Canvas App", LT_CANVAS, "https://example.com/g1/recruiting-canvas", 3),
        ]),
        ("Strength Management", "Unit strength and personnel readiness", [
            ("Dashboard", LT_DASHBOARD, "https://example.com/g1/strength-dashboard", 1),
            ("Open in MDA", LT_MODEL_DRIVEN, "https://example.com/g1/strength-mda", 2),
            ("Canvas App", LT_CANVAS, "https://example.com/g1/strength-canvas", 3),
        ]),
    ],
    "G2/G6/IA/ADS": [
        ("Intelligence Portal", "Classified info sharing workspace", [
            ("Dashboard", LT_DASHBOARD, "https://example.com/g2/intel-dashboard", 1),
            ("Open in MDA", LT_MODEL_DRIVEN, "https://example.com/g2/intel-mda", 2),
            ("Canvas App", LT_CANVAS, "https://example.com/g2/intel-canvas", 3),
        ]),
        ("Network Operations", "Network health, tickets, and incidents", [
            ("Dashboard", LT_DASHBOARD, "https://example.com/g6/netops-dashboard", 1),
            ("Open in MDA", LT_MODEL_DRIVEN, "https://example.com/g6/netops-mda", 2),
            ("Canvas App", LT_CANVAS, "https://example.com/g6/netops-canvas", 3),
        ]),
    ],
    "G3/G5/G5": [
        ("Training Management", "Unit training schedules and completion", [
            ("Dashboard", LT_DASHBOARD, "https://example.com/g3/training-dashboard", 1),
            ("Open in MDA", LT_MODEL_DRIVEN, "https://example.com/g3/training-mda", 2),
            ("Canvas App", LT_CANVAS, "https://example.com/g3/training-canvas", 3),
        ]),
        ("Readiness Tracker", "Operational readiness across units", [
            ("Dashboard", LT_DASHBOARD, "https://example.com/g3/readiness-dashboard", 1),
            ("Open in MDA", LT_MODEL_DRIVEN, "https://example.com/g3/readiness-mda", 2),
            ("Canvas App", LT_CANVAS, "https://example.com/g3/readiness-canvas", 3),
        ]),
    ],
    "G4/G9": [
        ("Supply Chain", "Equipment, ammunition, and supplies", [
            ("Dashboard", LT_DASHBOARD, "https://example.com/g4/supply-dashboard", 1),
            ("Open in MDA", LT_MODEL_DRIVEN, "https://example.com/g4/supply-mda", 2),
            ("Canvas App", LT_CANVAS, "https://example.com/g4/supply-canvas", 3),
        ]),
        ("Installation Management", "Base operations and facility mgmt", [
            ("Dashboard", LT_DASHBOARD, "https://example.com/g9/installations-dashboard", 1),
            ("Open in MDA", LT_MODEL_DRIVEN, "https://example.com/g9/installations-mda", 2),
            ("Canvas App", LT_CANVAS, "https://example.com/g9/installations-canvas", 3),
        ]),
    ],
    "G8": [
        ("Budget Portal", "Budget execution and fund tracking", [
            ("Dashboard", LT_DASHBOARD, "https://example.com/g8/budget-dashboard", 1),
            ("Open in MDA", LT_MODEL_DRIVEN, "https://example.com/g8/budget-mda", 2),
            ("Canvas App", LT_CANVAS, "https://example.com/g8/budget-canvas", 3),
        ]),
        ("Contract Management", "Contracts and procurement", [
            ("Dashboard", LT_DASHBOARD, "https://example.com/g8/contracts-dashboard", 1),
            ("Open in MDA", LT_MODEL_DRIVEN, "https://example.com/g8/contracts-mda", 2),
            ("Canvas App", LT_CANVAS, "https://example.com/g8/contracts-canvas", 3),
        ]),
    ],
}


def _req(env, token, method, path, body=None):
    url = f"{env}/api/data/v9.2/{path}"
    data = json.dumps(body).encode() if body is not None else None
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
        "OData-MaxVersion": "4.0",
        "OData-Version": "4.0",
        "Content-Type": "application/json",
        "Prefer": "return=representation",
    }
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    with urllib.request.urlopen(req) as resp:
        body_text = resp.read().decode() or "{}"
        return json.loads(body_text) if body_text.strip() else {}


def get_section_map(env, token):
    """Return {arng_code: arng_staffsectionid} for all staff sections."""
    q = "arng_staffsections?$select=arng_code,arng_staffsectionid"
    res = _req(env, token, "GET", q)
    return {r["arng_code"]: r["arng_staffsectionid"] for r in res["value"]}


def get_existing_products(env, token):
    """Return set of existing product names to avoid duplicates."""
    q = "arng_products?$select=arng_name"
    res = _req(env, token, "GET", q)
    return {r["arng_name"] for r in res["value"]}


def main():
    load_env()
    token = get_token()
    env = os.environ["DATAVERSE_URL"].rstrip("/")
    solution_name = os.environ.get("SOLUTION_NAME", "")

    print(f"Target env: {env}", flush=True)
    print(f"Solution:   {solution_name}", flush=True)

    section_map = get_section_map(env, token)
    print(f"\nFound {len(section_map)} staff sections: {list(section_map.keys())}", flush=True)

    existing_products = get_existing_products(env, token)
    if existing_products:
        print(f"Already have products: {existing_products}", flush=True)

    products_created = 0
    links_created = 0

    for section_code, products in SAMPLE.items():
        section_id = section_map.get(section_code)
        if not section_id:
            print(f"  ! skipping {section_code} — section not found", flush=True)
            continue

        print(f"\n[{section_code}]", flush=True)
        for product_name, description, links in products:
            if product_name in existing_products:
                print(f"  = {product_name} (already exists, skipping)", flush=True)
                continue

            product_body = {
                "arng_name": product_name,
                "arng_description": description,
                "arng_SectionId@odata.bind": f"/arng_staffsections({section_id})",
            }
            created = _req(env, token, "POST", "arng_products", product_body)
            product_id = created["arng_productid"]
            products_created += 1
            print(f"  + {product_name} -> {product_id}", flush=True)

            for link_name, link_type, url, sort in links:
                link_body = {
                    "arng_name": link_name,
                    "arng_linktype": link_type,
                    "arng_url": url,
                    "arng_displayorder": sort,
                    "arng_ProductId@odata.bind": f"/arng_products({product_id})",
                }
                _req(env, token, "POST", "arng_productlinks", link_body)
                links_created += 1
                print(f"      + {link_name} ({url})", flush=True)

    print(
        f"\nDone. Created {products_created} products and {links_created} links.",
        flush=True,
    )


if __name__ == "__main__":
    main()
