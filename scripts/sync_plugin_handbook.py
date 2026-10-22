#!/usr/bin/env python3
"""Synchronize the two explicitly reviewed public plugin overview pages."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBLIC_INPUTS = {
    "handbook/public/overview.en.md": "content/docs/plugins/_index.md",
    "handbook/public/overview.zh.md": "content/docs/plugins/_index.zh.md",
}
LEGACY_REDIRECTS = {
    "/": "https://docs.cheesesec.com/docs/plugins/",
    "/README.md": "https://docs.cheesesec.com/docs/plugins/",
    "/docs/index.md": "https://docs.cheesesec.com/zh/docs/plugins/",
    "/zh/": "https://docs.cheesesec.com/zh/docs/plugins/",
}
PRIVATE_MARKERS = re.compile(
    r"cloudflare|\bworker\b|\br2\b|bucket|binding|wrangler|publish_[a-z_]+|"
    r"CLOUDFLARE_|127\.0\.0\.1|localhost|cloudflare-routing|"
    r"\b(?:10|192\.168|172\.(?:1[6-9]|2[0-9]|3[01]))\.\d+\.",
    re.IGNORECASE,
)


def safe_read(root: Path, name: str) -> bytes:
    if name.startswith("/") or "\\" in name or any(p in {"", ".", ".."} for p in name.split("/")):
        raise ValueError(f"unsafe public source: {name}")
    source = root / name
    for candidate in (source, *source.parents):
        if candidate == root:
            break
        if candidate.is_symlink():
            raise ValueError(f"public source has symlink: {name}")
    if not source.is_file():
        raise ValueError(f"public source is not a regular file: {name}")
    data = source.read_bytes()
    text = data.decode("utf-8")
    if "\0" in text or PRIVATE_MARKERS.search(text):
        raise ValueError(f"public overview contains a forbidden deployment detail: {name}")
    if not text.startswith('{"title":'):
        raise ValueError(f"public overview is missing its Hugo metadata: {name}")
    return data


def outputs(root: Path = ROOT) -> dict[str, bytes]:
    sources = {name: safe_read(root, name) for name in PUBLIC_INPUTS}
    generated = {PUBLIC_INPUTS[name]: data for name, data in sources.items()}
    manifest = {
        "format": "public-plugin-overviews-v2",
        "public_inputs": {name: hashlib.sha256(data).hexdigest() for name, data in sources.items()},
        "legacy_redirects": LEGACY_REDIRECTS,
        "outputs": sorted(generated),
    }
    generated["data/plugin_handbook.json"] = (json.dumps(manifest, ensure_ascii=False, indent=2) + "\n").encode()
    return generated


def synchronize(root: Path = ROOT, check: bool = False) -> dict[str, bytes]:
    root = root.resolve()
    generated = outputs(root)
    expected_pages = set(PUBLIC_INPUTS.values())
    for prefix in ("content/docs/plugins", "static/plugins/reference"):
        for candidate in (root / prefix).rglob("*"):
            if candidate.is_symlink() or (candidate.is_file() and candidate.relative_to(root).as_posix() not in expected_pages):
                raise ValueError(f"unreviewed plugin publication file: {candidate.relative_to(root)}")
    for name, data in generated.items():
        target = root / name
        for candidate in (target, *target.parents):
            if candidate == root:
                break
            if candidate.is_symlink():
                raise ValueError(f"output symlink is forbidden: {name}")
        if check:
            if not target.is_file() or target.read_bytes() != data:
                raise ValueError(f"plugin overview is stale: {name}")
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
    return generated


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    try:
        generated = synchronize(check=args.check)
    except (OSError, ValueError) as error:
        parser.exit(1, f"plugin overview sync failed: {error}\n")
    print(f"public plugin overviews {'verified' if args.check else 'synchronized'} ({len(generated)} outputs)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
