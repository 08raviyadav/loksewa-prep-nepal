#!/usr/bin/env python3
"""Build the phone-openable single-file bundle for Lok Sewa Prep Nepal.

Reads index.html, inlines assets/css/style.css and assets/js/app.js, and
embeds data/exams.json + every file listed in app.js QUESTION_FILES as
window.EMBEDDED_EXAMS / window.EMBEDDED_QUESTIONS, plus data/papers.json,
data/notices.json, data/funfacts.json and every file listed in app.js
NOTES_FILES (data/notes/) as window.EMBEDDED_PAPERS / window.EMBEDDED_NOTICES /
window.EMBEDDED_FUNFACTS / window.EMBEDDED_NOTES / window.EMBEDDED_EXAMDATES /
window.EMBEDDED_COURSES / window.EMBEDDED_FESTIVALS.

The bundled loadData() uses the embedded data first (no fetch, so the file
works opened directly in a phone browser / file://) and falls back to the
original fetch() path only when embedded data is absent. The v2 demo mode is
preserved: with embedded data, loadConfig() is skipped (no config.js exists
in the bundle), CONFIG stays null, isDemoMode() is true, and the demo banner
shows — real Google sign-in is NOT faked.

Usage:  python3 scripts/build-bundle.py
Output: loksewa-prep-nepal-full.html  (in the project root)
        + a copy at ~/workspace/your_files/loksewa-prep-nepal-full.html
"""
import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "loksewa-prep-nepal-full.html"
YOUR_FILES = Path.home() / "workspace" / "your_files" / "loksewa-prep-nepal-full.html"

# The exact fetch block at the top of loadData() in assets/js/app.js.
FETCH_BLOCK = """  await loadConfig();
  try{
    const r=await fetch('data/exams.json'); EXAMS=await r.json();
  }catch(e){ EXAMS=[]; }
  QUESTIONS=[];
  // 106 files: fetch them in parallel, not one-by-one. The old sequential
  // loop cost one round-trip per file (106 round-trips on every load — seconds
  // on GitHub Pages). Promise.all preserves QUESTION_FILES order, and a
  // per-file catch keeps one bad file from losing the whole bank.
  // NOTE: scripts/build-bundle.py embeds this exact block (FETCH_BLOCK) —
  // keep the two in sync or the bundle build breaks.
  const _loaded=await Promise.all(QUESTION_FILES.map(f=>fetch('data/questions/'+f).then(r=>r.json()).catch(e=>{ console.warn('Could not load', f, e); return []; })));
  _loaded.forEach(arr=>{ QUESTIONS=QUESTIONS.concat(arr); });
"""

EMBEDDED_BLOCK = """  if (window.EMBEDDED_EXAMS && window.EMBEDDED_QUESTIONS) {
    // Single-file bundle: use embedded data, no fetch (works from file://).
    // loadConfig() is skipped here on purpose: there is no config.js in the
    // bundle, so CONFIG stays null and demo mode stays ON (banner shown).
    EXAMS = window.EMBEDDED_EXAMS; QUESTIONS = window.EMBEDDED_QUESTIONS.slice();
  } else {
""" + FETCH_BLOCK + """  }
"""


