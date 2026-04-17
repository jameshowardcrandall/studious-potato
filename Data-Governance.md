# REDM Enterprise Data Governance Framework

---

## REDM
Rapid Engagement Delivery Model

## Enterprise Data Governance Framework
*A CDO's Guide to Tool-Agnostic, Relationship-Driven Data Strategy*

James Crandall | Power Platform Solution Architect

# Table of Contents
# 1. The Philosophy: Data Gravity, Not Tool Loyalty
> **Core Principle**  *The value of enterprise data does not live in the tool that created it. It lives in how that data connects to everything else.*


Enterprise data strategies often collapse under the weight of vendor allegiance. Organizations spend years debating whether to standardize on Salesforce, ServiceNow, Power Platform, or Appian — when the real question is never which tool you use to produce data, but how that data leaves its origin and relates to everything else in the enterprise.

REDM's data governance philosophy starts here: stay agnostic at the production layer. Teams can keep the SaaS platforms that serve their operational workflows. The data engineers are the integration layer — they define the standard plug, not the device. As long as every source participates in a predictable integration contract, the enterprise can extract, model, and consume that data regardless of where it was born.

## 1.1 The Analogy That Lands
Think of it like electrical infrastructure. You do not care whether an appliance was made by Samsung, GE, or a niche manufacturer — as long as it uses the standard plug, it works. Your data strategy is about defining the standard plug. Teams can keep using Appian, Power Platform, ServiceNow, or spreadsheets. The data engineers wire everything to the same grid. What gets consumed on that grid is consistent, trustworthy, and connected.

## 1.2 Why This Matters for the CDO
A non-technical CDO does not need to commit to one platform. That decision is a trap that delays value delivery by years. The real commitments are much smaller and more durable:

* Where does our data land? (the integration layer)
* What does our data mean? (the semantic and canonical model)
* Who can use our data and how? (governance and consumption)

Everything else — which SaaS tools teams use, which databases they run, which vendor wins the next procurement — is operational detail. The strategy sits above all of that and remains valid even as individual tools change.

> **Key Insight**  *The enemy is not Salesforce or ServiceNow. The enemy is data that gets created and never leaves the tool it was born in. Good governance makes that impossible by design.*


# 2. The Three Core Questions
Every data governance framework must answer three questions clearly. These questions form the spine of REDM's approach and provide the CDO with a durable communication framework that transcends any specific technology decision.

## 2.1 Where Does Our Data Land?
This is the integration question. Every source system — regardless of vendor — must participate in a standard integration pattern. The enterprise defines a landing zone: one logical destination where raw data from every source arrives before any transformation occurs.

* A landing zone is not a warehouse. It is a staging area with full fidelity — no transformation, timestamped, and immutable.
* Every source system agrees to expose its data in a predictable way: CDC (Change Data Capture) for databases, API polling for SaaS platforms, event streaming for real-time signals, or batch extracts for legacy systems.
* The tool can be anything. The integration contract is what matters.

For Microsoft-centric organizations, Azure Data Lake Storage Gen2 is the natural landing zone. For cloud-agnostic deployments, S3 or equivalent blob storage works equally well. The format that provides the most interoperability — and works natively with both Databricks and Palantir Foundry — is Delta Lake (open table format with ACID transactions, time travel, and schema enforcement).

## 2.2 What Does Our Data Mean?
This is the semantic question, and it is where the most critical and underinvested work happens. The canonical model is the enterprise's answer to a simple but profound problem: the word 'customer' means different things in Salesforce, ServiceNow, Power Platform, and your finance system.

* Data engineers define what a Customer, Case, Asset, Contract, or Transaction means across the enterprise — once.
* Source systems map to that canonical model. The mapping is the hard work.
* Above the canonical model sits the semantic layer: metric definitions, business KPIs, and reporting views that express consistent meaning to any consumer.

> **Why It Matters**  *A number is only trustworthy if everyone agrees on where it came from and what it means. The canonical model is what makes that agreement durable — not a verbal consensus, but an enforced definition.*


## 2.3 Who Can Use Our Data and How?
This is the governance question. Access, classification, and lineage must be defined from the beginning — not retrofitted after data is already in production.

* Every dataset must be tagged with: domain owner, sensitivity classification (PII, CUI, business-sensitive), freshness SLA, and intended consumers.
* Row- and column-level security must be designed before Gold-layer data is published, not bolted on afterward.
* Lineage — end-to-end — must be available so any stakeholder can answer "where did this number come from?" before a board meeting, not after.

# 3. The Technical Architecture
REDM's data governance architecture follows a layered model that works whether your consumption target is Databricks, Palantir Foundry, or any other enterprise analytics platform. The key design decision is choosing Delta Lake as the open table format — it is natively supported by Databricks, readable by Foundry, and preserves optionality across both platforms.

