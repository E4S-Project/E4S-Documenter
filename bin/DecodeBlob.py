#!/usr/bin/env python3
"""DecodeBlob.py - Decode html_blob entries from a product-catalog.yml into HTML pages.

Usage:
    DecodeBlob.py <catalog.yml> <output_dir> [-p PRODUCT [PRODUCT ...]]

If no products are specified, all products are extracted.
If more than one product is requested an index.html is also generated.
"""

import argparse
import base64
import json
import os
import sys

HTML_WRAPPER = """\
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <style>
    body {{
      font-family: sans-serif;
      margin: 2em;
      max-width: 960px;
    }}
    .docsum {{
      white-space: pre-wrap;
      word-wrap: break-word;
      overflow-wrap: break-word;
      max-width: 100%;
      border-left: 3px solid #ccc;
      padding-left: 1em;
      margin: 0.5em 0 1em 0;
    }}
    details summary h3 {{
      display: inline;
    }}
    table, td, th {{
      border-collapse: collapse;
      border: 1px solid #aaa;
      padding: 0.3em 0.6em;
    }}
    h1 {{ border-bottom: 2px solid #333; }}
  </style>
</head>
<body>
<h1>{title}</h1>
{body}
</body>
</html>
"""

INDEX_WRAPPER = """\
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>E4S Product Catalog</title>
  <style>
    body {{ font-family: sans-serif; margin: 2em; max-width: 960px; }}
    h1 {{ border-bottom: 2px solid #333; }}
    ul {{ line-height: 1.8; }}
  </style>
</head>
<body>
<h1>E4S Product Catalog</h1>
<ul>
{items}
</ul>
</body>
</html>
"""


def load_catalog(path):
    """Load product-catalog.yml and return list of product dicts."""
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    # The file is valid JSON wrapped in YAML (it's just JSON with a "data" key)
    try:
        import yaml
        data = yaml.safe_load(content)
    except Exception:
        data = json.loads(content)
    if isinstance(data, dict) and "data" in data:
        return data["data"]
    if isinstance(data, list):
        return data
    raise ValueError("Unrecognised catalog format: expected {\"data\": [...]} or [...]")


def decode_blob(blob_str):
    """Base64-decode an html_blob string, tolerating whitespace."""
    cleaned = blob_str.replace("\n", "").replace("\r", "").replace(" ", "")
    return base64.b64decode(cleaned).decode("utf-8", errors="replace")


def safe_filename(name):
    """Convert a product name to a safe lowercase filename."""
    return name.lower().replace("/", "_").replace(" ", "_") + ".html"


def write_product_page(product, output_dir):
    """Decode and write a single product HTML page. Returns the output path."""
    name = product.get("name", "unknown")
    blob = product.get("html_blob", "")
    if not blob:
        print(f"WARNING: No html_blob for {name}, skipping.", file=sys.stderr)
        return None
    body_html = decode_blob(blob)
    full_html = HTML_WRAPPER.format(title=name, body=body_html)
    filename = safe_filename(name)
    out_path = os.path.join(output_dir, filename)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(full_html)
    return out_path


def write_index(products, output_dir):
    """Write an index.html linking to all product pages."""
    items = []
    for p in products:
        name = p.get("name", "unknown")
        area = p.get("area", "")
        desc = p.get("description", "")
        filename = safe_filename(name)
        area_str = f" &mdash; <em>{area}</em>" if area else ""
        desc_str = f": {desc}" if desc else ""
        items.append(
            f'  <li><a href="{filename}">{name}</a>{area_str}{desc_str}</li>'
        )
    index_html = INDEX_WRAPPER.format(items="\n".join(items))
    index_path = os.path.join(output_dir, "index.html")
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(index_html)
    return index_path


def main():
    parser = argparse.ArgumentParser(
        description="Decode html_blob entries from a product-catalog.yml into HTML pages."
    )
    parser.add_argument("catalog", help="Path to product-catalog.yml")
    parser.add_argument("output_dir", help="Directory to write HTML files into")
    parser.add_argument(
        "-p", "--products",
        nargs="+",
        metavar="PRODUCT",
        help="One or more product names to extract (case-insensitive). "
             "Omit to extract all products.",
    )
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)

    print(f"Loading catalog: {args.catalog}", file=sys.stderr)
    all_products = load_catalog(args.catalog)
    print(f"  {len(all_products)} products found.", file=sys.stderr)

    if args.products:
        requested = {p.lower() for p in args.products}
        selected = [p for p in all_products if p.get("name", "").lower() in requested]
        missing = requested - {p.get("name", "").lower() for p in selected}
        if missing:
            print(f"WARNING: Products not found: {', '.join(sorted(missing))}", file=sys.stderr)
    else:
        selected = all_products

    if not selected:
        print("ERROR: No matching products to extract.", file=sys.stderr)
        sys.exit(1)

    written = []
    for product in selected:
        out = write_product_page(product, args.output_dir)
        if out:
            print(f"  Written: {out}", file=sys.stderr)
            written.append(product)

    if len(written) > 1:
        index_path = write_index(written, args.output_dir)
        print(f"  Index:   {index_path}", file=sys.stderr)

    print(f"Done. {len(written)} page(s) written to {args.output_dir}", file=sys.stderr)


if __name__ == "__main__":
    main()
