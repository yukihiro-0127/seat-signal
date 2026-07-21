#!/usr/bin/env python3
"""Validate seat-signal/index.html for key requirements."""
import re, sys

with open("index.html", encoding="utf-8") as f:
    html = f.read()

errors = []
warnings = []

# ── サービス名 ────────────────────────────────────────────────
for banned in ["Seat Signal"]:
    if banned in html:
        errors.append(f'FAIL: "{banned}" still present in HTML')
for expected in ["Find my seat"]:
    if expected not in html:
        errors.append(f'FAIL: "{expected}" not found in HTML')
if "<title>Find my seat" not in html:
    errors.append("FAIL: <title> does not start with 'Find my seat'")
if '"Find my seat — 箱崎事業所"' not in html:
    errors.append("FAIL: document.title JP not updated to Find my seat")
if '"Find my seat — Hakodate Office"' not in html:
    errors.append("FAIL: document.title EN not updated to Find my seat")

# ── 4ステップUI ──────────────────────────────────────────────
for step in [1, 2, 3, 4]:
    if f'id="ciStep{step}Panel"' not in html:
        errors.append(f'FAIL: #ciStep{step}Panel not found')
    if f'id="st{step}"' not in html:
        errors.append(f'FAIL: #st{step} step indicator not found')
for sl in [1, 2, 3]:
    if f'id="sl{sl}"' not in html:
        errors.append(f'FAIL: #sl{sl} step-line not found')

# ── Step3 席グリッドUI ────────────────────────────────────────
if 'id="ciSeatGrid"' not in html:
    errors.append("FAIL: #ciSeatGrid not found")
if 'renderSeatGrid' not in html:
    errors.append("FAIL: renderSeatGrid() not found")
if 'genSeats' not in html:
    errors.append("FAIL: genSeats() not found")
if 'seat-grid' not in html:
    errors.append("FAIL: .seat-grid CSS not found")
if 'ciNext3' not in html:
    errors.append("FAIL: #ciNext3 button not found")
if 'ciBack3' not in html:
    errors.append("FAIL: #ciBack3 button not found")

# ── チェックイン中画面のバッジ ────────────────────────────────
if 'id="ciActiveType"' not in html:
    errors.append("FAIL: #ciActiveType badge element not found")
if 'id="ciActivePower"' not in html:
    errors.append("FAIL: #ciActivePower badge element not found")

# ── i18n キー（JA + EN 各1回以上） ───────────────────────────
required_i18n = [
    "ci_step3_desc", "ci_step3_no_result", "ci_step4",
    "ci_cand_avail", "ci_cand_updated", "ci_type_any_label",
]
for key in required_i18n:
    count = len(re.findall(re.escape(key), html))
    if count < 2:
        warnings.append(f'WARN: i18n key "{key}" found {count} time(s) (expected >=2 for JA+EN)')

# ── EN辞書に日本語が含まれていないか ────────────────────────
en_section_match = re.search(r'en:\{(.+?)(?=\n\};)', html, re.DOTALL)
if en_section_match:
    en_text = en_section_match.group(1)
    cjk = re.findall(r'[\u3040-\u30FF\u4E00-\u9FFF]+', en_text)
    if cjk:
        errors.append(f"FAIL: EN i18n section contains Japanese chars: {cjk[:5]}")

# ── 結果出力 ────────────────────────────────────────────────────
print("=== Find my seat — HTML Validation ===")
if errors:
    for e in errors:
        print(e)
if warnings:
    for w in warnings:
        print(w)
if not errors and not warnings:
    print("ALL CHECKS PASSED ✓")
elif not errors:
    print(f"PASSED with {len(warnings)} warning(s)")
    for w in warnings:
        print(w)
else:
    print(f"\n{len(errors)} error(s), {len(warnings)} warning(s)")
    sys.exit(1)
