import logging

from odoo import models, fields

_logger = logging.getLogger(__name__)


class HrHospitalDoctor(models.Model):
    _name = 'hr.hospital.doctor'
    _description = 'Doctor'

    name = fields.Char()

    hr_hospital_curator_doctor_id = fields.Many2one(
        comodel_name='hr.hospital.doctor',
        string="Curator",
    )

    active = fields.Boolean(
        default=True, )

    description = fields.Text()
