import logging

from odoo import models, fields

from . import hr_hospital_abstract_person

_logger = logging.getLogger(__name__)


class Patient(models.Model):
    _name = 'hr.hospital.patient'
    _inherit = 'hr.hospital.abstract.person'
    _description = 'Patient'

    name = fields.Char()

    active = fields.Boolean(
        default=True, )

    description = fields.Text()
