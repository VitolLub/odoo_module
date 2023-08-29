from odoo import models, fields, api, http
import requests
import base64
import logging
import sys
from google_images_search import GoogleImagesSearch
import random

class CustomModule(models.Model):
    _logger = logging.getLogger(__name__)
    _name = 'custom.module'

    name = fields.Char(string='Name', required=True)
    email = fields.Char(string='Email', required=True)
    phone = fields.Char(string='Phone', required=True)
    avatar = fields.Binary(string='Avatar', required=True, attachment=True)
    group_id = fields.Many2one('custom.module.group', string='Group', required=True)


    @api.model
    def create(self, vals):

        # Get image from URL
        image_base64 = self._image_to_base64(self._find_google_avatars())

        try:
            attachment_data = {
                'name': 'New Attachment',
                'datas': image_base64,
                'res_model': 'custom.module',
                'res_id':self._get_last_recorded_id(),
                'type': 'binary',
                'mimetype': 'image/png'
            }
            attachment = http.request.env['ir.attachment'].sudo().create(attachment_data)

            # assign the attachment to the record we just created
            vals['avatar'] = attachment.datas
            return super(CustomModule, self).create(vals)
        except Exception as e:
            self._logger.error('Error while creating attachment: %s' % e)
            self._logger.error('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))

    def _get_last_recorded_id(self):

        last_record = self.env['custom.module'].search([], order='id desc', limit=1)

        return last_record.id
    def _image_to_base64(self,url):

        # Get image from URL
        response = requests.get(url)

        if response.status_code == 200:
            # Convert image to base64
            image_base64 = base64.b64encode(response.content)

            return image_base64


    def _find_google_avatars(self):

        gis = GoogleImagesSearch('AIzaSyDzUeGQOCPQXxozKtZIe54Ph0QLnpaCjn0',
                                 '636c5584cb3734ad1')

        # Set the search parameters
        search_params = ['simple avatar', 'single avatar', 'simple single avatar', 'simple avatar icon',
                         'single avatar icon', 'simple single avatar icon', 'simple avatar image', 'single avatar image 60x60', 'simple single avatar image 60x60', 'simple avatar icon 60x60', 'single avatar icon 60x60', 'avatar icon 60x60']

        params_for_search = {
            'q': random.choice(search_params),
            'num': 1,  # Number of images to retrieve
            'safe': 'high',  # Safe search level: high, medium, off

        }

        # Perform the search
        gis.search(params_for_search)

        # Retrieve the image URLs
        url = ''
        for image in gis.results():
            url = image.url
            break

        return url




