# Proposed Sprint Plan — AccessiAI

These are planning baselines, not records of completed work. Dates should be copied from the faculty-approved schedule, not guessed.

## Sprint 1 — Core scanning foundation
**Goal:** Deliver a locally runnable application that can inspect a permitted public webpage and explain detected findings.

| ID | Work item | Owner proposal | Acceptance evidence |
|---|---|---|---|
| SB1-01 | Initialize Flask project and configuration | SR | App starts and home page loads |
| SB1-02 | Create Scan database model | SR | Scan record persists locally |
| SB1-03 | Implement public URL validation | VJ | Invalid/private URL tests pass |
| SB1-04 | Configure Playwright Chromium | VJ | Browser launches in test environment |
| SB1-05 | Integrate axe-core | VJ | Scan returns axe results on a test page |
| SB1-06 | Parse violations and affected nodes | VJ | Result payload contains rule, impact and count |
| SB1-07 | Add rule-based recommendations | SR | Known rules return useful guidance |
| SB1-08 | Build scan form and results UI | MS | User can submit URL and view findings |
| SB1-09 | Add loading, empty and error states | MS | UI handles success and failure clearly |
| SB1-10 | Run integration checks and document limits | All | Test log and known-limitations list |

## Sprint 2 — Personalization, history and deployment
**Goal:** Integrate user-facing accessibility controls, preserve scan records and prepare a verified cloud release.

| ID | Work item | Owner proposal | Acceptance evidence |
|---|---|---|---|
| SB2-01 | Add text-size controls | MS | Text scale changes within defined bounds |
| SB2-02 | Add high-contrast mode | MS | Contrast toggle changes page theme |
| SB2-03 | Add browser text-to-speech | MS | Read and stop controls work in supported browser |
| SB2-04 | Add scan history API and view | SR | Latest scans display after reload |
| SB2-05 | Improve scan error handling | SR | User-safe errors and rollback behavior |
| SB2-06 | Add health endpoint | SR | `/health` returns HTTP 200 |
| SB2-07 | Validate keyboard navigation | All | Manual checklist completed |
| SB2-08 | Validate screen-reader basics | All | Manual checklist completed |
| SB2-09 | Configure cloud deployment | SR + VJ | Build and start logs succeed |
| SB2-10 | Run deployed smoke test | All | Live URL and evidence captured |

## Sprint 3 — Proposed enhancements
Explore OCR/image accessibility support, expanded guidance and usability evaluation. Do not represent these as implemented until evidence exists.

## Sprint 4 — Proposed finalization
Refinement, regression testing, report completion, demonstration preparation and final release. Do not represent these as implemented until evidence exists.

## Team collaboration rule
The owner proposal identifies a primary contributor, not an excuse for other members to remain uninvolved. Each member should review the integrated work, contribute evidence and be able to explain the project during evaluation.
