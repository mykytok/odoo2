import logging

from odoo import models, fields

_logger = logging.getLogger(__name__)


class AbstractPerson(models.AbstractModel):
    _name = 'hr.hospital.abstract.person'
    _description = 'Person'

    full_name = fields.Char()

    phone = fields.Char()

    photo = fields.Image(
        max_wight=512,
        max_height=512,
    )

    gender = fields.Selection(
        [('male', 'Male'),
         ('female', 'Female')],
        # default="_",
    )
