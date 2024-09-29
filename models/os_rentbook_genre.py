from odoo import models, fields



class OsRentbookGenre(models.Model):
    _name = 'os.rentbook.genre'
    _description = 'Os Rentbook Genre'

    name = fields.Char(string='Nama')
    
