from ast import literal_eval
from odoo import http
from odoo.http import request
import io
import xlsxwriter


class XlsxSchoolReport(http.Controller):
    @http.route('/school/excel/report/<string:school_ids>', type='http', auth='user')  # Changed route to reflect "school"
    def download_school_excel_report(self, school_ids):  # Updated method name and parameter
        # Create an in-memory byte stream
        school_ids = request.env['school'].browse(literal_eval(school_ids))
        print(school_ids)
        output = io.BytesIO()

        # Create an xlsx writer object using the in-memory byte stream
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})

        # Add a worksheet to the workbook
        worksheet = workbook.add_worksheet('Schools')
        header_format = workbook.add_format({'bold': True, 'bg_color': '#3D3D3', 'border': 1, 'align': 'center'})
        string_format = workbook.add_format({'border': 1, 'align': 'center'})


        # Define headers
        headers = ['Name', 'Location', 'school_address']
        for col_num, header in enumerate(headers):
            # Write headers to the worksheet
            worksheet.write(0, col_num, header, header_format)

        row_num = 1
        for school in school_ids:
            worksheet.write(row_num, 0, school.name, string_format)
            worksheet.write(row_num, 1, school.location, string_format)
            worksheet.write(row_num, 2, school.school_address, string_format)
            row_num += 1

        workbook.close()

        # Get the content of the output byte stream
        output.seek(0)
        file_name = 'School Report.xlsx'

        # Return the file as an attachment
        return request.make_response(
            output.getvalue(),
            headers=[
                ('Content-Type', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'),
                ('Content-Disposition', 'attachment; filename="school_report.xlsx"')
            ]
        )
