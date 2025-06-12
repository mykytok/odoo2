from odoo import models, fields

class DoctorsSpecialty(models.Model):
    _name = 'hr.hospital.doctors.specialty'
    _description = "Doctor's specialty"

    name = fields.Char()

    active = fields.Boolean(
        default=True, )

    description = fields.Text()
