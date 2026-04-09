# Army Guard — Unit Portal

Internal landing page for an Army National Guard unit. Desktop canvas app that serves as a directory / jump-off point for all the apps and dashboards owned by each G-staff section. Users open one app, see a 3×2 grid of staff sections (COS, G1, G2/G6/IA/ADS, G3/G5/G5, G4/G9, G8), click a tile, and see that section's products with direct links to each product's Dashboard, Model-driven app, and Canvas app.

A **partial admin experience** is baked into the same canvas app so OPR admins can add/edit products. Link management is not yet in-app — see the *Known issues* section below.

## Architecture

```
studious-potato/army-guard-landing-page/
├── canvas-app/                     # Source YAML for the canvas app (pa.yaml)
│   ├── App.pa.yaml                 # App.OnStart, App.Formulas brand palette
│   ├── ScreenHome.pa.yaml          # 3×2 tile grid landing page
│   ├── ScreenDetail.pa.yaml        # Section drill-down with product links
│   ├── ScreenAdmin.pa.yaml         # Admin product gallery (LINKS button stubbed — see Known issues)
│   └── ScreenProductForm.pa.yaml   # Add/edit product (Patch-based form)
├── solutions/
│   └── ArmyGuardLandingPage/       # Unpacked Dataverse solution
│       ├── Entities/
│       │   ├── arng_StaffSection/  # 6 G-staff rows (drives tile grid)
│       │   ├── arng_Product/       # Apps/dashboards owned by a staff section
│       │   └── arng_ProductLink/   # Individual URLs (Dashboard/MDA/Canvas)
│       ├── CanvasApps/             # .msapp archive of the canvas app
│       └── Other/                  # Solution.xml, Customizations.xml, etc.
├── scripts/                        # Python SDK helpers
│   ├── auth.py                     # Token acquisition (Azure Identity)
│   ├── create_publisher_and_solution.py
│   ├── create_tables.py            # Creates arng_StaffSection / Product / ProductLink
│   ├── seed_staffsections.py       # Seeds the 6 rows used by the tile grid
│   ├── list_publishers.py
│   ├── verify_tables.py            # Prints current schema for the 3 tables
│   ├── add_tables_to_solution.py
│   └── enable-mcp-client.py        # Allowlists Claude/Copilot in the Dataverse MCP
├── .env.example                    # Copy to .env and fill in for your env
└── .gitignore
```

## Data model

| Table | Purpose | Notable columns |
|---|---|---|
| `arng_StaffSection` | One row per G-staff tile on the landing page | `arng_code` (COS, G1, G2/G6/IA/ADS, …), `arng_name`, `arng_displayorder` (1..6), `arng_color` |
| `arng_Product` | An app/product owned by a section | `arng_name`, `arng_description`, `arng_SectionId` (lookup → StaffSection) |
| `arng_ProductLink` | One URL per link type per product | `arng_name`, `arng_url`, `arng_displayorder`, `arng_linktype` (choice: DASHBOARD / MODEL_DRIVEN_APP / CANVAS_APP), `arng_ProductId` (lookup → Product) |

Publisher prefix: **`arng`** — never hardcode a different prefix; change the `PUBLISHER_PREFIX` in `.env` if you're deploying to a different publisher.

## Canvas app — brand palette (App.Formulas)

All colors are named formulas in `App.pa.yaml` so they can be re-themed in one place:

| Formula | Hex | Use |
|---|---|---|
| `ColorNavy` | `#14375B` | Primary screen background |
| `ColorNavySurface` | `#1C446E` | Tile/card fill |
| `ColorNavyDeep` | `#0C2640` | Header bar, hover state |
| `ColorGold` | `#C9A227` | Accents, primary button fill, large tile code |
| `ColorGoldHover` | `#E0B83A` | Button hover |
| `ColorGoldMuted` | `#C9A22759` | Borders, dividers |
| `ColorTextPrimary` | `#FFFFFF` | Body text on dark surfaces |
| `ColorTextSecondary` | `#DCD2AF` | Muted/gold-tinted body text |

Typography: **Segoe UI** throughout. Tile code at 40pt bold, section title at 24pt bold, body at 14pt.

## Setting up from scratch

Prereqs:
- **Python 3.10+** — `brew install python@3.12`
- **.NET 10 SDK** — needed for PAC CLI and the Canvas Authoring MCP proxy (`dnx`)
- **PAC CLI** — `dotnet tool install --global Microsoft.PowerApps.CLI.Tool`
- **Azure CLI** (optional, for service principal auth)

