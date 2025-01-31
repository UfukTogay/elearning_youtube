import re
import requests
from odoo import models, fields, api, _
from odoo.exceptions import UserError

class YouTubePlaylistImportWizard(models.TransientModel):
    _name = 'youtube.playlist.import.wizard'
    _description = 'Import YouTube Playlist Wizard'

    playlist_url = fields.Char(string='Playlist URL', required=True)

    def _get_youtube_api_key(self):
        return self.env['ir.config_parameter'].get_param('elearning_youtube.youtube_api_key', default='')

    def _extract_playlist_id(self, url):
        regex = r'(?:https?://)?(?:www\.)?youtube\.com/playlist\?list=([a-zA-Z0-9_-]+)'
        match = re.search(regex, url)
        return match.group(1) if match else None

    def _fetch_playlist_data(self, playlist_id):
        api_key = self._get_youtube_api_key()
        if not api_key:
            raise UserError(_('YouTube API Key is not configured.'))

        # Fetch playlist info
        url = f'https://www.googleapis.com/youtube/v3/playlists?part=snippet&id={playlist_id}&key={api_key}'
        response = requests.get(url)
        if response.status_code != 200:
            raise UserError(_('Failed to fetch playlist data. Check the API key and URL.'))
        data = response.json()
        if not data.get('items'):
            raise UserError(_('Playlist not found.'))
        playlist_info = data['items'][0]['snippet']

        # Fetch playlist items
        videos = []
        next_page_token = None
        while True:
            items_url = f'https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&maxResults=50&playlistId={playlist_id}&key={api_key}'
            if next_page_token:
                items_url += f'&pageToken={next_page_token}'
            response = requests.get(items_url)
            if response.status_code != 200:
                break
            items_data = response.json()
            for item in items_data.get('items', []):
                video_snippet = item['snippet']
                video_id = video_snippet['resourceId']['videoId']
                videos.append({
                    'title': video_snippet['title'],
                    'description': video_snippet.get('description', ''),
                    'video_id': video_id,
                })
            next_page_token = items_data.get('nextPageToken')
            if not next_page_token:
                break

        return {
            'title': playlist_info['title'],
            'description': playlist_info.get('description', ''),
            'videos': videos,
        }

    def action_import(self):
        self.ensure_one()
        playlist_id = self._extract_playlist_id(self.playlist_url)
        if not playlist_id:
            raise UserError(_('Invalid YouTube Playlist URL.'))

        data = self._fetch_playlist_data(playlist_id)

        # Get existing course from context
        course = self.env['slide.channel'].browse(self.env.context.get('active_id'))
        if not course.exists():
            raise UserError(_('Course not found. Please save the course first!'))

        course.write({
            'name': data['title'],  # Will overwrite manually entered title
            'description': data['description'] or course.description,
        })

        # Create Lessons (Slide Slides)
        for video in data['videos']:
            self.env['slide.slide'].create({
                'name': video['title'],
                'channel_id': course.id,
                'slide_category': 'video',
                'video_url': f'https://www.youtube.com/watch?v={video["video_id"]}',
                'description': video['description'],
            })

        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'slide.channel',
            'res_id': course.id,
            'target': 'current',
        }