
// ==========================================
// ACCESSIAI - WEBSITE ACCESSIBILITY SCANNER
// ==========================================

const form = document.getElementById('scan-form');
const button = document.getElementById('scan-button');
const loading = document.getElementById('loading');
const errorBox = document.getElementById('error');
const results = document.getElementById('results');

form.addEventListener('submit', async (event) => {
    event.preventDefault();

    errorBox.classList.add('hidden');
    results.classList.add('hidden');
    loading.classList.remove('hidden');
    button.disabled = true;

    try {
        const response = await fetch('/api/scan', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                url: document.getElementById('url').value
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'The scan could not be completed.');
        }

        document.getElementById('result-title').textContent =
            data.title || 'Scan results';

        document.getElementById('result-url').textContent = data.url;
        document.getElementById('score').textContent = data.score;
        document.getElementById('score-note').textContent = data.score_note;
        document.getElementById('violations').textContent = data.violation_count;
        document.getElementById('passes').textContent = data.passes;
        document.getElementById('incomplete').textContent = data.incomplete;

        const list = document.getElementById('issue-list');
        list.replaceChildren();

        if (!data.violations.length) {
            const p = document.createElement('p');
            p.className = 'empty';
            p.textContent =
                'No violations were reported by the selected automated checks. Manual testing is still recommended.';
            list.append(p);
        }

        data.violations.forEach(v => {
            const card = document.createElement('article');
            card.className = 'issue';

            const head = document.createElement('div');
            head.className = 'issue-head';

            const title = document.createElement('h4');
            title.textContent = v.title;

            const severity = document.createElement('span');
            severity.className = 'severity ' + (v.impact || 'moderate');
            severity.textContent =
                (v.impact || 'moderate') + ' · ' + v.count + ' affected';

            head.append(title, severity);

            const desc = document.createElement('p');
            desc.textContent = v.description;

            const advice = document.createElement('p');
            advice.textContent = v.recommendation;

            const id = document.createElement('code');
            id.textContent = v.id;

            card.append(head, desc, advice, id);
            list.append(card);
        });

        results.classList.remove('hidden');
        results.scrollIntoView({ behavior: 'smooth', block: 'start' });

    } catch (err) {
        errorBox.textContent = err.message;
        errorBox.classList.remove('hidden');

    } finally {
        loading.classList.add('hidden');
        button.disabled = false;
    }
});


// ==========================================
// ACCESSIBILITY CODE OPTIMIZER
// ==========================================

const htmlCode = document.getElementById('html-code');
const htmlFile = document.getElementById('html-file');

const analyzeCodeButton = document.getElementById('analyze-code-button');
const clearCodeButton = document.getElementById('clear-code-button');

const codeLoading = document.getElementById('code-loading');
const codeError = document.getElementById('code-error');
const codeResults = document.getElementById('code-results');

const codeIssueList = document.getElementById('code-issue-list');


// Upload HTML file and read its contents
htmlFile.addEventListener('change', async () => {
    const file = htmlFile.files[0];

    if (!file) return;

    codeError.classList.add('hidden');

    const validExtension = /\.(html|htm)$/i.test(file.name);

    if (!validExtension) {
        codeError.textContent = 'Please upload an HTML or HTM file.';
        codeError.classList.remove('hidden');
        htmlFile.value = '';
        return;
    }

    if (file.size > 500 * 1024) {
        codeError.textContent = 'File is too large. Maximum size is 500 KB.';
        codeError.classList.remove('hidden');
        htmlFile.value = '';
        return;
    }

    try {
        htmlCode.value = await file.text();
        codeResults.classList.add('hidden');

    } catch {
        codeError.textContent = 'Unable to read this file.';
        codeError.classList.remove('hidden');
    }
});


