import logging

from odoo import models, fields, api, exceptions

from . import hr_hospital_abstract_person

_logger = logging.getLogger(__name__)


class Doctor(models.Model):
    _name = 'hr.hospital.doctor'
    _inherit = 'hr.hospital.abstract.person'
    _description = 'Doctor'

    name = fields.Char()

    doctors_specialty_id = fields.Many2one(
        comodel_name='hr.hospital.doctors.specialty',
        string="Doctor's specialty",
    )

    is_intern = fields.Boolean(string="Intern")

    mentor_doctor_id = fields.Many2one(
        comodel_name='hr.hospital.doctor',
        string="Mentor doctor",
    )

    active = fields.Boolean(
        default=True, )

    description = fields.Text()

    @api.constrains('mentor_doctor_id')
    def _check_mentor_doctor_is_intern(self):
        for rec in self:
            _logger.info('==========================')
            _logger.info(rec.mentor_doctor_id.is_intern)
            if rec.mentor_doctor_id.is_intern:
                raise exceptions.ValidationError("Intern cannot be a mentor.")

    @api.onchange('is_intern')
    def _onchange_is_intern(self):
        for rec in self:
            if not rec.is_intern:
                rec.mentor_doctor_id = []
