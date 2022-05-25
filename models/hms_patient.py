from tkinter import HIDDEN
from odoo import models, fields, api, exceptions
from math import floor
from odoo.exceptions import UserError

class HmsPatient(models.Model):
    _name = "hms.patient"
    _rec_name="full_name"
    first_name = fields.Char()
    last_name = fields.Char()
    full_name = fields.Char(string='Full_name', compute='_compute_full_name')
    email = fields.Char(required=True) 
    birth_date = fields.Date(string='Birth date', default=fields.Date.today())
    history = fields.Html()
    cr_ratio = fields.Float()
    blood_type = fields.Selection([("A+","A+"), ("A-","A-"), ("B+","B+"), ("B-","B-"), ("O+","O+"), ("O-","O-")], default="A+")
    pcr = fields.Boolean()
    image = fields.Image()
    address = fields.Char()
    age = fields.Integer(compute="calculate_age")
    state = fields.Selection([
        ('u', 'Undetermined'),
        ('g', 'Good'),
        ('f', 'Fair'),
        ('s', 'Serious'),
    ], default='u')
    
    
    department_id = fields.Many2one("hms.department")
    doctors = fields.Many2many("hms.doctors")
    department_capacity = fields.Integer( related="department_id.capacity")
    logs = fields.One2many(comodel_name='hms.logs', inverse_name='patient_id', string="Logs")
    department_open = fields.Boolean(related='department_id.is_opened', default=True)
    
    def next_state(self):
        if self.state == 'u':
            self.state = 'g'
            self.changeState('Good')
        elif self.state == 'g':
            self.state = 'f'
            self.changeState('Fair')

        elif self.state == 'f':
            self.state = 's'
            self.changeState('Serious')

        elif self.state == 's':
            self.state = 'u'
            self.changeState('Undetermined')


    def changeState(self,state):
        self.env['hms.logs'].create({
            'description': "Patient State Changed To " + state,
            'patient_id': self.id
        })
        
    @api.depends('first_name', 'last_name')
    def _compute_full_name(self):
        for rec in self:
            rec.full_name = rec.first_name + ' ' + rec.last_name

    @api.onchange('department_id')
    def onchange_department_id(self):
        if not self.department_open and self.first_name:
            raise UserError("Department not opened")
    
    @api.depends('birth_date')
    def calculate_age(self):
        for record in self:
            get_today= fields.Date.today(record)
            get_birthdate= fields.Date.to_date(record.birth_date)
            record.age =floor((get_today - get_birthdate).days/365)
            

    @api.onchange('age')
    def onchange_age(self):
        if self.age < 30 and self.age != 0:
            self.pcr = True
            return {
            "warning": {
                "title":"Msg Title", 
                "message": "You have changes the PCR value"
            } 
            }
            
       

    @api.onchange('age')
    def onchange_age_reverse(self):
        if self.age >= 30:
            self.pcr = False
    
    _sql_constraints=[
        ('Duplicate_email' , 'UNIQUE(email)','email is already exists') 
        ] 
        
    @api.constrains('email')
    def check_email(self):
        if self.email:
            match = re.match('^([A-Z|a-z|0-9](\.|_){0,1})+[A-Z|a-z|0-9]\@([A-Z|a-z|0-9])+((\.){0,1}[A-Z|a-z|0-9]){2}\.[a-z]{2,3}$', self.email)
            if match == None:
                raise exceptions.ValidationError('Not a valid E-mail')

    