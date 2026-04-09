"""Re-add the 3 tables to ArmyGuardLandingPage solution with AddRequiredComponents=True.

This ensures every column of each table is included in the solution on next export.
Uses the AddSolutionComponent unbound action (Web API).

Idempotent — AddSolutionComponent is a no-op if the component is already present.
"""
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from auth import get_token, load_env  # noqa: E402

SOLUTION = "ArmyGuardLandingPage"
TABLES = ["arng_staffsection", "arng_product", "arng_productlink"]

# Component type 1 = Entity (Table)
COMPONENT_TYPE_ENTITY = 1


def get_metadata_id(env, token, logical_name):
    """Fetch MetadataId of a table."""
    url = (
        f"{env}/api/data/v9.2/EntityDefinitions(LogicalName='{logical_name}')"
        "?$select=MetadataId"
    )
    req = urllib.request.Request(
        url,
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/json",
            "OData-MaxVersion": "4.0",
            "OData-Version": "4.0",
        },
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())["MetadataId"]


def add_component(env, token, component_id, component_type):
    body = json.dumps({
        "ComponentId": component_id,
        "ComponentType": component_type,
        "SolutionUniqueName": SOLUTION,
        "AddRequiredComponents": True,
        "DoNotIncludeSubcomponents": False,
    }).encode()
    req = urllib.request.Request(
        f"{env}/api/data/v9.2/AddSolutionComponent",
        data=body,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "OData-MaxVersion": "4.0",
            "OData-Version": "4.0",
            "Accept": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req) as resp:
            return resp.status
    except urllib.error.HTTPError as e:
        msg = e.read().decode()
        raise RuntimeError(f"HTTP {e.code}: {msg}") from None


def main():
    load_env()
    token = get_token()
    env = os.environ["DATAVERSE_URL"].rstrip("/")

    for table in TABLES:
        print(f"[{table}] fetching metadata id...", flush=True)
        mid = get_metadata_id(env, token, table)
        print(f"  MetadataId: {mid}", flush=True)

        print(f"  Adding to solution '{SOLUTION}' (with subcomponents)...", flush=True)
        try:
            status = add_component(env, token, mid, COMPONENT_TYPE_ENTITY)
            print(f"  [OK] status={status}", flush=True)
        except Exception as e:
            print(f"  [ERR] {e}", flush=True)


if __name__ == "__main__":
    main()
