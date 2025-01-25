from odoo import models, fields, api
import requests

class SlideChannel(models.Model):
    _inherit = 'slide.channel'

    youtube_playlist_url = fields.Char(string='YouTube Playlist URL')
    youtube_playlist_id = fields.Char(string='YouTube Playlist ID', compute='_compute_youtube_playlist_id', store=True)

    @api.depends('youtube_playlist_url')
    def _compute_youtube_playlist_id(self):
        for record in self:
            if record.youtube_playlist_url:
                # Extract playlist ID from URL
                playlist_id = record.youtube_playlist_url.split('list=')[-1]
                record.youtube_playlist_id = playlist_id
            else:
                record.youtube_playlist_id = False

    def fetch_youtube_playlist(self):
        self.ensure_one()
        if not self.youtube_playlist_id:
            raise ValueError("YouTube Playlist ID not found!")

        # Fetch YouTube API Key from settings
        api_key = self.env['ir.config_parameter'].sudo().get_param('elearning_youtube.youtube_api_key')
        if not api_key:
            raise ValueError("YouTube API Key not found! Please add it in Settings.")
