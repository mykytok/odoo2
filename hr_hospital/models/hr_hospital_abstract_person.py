import logging

from odoo import models, fields, api

_logger = logging.getLogger(__name__)


class AbstractPerson(models.AbstractModel):
    """Abstract person model
                """
    _name = 'hr.hospital.abstract.person'
    _description = 'Person'

    full_name = fields.Char()

    phone = fields.Char()

    photo = fields.Image(
        max_width=512,
        max_height=512,
    )

    gender = fields.Selection(
        [('male', 'Male'),
         ('female', 'Female')],
        # default="_",
    )

    @api.depends('full_name')
    def _compute_display_name(self):
        for rec in self:
            rec.display_name = rec.full_name

    # @api.model
    # def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
    #     args = list(args or [])
    #     if name:
    #         args += [('full_name', operator, name)]
    #         return self._search(args, limit=limit, access_rights_uid=name_get_uid)
    #     return None

    # @api.model
    # def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None, order=None):
    #     args = list(args or [])
    #     if name:
    #         args += [('full_name', operator, name)]
    #         return self._search(args, limit=limit, order=order, access_rights_uid=name_get_uid)
    #     return None

    @api.model
    def _name_search(self, name='', args=None, operator='ilike', limit=100,
                     order=None):
        args = list(args or [])
        if name:
            args += [('full_name', operator, name)]
        return self._search(args, limit=limit, order=order)
