#!/usr/bin/env python3
"""Static addon quality/security checks that do not require an Odoo installation."""
import ast
import csv
import io
import re
import sys
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
ADDON = ROOT / "school"
errors = []


def verify(condition, message):
    if not condition:
        errors.append(message)


for path in ADDON.rglob("*.py"):
    if "__pycache__" in path.parts:
        continue
    try:
        ast.parse(path.read_text(encoding="utf-8-sig"), filename=str(path))
    except (SyntaxError, UnicodeError) as exc:
        errors.append(f"Python parse failed: {path.relative_to(ROOT)}: {exc}")

manifest = ast.literal_eval((ADDON / "__manifest__.py").read_text(encoding="utf-8-sig"))
verify(manifest["version"].startswith("17."), "Expected Odoo 17 addon version")
for path in manifest["data"]:
    file_path = ADDON / path
    verify(file_path.is_file(), f"Manifest references missing file: {path}")
    if file_path.is_file() and path.endswith(".xml"):
        try:
            ET.parse(file_path)
        except ET.ParseError as exc:
            errors.append(f"Invalid XML in {path}: {exc}")

for asset_paths in manifest.get("assets", {}).values():
    for path in asset_paths:
        verify((ROOT / path).is_file(), f"Missing declared asset: {path}")

csv_path = ADDON / "security" / "ir.model.access.csv"
with csv_path.open(encoding="utf-8-sig", newline="") as csv_file:
    rows = list(csv.DictReader(csv_file))
ids = {row["id"] for row in rows}
verify(len(ids) == len(rows), "Duplicated ACL XML IDs")
legacy = {
    "access_school", "access_student", "access_teacher", "access_school_type",
    "access_primary_school", "access_middle_school", "access_high_school",
    "access_change_school_wizard",
}
verify(legacy.issubset(ids), "Legacy ACL XML IDs must be preserved during upgrade")
for row in rows:
    verify(bool(row["group_id:id"]), f"Unrestricted access group in {row['id']}")
    for key in ("perm_read", "perm_write", "perm_create", "perm_unlink"):
        verify(row[key] in {"0", "1"}, f"Invalid {key} in {row['id']}")

active_controller = (ADDON / "controllers" / "school_api.py").read_text(encoding="utf-8")
verify(not re.search(r"auth\s*=\s*['\"](?:none|public)['\"]", active_controller),
       "School API must never use anonymous/public authentication")
verify(".sudo(" not in active_controller, "School API must obey Odoo ACLs and record rules")
verify(not (ADDON / "controllers" / "test_api.py").exists(),
       "Anonymous debug API must be removed")
verify("from . import school_api" in
       (ADDON / "controllers" / "__init__.py").read_text(encoding="utf-8"),
       "School API controller must be imported")

if errors:
    print("\n".join(f"FAIL: {message}" for message in errors), file=sys.stderr)
    sys.exit(1)
print(f"PASS: parsed Python, manifest files, XML, {len(rows)} restricted ACLs, and controller guards.")
