"""Create the ArmyNationalGuard publisher (if missing) and ArmyGuardLandingPage solution (if missing).

Idempotent — safe to re-run.
"""
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from auth import get_credential, load_env  # noqa: E402

from PowerPlatform.Dataverse.client import DataverseClient  # noqa: E402

PUBLISHER_UNIQUE = "ArmyNationalGuard"
PUBLISHER_FRIENDLY = "Army National Guard"
PUBLISHER_PREFIX = "arng"
PUBLISHER_DESCRIPTION = "Publisher for Army National Guard Power Platform solutions."

SOLUTION_UNIQUE = "ArmyGuardLandingPage"
SOLUTION_FRIENDLY = "Army Guard Landing Page"
SOLUTION_VERSION = "1.0.0.0"


def get_or_create_publisher(client):
    pages = client.records.get(
        "publisher",
        filter=f"uniquename eq '{PUBLISHER_UNIQUE}'",
        select=["publisherid", "uniquename", "customizationprefix"],
        top=1,
    )
    existing = [p for page in pages for p in page]
    if existing:
        pub = existing[0]
        print(
            f"[SKIP] Publisher '{PUBLISHER_UNIQUE}' already exists "
            f"(id={pub['publisherid']}, prefix={pub['customizationprefix']}_)",
            flush=True,
        )
        return pub["publisherid"]

    publisher_id = client.records.create(
        "publisher",
        {
            "uniquename": PUBLISHER_UNIQUE,
            "friendlyname": PUBLISHER_FRIENDLY,
            "customizationprefix": PUBLISHER_PREFIX,
            "description": PUBLISHER_DESCRIPTION,
        },
    )
    print(
        f"[CREATE] Publisher '{PUBLISHER_UNIQUE}' created "
        f"(id={publisher_id}, prefix={PUBLISHER_PREFIX}_)",
        flush=True,
    )
    return publisher_id


def get_or_create_solution(client, publisher_id):
    pages = client.records.get(
        "solution",
        filter=f"uniquename eq '{SOLUTION_UNIQUE}'",
        select=["solutionid", "uniquename", "friendlyname", "version"],
        top=1,
    )
    existing = [s for page in pages for s in page]
    if existing:
        sol = existing[0]
        print(
            f"[SKIP] Solution '{SOLUTION_UNIQUE}' already exists "
            f"(id={sol['solutionid']}, version={sol['version']})",
            flush=True,
        )
        return sol["solutionid"]

    solution_id = client.records.create(
        "solution",
        {
            "uniquename": SOLUTION_UNIQUE,
            "friendlyname": SOLUTION_FRIENDLY,
            "version": SOLUTION_VERSION,
            "publisherid@odata.bind": f"/publishers({publisher_id})",
        },
    )
    print(
        f"[CREATE] Solution '{SOLUTION_UNIQUE}' created (id={solution_id})",
        flush=True,
    )
    return solution_id


def main():
    load_env()
    client = DataverseClient(os.environ["DATAVERSE_URL"], get_credential())

    publisher_id = get_or_create_publisher(client)
    solution_id = get_or_create_solution(client, publisher_id)

    print(flush=True)
    print(f"PUBLISHER_ID={publisher_id}", flush=True)
    print(f"SOLUTION_ID={solution_id}", flush=True)
    print(f"PUBLISHER_PREFIX={PUBLISHER_PREFIX}", flush=True)
    print(f"SOLUTION_UNIQUE={SOLUTION_UNIQUE}", flush=True)


if __name__ == "__main__":
    main()
