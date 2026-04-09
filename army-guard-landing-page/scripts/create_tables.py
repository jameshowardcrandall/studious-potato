"""Create the 3 tables for the Army Guard Landing Page solution.

Schema:
  arng_staffsection  — the 6 tiles on the landing page
    arng_name          (primary, string) — display label, e.g. "G-1 Personnel"
    arng_code          (string)          — short code, e.g. "G1"
    arng_displayorder  (int)             — 1..6 for ordering tiles
    arng_color         (string)          — hex color for tile background

  arng_product  — apps/products owned by a staff section
    arng_name          (primary, string) — product name, e.g. "Recruiting System"
    arng_description   (text)            — optional description
    arng_SectionId     (lookup)          — -> arng_staffsection

  arng_productlink  — Dashboard/MDA/Canvas links under each product
    arng_name          (primary, string) — link display name, e.g. "Dashboard"
    arng_ProductId     (lookup)          — -> arng_product
    arng_linktype      (choice)          — Dashboard / ModelDrivenApp / CanvasApp
    arng_url           (string)          — the URL
    arng_displayorder  (int)             — ordering within a product

Phased creation per dv-metadata guidance:
  Phase 1: create all 3 tables (5s delay between)
  Phase 2: wait 20s for metadata propagation
  Phase 3: add choice column + create lookups
"""
import os
import sys
import time
from enum import IntEnum
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from auth import get_credential, load_env  # noqa: E402

from PowerPlatform.Dataverse.client import DataverseClient  # noqa: E402

SOLUTION = "ArmyGuardLandingPage"


class LinkType(IntEnum):
    DASHBOARD = 100000000
    MODEL_DRIVEN_APP = 100000001
    CANVAS_APP = 100000002


def retry_metadata(fn, description, max_attempts=5):
    """Retry wrapper for lock contention and transient errors."""
    for attempt in range(max_attempts):
        try:
            return fn()
        except Exception as e:
            err = str(e)
            low = err.lower()
            if "already exists" in low or "0x80040237" in low or "0x80048d0b" in low:
                print(f"  [SKIP] {description}: already exists", flush=True)
                return None
            if "another" in low and ("running" in low or "operation" in low):
                wait = 10 * (attempt + 1)
                print(
                    f"  [RETRY] {description}: lock contention, "
                    f"waiting {wait}s (attempt {attempt + 1}/{max_attempts})",
                    flush=True,
                )
                time.sleep(wait)
                continue
            if "0x80040216" in low or "0x80060891" in low:
                wait = 5 * (attempt + 1)
                print(
                    f"  [RETRY] {description}: metadata cache not ready, "
                    f"waiting {wait}s (attempt {attempt + 1}/{max_attempts})",
                    flush=True,
                )
                time.sleep(wait)
                continue
            raise
    print(f"  [FAIL] {description}: exhausted retries", flush=True)
    return None


def create_staffsection(client):
    print("[Phase 1] Creating arng_StaffSection...", flush=True)
    return retry_metadata(
        lambda: client.tables.create(
            "arng_StaffSection",
            {
                "arng_Code": "string",
                "arng_DisplayOrder": "int",
                "arng_Color": "string",
            },
            solution=SOLUTION,
            primary_column="arng_Name",
        ),
        "create table arng_StaffSection",
    )


def create_product(client):
    print("[Phase 1] Creating arng_Product...", flush=True)
    return retry_metadata(
        lambda: client.tables.create(
            "arng_Product",
            {
                "arng_Description": "string",
            },
            solution=SOLUTION,
            primary_column="arng_Name",
        ),
        "create table arng_Product",
    )


def create_productlink(client):
    print("[Phase 1] Creating arng_ProductLink...", flush=True)
    return retry_metadata(
        lambda: client.tables.create(
            "arng_ProductLink",
            {
                "arng_Url": "string",
                "arng_DisplayOrder": "int",
            },
            solution=SOLUTION,
            primary_column="arng_Name",
        ),
        "create table arng_ProductLink",
    )


def add_linktype_choice(client):
    print("[Phase 3] Adding arng_LinkType choice column to arng_ProductLink...", flush=True)
    # Note: b7 SDK add_columns() does not accept solution= kwarg. The column
    # inherits the solution from its parent table.
    return retry_metadata(
        lambda: client.tables.add_columns(
            "arng_productlink",
            {"arng_LinkType": LinkType},
        ),
        "add choice column arng_LinkType",
    )


def create_section_lookup(client):
    print("[Phase 3] Creating lookup arng_SectionId on arng_Product -> arng_staffsection...", flush=True)
    return retry_metadata(
        lambda: client.tables.create_lookup_field(
            referencing_table="arng_product",
            lookup_field_name="arng_SectionId",
            referenced_table="arng_staffsection",
            display_name="Staff Section",
            solution=SOLUTION,
        ),
        "create lookup arng_SectionId",
    )


def create_product_lookup(client):
    print("[Phase 3] Creating lookup arng_ProductId on arng_ProductLink -> arng_product...", flush=True)
    return retry_metadata(
        lambda: client.tables.create_lookup_field(
            referencing_table="arng_productlink",
            lookup_field_name="arng_ProductId",
            referenced_table="arng_product",
            display_name="Product",
            solution=SOLUTION,
        ),
        "create lookup arng_ProductId",
    )


def main():
    load_env()
    client = DataverseClient(os.environ["DATAVERSE_URL"], get_credential())

    # Phase 1: Create tables (5s delay between each)
    create_staffsection(client)
    time.sleep(5)
    create_product(client)
    time.sleep(5)
    create_productlink(client)

    # Phase 2: Wait for metadata propagation
    print("[Phase 2] Waiting 20s for metadata propagation...", flush=True)
    time.sleep(20)

    # Phase 3: Choice column + lookups (3s delay between each)
    add_linktype_choice(client)
    time.sleep(3)
    create_section_lookup(client)
    time.sleep(3)
    create_product_lookup(client)

    print("", flush=True)
    print("DONE. Summary of created schema:", flush=True)
    print("  Table: arng_staffsection", flush=True)
    print("    arng_name (primary, string)", flush=True)
    print("    arng_code (string)", flush=True)
    print("    arng_displayorder (int)", flush=True)
    print("    arng_color (string)", flush=True)
    print("  Table: arng_product", flush=True)
    print("    arng_name (primary, string)", flush=True)
    print("    arng_description (string)", flush=True)
    print("    arng_SectionId (lookup -> arng_staffsection)", flush=True)
    print("  Table: arng_productlink", flush=True)
    print("    arng_name (primary, string)", flush=True)
    print("    arng_url (string)", flush=True)
    print("    arng_displayorder (int)", flush=True)
    print("    arng_linktype (choice: Dashboard/ModelDrivenApp/CanvasApp)", flush=True)
    print("    arng_ProductId (lookup -> arng_product)", flush=True)


if __name__ == "__main__":
    main()
