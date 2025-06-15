import logging

from odoo import models, fields, api

_logger = logging.getLogger(__name__)


class PersonalDoctorUpdate(models.TransientModel):
    _name = 'hr.hospital.persdoc.update.wzd'
    _description = 'Personal doctor update'

    doctor_id = fields.Many2one(
        comodel_name='hr.hospital.doctor',
        string='Doctor',
    )

    patient_ids = fields.Many2many(
        comodel_name='hr.hospital.patient',
        string='Patient',
    )

    @api.model
    def default_get(self, vals):
        res = super().default_get(vals)
        if self.env.context.get('active_ids'):
            active_patient_ids = self.env['hr.hospital.patient'].browse(self.env.context.get('active_ids'))
            res['patient_ids'] = [(6, 0, active_patient_ids.mapped('id'))]
        return res

    def update_personal_doctor(self):
        self.ensure_one()
        # Stable approach for white objects
        self.patient_ids.write({'hr_hospital_personal_doctor_id': self.doctor_id})
        # Bad approach for white objects
        # for patient_id in self.patient_ids:
        #     patient_id.hr_hospital_personal_doctor_id = self.doctor_id
