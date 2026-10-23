"""Check local page assets and content without relying on external services."""

from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tags = []

    def handle_starttag(self, tag, attrs):
        self.tags.append((self.getpos()[0], tag, dict(attrs)))


def main():
    errors = []
    source = (ROOT / "index.html").read_text(encoding="utf-8")
    page = Page()
    page.feed(source)
    ids = Counter(attrs["id"] for _, _, attrs in page.tags if "id" in attrs)
    errors.extend(f"Duplicate id: {name}" for name, count in ids.items() if count > 1)

    def check_reference(value, base, context):
        parts = urlsplit(value)
        if parts.scheme or parts.netloc:
            if parts.scheme not in ("https", "http", "mailto", "tel", "data", ""):
                errors.append(f"{context}: unsupported URL scheme: {value}")
            return
        if not value:
            errors.append(f"{context}: empty reference")
            return
        if not parts.path:
            if not parts.fragment or unquote(parts.fragment) not in ids:
                errors.append(f"{context}: missing fragment target: {value}")
            return
        target = (ROOT if parts.path.startswith("/") else base) / unquote(parts.path).lstrip("/")
        if not target.is_file():
            errors.append(f"{context}: missing file: {value}")

    styles = []
    for line, tag, attrs in page.tags:
        context = f"index.html:{line}"
        for attr in ("href", "src"):
            if attr in attrs:
                check_reference(attrs[attr], ROOT, context)
        if tag == "img":
            if not attrs.get("alt", "").strip():
                errors.append(f"{context}: figure needs descriptive alternative text")
            for size in ("width", "height"):
                if not attrs.get(size, "").isdigit():
                    errors.append(f"{context}: figure needs an explicit {size}")
        if tag == "link" and attrs.get("rel") == "stylesheet":
            styles.append(urlsplit(attrs["href"]).path.removeprefix("./"))
    errors.extend(f"Repeated stylesheet: {name}" for name, count in Counter(styles).items() if count > 1)

    for stylesheet in styles:
        path = ROOT / stylesheet
        if path.is_file():
            for match in re.finditer(r"url\(\s*['\"]?([^)'\"\s]+)", path.read_text(encoding="utf-8")):
                check_reference(match.group(1), path.parent, str(path.relative_to(ROOT)))

    for path in (ROOT / "static").rglob("*"):
        if path.is_file() and path.suffix in (".js", ".png", ".jpg", ".woff", ".woff2"):
            start = path.read_bytes()[:200].lstrip().lower()
            if start.startswith((b"<!doctype html", b"<html")):
                errors.append(f"Downloaded error page disguised as an asset: {path.relative_to(ROOT)}")

    for token in ("\ufffd", "Lorem ipsum", "G-PYVRSFMDRL", "Deformable Neural Radiance Fields"):
        if token in source:
            errors.append(f"Unexpected placeholder or encoding residue: {token!r}")
    for required in ("README.md", "THIRD_PARTY_NOTICES.md"):
        if not (ROOT / required).is_file():
            errors.append(f"Missing repository documentation: {required}")

    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print("Site checks passed: local references, figures, stylesheets, assets, and documentation.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
