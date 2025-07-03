#!/usr/bin/env python3
"""
edit_pdf_phi_data.py
--------------------
Utility script to anonymise / update PHI data in a pathology PDF report using PyMuPDF.

Usage
-----
    # Ensure you are inside the project root
    $ python -m venv venv  # if not already created
    $ source venv/bin/activate
    (venv)$ pip install PyMuPDF

    # Run the script with paths
    (venv)$ python general/scripts/edit_pdf_phi_data.py \
        --input "smf/data/pathology/Report Fri, Oct 04 - 2024.pdf" \
        --output "smf/data/pathology/Report Fri, Oct 04 - 2024_phi_redacted.pdf"

The script will
1. Search for occurrences of the original PHI fields in the PDF.
2. Overlay a white rectangle to cover the original values.
3. Write the supplied replacement text on top, keeping original labels / structure intact.

Limitations
-----------
- Relies on text search; works reliably if field labels (e.g. "Name", "Age / Sex", "Contact", "Order") are present on the page as plain text.
- Coordinates obtained via `page.search_for()` are text-bound. Complex layouts or scanned images will not be processed.
- Order number digits are preserved in length but randomized. Only numeric section after the first non-digit character sequence is altered.
"""

from __future__ import annotations

import argparse
import random
import re
from pathlib import Path

import fitz  # PyMuPDF

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _randomise_digits(value: str) -> str:
    """Return *value* with every digit replaced by a new random digit."""
    return re.sub(r"\d", lambda _: str(random.randint(0, 9)), value)


def _cover_and_write(page: fitz.Page, bbox: fitz.Rect, new_text: str, font_size: int = 10):
    """Cover *bbox* with a white rectangle and write *new_text* at the same position."""
    # Expand bbox slightly for full coverage
    rect = fitz.Rect(bbox.x0 - 1, bbox.y0 - 1, bbox.x1 + 1, bbox.y1 + 1)
    page.draw_rect(rect, color=(1, 1, 1), fill=(1, 1, 1))
    page.insert_text((rect.x0, rect.y1 - font_size), new_text, fontname="helv", fontsize=font_size, color=(0, 0, 0))


# ---------------------------------------------------------------------------
# Configuration – what to replace and with what
# ---------------------------------------------------------------------------

LABELS = {
    "name": {
        "label": "Name",
        "new_value": "Sura Karthikeya",
    },
    "age_sex": {
        "label": "Age / Sex",
        "new_value": "22 years / Male",
    },
    "contact": {
        "label": "Contact",
        "new_value": "9100109700",
    },
    "order": {
        "label": "Order",
        # new_value will be computed dynamically per document
    },
}

# ---------------------------------------------------------------------------
# Main logic
# ---------------------------------------------------------------------------

def process_pdf(input_path: Path, output_path: Path) -> None:
    doc = fitz.open(input_path)

    PAGE_MARGIN_RIGHT = 10  # safety margin before right border

    for page in doc:
        words = page.get_text("words")  # list of 9-tuples

        # Map (block,line) -> list of words to find next-word relationships easily.
        lines_index = {}
        for w in words:
            x0, y0, x1, y1, word, block_no, line_no, *_ = w
            lines_index.setdefault((block_no, line_no), []).append(w)

        # Store replacement draw instructions to run AFTER redaction.
        pending_writes: list[tuple[fitz.Point, str]] = []

        for key, cfg in LABELS.items():
            label = cfg["label"]
            label_rects = page.search_for(label)
            if not label_rects:
                continue

            for rect in label_rects:
                # Find any word that intersects with label rect (to capture block/line index)
                target_word = None
                for w in words:
                    wx0, wy0, wx1, wy1, wtext, block_no, line_no, *_ = w
                    if fitz.Rect(wx0, wy0, wx1, wy1).intersects(rect) and wtext == label:
                        target_word = w
                        break

                if not target_word:
                    continue

                _, wy0, _, wy1, _, block_no, line_no, *_ = target_word
                line_words = sorted(lines_index[(block_no, line_no)], key=lambda w: w[0])

                # Identify first value word appearing to the right of the label.
                label_x1 = rect.x1
                value_word = None
                for w in line_words:
                    if w[0] > label_x1:  # word starts after label
                        value_word = w
                        break

                # Determine rectangle covering the original value area (start of value word → right margin)
                if value_word:
                    vx0 = value_word[0] - 1
                else:
                    vx0 = label_x1 + 2  # fallback

                cover_rect = fitz.Rect(vx0, rect.y0 - 1, page.rect.x1 - PAGE_MARGIN_RIGHT, rect.y1 + 1)

                # Compute replacement text
                if key == "order":
                    if value_word is None:
                        continue
                    order_value = value_word[4]
                    prefix = re.match(r"^[^\d]+", order_value).group(0)
                    order_digits = _randomise_digits(order_value[len(prefix):])
                    new_value = f"{prefix}{order_digits}"
                else:
                    new_value = cfg["new_value"]

                # Add redaction annotation (to truly remove old content)
                page.add_redact_annot(cover_rect, fill=(1, 1, 1))

                # Store write instruction – align with value's original x start when available, else after label
                insert_x = vx0 + 1
                insert_point = fitz.Point(insert_x, cover_rect.y1 - 2)
                pending_writes.append((insert_point, new_value))

        # Apply redactions – if none are present PyMuPDF may raise, so ignore.
        try:
            page.apply_redactions()
        except RuntimeError:
            pass

        # Now write replacement texts
        for pt, txt in pending_writes:
            page.insert_text(pt, txt, fontname="helv", fontsize=10, color=(0, 0, 0))

    # Save result
    doc.save(output_path, incremental=False, deflate=True)
    doc.close()


# ---------------------------------------------------------------------------
# Entry-point
# ---------------------------------------------------------------------------

def _parse_args():
    p = argparse.ArgumentParser(description="Replace PHI data in a pathology report PDF.")
    p.add_argument("--input", required=True, type=Path, help="Path to source PDF (will not be modified).")
    p.add_argument("--output", required=True, type=Path, help="Path where sanitized copy will be written.")
    return p.parse_args()


if __name__ == "__main__":
    args = _parse_args()
    if not args.input.exists():
        raise SystemExit(f"Input file {args.input} does not exist")

    if args.output.exists():
        raise SystemExit(f"Output file {args.output} already exists – will not overwrite")

    process_pdf(args.input, args.output)
    print(f"Sanitized PDF written to {args.output}") 