def main() -> int:
    html = (ROOT / "index.html").read_text(encoding="utf-8")
    css = (ROOT / "assets" / "css" / "style.css").read_text(encoding="utf-8")
    js = (ROOT / "assets" / "js" / "app.js").read_text(encoding="utf-8")
    # Birthday wishes + My Day digest (assets/js/birthday.js) — appended to
    # the SAME inline script block as app.js so the bundle keeps exactly 2
    # script blocks (test-bundle.js asserts this). It must load after app.js
    # (it calls app.js globals at render time, never at load time).
    bday_js = (ROOT / "assets" / "js" / "birthday.js").read_text(encoding="utf-8")

    # 1. Question files, in app.js order (authoritative list).
    m = re.search(r"const QUESTION_FILES = \[([^\]]*)\];", js, re.S)
    assert m, "QUESTION_FILES not found in app.js"
    files = re.findall(r"'([^']+\.json)'", m.group(1))
    assert files, "no question files listed"

    exams = json.loads((ROOT / "data" / "exams.json").read_text(encoding="utf-8"))
    questions = []
    for f in files:
        arr = json.loads((ROOT / "data" / "questions" / f).read_text(encoding="utf-8"))
        questions.extend(arr)
    papers = json.loads((ROOT / "data" / "papers.json").read_text(encoding="utf-8"))
    notices = json.loads((ROOT / "data" / "notices.json").read_text(encoding="utf-8"))
    funfacts = json.loads((ROOT / "data" / "funfacts.json").read_text(encoding="utf-8"))
    examdates = json.loads((ROOT / "data" / "exam-dates.json").read_text(encoding="utf-8"))
    # Festivals (data/festivals.json) for the festival-wishes feature.
    _fest_path = ROOT / "data" / "festivals.json"
    festivals = json.loads(_fest_path.read_text(encoding="utf-8")) if _fest_path.exists() else []
    # Theory courses, in app.js order (authoritative list).
    m3 = re.search(r"const COURSE_FILES = \[([^\]]*)\];", js, re.S)
    assert m3, "COURSE_FILES not found in app.js"
    course_files = re.findall(r"'([^']+\.json)'", m3.group(1))
    assert course_files, "no course files listed"
    courses = []
    for f in course_files:
        courses.append(json.loads((ROOT / "data" / "courses" / f).read_text(encoding="utf-8")))
    # Revision notes, in app.js order (authoritative list).
    m2 = re.search(r"const NOTES_FILES = \[([^\]]*)\];", js, re.S)
    assert m2, "NOTES_FILES not found in app.js"
    note_files = re.findall(r"'([^']+\.json)'", m2.group(1))
    assert note_files, "no note files listed"
    notes = []
    for f in note_files:
        notes.append(json.loads((ROOT / "data" / "notes" / f).read_text(encoding="utf-8")))

    # 2. Patch loadData() to prefer embedded data.
    assert FETCH_BLOCK in js, "loadData() fetch block changed — update EMBEDDED_BLOCK"
    js_patched = js.replace(FETCH_BLOCK, EMBEDDED_BLOCK, 1)

    # 3. Safety: nothing inlined may contain a literal </script>.
    for name, text in (("css", css), ("js", js_patched), ("birthday.js", bday_js)):
        assert "</script" not in text.lower(), f"</script> found in {name}"
    # NOTE: the marker below must NOT contain the literal file path —
    # the final assert checks that no "assets/js/..." src remains in the HTML.
    js_patched = js_patched + "\n/* ---- birthday feature (inlined) ---- */\n" + bday_js
    data_json = (
        "window.EMBEDDED_EXAMS="
        + json.dumps(exams, ensure_ascii=False, separators=(",", ":"))
        + ";\nwindow.EMBEDDED_QUESTIONS="
        + json.dumps(questions, ensure_ascii=False, separators=(",", ":"))
        + ";\nwindow.EMBEDDED_PAPERS="
        + json.dumps(papers, ensure_ascii=False, separators=(",", ":"))
        + ";\nwindow.EMBEDDED_NOTICES="
        + json.dumps(notices, ensure_ascii=False, separators=(",", ":"))
        + ";\nwindow.EMBEDDED_FUNFACTS="
        + json.dumps(funfacts, ensure_ascii=False, separators=(",", ":"))
        + ";\nwindow.EMBEDDED_NOTES="
        + json.dumps(notes, ensure_ascii=False, separators=(",", ":"))
        + ";\nwindow.EMBEDDED_EXAMDATES="
        + json.dumps(examdates, ensure_ascii=False, separators=(",", ":"))
        + ";\nwindow.EMBEDDED_COURSES="
        + json.dumps(courses, ensure_ascii=False, separators=(",", ":"))
        + ";\nwindow.EMBEDDED_FESTIVALS="
        + json.dumps(festivals, ensure_ascii=False, separators=(",", ":"))
        + ";"
    )
    assert "</script" not in data_json.lower(), "</script> found in embedded data"

    # 4. Assemble: inline CSS, embed data before the app script.
    assert '<link rel="stylesheet" href="assets/css/style.css">' in html
    html = html.replace(
        '<link rel="stylesheet" href="assets/css/style.css">',
        "<style>\n" + css + "\n</style>",
        1,
    )
    assert '<script src="assets/js/app.js"></script>' in html
    assert '<script src="assets/js/birthday.js"></script>' in html
    html = html.replace(
        '<script src="assets/js/app.js"></script>',
        "<script>\n" + data_json + "\n</script>\n<script>\n" + js_patched + "\n</script>",
        1,
    )
    # The birthday script tag is inlined above — remove the now-dead src tag
    # so the bundle has no external script refs and still has exactly 2
    # inline <script> blocks.
    html = html.replace('<script src="assets/js/birthday.js"></script>', '', 1)
    assert "EMBEDDED_QUESTIONS" in html and "EMBEDDED_EXAMS" in html
    assert "assets/js/app.js" not in html and "assets/js/birthday.js" not in html
    assert "assets/css/style.css" not in html

    OUT.write_text(html, encoding="utf-8")
    YOUR_FILES.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(OUT, YOUR_FILES)

    bilingual = sum(
        1
        for q in questions
        if q.get("question_ne") and isinstance(q.get("options_ne"), list)
        and len(q["options_ne"]) == 4 and q.get("explanation_ne")
    )
    print(f"question files: {len(files)}")
    print(f"exams: {len(exams)}")
    print(f"papers: {len(papers)} (transcribed: {sum(1 for p in papers if p.get('transcribed'))})")
    print(f"notices: {len(notices)}")
    print(f"fun facts: {len(funfacts)}")
    print(f"revision notes: {len(notes)} ({sum(len(n['bullets']) for n in notes)} bullets)")
    print(f"questions: {len(questions)} (unique ids: {len({q['id'] for q in questions})})")
    print(f"bilingual: {bilingual}/{len(questions)}")
    print(f"bundle: {OUT} ({OUT.stat().st_size} bytes)")
    print(f"copy:   {YOUR_FILES} ({YOUR_FILES.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
