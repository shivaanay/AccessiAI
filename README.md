# AccessiAI — AI-Assisted Accessibility Framework

AccessiAI is a student-built web prototype for inspecting public webpages for selected automated accessibility barriers and presenting understandable improvement guidance. It also demonstrates display preferences and browser speech assistance.

## MVP functionality
- Public webpage scan using Playwright and axe-core WCAG 2.0/2.1 A/AA rule tags.
- Violation summaries, affected-node counts, examples and rule-based recommendations.
- SQLite scan history and a JSON history endpoint.
- Text scaling, high-contrast demonstration mode and browser text-to-speech.
- Responsive dashboard and health endpoint.

## Important limitations
- This is an educational prototype, not a WCAG certification or conformance assessment. Automated checks cannot identify every accessibility barrier; manual keyboard and assistive-technology testing remains necessary.
- The displayed score is an illustrative indicator based on violation instances. It is not a recognized accessibility score.
- Recommendations are transparent rule-based guidance, not output from a trained AI model.
- Only scan public sites you own or have permission to test. Request interception rechecks destinations, but a production service still needs stronger network isolation, rate limiting, quotas, monitoring and security review.
- SQLite is suitable for local development. Cloud deployments with ephemeral filesystems need a persistent disk or managed database before relying on scan history.

## Local setup on macOS
1. Install Python 3.11+ and VS Code.
2. Open this folder in VS Code.
3. In the VS Code terminal run:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
playwright install chromium
python run.py
```

4. Open `http://127.0.0.1:5000`. The health check is at `/health`.

## Tests
Install development dependencies and run:

```bash
pip install -r requirements-dev.txt
python -m unittest discover -s tests -v
```

## GitHub
Create a repository named `ai-accessibility-framework`, then run from this folder:

```bash
git init
git add .
git commit -m "Initial AccessiAI MVP"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/ai-accessibility-framework.git
git push -u origin main
```

Replace `YOUR-USERNAME`. Never commit secrets, virtual environments or local database files.

## Cloud deployment
`render.yaml` is a deployment starting point, not proof of a successful deployment. Confirm the current Render plan limits, Chromium installation and persistent database configuration. Perform an end-to-end scan on the deployed service before recording deployment as complete.
