"""Authenticated, permission-aware HTTP endpoints for the school portfolio addon.

The original endpoints accepted anonymous writes with sudo(). This version
requires a logged-in School Manager for mutations and an authorized school
user/manager for reads. Write clients must provide Odoo's CSRF token.
"""
import logging

from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)

SCHOOL_FIELDS = {
    "name", "location", "school_type", "Principal_Name",
    "campus_size", "school_address",
}
SCHOOL_TYPES = {"primary", "secondary", "highschool"}


def ok(data, status=200):
    return request.make_json_response({"data": data}, status=status)


def error(message, status):
    return request.make_json_response({"error": message}, status=status)


def can_read():
    user = request.env.user
    return user.has_group("school.school_user_group") or user.has_group(
        "school.school_manager_group"
    )


def can_write():
    return request.env.user.has_group("school.school_manager_group")


def validate_payload(creating=False):
    data = request.httprequest.get_json(silent=True)
    if not isinstance(data, dict):
        return None, "Expected a JSON object."
    if not data:
        return None, "At least one field is required."
    invalid_fields = set(data) - SCHOOL_FIELDS
    if invalid_fields:
        return None, "Unknown or non-writable fields: " + ", ".join(sorted(invalid_fields))
    if (creating or "name" in data) and (
        not isinstance(data.get("name"), str) or not data["name"].strip()
    ):
        return None, "School name must be a non-empty string."
    if "name" in data:
        data["name"] = data["name"].strip()
    for field in ("location", "Principal_Name", "school_address"):
        if field in data and data[field] is not False and data[field] is not None and not isinstance(data[field], str):
            return None, field + " must be a string or null."
    if "school_type" in data and data["school_type"] not in SCHOOL_TYPES and data["school_type"] is not False:
        return None, "Unsupported school type."
    if "campus_size" in data and (
        isinstance(data["campus_size"], bool)
        or not isinstance(data["campus_size"], int)
        or data["campus_size"] < 0
    ):
        return None, "Campus size must be a non-negative integer."
    return data, None


class SchoolApi(http.Controller):
    @http.route("/v1/school", methods=["POST"], type="http", auth="user", csrf=True)
    def post_school(self, **kwargs):
        if not can_write():
            return error("School Manager permission required.", 403)
        values, problem = validate_payload(creating=True)
        if problem:
            return error(problem, 400)
        try:
            school = request.env["school"].create(values)
            return ok({"message": "School created.", "id": school.id, "name": school.name}, 201)
        except Exception:
            _logger.exception("Failed to create school")
            return error("Unable to create school.", 500)

    @http.route("/v1/school/<int:school_id>", methods=["GET"], type="http", auth="user")
    def get_school(self, school_id, **kwargs):
        if not can_read():
            return error("School access required.", 403)
        try:
            school = request.env["school"].search([("id", "=", school_id)], limit=1)
            if not school:
                return error("School not found.", 404)
            return ok({"id": school.id, "name": school.name})
        except Exception:
            _logger.exception("Failed to read school")
            return error("Unable to load school.", 500)

    @http.route("/v1/school/<int:school_id>", methods=["PUT"], type="http", auth="user", csrf=True)
    def update_school(self, school_id, **kwargs):
        if not can_write():
            return error("School Manager permission required.", 403)
        values, problem = validate_payload()
        if problem:
            return error(problem, 400)
        try:
            school = request.env["school"].search([("id", "=", school_id)], limit=1)
            if not school:
                return error("School not found.", 404)
            school.write(values)
            return ok({"message": "School updated.", "id": school.id, "name": school.name})
        except Exception:
            _logger.exception("Failed to update school")
            return error("Unable to update school.", 500)

    @http.route("/v1/school/<int:school_id>", methods=["DELETE"], type="http", auth="user", csrf=True)
    def delete_school(self, school_id, **kwargs):
        if not can_write():
            return error("School Manager permission required.", 403)
        try:
            school = request.env["school"].search([("id", "=", school_id)], limit=1)
            if not school:
                return error("School not found.", 404)
            school.unlink()
            return ok({"message": "School deleted."})
        except Exception:
            _logger.exception("Failed to delete school")
            return error("Unable to delete school.", 500)

    @http.route("/v1/schools", methods=["GET"], type="http", auth="user")
    def get_school_list(self, **kwargs):
        if not can_read():
            return error("School access required.", 403)
        args = request.httprequest.args
        try:
            page = int(args.get("page", "1"))
            limit = int(args.get("limit", "5"))
        except (ValueError, TypeError):
            return error("Page and limit must be integers.", 400)
        if page < 1 or not 1 <= limit <= 100:
            return error("Page must be >= 1; limit must be between 1 and 100.", 400)

        domain = []
        school_type = args.get("school_type")
        if school_type:
            if school_type not in SCHOOL_TYPES:
                return error("Unsupported school type.", 400)
            domain.append(("school_type", "=", school_type))
        try:
            model = request.env["school"]
            rows = model.search_read(
                domain, fields=["id", "name"], offset=(page - 1) * limit,
                limit=limit, order="id desc",
            )
            return ok({
                "total": model.search_count(domain),
                "page": page,
                "limit": limit,
                "schools": rows,
            })
        except Exception:
            _logger.exception("Failed to list schools")
            return error("Unable to list schools.", 500)