// Analyze pasted or uploaded HTML
analyzeCodeButton.addEventListener('click', async () => {
    const source = htmlCode.value;

    codeError.classList.add('hidden');
    codeResults.classList.add('hidden');

    if (!source.trim()) {
        codeError.textContent = 'Please paste HTML code or upload an HTML file.';
        codeError.classList.remove('hidden');
        return;
    }

    codeLoading.classList.remove('hidden');
    analyzeCodeButton.disabled = true;

    try {
        const response = await fetch('/api/analyze-code', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                code: source
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Code analysis failed.');
        }

        // Display summary
        document.getElementById('code-result-title').textContent =
            'HTML accessibility analysis';

        document.getElementById('code-issue-count').textContent =
            data.issue_count;

        document.getElementById('code-status').textContent =
            data.issue_count > 0 ? 'Issues found' : 'No issues found';

        document.getElementById('code-result-message').textContent =
            data.message;

        document.getElementById('code-result-note').textContent =
            data.note;

        // Display detected issues
        codeIssueList.replaceChildren();

        if (data.issues.length === 0) {
            const message = document.createElement('p');
            message.className = 'empty';
            message.textContent =
                'No issues were detected by the current static checks. Manual testing is still recommended.';

            codeIssueList.append(message);
        }

        data.issues.forEach(issue => {
            const card = document.createElement('article');
            card.className = 'issue';

            const heading = document.createElement('div');
            heading.className = 'issue-head';

            const title = document.createElement('h4');
            title.textContent = issue.title;

            const severity = document.createElement('span');
            severity.className =
                'severity ' + (issue.impact || 'moderate');

            severity.textContent = issue.impact || 'moderate';

            heading.append(title, severity);

            const description = document.createElement('p');
            description.textContent = issue.description;

            const recommendation = document.createElement('p');
            recommendation.textContent =
                'Recommendation: ' + issue.recommendation;

            const exampleLabel = document.createElement('p');
            exampleLabel.textContent = 'Suggested code example:';

            const example = document.createElement('pre');
            const code = document.createElement('code');

            code.textContent = issue.example || '';
            example.append(code);

            const issueId = document.createElement('code');
            issueId.textContent = 'Rule: ' + issue.id;

            card.append(
                heading,
                description,
                recommendation,
                exampleLabel,
                example,
                issueId
            );

            codeIssueList.append(card);
        });

        codeResults.classList.remove('hidden');

        codeResults.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
        });

    } catch (err) {
        codeError.textContent = err.message;
        codeError.classList.remove('hidden');

    } finally {
        codeLoading.classList.add('hidden');
        analyzeCodeButton.disabled = false;
    }
});


// Clear editor
clearCodeButton.addEventListener('click', () => {
    htmlCode.value = '';
    htmlFile.value = '';

    codeResults.classList.add('hidden');
    codeError.classList.add('hidden');
});


// ==========================================
// PERSONALIZATION FEATURES
// ==========================================

// Text size
let textScale = 1;

document.getElementById('smaller').addEventListener('click', () => {
    textScale = Math.max(0.85, textScale - 0.05);

    document.documentElement.style.setProperty(
        '--body-scale',
        textScale
    );
});

document.getElementById('larger').addEventListener('click', () => {
    textScale = Math.min(1.3, textScale + 0.05);

    document.documentElement.style.setProperty(
        '--body-scale',
        textScale
    );
});


// High contrast
document.getElementById('contrast').addEventListener('change', (event) => {
    document.body.classList.toggle(
        'high-contrast',
        event.target.checked
    );
});


// Text-to-speech
document.getElementById('read-page').addEventListener('click', () => {
    if (!('speechSynthesis' in window)) {
        alert('Speech is not supported in this browser.');
        return;
    }

    speechSynthesis.cancel();

    const text = document.querySelector('main').innerText;

    speechSynthesis.speak(
        new SpeechSynthesisUtterance(text)
    );
});


// Stop speech
document.getElementById('stop-reading').addEventListener('click', () => {
    if ('speechSynthesis' in window) {
        speechSynthesis.cancel();
    }
});
