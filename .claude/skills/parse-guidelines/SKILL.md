# Skill: /parse-guidelines

**Trigger phrases:** `/parse-guidelines`, "parse journal guidelines", "extract journal requirements", "set up guidelines for [journal]"

---

## Instructions

Extract structured requirements from journal author guidelines and save to `guidelines/[journal-name].yml`.

### Arguments

```
/parse-guidelines [journal-name] [URL or "paste"]
```

- `[journal-name]`: Short identifier for the journal (lowercase, hyphenated). Example: `lancet-eb`, `nejm`, `plos-one`
- `[URL or "paste"]`: URL to the journal's author instructions page, OR the word "paste" to enter text manually

### Step-by-Step Workflow

**Step 1: Obtain the guidelines**

If URL given:
- Launch `guidelines-extractor` agent with the URL
- Agent uses WebFetch to retrieve the page
- If page is inaccessible or behind login: ask user to paste the text and re-run with "paste"

If "paste" given:
- Ask user: "Please paste the journal's author guidelines text now."
- Wait for user to paste text
- Pass pasted text to `guidelines-extractor` agent

**Step 2: Extract and save**

The `guidelines-extractor` agent:
- Parses all requirements from the guidelines text
- Writes `guidelines/[journal-name].yml`
- Returns a human-readable summary

**Step 3: Present summary**

Display the summary from the agent. Then ask:
> "Does this look correct? If any requirements are missing or wrong, let me know and I'll update the YAML."

**Step 4: Confirm and ready**

Once user confirms, respond:
> "Guidelines for [journal-name] saved to `guidelines/[journal-name].yml`. You can now run `/format-manuscript [file] [journal-name]`."

---

## Examples

```
/parse-guidelines lancet-eb https://www.thelancet.com/pb/assets/raw/Lancet/authors/lancet-information-for-authors.pdf
```

```
/parse-guidelines nejm paste
```

```
/parse-guidelines plos-one https://journals.plos.org/plosone/s/submission-guidelines
```

---

## Troubleshooting

- **Page requires login / returns 403:** Ask user to paste the guidelines text directly.
- **PDF guidelines:** WebFetch may not handle PDFs well. Ask user to copy-paste text from the PDF.
- **YAML validation error after writing:** Open the file and check for unescaped special characters in strings. YAML strings with colons need quotes.
- **Requirements seem incomplete:** Check if the journal has separate pages for different article types (Research Article, Review, etc.). Ask user which article type they are submitting.
