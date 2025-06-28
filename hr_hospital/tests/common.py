from datetime import datetime
from odoo.tests.common import TransactionCase


class TestCommon(TransactionCase):

    def setUp(self):
        super(TestCommon, self).setUp()

        self.doctor1 = self.env['hr.hospital.doctor'].create({
            'full_name': 'Test Doc 1'
        })
        self.doctor2 = self.env['hr.hospital.doctor'].create({
            'full_name': 'Test Doc 2'
        })
        self.patient1 = self.env['hr.hospital.patient'].create({
            'full_name': 'Test Patient 1',
            'hr_hospital_personal_doctor_id': self.doctor1.id
        })
        self.visit1 = self.env['hr.hospital.patient.visit'].create({
            'hr_hospital_patient_id': self.patient1.id,
            'hr_hospital_doctor_id': self.doctor1.id,
            'scheduled_datetime': datetime(2025, 1, 1, 0, 0),
        })
        self.visit2 = self.env['hr.hospital.patient.visit'].create({
            'hr_hospital_patient_id': self.patient1.id,
            'hr_hospital_doctor_id': self.doctor1.id,
            'scheduled_datetime': datetime(2025, 1, 2, 0, 0),
        })
