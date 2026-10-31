#!/usr/bin/env python3
"""Extract the 10,000 MCQs from the Lok Sewa Prep Nepal PDF into structured JSON.

Source PDF: ~/workspace/user/files/loksewa-10000-new-questions-answer-key_0_3hfx.pdf
  Title: "Lok Sewa Prep Nepal — 10,000 New Exam Questions & Master Answer Key (2082/83 BS)"
  919 pages, real text layer (Chrome/Skia print-to-PDF, NOT scanned).

Layout facts (verified by inspection 2026-10-27):
  * Questions Q1-Q10000, one per block, start at line start as "Q<n>. ".
  * 25 sections, each introduced by a line "Section N: <Topic> (Q<a>-Q<b> - <count> New Questions)".
  * Each question: stem text, then options inline as
        (A) <opt> • (B) <opt> • (C) <opt> • (D) <opt>
    where "•" (U+2022) is the separator. Every question block contains exactly 3 bullets.
  * No explanations anywhere in the PDF (no "explanation" string).
  * Master answer key is a grid at the very end, after the heading
        "Master Answer Key & Verified Correct Responses (Q1-Q10,000)"
    with entries "Q<n>(<A|B|C|D>)". Answers are recorded exactly as printed; nothing is "fixed".
  * Page headers ("LOK SEWA PREP NEPAL ...") and footers ("Zero-Duplicate Verified
    Expansion Set ... Page N of 919") repeat on every page and can land mid-question
    when a question spans a page break; they are stripped line-wise.
  * Quirks handled:
      - Option text may contain "(A)"/"(B)"/"(C)" look-alikes, e.g. "Tr(A)",
        "Carbon (C)", "Boron (B)". Splitting is done on the full bullet chain
        "(A) ... • (B) ... • (C) ... • (D) ..." instead of bare "(A)" markers,
        so those in-text look-alikes never split an option.
      - 15 questions have a paragraph break between the last bullet and "(D)"
        ("•\\n\\n\\n\\n(D) ..."), so the regex uses \\s+ around bullets.
      - The "(D)" option of Q7331 ends with "Carbon (C)" and the stem of Q7371
        quotes "Boron (B)"; both are legitimate content, not markers.

Usage:
    python3 pdf-extract-2026-10-27.py [pdf_path] [out_json]
Defaults point at the workspace locations. Requires `pdftotext` (poppler) on PATH.
"""

import json
import random
import re
import subprocess
import sys
from pathlib import Path

PDF_DEFAULT = Path.home() / "workspace/user/files/loksewa-10000-new-questions-answer-key_0_3hfx.pdf"
OUT_DEFAULT = Path.home() / "workspace/loksewa-prep-nepal/data/pdf-extract-raw.json"

HEADER_RE = re.compile(r"^LOK SEWA PREP NEPAL")
FOOTER_RE = re.compile(r"^Zero-Duplicate Verified Expansion Set")
SECTION_RE = re.compile(r"^Section (\d+):\s*(.*?)\s*\(Q(\d+)\s*[–-]\s*Q?(\d+)")
SECTION_START_RE = re.compile(r"^Section (\d+):")
KEY_HEADING = "Master Answer Key & Verified Correct Responses"
BLOCK_RE = re.compile(r"(?m)^Q(\d+)\.\s")
OPT_RE = re.compile(
    r"\(A\)\s+(.*?)\s+•\s+\(B\)\s+(.*?)\s+•\s+\(C\)\s+(.*?)\s+•\s+\(D\)\s+(.*)$",
    re.S,
)
KEY_ENTRY_RE = re.compile(r"Q(\d+)\(([ABCD])\)")


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()


def extract_text(pdf_path: Path) -> str:
    """Full-document text via pdftotext -layout (preserves the bullet separators)."""
    proc = subprocess.run(
        ["pdftotext", "-layout", str(pdf_path), "-"],
        capture_output=True, check=True,
    )
    return proc.stdout.decode("utf-8", errors="replace")


def parse_sections(lines):
    """Return {section_no: (topic, q_start, q_end)}.

    Section header lines can wrap across two lines in -layout output
    (e.g. 'Office Management & Public' / 'Service (Q2851-Q3300 ...)'),
    so a header line without its (Q<a>-Q<b>) range is joined with the next line.
    """
    sections = {}
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        m = SECTION_RE.match(line)
        if m:
            sections[int(m.group(1))] = (m.group(2), int(m.group(3)), int(m.group(4)))
            i += 1
            continue
        if SECTION_START_RE.match(line):
            joined = line + " " + (lines[i + 1].strip() if i + 1 < len(lines) else "")
            m2 = SECTION_RE.match(joined)
            if m2:
                sections[int(m2.group(1))] = (m2.group(2), int(m2.group(3)), int(m2.group(4)))
                i += 2
                continue
        i += 1
    return sections


def topic_for(num, sections):
    for _sec, (topic, lo, hi) in sorted(sections.items()):
        if lo <= num <= hi:
            return topic
    return None


