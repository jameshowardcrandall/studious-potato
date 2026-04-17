# REDM Engagement Kickoff Checklist

---

## Before Day One — Confirm Foundations
- [ ] Engagement sponsor confirmed and accessible for decisions throughout the engagement
- [ ] Mission owner / OPR identified by name and office
- [ ] Initial SMEs identified by name, office, and area of expertise
- [ ] Power Platform environment provisioning requested from your cloud/infrastructure team
- [ ] Dataverse environment licenses confirmed and committed for DEV, TEST, and PROD
- [ ] Security/IA contact identified for security baseline and compliance review
- [ ] Communication channel established (Teams, email list, or engagement workspace)
- [ ] CAC/PIV access confirmed for all team members needing environment access

## Day 1 — Mission Alignment Session
- [ ] Operational problem framed in the mission owner's own words and written down
- [ ] Pain points documented: current workarounds, friction points, and documented failures
- [ ] Personnel impacted identified: who will use the system, who will operate it, who will lead it
- [ ] Data domains sketched: what data exists today, what needs to be created, what must integrate
- [ ] Security baseline established: classification level, IL requirements, identity provider, access model
- [ ] Review cadence confirmed: Tue/Thu standing sessions until IOC
- [ ] Decision log location established and shared with all participants
- [ ] Roles confirmed: solution architect, product owner, Schema Owner, SMEs, security contact

## Days 2–3 — Environment and Schema Setup
- [ ] DEV environment created, configured, and accessible to the entire team
- [ ] Publisher prefix defined, documented, and shared with all developers
- [ ] Solution created in DEV environment (unmanaged, ready for development)
- [ ] Schema Owner designated by name and given explicit authority over data model decisions
- [ ] Naming conventions documented and socialized to all developers (entities, fields, processes, roles)
- [ ] Connection references created in the solution (no hardcoded values in plugins, flows, or formulas)
- [ ] Environment variables configured for URLs, endpoints, and credentials
- [ ] TEST environment provisioned or requested with provisioning date confirmed
- [ ] ALM pipeline stub configured: DEV → TEST promotion path ready, even if not yet used
- [ ] Initial security roles created based on persona map from Day 1 Mission Alignment
- [ ] All team members granted appropriate environment access with read/write/admin levels confirmed

## Days 3–5 — Co-Design Phase Kickoff
- [ ] Co-Design workshop scheduled with all required SMEs present for full duration
- [ ] Day 1 current-state walkthrough completed: legacy system, current data flows, pain points shown live
- [ ] First prototype built and demoed to stakeholders by end of Day 2 of Co-Design
- [ ] Core Dataverse schema drafted: primary entities, fields, relationships, and cardinality documented
- [ ] Schema Owner has reviewed and approved initial schema design
- [ ] Security role assignments mapped to personas identified in Mission Alignment
- [ ] First demo/review session scheduled on the engagement calendar for next week
- [ ] Product owner briefed on their role in leading future co-design walkthroughs and feedback sessions
- [ ] Decision log has first entries: schema decisions, security decisions, and deferred items recorded

## Before First Build Cycle Begins — Architecture Readiness Gates
| **Gate** | **Status** | **Notes** |
| Core schema is stable (primary entities defined, relationships mapped) |  |  |
| Schema Owner is designated and has reviewed the schema |  |  |
| Security roles exist for all personas |  |  |
| Environment variables and connection references are in place |  |  |
| ALM pipeline is configured for DEV → TEST promotion |  |  |
| Decision log is active and has at least one entry |  |  |
| Review cadence is confirmed with product owner |  |  |
| New team members have completed data model walkthrough |  |  |

## Ongoing — First Two Weeks
- [ ] Tuesday/Thursday engagement sessions running, with product owner or designee in attendance
- [ ] Stakeholder feedback being integrated same-day for Do Now items, or within 48 hours for Queue items
- [ ] Decision log updated after every session with outcomes, agreed architecture decisions, and deferred work
- [ ] Triage bucket applied to every incoming request: Do Now (this week), Queue (backlog), Escalate (sponsor decision)
- [ ] Architect reviewing DEV environment daily and signing off on schema changes before merge to TEST
- [ ] Schema changes going through Schema Owner approval before any field, relationship, or entity is created
- [ ] No new tables created without Schema Owner review and approval; no schema changes committed to main without architect sign-off

- [ ] A kickoff that skips environment setup and schema ownership documentation is borrowing against the build. You will pay it back with interest during validation. Do not skip this phase.