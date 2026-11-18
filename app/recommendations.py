"""Transparent, rule-based guidance for common axe-core accessibility findings."""

GUIDANCE = {
    "image-alt": ("Add meaningful alternative text", "Give informative images concise alt text that communicates their purpose. Use alt=\"\" for purely decorative images."),
    "label": ("Give form controls accessible names", "Associate each input with a visible label, or provide an appropriate accessible name."),
    "color-contrast": ("Improve text colour contrast", "Adjust foreground and background colours to meet WCAG contrast requirements. Check normal and large text separately."),
    "button-name": ("Name the button", "Add visible text or an accessible name that clearly describes the button action."),
    "link-name": ("Make link purpose clear", "Use descriptive link text instead of vague labels such as 'click here'."),
    "html-has-lang": ("Declare the page language", "Set the lang attribute on the html element, for example lang=\"en\"."),
    "document-title": ("Add a descriptive page title", "Provide a unique, meaningful title in the document head."),
    "heading-order": ("Use a logical heading hierarchy", "Organize headings by topic and level. Avoid skipping levels for visual styling."),
    "landmark-one-main": ("Provide a main landmark", "Use one main element to identify the primary content of the page."),
}

def explain_violation(item):
    rule = item.get("id", "")
    title, advice = GUIDANCE.get(rule, ("Review this accessibility issue", item.get("help", "Review the affected element and the rule description.")))
    return {"title": title, "recommendation": advice}