## 3.1 The Five-Layer Model
| **Layer** | **Purpose** | **Key Outputs** |
| 1. Source Systems | Operational tools that generate data (Power Platform, Salesforce, ServiceNow, Appian, etc.) | Operational records, events, transactions |
| 2. Landing Zone (Bronze) | Raw, full-fidelity ingest — no transformation. Timestamped, immutable. | Delta tables, raw JSON/Parquet files |
| 3. Conformed Layer (Silver) | Cleaned, deduplicated, schema-enforced. Maps to the canonical model. | Canonical domain entities, validated datasets |
| 4. Domain Products (Gold) | Business-ready, domain-specific aggregations and metrics. Governed and published. | KPIs, dashboards, ML feature stores |
| 5. Consumption Layer | Databricks, Foundry, Power BI, or other analytics surfaces where business users work. | Reports, models, applications |

## 3.2 Ingestion Patterns by Source Type
Not all sources are equal. The ingestion pattern is chosen based on the source system's capability, not based on a vendor preference.

| **Pattern** | **Best For** | **Tools / Approach** |
| CDC (Change Data Capture) | Operational databases with high-frequency changes | Debezium, Azure Data Factory incremental, Fivetran |
| API Polling | SaaS platforms (Salesforce, Power Platform, ServiceNow) | Custom connectors, Azure Functions, Dataflows |
| Event Streaming | Real-time signals, IoT, user activity | Azure Event Hubs, Kafka → Delta Lake |
| Batch Extract | Legacy systems, flat files, spreadsheets | SFTP, ADF bulk copy, manual upload pipelines |

## 3.3 Databricks vs. Foundry: Choosing Without Committing
Both Databricks and Palantir Foundry are strong consumption layers with meaningfully different philosophies. The REDM approach is designed so neither choice requires re-engineering the lower layers.

* Databricks is table/SQL-centric. It excels at data engineering workflows, ML pipelines, and SQL analytics. Unity Catalog provides centralized governance across workspaces.
* Palantir Foundry is object/ontology-centric. It models the world as Objects and Links (Person, Asset, Case) rather than tables. Its value compounds when the ontology is well-designed and consistently applied.
* The Delta Lake Silver layer is the hedge. Both platforms can read it. Organizations can run Databricks today and extend to Foundry tomorrow without rebuilding ingestion or the canonical model.

> **Architecture Decision**  *The Delta Lake open format is your platform insurance policy. Build your Silver layer there and you preserve optionality across every major analytics platform on the market today.*


# 4. Governance Pillars
Data governance is not a committee. It is an operational discipline enforced through tooling, policy, and culture. REDM's governance model rests on four pillars that must be implemented from day one, not retrofitted after data is already in production.

## 4.1 Data Classification
Every dataset entering the landing zone must be classified before it advances to Silver. Classification is not a one-time label — it is enforced at the cell level in sensitive domains.

* PII (Personally Identifiable Information): Names, SSNs, email addresses, contact records. Governed under NIST SP 800-53, CCPA, GDPR, or applicable DoD regulations.
* CUI (Controlled Unclassified Information): For DoD and federal contexts. Requires handling controls and access logging.
* Business-Sensitive: Internal financial projections, personnel data, acquisition targets. Not public-law regulated but governed by internal policy.
* Unclassified / Open: Operational metrics, public records, reference data. Lowest restriction tier.

## 4.2 Data Catalog
Every dataset published to Gold must be registered in the enterprise data catalog. The catalog is the single source of truth for what data exists, who owns it, and how to access it.

* Minimum metadata per dataset: domain owner, classification tier, freshness SLA, row count, schema version, access policy, and lineage reference.
* In Databricks environments, Unity Catalog serves this function natively. In Foundry, the Ontology itself is the catalog. For environments without a platform catalog, tools like Alation or Collibra fill the gap.
* The catalog must be updated automatically by pipeline runs — not maintained manually. Manual catalogs decay within weeks.

## 4.3 Lineage
Lineage is the ability to answer, for any data point in any downstream report: where did this come from, what transformations were applied, and when was it last refreshed? Without lineage, trust in data degrades every time a number is questioned.

* End-to-end lineage must trace from the source system record through every transformation to the consuming report or model.
* Lineage should be captured automatically by the pipeline framework. Databricks and Foundry both provide lineage tooling natively.
* Spot-audit lineage quarterly. Assign a data owner responsible for resolving lineage breaks within 48 hours.

## 4.4 Access and Row/Column Security
Access control must be designed before Gold-layer data is published. The default posture is least privilege — access is denied until explicitly granted through a documented request and approval workflow.

