import logging

from odoo import models, fields

from . import hr_hospital_abstract_person

_logger = logging.getLogger(__name__)


class Doctor(models.Model):
    _name = 'hr.hospital.doctor'
    _inherit = 'hr.hospital.abstract.person'
    _description = 'Doctor'

    name = fields.Char()

    hr_hospital_curator_doctor_id = fields.Many2one(
        comodel_name='hr.hospital.doctor',
        string="Curator",
    )

    active = fields.Boolean(
        default=True, )

    description = fields.Text()
