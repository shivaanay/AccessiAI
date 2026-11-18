
from html.parser import HTMLParser


class AccessibilityParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.issues = []
        self.labels = set()
        self.inputs = []
        self.heading_levels = []
        self.html_language = False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)

        if tag == "html":
            self.html_language = bool(attrs.get("lang"))

        if tag == "img":
            if "alt" not in attrs:
                self.issues.append({
                    "id": "image-alt",
                    "title": "Image missing alternative text",
                    "impact": "critical",
                    "description": "An image does not have an alt attribute.",
                    "recommendation": "Add descriptive alternative text using the alt attribute.",
                    "example": '<img src="photo.jpg" alt="Description of the image">'
                })

        if tag == "label" and attrs.get("for"):
            self.labels.add(attrs["for"])

        if tag == "input":
            self.inputs.append(attrs)

        if tag in ("button", "a"):
            if not attrs.get("aria-label") and not attrs.get("title"):
                self.issues.append({
                    "id": "interactive-name",
                    "title": f"{tag.capitalize()} may lack an accessible name",
                    "impact": "serious",
                    "description": f"A {tag} has no aria-label or title attribute. Its text content may still provide a name.",
                    "recommendation": f"Ensure the {tag} has a meaningful accessible name.",
                    "example": f'<{tag} aria-label="Describe the action">...</{tag}>'
                })

        if tag.startswith("h") and len(tag) == 2 and tag[1].isdigit():
            self.heading_levels.append(int(tag[1]))

    def finish(self):
        if not self.html_language:
            self.issues.append({
                "id": "html-lang",
                "title": "Page language is not declared",
                "impact": "moderate",
                "description": "The HTML element does not declare a language.",
                "recommendation": "Add a lang attribute to the HTML element.",
                "example": '<html lang="en">'
            })

        for attrs in self.inputs:
            input_id = attrs.get("id")
            input_type = attrs.get("type", "text")

            if input_type in ("hidden", "submit", "button", "reset"):
                continue

            has_label = (
                input_id in self.labels
                or bool(attrs.get("aria-label"))
                or bool(attrs.get("aria-labelledby"))
            )

            if not has_label:
                self.issues.append({
                    "id": "input-label",
                    "title": "Form input may lack an accessible label",
                    "impact": "serious",
                    "description": "An input has no associated label or accessible name.",
                    "recommendation": "Associate a label with the input or provide an accessible name.",
                    "example": '<label for="email">Email</label>\n<input id="email" type="email">'
                })

        for previous, current in zip(
            self.heading_levels, self.heading_levels[1:]
        ):
            if current > previous + 1:
                self.issues.append({
                    "id": "heading-order",
                    "title": "Heading levels may skip",
                    "impact": "moderate",
                    "description": "The heading hierarchy skips one or more levels.",
                    "recommendation": "Use a logical heading order without unnecessary level jumps.",
                    "example": "<h2>Section</h2>\n<h3>Subsection</h3>"
                })
                break


def analyze_html(source):
    if not source or not source.strip():
        raise ValueError("Please paste HTML code or upload an HTML file.")

    if len(source) > 500_000:
        raise ValueError("The HTML file is too large. Maximum size is 500 KB.")

    parser = AccessibilityParser()

    try:
        parser.feed(source)
        parser.close()
    except Exception as exc:
        raise ValueError("The supplied HTML could not be parsed.") from exc

    parser.finish()

    return {
        "issue_count": len(parser.issues),
        "issues": parser.issues,
        "message": (
            "Potential accessibility issues were found."
            if parser.issues
            else "No issues were detected by these basic checks."
        ),
        "note": "This is a preliminary static analysis, not a complete WCAG audit."
    }