* Row-level security (RLS): Restrict which rows a user or role can see. Common for multi-organization datasets, geographic partitions, or sensitivity tiers.
* Column-level security (CLS): Mask or restrict PII/CUI columns for users without proper clearance. Both Databricks Unity Catalog and Foundry support CLS natively.
* Access requests are logged, reviewed, and time-bounded. Quarterly access reviews recertify all elevated grants.

# 5. REDM-Specific Data Governance Rules
REDM engagements involve rapid delivery cycles — often delivering working capability within days. This speed creates specific data governance risks that the REDM Data Governance framework is designed to prevent. The rules in this section apply to every REDM engagement from Day 1.

## 5.1 Schema Ownership
Every data domain in the REDM engagement has a designated Schema Owner — a senior developer who is the sole authority over the structure of that domain's data model.

* No new tables, columns, or relationships may be created without the Schema Owner's explicit approval.
* The Schema Owner is identified and onboarded before the first line of code is written.
* Schema changes are reviewed in the Co-Design phase and documented in the Canonical Model Registry.

> **Why This Exists**  *This rule was forged in the field. A new developer was onboarded to an active REDM engagement and, eager to contribute, began creating tables in Dataverse without knowing what already existed. Within two days, duplicate data models, broken relationships, and orphaned records created hours of cleanup work. Schema Ownership is the control that prevents this — not because developers can't be trusted, but because no individual can have full context of a living data model without being explicitly briefed.*


## 5.2 Developer Onboarding Protocol for Data
Every developer added to a REDM engagement must complete a structured data onboarding session before accessing the development environment. This is non-negotiable and is the responsibility of the Schema Owner to deliver.

| **Step** | **Action** | **Responsible** |
| 1 | Walk through the Canonical Model Registry — every existing table, column, and relationship, with purpose. | Schema Owner |
| 2 | Explain the three-bucket rule: before creating anything new, check if it already exists. | Schema Owner |
| 3 | Confirm the developer understands the approval workflow for schema changes. | Schema Owner + Tech Lead |
| 4 | Add the developer to the Schema Change Request channel or tracking mechanism. | Tech Lead |
| 5 | Grant dev environment access only after onboarding is complete. | Environment Admin |

## 5.3 Schema Change Request Workflow
When a developer identifies a legitimate need for a new table, column, or relationship, the following workflow applies:

* Developer submits a Schema Change Request describing: the data need, the proposed structure, and why an existing entity does not cover the need.
* Schema Owner reviews within one business day and either approves, requests modification, or denies with rationale.
* Approved changes are documented in the Canonical Model Registry before implementation.
* Changes are implemented in DEV, reviewed at the next cycle demo, and promoted to TEST/PROD through the ALM pipeline.

## 5.4 The Canonical Model Registry
The Canonical Model Registry is the living document of record for all data structures in the engagement. It is not optional and not aspirational — it must be current at all times.

* Format: A versioned spreadsheet or Dataverse-backed record listing every table (entity), its columns, data types, relationships, and ownership.
* Updated by the Schema Owner within 24 hours of any approved schema change.
* Reviewed in each Phase Gate review as a condition of promotion to the next phase.
* Archived at engagement close and handed off as a deliverable to the government or client data team.

## 5.5 Environment Data Governance
REDM's three-environment model (DEV / TEST / PROD) has specific data governance rules for each tier:

| **Environment** | **Real Data Allowed?** | **PII Rules** | **Schema Change Authority** |
| DEV | No | Synthetic data only. No PII ever in DEV. | Schema Owner approval required |
| TEST | Anonymized only | Scrubbed/masked copies of production records. No direct PII. | Schema Owner + Program Manager |
| PROD | Yes | Full PII/CUI controls active. Access logged and audited. | Change Board + Schema Owner |

# 6. Communicating Data Governance to Non-Technical Leaders
A data governance strategy only succeeds when organizational leaders understand and champion it. This section provides the CDO with a communication framework designed for non-technical stakeholders — one that frames governance as a business capability, not an IT initiative.

## 6.1 The Business Case
Data governance is not about compliance. It is about not having to answer 'I don't know' in a briefing. It is about being able to say yes when an operator asks if two systems are telling the same story. It is about building analytical capability that compounds over time instead of starting from scratch every two years.

* Without governance: data is created in tools and never leaves them. Every report is a one-time manual effort. Every decision is made on incomplete information.
* With governance: data flows from operational tools to a governed consumption layer automatically. Reports are reproducible. Analysts spend time on analysis, not on data assembly.

## 6.2 The Three Questions — Simplified
For executive audiences, the entire strategy collapses to three durable questions. Every technology decision, vendor selection, and pipeline investment is evaluated against these:

