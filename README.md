# YouTube Playlist to eLearning

This Odoo App fetches videos from a YouTube playlist and saves them as courses in the Odoo eLearning platform.

## Features
- Fetch videos using a YouTube playlist URL.
- Automatically add videos to the eLearning platform.
- Manage YouTube API Key from the Settings menu.

## Installation & Usage

### Requirements
- Odoo 15 or higher.
- YouTube API Key (obtainable from Google Cloud Console).

### Steps
1. Download or clone the module:
   ```bash
   git clone https://github.com/your-username/youtube_elearning.git
2. Place the module in Odoo's addons directory.
3. Restart Odoo.
4. Go to the Apps menu in Odoo
5. Search for the elearning_youtube module and install it.
6. Open eLearning app
7. Go to the Configuration/Settings menu and enter your YouTube API Key (obtained from Google Cloud Console) in the YouTube API Key field.
8. Create a new Course
9. Set Course Title and Click Import From YouTube
10. Enter YouTube playlist URL
11. Click Fetch and Import button
12. Wait for the magic to happen

## ToDo List
1. Get transcript of videos
2. Create quizes for each video automatically using ChatGPT
