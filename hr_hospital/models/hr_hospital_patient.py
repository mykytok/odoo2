import datetime
import logging

from odoo import models, fields, api

_logger = logging.getLogger(__name__)


class Patient(models.Model):
    """A model for storing Patient
                            """

    _name = 'hr.hospital.patient'
    _inherit = 'hr.hospital.abstract.person'
    _description = 'Patient'

    res_user_id = fields.Many2one('res.users')

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

    diagnosis_ids = fields.One2many(
        comodel_name='hr.hospital.diagnosis',
        inverse_name='patient_id',
        string="Diagnosis",
    )

    patient_visit_ids = fields.One2many(
        comodel_name='hr.hospital.patient.visit',
        inverse_name='hr_hospital_patient_id',
        string="Patient visits",
    )

    @api.depends('birth_date')
    def _compute_age(self):
        today = datetime.date.today()
        for record in self:
            record.age = (today.year - record.birth_date.year
                          - ((today.month,
                              today.day)
                             < (record.birth_date.month,
                                record.birth_date.day)))


    def current_patient_visit_status(self, doctor_id):
        self.ensure_one()
        rec = self.env['hr.hospital.patient.visit'].search(
            [('hr_hospital_doctor_id', '=', self.hr_hospital_personal_doctor_id.id),
             ('hr_hospital_patient_id', '=', self.id)],
            order='scheduled_datetime desc',
            limit=1
        )
        if rec:
            return rec[0].status

        return 'empty'
