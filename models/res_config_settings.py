from odoo import models, fields

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    youtube_api_key = fields.Char(string='YouTube API Key', config_parameter='elearning_youtube.youtube_api_key')