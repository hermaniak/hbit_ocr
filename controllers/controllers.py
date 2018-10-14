# -*- coding: utf-8 -*-
from odoo import http

# class HbitOcr(http.Controller):
#     @http.route('/hbit_ocr/hbit_ocr/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hbit_ocr/hbit_ocr/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('hbit_ocr.listing', {
#             'root': '/hbit_ocr/hbit_ocr',
#             'objects': http.request.env['hbit_ocr.hbit_ocr'].search([]),
#         })

#     @http.route('/hbit_ocr/hbit_ocr/objects/<model("hbit_ocr.hbit_ocr"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hbit_ocr.object', {
#             'object': obj
#         })