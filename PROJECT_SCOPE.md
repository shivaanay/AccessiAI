# AccessiAI — Project Scope and Delivery Baseline

## Project title
AI Framework for Accessibility Optimization for Disabled Users

## Product concept
AccessiAI is a web-based educational prototype that helps developers inspect public webpages for selected accessibility barriers, understand the findings and explore practical improvements. It also demonstrates interface personalization and speech assistance.

## MVP modules
1. Automated public webpage inspection using Playwright and axe-core.
2. Categorized findings with impact, affected-node counts and examples.
3. Transparent rule-based explanations and improvement suggestions.
4. Demonstration preferences: text scaling and high contrast.
5. Browser-based text-to-speech.
6. Scan history and health endpoint.

## Proposed sprint goals
- **SB1:** application foundation, database, browser automation, accessibility scan, finding extraction and recommendation mapping.
- **SB2:** preference controls, speech assistance, scan history, integration, testing and deployment preparation.
- **SB3:** usability improvements, expanded rule guidance, OCR/image-accessibility exploration and additional validation.
- **SB4:** refinement, documentation, evaluation and final release preparation.

SB3 and SB4 are proposed future work. Sprint scope and dates must be confirmed against faculty instructions.

## Proposed ownership (not evidence of completed work)
- **Shivani Rajput (SR):** Flask backend, integration, coordination and test tracking.
- **Veer Jain (VJ):** scanner behavior, axe rule interpretation and validation.
- **Mumuksha Sharma (MS):** frontend, personalization, speech controls and usability review.

All members should review and understand the integrated application.

## Acceptance criteria for the MVP
- The application starts locally without an unhandled error.
- The home page and health endpoint respond successfully.
- Invalid, credential-bearing and private-network URLs are rejected.
- A permitted public webpage can be scanned in a configured environment with Playwright Chromium.
- Findings are displayed with rule identifier, impact, description, affected count and guidance.
- A completed scan is recorded in the configured database.
- Text size, contrast and speech controls work in a supported browser.
- The team performs manual keyboard and screen-reader checks and documents limitations.
- Deployment is marked complete only after a live URL and successful smoke test exist.

## Evidence and reporting policy
Never mark work complete without implementation evidence. Burndown actuals must be based on daily remaining-work records. Planned features are not results. The tool's indicative score is not WCAG certification.
