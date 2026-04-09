"""Verify the 3 Army Guard tables and list their columns via Web API.

SDK b7 doesn't expose a get_columns helper, so we use EntityDefinitions directly.
"""
import json
import os
import sys
import urllib.parse
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from auth import get_token, load_env  # noqa: E402

TABLES = ["arng_staffsection", "arng_product", "arng_productlink"]


def fetch(url, token):
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
        return json.loads(resp.read())


def main():
    load_env()
    token = get_token()
    env = os.environ["DATAVERSE_URL"].rstrip("/")

    for table in TABLES:
        print(f"=== {table} ===", flush=True)
        # Get table metadata
        url = (
            f"{env}/api/data/v9.2/EntityDefinitions(LogicalName='{table}')"
            "?$select=LogicalName,SchemaName,EntitySetName,MetadataId"
        )
        try:
            info = fetch(url, token)
            print(f"  LogicalName:   {info.get('LogicalName')}", flush=True)
            print(f"  SchemaName:    {info.get('SchemaName')}", flush=True)
            print(f"  EntitySetName: {info.get('EntitySetName')}", flush=True)
        except Exception as e:
            print(f"  ERROR: {e}", flush=True)
            continue

        # List all attributes on the table
        url = (
            f"{env}/api/data/v9.2/EntityDefinitions(LogicalName='{table}')/Attributes"
            "?$select=LogicalName,SchemaName,AttributeType,IsCustomAttribute,IsPrimaryName"
        )
        try:
            data = fetch(url, token)
            attrs = data.get("value", [])
            custom = [
                a for a in attrs
                if a.get("IsCustomAttribute")
                and str(a.get("LogicalName", "")).startswith("arng_")
            ]
            print(f"  Custom arng_ columns: {len(custom)}", flush=True)
            for a in sorted(custom, key=lambda x: x.get("LogicalName", "")):
                flags = " [primary]" if a.get("IsPrimaryName") else ""
                print(
                    f"    - {a.get('LogicalName'):<30} "
                    f"{a.get('AttributeType'):<15} "
                    f"schema={a.get('SchemaName')}{flags}",
                    flush=True,
                )
        except Exception as e:
            print(f"  (attributes error: {e})", flush=True)
        print("", flush=True)


if __name__ == "__main__":
    main()
