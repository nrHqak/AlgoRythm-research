#!/usr/bin/env python3
"""Render the РКНП companion documents (research diary, supervisor review draft)
from their Markdown sources into DOCX, using exactly the same page geometry,
font and heading styles as the main submission.

Sources (authored by hand, no generated content):
  paper/RKNP_RESEARCH_DIARY_RU.md
  paper/RKNP_SUPERVISOR_REVIEW_DRAFT_RU.md
"""

from __future__ import annotations

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from build_rknp_submission import (  # noqa: E402
    PAPER,
    parse_blocks,
    register_fonts,
    render_docx,
)

DOCS = [
    ("RKNP_RESEARCH_DIARY_RU.md", "RKNP_RESEARCH_DIARY_RU.docx"),
    ("RKNP_SUPERVISOR_REVIEW_DRAFT_RU.md", "RKNP_SUPERVISOR_REVIEW_DRAFT_RU.docx"),
]


def main() -> None:
    register_fonts()
    for src, dst in DOCS:
        md = (PAPER / src).read_text(encoding="utf-8")
        md = md.replace("\n---\n", "\n")          # horizontal rules -> spacing
        blocks = parse_blocks(md, [])
        render_docx(blocks, [], out_path=PAPER / dst,
                    break_before_first_h1=False)
        print("wrote", dst)


if __name__ == "__main__":
    main()
