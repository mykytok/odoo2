import logging

from odoo import models, fields

_logger = logging.getLogger(__name__)


class OSLBook(models.Model):
    _name = 'hr.hospital.patient.visit'
    _description = 'Patient visit'

    active = fields.Boolean(
        default=True, )

    description = fields.Text()

    hr_hospital_doctor_id = fields.Many2one(
        comodel_name='hr.hospital.doctor',
        string="Doctor",
    )

    hr_hospital_patient_id = fields.Many2one(
        comodel_name='hr.hospital.patient',
        string="Patient",
    )

    hr_hospital_disease_ids = fields.Many2many(
        comodel_name='hr.hospital.disease',
        string="Diseases",
    )
