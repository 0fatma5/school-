"""School Excel export with group checks and record-rule enforcement."""
import io
import re

import xlsxwriter
from odoo import http
from odoo.http import request


def parse_ids(text):
    # Accept compact IDs from the new button and legacy [1, 2] URLs without
    # using eval / literal_eval, and reject invalid or excessively large lists.
    if not isinstance(text, str):
        raise ValueError("Invalid school identifiers")
    trimmed = text.strip()
    if trimmed.startswith("[") and trimmed.endswith("]"):
        trimmed = trimmed[1:-1]
    if not re.fullmatch(r"[1-9][0-9]*(?:\s*,\s*[1-9][0-9]*)*", trimmed):
        raise ValueError("Invalid school identifiers")
    values = [int(x.strip()) for x in trimmed.split(",")]
    if len(values) > 200 or len(set(values)) != len(values):
        raise ValueError("Select 1 to 200 distinct schools")
    return values


class XlsxSchoolReport(http.Controller):
    @http.route("/school/excel/report/<string:school_ids>", type="http", auth="user")
    def download_school_excel_report(self, school_ids, **kwargs):
        user = request.env.user
        if not (user.has_group("school.school_manager_group")
                or user.has_group("school.school_user_group")):
            return request.make_response("Forbidden", status=403)

        try:
            ids = parse_ids(school_ids)
        except ValueError:
            return request.make_response("Invalid school IDs", status=400)

        # No sudo: users must have read access to every requested record.
        schools = request.env["school"].search([("id", "in", ids)])
        if len(schools) != len(ids):
            return request.make_response("One or more schools are unavailable", status=404)

        output = io.BytesIO()
        # Prevent school names/addresses from turning into Excel formulas/URLs.
        workbook = xlsxwriter.Workbook(
            output, {"in_memory": True, "strings_to_formulas": False, "strings_to_urls": False}
        )
        worksheet = workbook.add_worksheet("Schools")
        heading = workbook.add_format({
            "bold": True, "bg_color": "#E5E7EB", "border": 1, "align": "center"
        })
        cell = workbook.add_format({"border": 1})
        worksheet.set_column(0, 2, 24)
        for col, title in enumerate(("Name", "Location", "Address")):
            worksheet.write_string(0, col, title, heading)

        for row, school in enumerate(schools, start=1):
            worksheet.write_string(row, 0, school.name or "", cell)
            worksheet.write_string(row, 1, school.location or "", cell)
            worksheet.write_string(row, 2, school.school_address or "", cell)

        workbook.close()
        return request.make_response(output.getvalue(), headers=[
            ("Content-Type", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"),
            ("Content-Disposition", 'attachment; filename="school_report.xlsx"'),
            ("X-Content-Type-Options", "nosniff"),
        ])