def main():
    pdf_path = Path(sys.argv[1]) if len(sys.argv) > 1 else PDF_DEFAULT
    out_path = Path(sys.argv[2]) if len(sys.argv) > 2 else OUT_DEFAULT

    text = extract_text(pdf_path)

    # --- split off the master answer key (it sits after the last question) ---
    key_pos = text.find(KEY_HEADING)
    if key_pos == -1:
        raise SystemExit("ERROR: master answer key heading not found")
    q_text, key_text = text[:key_pos], text[key_pos:]

    lines = q_text.split("\n")
    sections = parse_sections(lines)
    if len(sections) != 25:
        raise SystemExit(f"ERROR: expected 25 sections, found {len(sections)}: {sections}")

    # --- strip repeating page headers/footers and section header lines ---
    clean_lines = []
    for ln in lines:
        s = ln.strip()
        if HEADER_RE.match(s) or FOOTER_RE.match(s):
            continue
        if SECTION_START_RE.match(s):
            continue
        clean_lines.append(ln)
    q_text = "\n".join(clean_lines)

    # --- split into question blocks ---
    parts = re.split(BLOCK_RE, q_text)
    preamble = parts[0]
    blocks = {}
    for i in range(1, len(parts), 2):
        blocks[int(parts[i])] = parts[i + 1]

    # --- parse the master answer key ---
    key = {}
    for num_s, letter in KEY_ENTRY_RE.findall(key_text):
        key[int(num_s)] = "ABCD".index(letter)

    failures = []
    questions = []
    for num in sorted(blocks):
        raw = blocks[num]
        raw_text = norm("Q%d. %s" % (num, raw))
        m = OPT_RE.search(raw)
        if not m:
            failures.append({"pdf_num": num, "reason": "no (A)-(D) bullet chain found",
                             "raw_snippet": raw_text[:300]})
            continue
        stem = norm(raw[: m.start()])
        options = [norm(g) for g in m.groups()]
        if not stem or any(not o for o in options):
            failures.append({"pdf_num": num, "reason": "empty stem or empty option",
                             "raw_snippet": raw_text[:300]})
            continue
        if num not in key:
            failures.append({"pdf_num": num, "reason": "no answer in master key",
                             "raw_snippet": raw_text[:300]})
            continue
        topic = topic_for(num, sections)
        if topic is None:
            failures.append({"pdf_num": num, "reason": "no section range covers this number",
                             "raw_snippet": raw_text[:300]})
            continue
        questions.append({
            "pdf_num": num,
            "topic": topic,
            "question": stem,
            "options": options,
            "pdf_answer": key[num],
            "explanation": None,  # PDF contains no explanations
            "raw_text": raw_text,
        })

    # --- validation summary (printed; the report file is written separately) ---
    parsed_nums = [q["pdf_num"] for q in questions]
    missing = [n for n in range(1, 10001) if n not in set(parsed_nums)]
    from collections import Counter
    per_topic = Counter(q["topic"] for q in questions)
    answer_dist = Counter(q["pdf_answer"] for q in questions)

    # --- spot check: 20 random questions, re-verify stem + options against raw_text ---
    rng = random.Random(20261027)
    sample = rng.sample(questions, 20) if len(questions) >= 20 else questions
    spot_ok, spot_bad = 0, []
    for q in sample:
        raw = q["raw_text"]
        if q["question"] in raw and all(o in raw for o in q["options"]):
            spot_ok += 1
        else:
            spot_bad.append(q["pdf_num"])

    print(f"sections: {len(sections)}")
    print(f"blocks found: {len(blocks)}")
    print(f"parsed: {len(questions)}")
    print(f"missing pdf_nums: {missing}")
    print(f"parse failures: {len(failures)}")
    for f in failures:
        print("  FAIL", f)
    print(f"key entries: {len(key)} (unique nums 1..10000 complete: "
          f"{sorted(key) == list(range(1, 10001))})")
    print("per-topic counts:")
    for topic, lo, hi in sorted(((t, l, h) for (t, l, h) in sections.values()), key=lambda x: x[1]):
        print(f"  {topic}: {per_topic.get(topic, 0)} (expected {hi - lo + 1})")
    print(f"answer distribution A/B/C/D: {[answer_dist.get(i, 0) for i in range(4)]}")
    print(f"spot check: {spot_ok}/{len(sample)} OK; bad: {spot_bad}")
    print(f"sampled pdf_nums: {sorted(q['pdf_num'] for q in sample)}")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(questions, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"wrote {out_path} ({len(questions)} questions)")

    # stash validation details for the report writer
    summary = {
        "sections": {str(k): v for k, v in sections.items()},
        "blocks_found": len(blocks),
        "parsed": len(questions),
        "missing": missing,
        "failures": failures,
        "key_entries": len(key),
        "key_complete": sorted(key) == list(range(1, 10001)),
        "per_topic": dict(per_topic),
        "answer_distribution": [answer_dist.get(i, 0) for i in range(4)],
        "spot_check_ok": spot_ok,
        "spot_check_total": len(sample),
        "spot_check_bad": spot_bad,
        "spot_check_nums": sorted(q["pdf_num"] for q in sample),
    }
    Path(str(out_path) + ".summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=1), encoding="utf-8")
    return 0 if len(questions) == 10000 and not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
