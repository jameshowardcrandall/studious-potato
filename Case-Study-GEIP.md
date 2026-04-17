# Case Study — GEIP

**Guard Enterprise Installation Platform**

---

## The Situation
The Army National Guard needed a unified enterprise platform to manage the operational and administrative complexity of military installations — personnel readiness, in/out processing, contract management, access control, and physical asset tracking — across a geographically dispersed force. Existing solutions were fragmented across spreadsheets, legacy systems, and point tools with no integration layer.

A commercial vendor had been approached. The proposal came back at over five million dollars with a multi-year timeline. The mission couldn't wait that long, and the money wasn't there.

> **The Challenge**  *The question wasn't whether the capability could be built. It was whether it could be built fast enough to matter — and at a cost that was defensible.*


## The REDM Approach
Rather than procure a vendor platform, the decision was made to build GEIP on Microsoft Power Platform using REDM. An architect-led team worked directly with stakeholders at TARC (The Army Readiness Center) to co-design, build, and iterate on a modular solution — delivering working capability early and expanding from there.

The engagement followed REDM's core pattern: frequent stakeholder sessions, IOC-first delivery, schema governance from day one, and a modular ALM pipeline that allowed components to be deployed and updated independently without taking down the entire platform.

| **Principle** | **How It Applied in GEIP** |
| --- | --- |
| IOC First | PERSTAT tracking went live with core functionality while contract management and asset modules were still in build. Real users drove real requirements. |
| Schema Ownership | Dataverse schema locked by domain: HCM, Access, Contract, Asset. No cross-domain changes without architect review. |
| Modular ALM | Six independently deployable solutions (Core, Flows, Plugins, HCM, Access Request, Contract Management). Updates to one don't touch the others. |
| Sustained Engagement | No engagement end date. Enhancement cycles continue as the platform expands to new states and new mission requirements emerge. |

## The Architecture
GEIP is a multi-solution Power Platform ecosystem with every major platform component in use:

| **Component** | **Purpose** |
| --- | --- |
| Dataverse | Core data layer across all modules. Shared entity model for personnel, org structure, contracts, and assets. |
| Model-Driven Apps | Admin and leadership functions: org structure management, contract oversight, access request approvals, leadership dashboards. |
| Canvas Apps | High-throughput operational UX: CAC barcode scanning for in/out processing, mobile check-in, PERSTAT entry. |
| Power Pages Portal | External-facing personnel portal for PERSTAT status updates with Azure AD SSO and automatic account provisioning on first login. |
| Power Automate | Workflow automation: PERSTAT record generation, approval routing, notification flows, automated role assignment. |
| Power BI | Analytics: daily PERSTAT trends, readiness dashboards, leadership reporting. |
| Teams Integration | PERSTAT status updates via Teams chatbot — no portal login required for routine status submissions. |
| Power Platform Pipelines + Azure Repos | ALM: CI/CD pipeline for promotion from DEV through TEST to PROD with managed solution packages. |

## The Results
GEIP went from concept to production capability at TARC and is now being rolled out to all 54 states and territories. The engagement never ended — it evolved into a sustained delivery relationship where the platform grows with the mission.

* 8,000+ personnel tracked daily through the PERSTAT system.
* CAC barcode scanning eliminated manual entry for in/out processing across the installation.
* Three-tier automated security role management replaced manual admin overhead.
* Contract management and physical asset tracking unified in a single platform.
* Joint Staff expansion underway — extending the same ecosystem to a new organizational layer.
* Cost: a fraction of the $5M+ vendor alternative. Timeline: months, not years.

> **What It Proves**  *GEIP is what REDM's Sustainment and Growth phase looks like in practice. The platform doesn't retire — it compounds. Every new state that comes on inherits the architecture, the schema governance, and the delivery relationship. The cost of expansion is a fraction of the cost of the original build.*
