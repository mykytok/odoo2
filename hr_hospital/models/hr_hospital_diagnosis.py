# Візит - (модель "Візити пацієнтів")
# Хвороба
# Опис - (Призначення для лікування)
# Затверджено - (булева ознака) Коментар до пункту 3.3.1: Ця ознака вказує що даний діагноз,
# зроблений лікарем-ментором, був перевірений та затверджений його ментором.
import logging

from odoo import models, fields

_logger = logging.getLogger(__name__)


class Diagnosis(models.Model):
    _name = 'hr.hospital.diagnosis'
    _description = 'Diagnosis'

    name = fields.Char()

    hr_hospital_patient_visit_id = fields.Many2one(
        comodel_name='hr.hospital.patient.visit',
        string="Visit",
    )

    hr_hospital_disease_id = fields.Many2one(
        comodel_name='hr.hospital.disease',
        string="Disease",
    )

    approved = fields.Boolean(
        default=False,
        string="Approved",
    )

    active = fields.Boolean(
        default=True, )

    description = fields.Text()
