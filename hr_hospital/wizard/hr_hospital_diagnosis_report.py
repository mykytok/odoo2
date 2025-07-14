import logging

from odoo import models, fields, api

_logger = logging.getLogger(__name__)


class DiagnosisReport(models.TransientModel):
    _name = 'hr.hospital.diagnosis.report'
    _description = 'Diagnosis report'

    doctor_ids = fields.Many2many(
        comodel_name='hr.hospital.doctor',
        string='Doctors',
    )
    disease_ids = fields.Many2many(
        comodel_name='hr.hospital.disease',
        string='Diseases',
    )
    start_date = fields.Date(
        string="Start date"
    )
    end_date = fields.Date(
        string="End date"
    )

    @api.model
    def default_get(self, vals):
        res = super().default_get(vals)
        if self.env.context.get('active_ids'):
            active_doctor_ids = self.env['hr.hospital.doctor'].browse(
                self.env.context.get('active_ids')
            )
            res['doctor_ids'] = [(6, 0, active_doctor_ids.mapped('id'))]
        return res

    def update_diagnosis_ids(self):
        self.ensure_one()
        search_list = [
            ('hr_hospital_patient_visit_id.visit_datetime',
             '>=',
             self.start_date),
            ('hr_hospital_patient_visit_id.visit_datetime',
             '<=',
             self.end_date)
        ]
        if self.doctor_ids:
            search_list.append(
                ('hr_hospital_patient_visit_id.hr_hospital_doctor_id',
                 'in',
                 self.mapped('doctor_ids.id'))
            )
        if self.disease_ids:
            search_list.append(
                ('hr_hospital_disease_id',
                 'in',
                 self.mapped('disease_ids.id'))
            )
        rec = self.env['hr.hospital.diagnosis'].search(search_list)

        return {
            'name': 'Diagnosis',
            'views': [[
                self.env.ref('hr_hospital.hr_hospital_diagnosis_tree_group_disease').id,
                'tree'
            ]],
            'type': 'ir.actions.act_window',
            'res_model': 'hr.hospital.diagnosis',
            'view_mode': 'tree',
            'res_id': False,
            'target': 'self',
            'domain': [('id', 'in', rec.mapped('id'))],
        }
