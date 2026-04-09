# Army Guard — Unit Portal

Internal landing page for an Army National Guard unit. Desktop canvas app that serves as a directory / jump-off point for all the apps and dashboards owned by each G-staff section. Users open one app, see a 3×2 grid of staff sections (COS, G1, G2/G6/IA/ADS, G3/G5/G5, G4/G9, G8), click a tile, and see that section's products with direct links to each product's Dashboard, Model-driven app, and Canvas app.

An **admin experience** is baked into the same canvas app so OPR admins can add/edit/delete products and their links without leaving the portal.

## Architecture

```
studious-potato/army-guard-landing-page/
├── canvas-app/                     # Source YAML for the canvas app (pa.yaml)
│   ├── App.pa.yaml                 # App.OnStart, App.Formulas brand palette
│   ├── ScreenHome.pa.yaml          # 3×2 tile grid landing page
│   ├── ScreenDetail.pa.yaml        # Section drill-down with product links
│   ├── ScreenAdmin.pa.yaml         # Admin product gallery
│   ├── ScreenProductForm.pa.yaml   # Add/edit product (Patch-based form)
│   ├── ScreenLinksAdmin.pa.yaml    # Per-product links management
│   └── ScreenLinkForm.pa.yaml      # Add/edit link (Patch-based form)
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
pac solution pack --folder solutions/ArmyGuardLandingPage \
    --zipfile solutions/ArmyGuardLandingPage.zip --packagetype Unmanaged
pac solution import --path solutions/ArmyGuardLandingPage.zip --publish-changes

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
                          └─LINKS──►  ScreenLinksAdmin  ──EDIT──►  ScreenLinkForm
```

Shared state (global variables):
- `selectedSection` — the staff section chosen on ScreenHome, read by ScreenDetail
- `editProduct` — the product row being edited in ScreenProductForm
- `editLink` — the link row being edited in ScreenLinkForm
- `currentProduct` — the product whose links are being managed in ScreenLinksAdmin / ScreenLinkForm
- `editMode` — `"new"` or `"edit"`, controls form branching

## Per-OPR security

The app does **not** enforce row-level access at the canvas layer. All filtering is assumed to happen via **Dataverse security roles + business unit scoping** so that admins can only read/write products for their own staff section. The canvas app will surface permission-denied errors at Patch/SubmitForm time when a user tries to edit outside their scope — this is intended.

If you want a softer UX (hide rows users can't edit rather than surface errors), add a filter on `galAdminProducts.Items` that restricts to rows the current user owns.
