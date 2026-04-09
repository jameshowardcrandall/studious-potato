"""List existing non-Microsoft publishers in the target Dataverse environment."""
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from auth import get_credential, load_env  # noqa: E402

from PowerPlatform.Dataverse.client import DataverseClient  # noqa: E402


def main():
    load_env()
    client = DataverseClient(os.environ["DATAVERSE_URL"], get_credential())

    pages = client.records.get(
        "publisher",
        filter=(
            "customizationprefix ne 'none' "
            "and uniquename ne 'MicrosoftCorporation' "
            "and uniquename ne 'Microsoftdynamic'"
        ),
        select=["publisherid", "uniquename", "friendlyname", "customizationprefix"],
        top=50,
    )
    publishers = [p for page in pages for p in page]

    if not publishers:
        print("NO_CUSTOM_PUBLISHERS_FOUND", flush=True)
        return

    print(f"Found {len(publishers)} custom publisher(s):", flush=True)
    for p in publishers:
        print(
            f"  - uniquename={p.get('uniquename')!r} "
            f"friendlyname={p.get('friendlyname')!r} "
            f"prefix={p.get('customizationprefix')!r} "
            f"id={p.get('publisherid')}",
            flush=True,
        )


if __name__ == "__main__":
    main()
