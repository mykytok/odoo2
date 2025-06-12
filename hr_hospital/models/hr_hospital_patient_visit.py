import logging

import pytz

from odoo import models, fields, api, tools, exceptions

_logger = logging.getLogger(__name__)


class PatientVisit(models.Model):
    _name = 'hr.hospital.patient.visit'
    _description = 'Patient visit'

    active = fields.Boolean(
        default=True, )

    description = fields.Text()

    hr_hospital_doctor_id = fields.Many2one(
        comodel_name='hr.hospital.doctor',
        string="Doctor",
    )

    hr_hospital_patient_id = fields.Many2one(
        comodel_name='hr.hospital.patient',
        string="Patient",
    )

    hr_hospital_diagnosis_ids = fields.One2many(
        comodel_name='hr.hospital.diagnosis',
        inverse_name='hr_hospital_patient_visit_id',
        string="Diagnosis",
    )

    status = fields.Selection(
        [('scheduled', 'Scheduled'),
         ('completed', 'Completed'),
         ('cancelled', 'Cancelled')],
        default="scheduled",
        string="Status",
    )

    scheduled_datetime = fields.Datetime(
        default=lambda self: fields.Datetime.now(),
        string = "Scheduled date and time of visit"
    )

    visit_datetime = fields.Datetime(
        string="Date and time of visit"

    )

    # Work with field before save
    def write(self, vals):
        for rec in self:
            if (rec.status == 'completed'
                    and any(field in vals for field in ['hr_hospital_doctor_id', 'visit_datetime'])):
                raise exceptions.UserError('It is forbidden to change fields "Doctor", "Date and time of visit" '
                                  'after setting the status Completed')
            if (rec.active
                    and 'active' in vals
                    and not vals['active']
                    and rec.hr_hospital_diagnosis_ids):
                 raise exceptions.UserError('It is forbidden to Archive if there are Diagnoses')
        return super().write(vals)

    # # On Delete object
    # def unlink(self):
    #     for rec in self:
    #         if rec.hr_hospital_diagnosis_ids:
    #             raise UserError('It is forbidden to Delete if there are Diagnoses')
    #     return super().unlink()
    @api.ondelete(at_uninstall=False)
    def _unlink_is_diagnosis(self):
          for rec in self:
              if rec.hr_hospital_diagnosis_ids:
                  raise exceptions.UserError('It is forbidden to Delete if there are Diagnoses')

    # Додати перевірку, щоб не можна було записати одного
    # пацієнта до одного лікаря в один день більше одного разу.
    @api.constrains('hr_hospital_doctor_id', 'hr_hospital_patient_id', 'scheduled_datetime')
    def _check_duplicate_visit_in_scheduled_date(self):
        ltz = pytz.timezone(self.env.user.tz)
        for rec in self:
            scheduled_datetime_utcnow = rec.scheduled_datetime.utcnow()
            offset = ltz.utcoffset(scheduled_datetime_utcnow)
            datetime_for_search = rec.scheduled_datetime + offset
            start_day = tools.start_of(datetime_for_search, 'day') - offset
            end_day = tools.end_of(datetime_for_search, 'day') - offset

            other_visits_in_scheduled_date = self.env['hr.hospital.patient.visit'].search([
                ('id', '!=', rec.id),
                ('hr_hospital_doctor_id', '=', rec.hr_hospital_doctor_id.id),
                ('hr_hospital_patient_id', '=', rec.hr_hospital_patient_id.id),
                ('scheduled_datetime', '>=', start_day),
                ('scheduled_datetime', '<=', end_day)
            ])
            if other_visits_in_scheduled_date:
                raise exceptions.UserError("On the scheduled day, "
                                "the visit to the current doctor is already present.")
