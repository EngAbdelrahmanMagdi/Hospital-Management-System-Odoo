{
    'name': 'hms',
    
    'description': """A module for hospital management system""",
    'depends':['crm'],
    'data': [
        'views/hms_patient_views.xml', 'views/hms_department_views.xml', 'views/hms_doctors_views.xml', 'views/crm_customers_view.xml', 'reports/hms_reports.xml',
        'reports/hms_templates.xml', 'security/hms_security.xml', 'security/ir.model.access.csv', 'reports/hms_reports.xml', 'reports/hms_templates.xml'],
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
