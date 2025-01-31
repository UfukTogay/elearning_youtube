from odoo import models, api

class SlideChannel(models.Model):
    _inherit = 'slide.channel'

    def action_open_import_youtube_wizard(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Import YouTube Playlist',
            'res_model': 'youtube.playlist.import.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_channel_id': self.id},
        }