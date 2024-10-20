from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError



class OsRentbookMember(models.Model):
    _name = 'os.rentbook.member'
    _description = 'Os Rentbook Member'

    name = fields.Char(string='Name', required=True)
    membership_id = fields.Char(string='Membership ID')
    email = fields.Char(string='Email')
    phone_number = fields.Char(string='Phone Number')
    address = fields.Text(string='Address')

    @api.constrains('email')
    def _check_email(self):
        for rec in self:
            if rec.email:
                # Menggunakan query SQL untuk memeriksa karakter '@'
                self.env.cr.execute("SELECT 1 FROM os_rentbook_member WHERE id = %s AND email LIKE '%%@%%'", (rec.id,))
                result = self.env.cr.fetchone()
                if not result:
                    raise ValidationError("Email harus mengandung karakter '@'.")
