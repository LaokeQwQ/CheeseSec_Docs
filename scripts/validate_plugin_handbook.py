#!/usr/bin/env python3
"""Validate the two public plugin overviews and the withdrawn-content boundary."""
from __future__ import annotations

import argparse
import json
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit

from sync_plugin_handbook import LEGACY_REDIRECTS, ROOT, synchronize

WITHDRAWN = (
    "cloudflare-routing", "crp-development", "store-ota", "notification-plugins",
    "duckdb-extension", "examples/crp-v1", "examples/store-v1",
    "reference/crp-v1", "reference/store-v1", "plugins/reference/", "commercial-architecture",
)


class Page(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[str] = []
        self.ids: set[str] = set()

    def handle_starttag(self, tag: str, attributes: list[tuple[str, str | None]]) -> None:
        values = dict(attributes)
        if values.get("id"):
            self.ids.add(str(values["id"]))
        for field in ("href", "src"):
            if values.get(field):
                self.links.append(str(values[field]))


def validate(site: Path, root: Path = ROOT) -> tuple[int, int, int]:
    synchronize(root, check=True)
    manifest = json.loads((root / "data/plugin_handbook.json").read_text())
    if manifest["legacy_redirects"] != LEGACY_REDIRECTS:
        raise ValueError("legacy redirects must contain only the four overview routes")
    parsed: dict[Path, Page] = {}
    scanned = 0
    for path in site.rglob("*"):
        if not path.is_file() or path.suffix not in {".html", ".md", ".json", ".xml", ".txt"}:
            continue
        relative = path.relative_to(site).as_posix()
        text = path.read_text()
        if any(marker in relative or marker in text for marker in WITHDRAWN):
            raise ValueError(f"withdrawn plugin content remains in the site: {relative}")
        scanned += 1
        if path.suffix == ".html":
            page = Page()
            page.feed(text)
            parsed[path.resolve()] = page
    if any(path.is_file() for path in (site / "plugins/reference").rglob("*")):
        raise ValueError("raw plugin reference downloads remain in the site")
    local_links = 0
    for language in ("en", "zh"):
        prefix = "/zh" if language == "zh" else ""
        relative = prefix.lstrip("/") + "/docs/plugins/index.html"
        path = site / relative.lstrip("/")
        if not path.is_file():
            raise ValueError(f"public plugin overview missing: {relative}")
        page = parsed[path.resolve()]
        base = f"https://docs.cheesesec.com{prefix}/docs/plugins/"
        destinations = [urlsplit(urljoin(base, link)).path for link in page.links]
        if not all(route in destinations for route in ("/docs/plugins/", "/zh/docs/plugins/")):
            raise ValueError(f"missing bilingual overview navigation: {relative}")
        if not any(urlsplit(link).netloc == "store.cheesesec.com" for link in page.links):
            raise ValueError(f"missing plugin store link: {relative}")
        for link in page.links:
            destination = urlsplit(urljoin(base, link))
            if destination.scheme not in {"http", "https"} or destination.netloc != "docs.cheesesec.com":
                continue
            target = site / unquote(destination.path).lstrip("/")
            if target.is_dir() or destination.path.endswith("/"):
                target /= "index.html"
            target = target.resolve()
            if site.resolve() not in target.parents or not target.is_file():
                raise ValueError(f"broken local link: {relative}: {link}")
            if destination.fragment and target in parsed and unquote(destination.fragment) not in parsed[target].ids:
                raise ValueError(f"missing local anchor: {relative}: {link}")
            local_links += 1
        indexes = list(site.glob(f"offline-search-index.{language}.*.json"))
        if len(indexes) != 1 or f"{prefix}/docs/plugins/" not in indexes[0].read_text():
            raise ValueError(f"public overview missing from {language} search index")
    return 2, local_links, scanned


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("site", type=Path)
    args = parser.parse_args()
    try:
        count, links, scanned = validate(args.site.resolve())
    except (OSError, ValueError, KeyError) as error:
        parser.exit(1, f"public plugin overview validation failed: {error}\n")
    print(f"public plugin overviews validated ({count} languages, {links} local links, {scanned} publication files scanned)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
