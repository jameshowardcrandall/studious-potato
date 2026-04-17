# Case Study — Nomination & Panel Scoring

**Three-App System Delivered in One Day**

---

## The Situation
A nomination and panel scoring process was needed immediately. Five panelists would score nominees across four questions each, with a 500-point total per nominee. Three distinct user types needed clearly separated access: supervisors submitting nominations, HR reviewing eligibility, and panelists entering scores from mobile devices.

This wasn't a prototype. It needed full role-based access control from day one, real data, and real users. And it was needed now — not at the end of a sprint cycle.

> **The Starting Point**  *When the ask came in, the architecture was the answer. The question wasn't whether it could be built. It was how fast the right decisions could be made.*


## The REDM Approach
One solution architect. Product owners iterating live in the room. No handoffs. No approval queues for requirements. Decisions were made in real time as the build happened — which is exactly what REDM is designed for.

The architect made the key call early: one Dataverse core, three separate apps optimized for three different workflows, separate security roles for each persona enforced at the data layer. That decision took ten minutes. It structured the rest of the day.

## The Architecture
| **App** | **Type** | **User** | **Purpose** |
| --- | --- | --- | --- |
| Nominations App | Canvas App | Supervisors | Submit nominations for review. Simple guided workflow — enter nominee, complete required fields, submit for HR eligibility review. |
| Eligibility Review App | Model-Driven App | HR Personnel | Review submitted nominations against eligibility criteria. Approve or flag for follow-up. Full audit trail, record management, Dataverse security enforced. |
| Panelist Scoring App | Mobile Canvas App | Panelists | Score nominees on four questions, 500 points total. Mobile-first, optimized for quick entry without navigation overhead. |

**One Dataverse core.** All three apps write to and read from the same data layer. Security roles are separate per persona — supervisors can't see panelist scores, panelists can't see eligibility decisions, HR sees what they need to see. Enforcement happens at the data layer, not in app logic.

## The Timeline
| **Time** | **What Happened** |
| --- | --- |
| Morning | Requirements gathered. Architecture decided. Dataverse schema created. Security roles defined. |
| Midday | Supervisor nomination app built and reviewed live with product owner. HR model-driven app configured. Security roles tested. |
| Afternoon | Panelist mobile app built and tested. End-to-end flow validated. All three personas tested by real users before end of day. |
| End of Day | Deployed to production. Not a pilot. Not a test environment. Production. |
| Next Morning | Supervisors entering nominations. HR reviewing eligibility. Panelists ready to score. The system was running before most development cycles would have finished sprint planning. |

## The Results
* Full multi-role nomination and scoring system in production in one 8-hour day.
* Three distinct user personas with separate, enforced security roles — no data leakage between roles.
* 500-point scoring model across five panelists, four questions each, tracked per nominee in Dataverse.
* Mobile scoring enabled — panelists scored from phones without any adaptation required.
* Zero rework. The architecture decisions made in the first hour held through production.

> **What It Proves**  *The speed wasn't luck and it wasn't cutting corners. It was the result of an architect making the right structural decisions fast, stakeholders who were in the room and trusted the process, and a delivery model that doesn't waste time on things that don't move the build forward. That's REDM.*


## The Reuse Value
The Dataverse schema, the security role architecture, and the three-app pattern built for this nomination system are reusable. Any future scoring, selection, or review process can build on this foundation. The next version of this system — or a new one for a different nomination cycle — starts from a working base, not from scratch.

In REDM, the first engagement doesn't just solve the immediate problem. It builds the layer that makes the next engagement faster.