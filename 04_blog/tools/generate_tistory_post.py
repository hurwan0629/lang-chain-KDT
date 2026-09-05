from __future__ import annotations

import html
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "workspace/personal/machinelearning/05_from_first_again/01_2026-08-08_from_first/01_how_to_make_ml_model.md"
STYLE = ROOT / "docs/blog/hurwan.tistory.com/templates/style.css"
OUTPUT = ROOT / "docs/blog/hurwan.tistory.com/build/05_How_To_Model_AI_machime.html"


EXTRA_CSS = """
.code-box,
.output-box {
  overflow-x: auto;
  margin: 14px 0;
  padding: 16px 18px;
  border: 1px solid rgba(148, 163, 184, 0.16);
  border-radius: 16px;
  background: #0f172a;
  color: #e2e8f0;
  font-family: "JetBrains Mono", "D2Coding", Consolas, monospace;
  font-size: 13px;
  line-height: 1.65;
  white-space: pre;
}

.code-box code,
.output-box code {
  padding: 0;
  border: 0;
  background: transparent;
  color: inherit;
  font: inherit;
}
"""


def inline(text: str) -> str:
    parts = re.split(r"(`[^`]+`)", text)
    rendered: list[str] = []
    for part in parts:
        if part.startswith("`") and part.endswith("`"):
            rendered.append(f"<code>{html.escape(part[1:-1])}</code>")
        else:
            rendered.append(html.escape(part))
    return "".join(rendered)


def render_blocks(lines: list[str]) -> str:
    out: list[str] = ['      <div class="post-card stack">']
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if not stripped:
            i += 1
            continue

        if stripped.startswith("```"):
            code_lines: list[str] = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("```"):
                code_lines.append(lines[i])
                i += 1
            if i < len(lines):
                i += 1
            out.append(f'<pre class="code-box"><code>{html.escape(chr(10).join(code_lines))}</code></pre>')
            continue

        if stripped.startswith("#### "):
            out.append(f"        <h3>{inline(stripped[5:])}</h3>")
            i += 1
            continue

        if stripped.startswith("### "):
            out.append(f"        <h3>{inline(stripped[4:])}</h3>")
            i += 1
            continue

        if stripped.startswith(">"):
            quote_lines: list[str] = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                quote_lines.append(lines[i].strip()[1:].strip())
                i += 1
            quote = " ".join(q for q in quote_lines if q)
            out.append(f'        <div class="post-note"><p>{inline(quote)}</p></div>')
            continue

        if re.match(r"^\d+\.\s+", stripped):
            items: list[str] = []
            while i < len(lines) and re.match(r"^\d+\.\s+", lines[i].strip()):
                items.append(re.sub(r"^\d+\.\s+", "", lines[i].strip()))
                i += 1
            out.append('        <ol class="numbered-list">')
            out.extend(f"          <li>{inline(item)}</li>" for item in items)
            out.append("        </ol>")
            continue

        if stripped.startswith("- "):
            items = []
            while i < len(lines) and lines[i].strip().startswith("- "):
                items.append(lines[i].strip()[2:])
                i += 1
            out.append('        <ul class="post-list">')
            out.extend(f"          <li>{inline(item)}</li>" for item in items)
            out.append("        </ul>")
            continue

        paragraph = [stripped]
        i += 1
        while i < len(lines):
            nxt = lines[i].strip()
            if (
                not nxt
                or nxt.startswith(("#", ">", "```", "- "))
                or re.match(r"^\d+\.\s+", nxt)
            ):
                break
            paragraph.append(nxt)
            i += 1
        out.append(f"        <p>{inline(' '.join(paragraph))}</p>")

    out.append("      </div>")
    return "\n".join(out)


def main() -> None:
    source = SOURCE.read_text(encoding="utf-8")
    lines = source.splitlines()
    title = lines[0].removeprefix("#").strip()
    subtitle = ""
    content_start = 1
    if len(lines) > 1 and lines[1].strip().startswith(">"):
        subtitle = lines[1].strip()[1:].strip()
        content_start = 2

    sections: list[tuple[str, list[str]]] = []
    current_title = ""
    current_lines: list[str] = []
    for line in lines[content_start:]:
        if line.startswith("## "):
            if current_title:
                sections.append((current_title, current_lines))
            current_title = line[3:].strip()
            current_lines = []
        elif line.startswith("# ") and line.strip() != lines[0].strip():
            if current_title:
                sections.append((current_title, current_lines))
            current_title = line[2:].strip()
            current_lines = []
        else:
            current_lines.append(line)
    if current_title:
        sections.append((current_title, current_lines))

    toc_items = []
    body_sections = []
    for index, (section_title, section_lines) in enumerate(sections, start=1):
        section_id = f"section-{index:02d}"
        toc_items.append(
            f'        <li><a href="#{section_id}"><span class="toc-index">{index:02d}</span><span class="toc-main">{inline(section_title)}</span></a></li>'
        )
        body_sections.append(
            "\n".join(
                [
                    f'    <section class="post-section" id="{section_id}">',
                    f'      <h2 class="section-title">{inline(section_title)}</h2>',
                    render_blocks(section_lines),
                    "    </section>",
                ]
            )
        )
        if index < len(sections):
            body_sections.append('    <hr class="post-divider">')

    css = STYLE.read_text(encoding="utf-8").rstrip() + "\n" + EXTRA_CSS.strip()
    document = f"""<!doctype html>
<html lang="ko">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)}</title>
  <style>
{css}
  </style>
</head>
<body>
  <article class="tech-post">
    <header class="post-hero">
      <div class="post-hero-inner">
        <p class="post-kicker">Machine Learning</p>
        <h1 class="post-title">{inline(title)}</h1>
        <p class="post-subtitle">{inline(subtitle)}</p>
      </div>
    </header>

    <details class="source-toggle">
      <summary>gpt가 디자인 하기 전 원본</summary>
      <pre class="source-box"><code>{html.escape(source)}</code></pre>
    </details>

    <nav class="post-toc">
      <strong>목차</strong>
      <ol>
{chr(10).join(toc_items)}
      </ol>
    </nav>

{chr(10).join(body_sections)}
  </article>
</body>
</html>
"""
    OUTPUT.write_text(document, encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()
