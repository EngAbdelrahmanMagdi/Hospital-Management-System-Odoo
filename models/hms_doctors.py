from odoo import models, fields


class HmsDoctor(models.Model):
    _name = "hms.doctors"
    
    first_name = fields.Char()
    last_name = fields.Char()
    image = fields.Image()
    patients = fields.Many2many(comodel_name='hms.patient',read_only=True)