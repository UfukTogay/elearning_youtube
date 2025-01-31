{
    'name': 'YouTube Playlist to eLearning',
    'version': '1.0',
    'summary': 'Create eLearning course from YouTube playlist',
    'description': 'Fetches videos from a YouTube playlist and saves them as courses in the Odoo eLearning platform.',
    'author': 'Ufuk Togay',
    'website': 'https://fimeltd.com',
    'category': 'eLearning',
    'depends': ['website_slides'],
    'data': [
        'security/ir.model.access.csv',
        'views/res_config_settings_views.xml',
        'views/slide_channel_views.xml',
        'views/youtube_playlist_import_wizard_views.xml',
    ],
    'i18n': [
        'i18n/tr_TR.po',
        'i18n/en_US.po',
    ],
    'installable': True,
    'application': True,
}