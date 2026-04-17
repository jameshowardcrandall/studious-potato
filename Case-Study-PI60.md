# Case Study — PI60

**Military Exercise Personnel Management**

---

## The Situation
PI60 was a large-scale military exercise with 5,000 soldiers arriving from across the force. Leadership needed real-time personnel accountability from the moment soldiers checked in through the duration of the mission — who was present, who was on leave, what their status was at the task force level, and how readiness rolled up to the mission general.

There was no existing system that could handle this. The timeline was fixed — the exercise had a start date that wouldn't move. A traditional development approach wasn't on the table.

> **The Problem**  *5,000 soldiers. A fixed exercise start date. No existing system. The mission needed accountability on day one — not at the end of a development cycle.*


## The REDM Approach
An architect-led Power Platform team built the PI60 system in under two months using REDM's rapid build cycle approach. Stakeholders were engaged throughout — not at the end of a sprint. The architecture was set early and locked, allowing the three components to be built in parallel with a shared Dataverse core.

The delivery pattern was IOC-first: get check-in working, get PERSTAT populated, get the dashboard visible to leadership — then refine. The exercise start date was the IOC. There was no negotiating with the calendar.

## The Architecture
Three components, one Dataverse core, designed for operational tempo:

| **Component** | **What It Does** | **Who Uses It** |
| --- | --- | --- |
| Canvas App — CAC Check-In | Scans a soldier's CAC card (Common Access Card) to read their identity data. If the soldier exists in Dataverse, they're checked in. If not, the user completes the record on the spot. Fast, mobile, works at scale. | Check-in staff at entry points |
| Power Pages Portal — Task Force PERSTAT | Commanders manage daily personnel status for their soldiers at the task force level. Default status is Present for all checked-in soldiers. Status changes carry forward until updated by an S1. No data entry required for routine accountability. | Commanders and S1 personnel |
| Power BI Dashboard — Mission Pulse | All personnel data rolls up to a real-time readiness dashboard visible to the mission general and senior leadership. Task force-level status, readiness trends, and exception reporting at a glance. | Mission general and senior leadership |

The data flow was intentional: check-in drives PERSTAT, PERSTAT drives the dashboard. Commanders don't build reports — they manage status. The dashboard builds itself.

## The Results
PI60 went live before the exercise started. On day one, soldiers were checking in via CAC scan. Commanders were updating PERSTAT from the portal. The mission general had a live readiness dashboard without anyone manually assembling a slide.

* 5,000 soldiers tracked in real time from day one of the exercise.
* CAC scanning eliminated manual check-in data entry entirely.
* Task force commanders had personnel status tooling purpose-built for their workflow — no spreadsheets, no manual reporting up the chain.
* Mission general had live readiness data without a separate reporting cycle.
* Delivered in under two months with a fixed, immovable exercise start date.

> **What It Proves**  *The exercise didn't wait for the system to be ready. The system had to be ready when the exercise started. REDM is built for exactly this kind of deadline — not because it cuts corners, but because it doesn't waste time on process that doesn't serve the mission.*


## The Reuse Potential
The PI60 architecture — CAC check-in, task force PERSTAT, leadership dashboard — is not specific to PI60. The same pattern applies to any organization that needs to account for personnel across a large, time-bounded event: training exercises, mobilizations, natural disaster response, joint operations.

REDM's delivery model didn't just build a system. It produced a reusable architectural pattern that can be stood up for the next exercise faster than it was built the first time.