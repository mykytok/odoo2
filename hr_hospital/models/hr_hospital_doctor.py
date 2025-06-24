import logging

from odoo import models, fields, api, exceptions

from . import hr_hospital_abstract_person

_logger = logging.getLogger(__name__)


class Doctor(models.Model):
    _name = 'hr.hospital.doctor'
    _inherit = 'hr.hospital.abstract.person'
    _description = 'Doctor'

    doctors_specialty_id = fields.Many2one(
        comodel_name='hr.hospital.doctors.specialty',
        string="Doctor's specialty",
    )

    is_intern = fields.Boolean(string="Intern")

    mentor_doctor_id = fields.Many2one(
        comodel_name='hr.hospital.doctor',
        string="Mentor doctor",
    )

    mentor_doctors_specialty_id = fields.Many2one(
        related='mentor_doctor_id.doctors_specialty_id',
        string="Mentor's specialty"
    )

    intern_doctor_ids = fields.One2many(
        comodel_name='hr.hospital.doctor',
        inverse_name='mentor_doctor_id',
    )

    is_mentor = fields.Boolean(
        compute='_compute_is_mentor',
        default=False
    )

    patient_visit_ids = fields.One2many(
        comodel_name='hr.hospital.patient.visit',
        inverse_name='hr_hospital_doctor_id',
    )

    patient_ids = fields.One2many(
        comodel_name='hr.hospital.patient',
        inverse_name='hr_hospital_personal_doctor_id',
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
                raise exceptions.UserError("Intern cannot be a mentor.")

    @api.onchange('is_intern')
    def _onchange_is_intern(self):
        for rec in self:
            if not rec.is_intern:
                rec.mentor_doctor_id = []

    def _get_report_base_filename(self):
        self.ensure_one()
        return 'Doctor - %s' % (self.full_name)

    @api.depends('intern_doctor_ids')
    def _compute_is_mentor(self):
        for record in self:
            record.is_mentor = record.intern_doctor_ids

    def archive(self):
        for rec in self:
            rec.write({'active': False})