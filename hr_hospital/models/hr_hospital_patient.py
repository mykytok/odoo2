import datetime
import logging

from odoo import models, fields, api

_logger = logging.getLogger(__name__)


class Patient(models.Model):
    _name = 'hr.hospital.patient'
    _inherit = 'hr.hospital.abstract.person'
    _description = 'Patient'

    hr_hospital_personal_doctor_id = fields.Many2one(
        comodel_name='hr.hospital.doctor',
        string="Personal doctor",
    )

    birth_date = fields.Date(
        default=fields.Date.today(),
        string="Date of birth",
    )

    age = fields.Integer(
        compute='_compute_age',
        store=True,
    )

    passport_data = fields.Char()

    contact_person = fields.Char()

    active = fields.Boolean(
        default=True,
    )

    description = fields.Text()

    @api.depends('birth_date')
    def _compute_age(self):
        today = datetime.date.today()
        for record in self:
            record.age = (today.year - record.birth_date.year
                          - ((today.month,
                              today.day)
                             < (record.birth_date.month,
                                record.birth_date.day)))
