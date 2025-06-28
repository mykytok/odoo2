from datetime import datetime
from odoo.tests import tagged
from odoo.exceptions import UserError
from .common import TestCommon


@tagged('post_install', '-at_install', 'hr_hospital')
class TestPatientVisitMethods(TestCommon):

    def test_check_duplicate_visit_in_scheduled_date(self):
        with self.assertRaises(UserError):
            self.visit2.write(
                {'scheduled_datetime': datetime(2025, 1, 1, 0, 0)}
            )

    def test_check_unlink_is_diagnosis(self):
        self.env['hr.hospital.diagnosis'].create({
            'hr_hospital_patient_visit_id': self.visit1.id,
        })
        with self.assertRaises(UserError):
            self.visit1.unlink()

    def test_check_visit_completed_status(self):
        self.visit1.status = 'completed'
        with self.assertRaises(UserError):
            self.visit1.write(
                {'hr_hospital_doctor_id': self.doctor2}
            )
