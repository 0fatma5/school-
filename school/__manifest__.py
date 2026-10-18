{
    'name': "School",
    'author': "Fatma Ahmed",
    'version': '17.0.0.1.0',
    'depends': [
        'base',
    ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/data.xml',
        'views/base_menu.xml',
        'views/school_view.xml',
        'views/student_view.xml',
        'views/teacher_view.xml',
        'views/school_type_view.xml',
        'views/primary_school_view.xml',
        'views/middle_school_view.xml',
        'views/high_school_view.xml',
        'reports/student_report.xml',
        'reports/school_report.xml',
        'wizard/change_school_wizard.xml',

    ],
    'assets': {
        'web.assets_backend': [
            'school/static/src/components/listView/listView.js',
            'school/static/src/components/listView/listView.xml',
            'school/static/src/components/listView/listView.css',
        ],

    },

    'summary': 'Personal Odoo 17 education management learning addon',
    'category': 'Education',
    'external_dependencies': {'python': ['xlsxwriter']},
    'application': True
}