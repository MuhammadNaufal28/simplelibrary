from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

class OsRentbookLoan(models.Model):
    _name = 'os.rentbook.loan'
    _description = 'Os Rentbook Loan'
    _rec_name = 'member_id'


    member_id = fields.Many2one('os.rentbook.member', string='Member', required=True)
    book_id = fields.Many2one('os.rentbook.book', string='Book', required=True)
    loan_date = fields.Date(string='Loan Date', default=fields.Date.today, required=True)
    return_date = fields.Date(string='Return Date')
    quantity_loan = fields.Integer(string='Quantity Loan')
    status = fields.Selection([
        ('draft', 'Draft'),
        ('borrowed', 'Borrowed'),
        ('overdue', 'Overdue'),
        ('returned', 'Returned')
    ], string='Status', default='draft')

    def action_borrowed(self):
        self.write({'status': 'borrowed'})

    def action_overdue(self):
        self.write({'status': 'overdue'})

    def action_returned(self):
        self.write({'status': 'returned'})

    def action_draft(self):
        self.write({'status': 'draft'})

    def write(self, vals):
        # Call the super method to perform the actual write operation
        result = super(OsRentbookLoan, self).write(vals)

        # Check if the status is being set to 'returned'
        if 'status' in vals and vals['status'] == 'returned':
            # Delete related overdue records
            self.env['os.rentbook.overdue'].search([('loan_id', 'in', self.ids)]).unlink()

        return result


    def unlink(self):
        # Delete related overdue records when deleting loan records
        for record in self:
            self.env['os.rentbook.overdue'].search([('loan_id', '=', record.id)]).unlink()

        return super(OsRentbookLoan, self).unlink()

    overdue_days = fields.Integer(string='Overdue Days', compute='_compute_overdue_days', store=True)
    late_charge = fields.Float(string='Late Charge', compute='_compute_late_charge', store=True)
    late_amount_charge = fields.Float(string='Late Amount Charge', related='book_id.late_amount_charge', readonly=True)

    @api.depends('return_date')
    def _compute_overdue_days(self):
        today = fields.Date.today()
        for record in self:
            if record.return_date and today > record.return_date:
                record.overdue_days = (today - record.return_date).days
            else:
                record.overdue_days = 0

    @api.depends('overdue_days', 'book_id.late_amount_charge')
    def _compute_late_charge(self):
        for record in self:
            record.late_charge = record.overdue_days * record.late_amount_charge

    def action_overdue(self):
        # Update status
        self.write({'status': 'overdue'})
        
        # Create overdue record
        overdue_model = self.env['os.rentbook.overdue']
        for loan in self:
            overdue_model.create({
                'name': loan.book_id.name,
                'loan_id': loan.id,
                'overdue_days': loan.overdue_days,
                'fine_amount': loan.late_charge
            })

    @api.constrains('return_date', 'loan_date')
    def _check_return_date(self):
        for record in self:
            if record.return_date and record.loan_date and record.return_date < record.loan_date:
                raise ValidationError("The return date cannot be earlier than the loan date!")
            elif not record.return_date:
                raise ValidationError("Return Date Cannot Empty")

    @api.constrains('quantity_loan')
    def _check_quantity_loan(self):
        for record in self:
            if record.quantity_loan == 0:
                raise ValidationError("Quantity cannot be 0")
            elif record.quantity_loan < 0:
                raise ValidationError("Quantity cannot be less than 0")


    
    