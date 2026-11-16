#!/usr/bin/env python3
"""One-time import of the fullstack template's agent-docs (D8 step 1).

Renders the template's Handlebars agent-docs to static markdown:
- {{{docLink "path" "text" "skill"}}}      -> [text](path)
- {{{localHubLink "text" "skill"}}}        -> [text](./README.md)
- {{ lowerCase model.name }} / {{ model.name }} -> neutral model name
- \\{{ ... }}  (escaped Handlebars)        -> {{ ... }} literal
- {{#if x}}...{{/if}} inside code fences   -> kept verbatim (they are examples)
Drops domain/ (per-project, no longer generated).

Usage: render.py <template agent-docs dir> <out dir> [--model-name myapp]
"""
import argparse
import pathlib
import re
import sys

DOC_LINK = re.compile(r'\{\{\{\s*docLink\s+"([^"]*)"\s+"([^"]*)"(?:\s+"[^"]*")?\s*\}\}\}')
HUB_LINK = re.compile(r'\{\{\{\s*localHubLink\s+"([^"]*)"(?:\s+"[^"]*")?\s*\}\}\}')
MODEL_LOWER = re.compile(r'\{\{\s*lowerCase\s+model\.name\s*\\?\}\}')
MODEL_NAME = re.compile(r'\{\{\s*model\.name\s*\}\}')
ESCAPED = re.compile(r'\\(\{\{)')


def render(text: str, model: str) -> str:
    text = DOC_LINK.sub(lambda m: f"[{m.group(2)}]({m.group(1)})", text)
    text = HUB_LINK.sub(lambda m: f"[{m.group(1)}](./README.md)", text)
    text = MODEL_LOWER.sub(model.lower(), text)
    text = MODEL_NAME.sub(model, text)
    text = ESCAPED.sub(r"\1", text)
    return text


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("src")
    ap.add_argument("out")
    ap.add_argument("--model-name", default="myapp")
    a = ap.parse_args()
    src, out = pathlib.Path(a.src), pathlib.Path(a.out)
    n = 0
    for f in sorted(src.rglob("*.hbs")):
        rel = f.relative_to(src)
        if rel.parts[0] == "domain":
            continue
        dst = out / str(rel)[: -len(".hbs")]
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_text(render(f.read_text(), a.model_name))
        n += 1
    left = [str(p) for p in out.rglob("*.md") if re.search(r"\{\{\{?\s*(docLink|localHubLink|lowerCase)", p.read_text())]
    print(f"rendered {n} docs; unrendered helpers in {len(left)} files")
    for p in left:
        print("  ", p)
    return 1 if left else 0


if __name__ == "__main__":
    sys.exit(main())