Steps:

```bash
cd army-guard-landing-page

# 1. Copy env template and fill in values
cp .env.example .env
# edit .env — set DATAVERSE_URL, TENANT_ID, PAC_AUTH_PROFILE

# 2. Authenticate PAC CLI to your Dataverse environment
pac auth create --name armyguard-dev
pac org who   # verify

# 3. Python virtual env + SDK dependencies
python3.12 -m venv .venv
source .venv/bin/activate
pip install --upgrade azure-identity requests PowerPlatform-Dataverse-Client pandas

# 4. Import the solution (tables + canvas app)
#    The pre-packed ZIP is already committed at solutions/ArmyGuardLandingPage.zip
#    so you can import directly:
pac solution import --path solutions/ArmyGuardLandingPage.zip --publish-changes
#
#    Or, if you've made edits to the unpacked source under
#    solutions/ArmyGuardLandingPage/, re-pack before importing:
# pac solution pack --folder solutions/ArmyGuardLandingPage \
#     --zipfile solutions/ArmyGuardLandingPage.zip --packagetype Unmanaged
# pac solution import --path solutions/ArmyGuardLandingPage.zip --publish-changes

# 5. Seed the 6 staff sections
python scripts/seed_staffsections.py

# 6. (Optional) Verify schema
python scripts/verify_tables.py
```

The canvas app is imported as part of the solution. To make further changes, open it in Power Apps Studio — the `canvas-app/*.pa.yaml` files are the source of truth for the current state as of the last commit, but they are generated from the Power Apps authoring service and can be re-synced via the Canvas Authoring MCP (`sync_canvas`) or by re-exporting the solution.

## Canvas app screen flow

```
ScreenHome  ──click tile──►  ScreenDetail  (drill-down, end-user view)
   │
   └──click ADMIN──►  ScreenAdmin  ──EDIT──►  ScreenProductForm
                          │
                          └─LINKS──►  (currently stubbed — returns to ScreenHome)
```

Shared state (global variables):
- `selectedSection` — the staff section chosen on ScreenHome, read by ScreenDetail
- `editProduct` — the product row being edited in ScreenProductForm
- `editMode` — `"new"` or `"edit"`, controls form branching
- `currentProduct` — set by the (stubbed) LINKS button; reserved for future link-management screens

## Known issues

**Link management is not yet in-app.** Full admin originally included `ScreenLinksAdmin` and `ScreenLinkForm` screens for managing the `arng_ProductLink` rows per product. Pushing those additional screens caused a rendering regression on ScreenHome/ScreenDetail: the `ThisItem.Code` / `ThisItem.Name` text in the tile grid and the `selectedSection.arng_name` header on the detail screen failed to render (text went blank while rectangles/buttons still rendered fine). Root cause is suspected to be Power Apps' display-name resolver getting confused by this schema's primary key columns (`arng_staffsectionid`, `arng_productid`) which have the auto-generated display names `arng_StaffSection` / `arng_Product` / `arng_ProductLink` that collide with the table schema names. The regression scales with formula-graph complexity, which is why it only shows up when ≥ 3 admin screens are added.

**Working hypotheses for the fix (any one of these should unstick it):**
1. **Rewrite lookup filters to avoid dot-walking through the PK GUID.** Change `Filter(arng_Products, arng_SectionId.arng_staffsectionid = selectedSection.arng_staffsectionid)` to `Filter(arng_Products, arng_SectionId = selectedSection)` — Power Fx supports direct record comparison on lookup columns.
2. **Rename the PK display names** on `arng_StaffSection` / `arng_Product` / `arng_ProductLink` from the auto-generated same-as-schema-name form to something unambiguous (e.g., `Staff Section Id`, `Product Id`, `Product Link Id`).
3. **Re-author the admin screens manually in Power Apps Studio** rather than pushing `.pa.yaml` via the Canvas Authoring MCP, in case this is a coauthoring-push quirk rather than a formula issue.

Until then, product links can be managed directly via the `arng_ProductLink` table in the Dataverse maker portal, or by running the seed/import scripts in this folder.

## Per-OPR security

The app does **not** enforce row-level access at the canvas layer. All filtering is assumed to happen via **Dataverse security roles + business unit scoping** so that admins can only read/write products for their own staff section. The canvas app will surface permission-denied errors at Patch/SubmitForm time when a user tries to edit outside their scope — this is intended.

If you want a softer UX (hide rows users can't edit rather than surface errors), add a filter on `galAdminProducts.Items` that restricts to rows the current user owns.
