# -*- coding: utf-8 -*-
# from odoo import http


# class RentBook(http.Controller):
#     @http.route('/rent_book/rent_book', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/rent_book/rent_book/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('rent_book.listing', {
#             'root': '/rent_book/rent_book',
#             'objects': http.request.env['rent_book.rent_book'].search([]),
#         })

#     @http.route('/rent_book/rent_book/objects/<model("rent_book.rent_book"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('rent_book.object', {
#             'object': obj
#         })
