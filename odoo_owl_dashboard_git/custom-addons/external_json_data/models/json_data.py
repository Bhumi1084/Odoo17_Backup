import requests
from odoo import models, fields, api

class CountryImport(models.TransientModel):
    _name = 'country.import'
    _description = 'Country Import'


    name = fields.Char(string="Country Name")
    code = fields.Char(string="Country Code")
    tld = fields.Char(string="Country TLD")
    flag = fields.Binary(string="Flag Image")