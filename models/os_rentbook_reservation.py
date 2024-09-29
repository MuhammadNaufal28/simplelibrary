from odoo import models, fields


class OsRentbookReservation(models.Model):
    _name = 'os.rentbook.reservation'
    _description = 'Os Rentbook Reservation'
    _rec_name = 'member_id'

    member_id = fields.Many2one('os.rentbook.member', string='Member', required=True)
    book_id = fields.Many2one('os.rentbook.book', string='Book', required=True)
    reservation_date = fields.Date(string='Reservation Date', default=fields.Date.today, required=True)
    status = fields.Selection([
        ('active', 'Active'),
        ('cancelled', 'Cancelled'),
        ('fulfilled', 'Fulfilled')
    ], string='Status', default='active')