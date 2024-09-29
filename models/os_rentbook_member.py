from odoo import models, fields



class OsRentbookMember(models.Model):
    _name = 'os.rentbook.member'
    _description = 'Os Rentbook Member'

    name = fields.Char(string='Name', required=True)
    membership_id = fields.Char(string='Membership ID')
    email = fields.Char(string='Email')
    phone_number = fields.Char(string='Phone Number')
    address = fields.Text(string='Address')
    