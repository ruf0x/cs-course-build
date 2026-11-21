# CS Courses

My computer science courses as PowerPoint decks, for revision and for teaching.

Each topic is **one Markdown file** inside a field folder in `topics/`. A build script turns it into a styled `.pptx` in `decks/` and a PDF in `decks/pdf/`, in the same folder layout.
To change a course, edit the Markdown and rebuild. Don't edit the `.pptx` directly: the next build overwrites it.

```
cs-courses/
├── topics/                  ← the course content (edit these)
│   ├── _template.md               copy this into a field folder to start a topic
│   ├── algorithms/                01-big-o-notation.md
│   ├── enterprise-networking/     01-ipv4-subnetting.md
│   ├── network-security/          01-firewalls-and-acls.md
│   ├── red-team/                  01-recon-and-osint.md
│   └── blue-team/                 01-incident-response.md
├── images/                  ← pictures and diagrams used in slides
├── decks/                   ← generated .pptx files, one folder per field
│   └── pdf/                       the PDF copies, same folders
├── build.js         ← Markdown → PowerPoint, plus the design (colors, fonts)
└── lib/             ← helper used by the build
```

## Build

```bash
npm run build                                        # every topic in every field
node build.js topics/red-team                        # one whole field
node build.js topics/red-team/01-recon-and-osint.md  # just one topic
```

Pictures go in `images/`. A slide with a picture and bullets puts the text on the left and the picture on the right; a picture on its own is centered.

Each build writes the `.pptx` to `decks/` and, if LibreOffice is installed, a PDF copy to `decks/pdf/`.
Add `--no-pdf` to skip the PDF (it's faster).

If PowerPoint has the deck open, close it first, or the build can't overwrite the file.

## Writing a topic

Copy `topics/_template.md` into a field folder and rename it (`02-vlans.md`). Number the files so they sort in course order. Want a new field? Just make a new folder in `topics/`. Files whose names start with `_` are skipped.

| You write | You get |
|---|---|
| `---` front matter (`title`, `subtitle`, `course`, `author`) | Title slide |
| `# Section name` + a sentence | Section divider slide (and an entry on the auto agenda) |
| `## Slide title` | A new content slide |
| `- bullet`, indent two spaces for a sub-bullet | Bullet list. 5 or fewer short bullets are shown as numbered rows |
| `**bold**`, `` `code` `` | Bold text, inline code |
| `> sentence` | "Key idea" panel. On its own, it fills the slide as one big statement |
| `- **Term**: definition` (2–6 of them) | Term cards in a grid |
| `1. step` (2–5 of them) | Step-by-step process cards |
| fenced code block with a language | Code window, with the explanation bullets beside it |
| Markdown table | Styled table |
| `![caption](../../images/file.png)` | Picture with caption |
| `## ? Question` + bullets | Quiz: a question slide, then an answer slide |
| `Note: …` | Speaker notes (what to say when teaching) |

The layout for each slide is chosen from what the slide contains, so you never place boxes by hand.

## Changing the look

The decks use **JetBrains Mono** (installed on this PC). PDFs carry the font inside them, so they look the same everywhere; a `.pptx` opened on a PC without the font falls back to another one.

Your name (`AUTHOR`), the font (`FONT`) and the colors (`THEME`) are at the top of `build.js`. A topic can override the name with `author:` in its front matter. Change them, rebuild, and every deck updates.
