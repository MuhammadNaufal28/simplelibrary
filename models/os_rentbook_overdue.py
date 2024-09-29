
from odoo import models, fields


class OsRentbookOverdue(models.Model):
    _name = 'os.rentbook.overdue'
    _description = 'Os Rentbook Overdue'

    name = fields.Char(string='Book')
    loan_id = fields.Many2one('os.rentbook.loan', string='Loan', required=True)
    overdue_days = fields.Integer(string='Overdue Days', store=True)
    fine_amount = fields.Float(string='Fine Amount', store=True)