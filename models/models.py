# -*- coding: utf-8 -*-

from pdf2image import convert_from_bytes
import pytesseract
import logging
import re
from odoo import models, fields, api

_logger = logging.getLogger(__name__)

class hbit_ocr(models.Model):
     _name = 'hbit_ocr.hbit_ocr'
     _description='Regular expressions for data extraction via OCR'
     _order = "re_prio desc"

     re_name = fields.Char(string='Id', required=True)
     re_exp = fields.Char(string='Regex', required=True)
     re_model = fields.Char(string='target model', required=True)
     re_field = fields.Char(string='target field', required=True)
     re_value = fields.Char(string='default value')
     re_prio = fields.Integer(string='Priority')
     re_searchModel = fields.Char(string='get id from model')
     re_searchString = fields.Char(string='re search string')

     @api.multi
     def ocr(self,pdf_bin,search_model):
          if not search_model:
               search_model=""
          res_data={}
          try:
               images = convert_from_bytes(pdf_bin)
          except:
               _logger.warning('Failed to convert pdf')
               return None
          text = ''
          for im in images:
               try:
                    text += pytesseract.image_to_string(im,lang='spa')
               except:
                    _logger.warning('Failed to OCR')
                    return None
          for rex in self.search([('re_model', 'ilike', search_model)]):
               res=re.search(rex.re_exp,text,re.MULTILINE | re.DOTALL | re.IGNORECASE)
               if res:
                    if not rex.re_model in res_data:
                         res_data[rex.re_model]={}
                    if rex.re_field not in res_data[rex.re_model]:
                        if rex.re_searchModel:
                            reA=rex.re_searchString.split(',')
                            rec=self.env[rex.re_searchModel].search([(reA[0],reA[1],reA[2])])
                            if rec and len(rec) > 0:
                                res_data[rex.re_model][rex.re_field]=rec[0].id
                        else:
                            if rex.re_value:
                                value=rex.re_value
                            else:
                                value=res.group(1)
                            if rex.re_field=='unit_amount':
                                value=float(value.replace(',','.'))
                                if value < 2:
                                    _logger.warning('value too small: %s. regex: %s' % (value, rex.re_exp))
                            res_data[rex.re_model][rex.re_field]=value
          if search_model not in res_data:
              res_data[search_model]={}
          res_data[search_model]['description']=text
          return res_data





#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()

#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100
