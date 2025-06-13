import logging

from odoo import models, fields

_logger = logging.getLogger(__name__)


class Disease(models.Model):
    _name = 'hr.hospital.disease'
    _description = 'Disease'

    name = fields.Char()

    parent_id = fields.Many2one(
        comodel_name='hr.hospital.disease',
        string='Parent'
    )
    child_ids = fields.One2many(
        comodel_name='hr.hospital.disease',
        inverse_name='parent_id',
        string='Children'
    )
    parent_path = fields.Char(index=True, unaccent=False)

    active = fields.Boolean(
        default=True, )

    description = fields.Text()
