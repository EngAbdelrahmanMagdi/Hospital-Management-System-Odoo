from asyncio.windows_events import NULL
from odoo import api, models , fields, exceptions
from odoo.exceptions import UserError

class CrmCustomersInherit(models.Model):
    _inherit='res.partner'
    
    salary=fields.Float()
    related_patient_id = fields.Many2one("hms.patient")
    
            
    def unlink(self):
        for record in self:
            if record.related_patient_id:
                raise UserError("Can't delete") 
        super().unlink()
    
    
    @api.constrains('related_patient_id')
    def check_email(self):
        if self.related_patient_id.email != self.email and not self.env['hms.patient'].search([('email','=',self.email)]):
            raise exceptions.ValidationError('email exists for a patient')

            
