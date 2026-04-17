# REDM Story Points

> Story points in REDM are not velocity trackers. They are effort signals — lightweight estimates that inform triage decisions, trigger architect review when scope is growing, and keep the Do Now / Queue / Escalate system honest. Each team owns its own scale. Dev Team points and Data Team points are never compared.

---

## The REDM Approach to Story Points

Traditional Agile uses story points to measure velocity and predict sprint capacity. REDM does not use them that way. There are no burndown charts in REDM, no velocity tracking, and no management reporting tied to point output. Points exist for one purpose: to help the team and architect make good triage decisions during engagement sessions.

The question a point estimate answers is not *"how long will this take?"* — it is *"how complex is this relative to other things we do?"* That relative signal tells the team whether something belongs in the current build cycle, the queue, or needs to be broken down before it can be committed to.

> **The Core Principle:** Points above 5 get architect eyes. Points of 13 never get committed — they get decomposed. Everything else is a triage tool, not a performance metric.

---

## How Points Map to REDM Triage

| Category | Point Range | Action | Architect Required? |
|----------|-------------|--------|---------------------|
| **Do Now** | 1–3 | Incorporate in current build cycle (within 48 hours of session) | Not required |
| **Queue** | Any size | Log in backlog; discuss priority at next session | Flagged if ≥5 |
| **Escalate** | 5+ | Requires sponsor or architect decision before committing | Required |
| **Break Down** | 13 | Never commit — decompose before the next session | Required |

---

## Dev Team Story Points

The Dev Team scale covers Microsoft Power Platform delivery — canvas apps, model-driven apps, Power Automate flows, Dataverse schema, Power Pages, Power BI, and ALM. A Dev Team point reflects relative effort and complexity within Power Platform, not hours.

> **Schema Changes:** Any work that adds, modifies, or removes Dataverse entities, columns, or relationships must go through the Schema Owner before it enters a build cycle, regardless of point value.

| Pts | Label | What It Covers |
|-----|-------|----------------|
| **1** | Quick Config | Add/modify field on existing form; update view filter or column sort; minor flow step change; label or UI text update; simple formula fix in canvas app; security role permission adjustment |
| **2** | Standard Feature | New form on an existing entity; new canvas app screen (basic logic); new Power Automate flow (standard); new Power BI report page (basic charts); new business rule; add security role from scratch |
| **3** | Moderate Build | New entity with relationships and security roles; canvas screen with complex logic (offline, delegation, nested galleries); multi-branch flow with error handling; Power BI report with custom DAX; model-driven app view or subgrid update; plugin modification (existing plugin) |
| **5** | High Complexity | Multi-entity schema change with relationship updates; canvas app with cross-entity lookups and complex UX; external API integration flow; new model-driven app module from scratch; Power Pages page with row-level security; Power BI dashboard with RLS and multiple data sources |
| **8** | Architect Scope | New solution component (requires architect sign-off before start); major schema redesign affecting multiple entities; new ALM pipeline configuration; enterprise-scale canvas app (multi-screen, full feature); major security model overhaul; new integration pattern |
| **13** | Must Break Down | Any item estimated at 13 must be decomposed into smaller items before it enters a build cycle. A 13 is the team's signal that scope clarity is missing. |

---

## Data Team Story Points

The Data Team scale covers data engineering, analytics, architecture, and governance — pipelines, schema design, Databricks notebooks, Foundry/Vantage, canonical model changes, and data products. A Data Team point reflects relative effort within the data domain.

> **Cross-Domain Changes:** Any canonical model update or schema change that affects multiple data consumers requires architect review before commitment, regardless of point value.

| Pts | Label | What It Covers |
|-----|-------|----------------|
| **1** | Quick Data Work | Simple SQL query or view update; minor pipeline config change; basic data validation rule; existing report filter/parameter update; schema documentation update |
| **2** | Standard Data | New single-source data transformation; standard ETL pipeline update; new report or dashboard page (standard metrics); basic data quality check; simple API data pull to existing model |
| **3** | Moderate Data | New multi-step pipeline (single source, moderate logic); canonical model update within one domain; Medallion layer update (Bronze→Silver or Silver→Gold); new analytical model (standard aggregations); data governance rule implementation; Foundry pipeline or object update (existing ontology) |
| **5** | High Complexity | Complex ETL/ELT pipeline (multi-source, heavy transformation); new data domain design (schema + lineage); cross-domain data integration; Databricks notebook with ML feature engineering or complex logic; major canonical model update affecting multiple consumers; Foundry ontology build or significant object type addition |
| **8** | Architect Scope | New data domain architecture from scratch (requires architect sign-off); Medallion layer redesign or major restructure; enterprise schema change affecting multiple downstream consumers; ML model development, training, and deployment pipeline; new data product end-to-end; major governance framework change |
| **13** | Must Break Down | Any item estimated at 13 must be decomposed before commitment. A 13 signals that scope or approach has not been sufficiently defined. |

---

## Ground Rules

| Rule | What It Means |
|------|---------------|
| **Dev point ≠ Data point** | The two scales are independent. Never compare points across teams or use them to measure relative output. |
| **Points are not velocity** | No burndown charts. No sprint velocity. Points are a triage and communication tool only. |
| **Team estimates together** | Points are assigned by the team, not by the architect or PM. The person doing the work has the most accurate signal. |
| **8+ requires architect visibility** | Any item estimated at 8 or above must be reviewed by the solution architect before the team commits. |
| **13 means stop and decompose** | A 13 is never accepted into a build cycle. It means scope clarity is missing. |
| **Do Now items must be ≤3** | Items going into the current cycle should be 3 points or less. Higher estimates belong in Queue. |

---

## Cross-Team Coordination

Dev Team and Data Team story points are independent, but the teams are not. When a deliverable requires both teams — a new data domain feeding a Power BI dashboard, a canvas app writing to a Dataverse entity that feeds a Databricks pipeline — the following applies:

- Both teams estimate their portion independently on their own scale
- The architect identifies cross-team dependencies at the start of each session
- Items with cross-team dependencies are flagged in the decision log and reviewed jointly
- Neither team commits to their portion until both portions have been reviewed by the architect
- Sequencing (which team goes first) is an architect decision

---

> **Remember:** Story points are a communication tool. The moment they become a management metric or a cross-team comparison, they stop serving REDM and start adding the overhead REDM was designed to eliminate.
