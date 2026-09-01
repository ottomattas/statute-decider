"""Render the full Road Traffic Act to PDF with the used provisions highlighted.

The point for students: a real act is enormous, and a concrete service
touches only a handful of provisions. The PDF shows the whole act with the
renewal-relevant paragraphs marked in yellow, so the "find your few
paragraphs in the big law" step of the workflow is visible.

Usage (from the repo root; requires `uv pip install fpdf2`):

    .venv/bin/python examples/teaching/renew_driving_licence/highlight_law.py

Reads  data/statutes/driving_licence_renewal/road_traffic_act_en_full.txt
Writes data/statutes/driving_licence_renewal/road_traffic_act_en_highlighted.pdf
"""

from __future__ import annotations

from pathlib import Path

from fpdf import FPDF

HERE = Path(__file__).resolve().parent
STATUTE_DIR = HERE / "data" / "statutes" / "driving_licence_renewal"
SOURCE = STATUTE_DIR / "road_traffic_act_en_full.txt"
TARGET = STATUTE_DIR / "road_traffic_act_en_highlighted.pdf"

FONT_DIR = Path("/System/Library/Fonts/Supplemental")

# A paragraph is highlighted when it starts with one of these strings.
# Together they are every provision the renewal service decision uses.
HIGHLIGHT_PREFIXES = [
    # state fee for issuing/replacing a licence
    "(9) A state fee is payable for issuing or replacing a driving licence.",
    # right to drive proven by the motor register (within § 96 (7))
    "(7) At the time of formalisation of a provisional driving licence",
    # ten-year validity of category B licences
    "(7) A driving licence for motor vehicles of categories AM, A, B and T",
    # issue/replacement by the Transport Administration
    "(1) Provisional driving licences and driving licences are issued, replaced",
    # replacement application, ten working days
    "(2) Provisional driving licences and driving licences are issued within ten working days",
    # no licence while the right to drive is suspended/withdrawn
    "(3) A provisional driving licence and a driving licences is not issued",
    # medical certificate proves compliance with health requirements
    "(1) The state of health of a motor vehicle driver and applicant",
    # certificate arrives via the health information system
    "(8) Upon arrival of the due date for the next medical examination",
]

HIGHLIGHTED_SECTIONS = {"§ 96.", "§ 97.", "§ 98.", "§ 101."}


def main() -> None:
    paragraphs = [p for p in SOURCE.read_text(encoding="utf-8").split("\n")]

    pdf = FPDF(format="A4")
    pdf.set_margins(18, 16, 18)
    pdf.set_auto_page_break(auto=True, margin=16)
    pdf.add_font("Arial", "", FONT_DIR / "Arial.ttf")
    pdf.add_font("Arial", "B", FONT_DIR / "Arial Bold.ttf")
    pdf.add_page()

    # Cover note
    pdf.set_font("Arial", "B", 15)
    pdf.multi_cell(0, 7, "Road Traffic Act — full text, with the provisions used by the driving licence renewal service highlighted")
    pdf.ln(2)
    pdf.set_font("Arial", "", 9.5)
    pdf.multi_cell(
        0,
        4.8,
        "Official English translation: https://www.riigiteataja.ee/en/akt/527072026001\n"
        "Legally binding Estonian consolidated text (RT I, 11.07.2026, 44): "
        "https://www.riigiteataja.ee/et/akt/111072026044\n\n"
        "Yellow paragraphs are the only provisions the renewal decision needs: "
        "§ 96 (7) and (9), § 97 (7), § 98 (1)-(3), § 101 (1) and (8). "
        "Everything else in this act is real, in force, and irrelevant to this one service — "
        "finding your few paragraphs inside the big law is the first step of the workflow.",
    )
    pdf.ln(4)

    section = ""
    for para in paragraphs:
        text = para.strip()
        if not text:
            continue
        is_heading = text.startswith(("§ ", "Chapter ", "Subchapter ", "Division "))
        if text.startswith("§ "):
            section = text.split(maxsplit=2)[0] + " " + text.split(maxsplit=2)[1]
        highlight = section in HIGHLIGHTED_SECTIONS and any(
            text.startswith(prefix) for prefix in HIGHLIGHT_PREFIXES
        )
        if is_heading:
            pdf.set_font("Arial", "B", 9.5)
            pdf.ln(1.5)
        else:
            pdf.set_font("Arial", "", 8.5)
        if highlight:
            pdf.set_fill_color(255, 235, 120)
            pdf.multi_cell(0, 4.2, text, fill=True)
        else:
            pdf.multi_cell(0, 4.2, text)
        pdf.ln(0.6)

    pdf.output(str(TARGET))
    print(f"wrote {TARGET} ({TARGET.stat().st_size / 1e6:.1f} MB, {pdf.page_no()} pages)")


if __name__ == "__main__":
    main()
