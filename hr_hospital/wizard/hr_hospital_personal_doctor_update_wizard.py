import logging

from odoo import models, fields

_logger = logging.getLogger(__name__)


class PersonalDoctorUpdate(models.TransientModel):
    _name = 'hr.hospital.personal.doctor.update.wizard'
    _description = 'Personal doctor update'

    doctor_id = fields.Many2one(
        comodel_name='hr.hospital.doctor',
        string='Doctor',
    )

    def update_personal_doctor(self):
        self.ensure_one()
        patient_ids = self.env['hr.hospital.patient'].search([])
        for patient_id in patient_ids:
            patient_id.hr_hospital_personal_doctor_id = self.doctor_id
