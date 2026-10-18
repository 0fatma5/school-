# School Management — Odoo 17 Addon

A personal **Odoo 17 learning project** for managing schools, students, teachers, transfers, school types, an OWL list view, and HTML/Excel reports.

> **Security status:** This repository is a learning project. A security-hardening branch replaces anonymous API routes and broad model permissions, but **a real Odoo installation/upgrade and authorization test is required before deployment**. Do not use real student information in demos.

## Features

- School, student, and teacher records
- Primary, middle, and high school models
- School transfer wizard with history
- School HTML reports and Excel export
- Custom OWL list view
- Authenticated HTTP JSON endpoints to list, read, create, update, and delete schools

## Requirements

- **Odoo 17** and PostgreSQL configured locally
- Python package `xlsxwriter` available to the Odoo Python environment

## Installation

1. Place the `school/` folder in your Odoo custom addons directory.
2. Restart Odoo and update the Apps list.
3. Install the **School** module on a **fresh test database**.
4. Assign the appropriate user groups under Odoo settings:
   - **School Manager:** full CRUD access to school, student, teacher, school types, and transfer operations.
   - **School User (Read Only):** can read schools they created, plus read-only school type records. Cannot modify schools or access students/teachers directly.

> If upgrading an existing installation, **back up the database first**. Previously existing unrestricted ACL entries are updated using their original XML IDs. Still verify the effective ACLs, any extra rules, and user-group assignments after upgrade.

## API endpoints

| Method | Path | Access |
| --- | --- | --- |
| GET | `/v1/schools?page=1&limit=5` | School User or School Manager |
| GET | `/v1/school/<id>` | School User or School Manager |
| POST | `/v1/school` | School Manager |
| PUT | `/v1/school/<id>` | School Manager |
| DELETE | `/v1/school/<id>` | School Manager |

All endpoints now require an **authenticated Odoo session**. Modifications also require an **Odoo CSRF token**. Anonymous requests should not be permitted. Use an actual logged-in Odoo environment to exercise API routes; do not disable CSRF for convenience.

Example create payload:

```json
{
  "name": "Example Academy",
  "school_type": "primary",
  "location": "Demo City",
  "campus_size": 750
}
```

Only permitted school fields can be created/updated. Model internals, IDs, relationships, and arbitrary record fields cannot be set via the HTTP API.

List queries support page >= 1, limit 1–100, and optional `school_type` filter: `primary`, `secondary`, or `highschool`. Unauthorized users receive an access error.

## Excel report

The Excel report is available from the Schools list. IDs are parsed without `eval` or `literal_eval`, and reports use Odoo record rules instead of `sudo()`. User-supplied school names/addresses are written as strings to avoid spreadsheet formulas.

## Validation

A lightweight GitHub Actions check validates Python syntax, manifest file references, XML parsing, access CSV rules, and unsafe controller patterns. It does **not** replace running an actual Odoo 17 server.

Run the checks locally:

```bash
python scripts/check_addon.py
```

Manual checklist before merging:

1. Install the addon on a new Odoo 17 test database.
2. Upgrade the existing addon on a cloned test database and verify old ACL XML IDs are updated.
3. Verify anonymous GET/POST/PUT/DELETE access fails.
4. Verify logged-in School User cannot create/update/delete schools or read students/teachers.
5. Verify School Manager can create/update/delete and see authorized records.
6. Verify CSRF protection rejects write requests without a valid token.
7. Verify school transfers preserve history and reject same-school transfers.
8. Verify Excel export works for allowed school records and rejects forbidden IDs.
9. Verify OWL list view, navigation, and reports still render.

## Portfolio notes

Suggested description: *Personal Odoo 17 school management addon with students, teachers, transfer wizard, reports, OWL views, and secured HTTP API.*

Suggested topics: `odoo`, `odoo17`, `python`, `postgresql`, `owl`, `api-security`, `education`.

There is **no demo video yet**. Only add a genuine screen recording from the installed working module, using synthetic data.
