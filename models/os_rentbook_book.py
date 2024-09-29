from odoo import models, fields, api, _


class os_rentbook_book(models.Model):
    _name = 'os.rentbook.book'
    _description = 'rentbook book'

    name = fields.Char(string='Title', required=True)
    author = fields.Char(string='Author')
    isbn = fields.Char(string='ISBN')
    genre_id = fields.Many2one('os.rentbook.genre', string='Genre')
    publisher = fields.Char(string='Publisher')
    publication_date = fields.Date(string='Publication Date')
    number_of_copies = fields.Integer(string='Number of Copies', required=True)
    available = fields.Integer(string='Available', compute='_compute_available', store=True)
    late_amount_charge = fields.Float(string='Late Amount Charge', required=True, help='Amount charged per day for late returns')
    image = fields.Binary(string='Book Cover')
    loan_ids = fields.One2many('os.rentbook.loan', 'book_id', string='Loans')


    @api.depends('number_of_copies', 'loan_ids.quantity_loan', 'loan_ids.status')
    def _compute_available(self):
        for record in self:
            total_quantity_loan = 0  # Inisialisasi jumlah pinjaman
            for loan in record.loan_ids:
                if loan.status == 'borrowed':  # Hanya hitung pinjaman yang berstatus borrowed
                    total_quantity_loan += loan.quantity_loan

            if total_quantity_loan > 0:
                record.available = record.number_of_copies - total_quantity_loan
            else:
                record.available = record.number_of_copies  # Jika tidak ada pinjaman, samakan dengan number_of_copies



    
    
    
    
    
    
    
    
    