| **Question** | **Plain Language** | **Technical Equivalent** |
| Where does our data land? | We have one front door for all data, regardless of source. | Landing zone / Bronze layer |
| What does our data mean? | Revenue means one thing. Customer means one thing. Everywhere. | Canonical model / Silver layer |
| Who can use our data, and how? | The right people see the right data, and we can prove it. | Access control, classification, lineage |

## 6.3 What to Champion, What to Delegate
The CDO's job is to champion the strategy and hold the organization accountable to the three questions. The CDO does not need to make technology decisions — those are delegated to the data engineering team.

* Champion: the data contract standard (every source system must participate), the canonical model as the authoritative definition of enterprise entities, and the governance review cycle.
* Delegate: specific tool selection, pipeline architecture, catalog implementation, and environment management.
* Hold accountable: every domain that produces data without a defined integration pattern, every report that cannot trace its lineage, every number that contradicts another number in a briefing.

## 6.4 Quick Wins to Build Momentum
A data governance program that starts with a multi-year roadmap and no visible output loses organizational support before it delivers value. REDM recommends a quick-win approach in the first 90 days:

| **Timeline** | **Quick Win** | **Why It Matters** |
| Day 1–30 | Publish the first data catalog with five datasets, fully documented with owner, classification, and freshness SLA. | Demonstrates the governance model is real and operational. |
| Day 31–60 | Deliver one executive dashboard from the Gold layer with visible lineage — click a number, see where it came from. | Builds CDO confidence and stakeholder trust in governed data. |
| Day 61–90 | Complete the first quarterly access review and recertify all elevated grants. | Demonstrates governance is not a one-time audit, but an ongoing discipline. |

# 7. Implementation Roadmap
The REDM data governance implementation follows a phased approach that prioritizes visible value delivery over comprehensive planning. Each phase has a defined outcome and a clear gate condition.

## Phase 1 — Foundation (Weeks 1–4)
* Stand up the landing zone. Define the integration contract standard.
* Identify the five highest-priority data sources and their owners.
* Appoint Schema Owners for each data domain.
* Deploy the Canonical Model Registry (initial version).
* Implement data classification for the first ingested datasets.

Gate condition: Landing zone is live. At least three source systems are delivering data via a defined integration pattern. Classification is applied to all ingested datasets.

## Phase 2 — Canonical Model (Weeks 5–10)
* Build the Silver/Conformed layer for the top three domain entities (e.g., Customer, Case, Asset).
* Define and document entity relationships in the Canonical Model Registry.
* Implement row- and column-level security for the first Gold-layer dataset.
* Deliver the first executive dashboard with lineage.

Gate condition: At least one Gold-layer dataset is live, governed, and accessible to the intended consumer group. Lineage is traceable end-to-end.

## Phase 3 — Scale and Sustain (Weeks 11+)
* Onboard remaining data domains and source systems.
* Automate catalog updates via pipeline metadata.
* Conduct the first quarterly access review.
* Expand the semantic layer (metric definitions, KPI catalog).
* Publish the data governance policy and training materials for domain data owners.

Gate condition: All priority data domains are in the catalog. Access review cycle is established. Data governance policy is published and acknowledged by all domain owners.

## Roles and Responsibilities
| **Role** | **Responsibility** |
| CDO (Chief Data Officer) | Champions the strategy. Holds domains accountable. Resolves cross-domain disputes on canonical definitions. |
| Schema Owner (per domain) | Approves all schema changes. Maintains the Canonical Model Registry. Delivers developer onboarding. |
| Data Engineer | Builds and maintains ingestion pipelines, transformations, and the canonical model mapping. |
| Environment Admin | Controls access to DEV/TEST/PROD. Enforces the data classification policy per environment. |
| Domain Data Owner | Business-side owner of a data domain. Signs off on canonical definitions. Participates in access reviews. |

# 8. Conclusion: The Data That Connects Wins
> **The Goal**  *A customer record in Salesforce is interesting. That same customer record linked to their contract in ServiceNow, their support tickets in another system, and their invoices in your ERP — that is intelligence.*


Enterprise data governance is not about picking the right tool. It is about building the connective tissue that allows any tool to participate in a coherent data ecosystem. REDM's approach gives organizations a framework that is durable across vendor changes, scalable across domains, and communicable to any leader — technical or not.

The three questions are the compass: Where does it land? What does it mean? Who can use it? Answer those three questions consistently and enforce the answers through Schema Ownership, the Canonical Model Registry, and the classification and access discipline — and the data your organization produces will compound in value over time rather than decay in silos.

Start with five datasets. Govern them perfectly. Demonstrate that a number on a dashboard can be traced to its source in under five minutes. That proof of concept — more than any strategy document — is what earns organizational commitment to the governance program.

— James Crandall, Power Platform Solution Architect

*REDM — Rapid Engagement Delivery Model*