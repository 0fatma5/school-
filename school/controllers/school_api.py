import json
import logging
from urllib.parse import parse_qs

from odoo import http
from odoo.http import request

# Logger for debugging and error tracking
_logger = logging.getLogger(__name__)

# Utility function for consistent responses
def valid_response(data, status):
    response_body = {'data': data}
    return request.make_json_response(response_body, status=status)

def invalid_response(error, status):
    response_body = {'error': error}
    return request.make_json_response(response_body, status=status)


class SchoolApi(http.Controller):

    @http.route("/v1/school", methods=["POST"], type="http", auth="none", csrf=False)
    def post_school(self, **kwargs):
        try:
            vals = json.loads(request.httprequest.data.decode())
            # Validate required fields
            required_fields = ['name']
            missing_fields = [field for field in required_fields if not vals.get(field)]
            if missing_fields:
                return invalid_response(f"Missing required fields: {', '.join(missing_fields)}", status=400)

            # Create the school record
            school_rec = request.env['school'].sudo().create(vals)
            return valid_response({
                "message": "School has been created successfully.",
                "id": school_rec.id,
                "name": school_rec.name,
            }, status=201)
        except Exception as e:
            _logger.exception("Error creating school.")
            return invalid_response("An unexpected error occurred.", status=500)


    @http.route("/v1/school/<int:school_id>", methods=["GET"], type="http", auth="none", csrf=False)
    def get_school(self, school_id):
        try:
            school_rec = request.env['school'].sudo().search([('id', '=', school_id)])
            if not school_rec:
                return invalid_response("ID does not exist!", status=404)
            return valid_response({
                "id": school_rec.id,
                "name": school_rec.name,
            }, status=200)
        except Exception as e:
            _logger.exception("Error fetching school details.")
            return invalid_response("An unexpected error occurred.", status=500)

    @http.route("/v1/school/<int:school_id>", methods=["PUT"], type="http", auth="none", csrf=False)
    def update_school(self, school_id):
        try:
            school_rec = request.env['school'].sudo().search([('id', '=', school_id)])
            if not school_rec:
                return invalid_response(f"School with ID {school_id} not found.", status=404)

            vals = json.loads(request.httprequest.data.decode())
            # Filter out invalid fields
            existing_fields = request.env['school']._fields.keys()
            valid_vals = {key: value for key, value in vals.items() if key in existing_fields}
            if not valid_vals:
                return invalid_response("No valid fields provided for update.", status=400)

            # Update the school record
            school_rec.write(valid_vals)
            return valid_response({
                "message": "School updated successfully.",
                "id": school_rec.id,
                "name": school_rec.name,
            }, status=200)
        except Exception as e:
            _logger.exception("Error updating school.")
            return invalid_response("An unexpected error occurred.", status=500)

    @http.route("/v1/school/<int:school_id>", methods=["DELETE"], type="http", auth="none", csrf=False)
    def delete_school(self, school_id):
        try:
            school_rec = request.env['school'].sudo().search([('id', '=', school_id)])
            if not school_rec:
                return invalid_response(f"School with ID {school_id} not found.", status=404)

            # Delete the school record
            school_rec.unlink()
            return valid_response({"message": "School deleted successfully."}, status=200)
        except Exception as e:
            _logger.exception("Error deleting school.")
            return invalid_response("An unexpected error occurred.", status=500)

    @http.route("/v1/schools", methods=["GET"], type="http", auth="none", csrf=False)
    def get_school_list(self):
        try:
            params = parse_qs(request.httprequest.query_string.decode('utf-8'))
            school_domain = []
            offset = 0
            limit = 5

            # Parse query parameters for pagination and filtering
            if params.get('limit'):
                try:
                    limit = int(params['limit'][0])
                except ValueError:
                    return invalid_response("Invalid 'limit' parameter. Must be an integer.", status=400)

            if params.get('page'):
                try:
                    page = int(params['page'][0])
                    offset = (page - 1) * limit
                except ValueError:
                    return invalid_response("Invalid 'page' parameter. Must be an integer.", status=400)

            if params.get('state'):
                school_domain.append(('state', '=', params['state'][0]))

            school_ids = request.env['school'].sudo().search(school_domain, offset=offset, limit=limit, order='id desc')
            school_count = request.env['school'].sudo().search_count(school_domain)

            if not school_ids:
                return valid_response({
                    "total": school_count,
                    "schools": []
                }, status=200)

            return valid_response({
                "total": school_count,
                "page": page if params.get('page') else 1,
                "limit": limit,
                "schools": school_ids.mapped(lambda rec: {
                    "id": rec.id,
                    "name": rec.name,
                }),
            }, status=200)
        except Exception as e:
            _logger.exception("Error fetching school list.")
            return invalid_response("An unexpected error occurred.", status=500)
