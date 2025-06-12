{
    'name': 'HR Hospital',
    'version': '17.0.1.0.1',
    'author': 'Terminator 2',
    'website': 'https://www.nytimes.com/',
    'category': 'Customizations',
    'license': 'OPL-1',

    'depends': [
        'base',
    ],

    'external_dependencies': {
        'python': [],
    },

    'data': [
        'security/ir.model.access.csv',

        'views/hr_hospital_menu.xml',
        'views/hr_hospital_disease_views.xml',
        'views/hr_hospital_doctors_specialty_views.xml',
        'views/hr_hospital_doctor_views.xml',
        'views/hr_hospital_patient_views.xml',
        'views/hr_hospital_patient_visit_views.xml',
        'views/hr_hospital_diagnosis_views.xml',

        'data/hr.hospital.disease.csv',
    ],
    'demo': [
        'demo/hr.hospital.doctor.csv',
        'demo/hr.hospital.patient.csv',
        'demo/hr.hospital.disease.csv',
    ],

    'installable': True,
    'auto_install': False,

    'images': [
        'static/description/icon.png'
    ]
}
