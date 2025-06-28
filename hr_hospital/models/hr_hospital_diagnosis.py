import logging

from odoo import models, fields, api

_logger = logging.getLogger(__name__)


class Diagnosis(models.Model):
    """A model for storing Diagnosis
                """

    _name = 'hr.hospital.diagnosis'
    _description = 'Diagnosis'

    hr_hospital_patient_visit_id = fields.Many2one(
        comodel_name='hr.hospital.patient.visit',
        string="Visit",
    )

    doctor_id = fields.Many2one(
        related='hr_hospital_patient_visit_id.hr_hospital_doctor_id'
    )

    patient_id = fields.Many2one(
        related='hr_hospital_patient_visit_id.hr_hospital_patient_id'
    )

    visit_datetime = fields.Datetime(
        related='hr_hospital_patient_visit_id.visit_datetime',
        store=True
    )

    hr_hospital_disease_id = fields.Many2one(
        comodel_name='hr.hospital.disease',
        string="Disease",
    )

    approved = fields.Boolean(
        compute='_compute_approved',
        store=True
    )

    active = fields.Boolean(
        default=True, )

    description = fields.Text()

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if 'hr_hospital_patient_visit_id' in vals:
                patient_visits = self.env['hr.hospital.patient.visit'].search(
                    [('id', '=', vals['hr_hospital_patient_visit_id'])]
                )
                for hr_hospital_patient_visit_id in patient_visits:
                    if not (hr_hospital_patient_visit_id
                            .hr_hospital_doctor_id.is_intern):
                        vals["approved"] = True
        return super().create(vals_list)

    @api.depends('doctor_id')
    @api.onchange('doctor_id')
    def _compute_approved(self):
        for rec in self:
            rec.approved = not rec.doctor_id.is_intern
