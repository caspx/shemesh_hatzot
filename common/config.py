# -*- coding: utf-8 -*-

import os
from datetime import datetime

TODAY = datetime.today().strftime('%d-%m-%Y')

CONFIG_FOLDER = os.path.expanduser('~/.config')
WS = os.path.join(CONFIG_FOLDER, 'shemesh_hatzot')

FOLDER_IMAGES = os.path.join(WS, f'images/{TODAY}/')
FOLDER_SAVES = os.path.join(WS, 'saves')
FOLDER_TWEETS = os.path.join(WS, 'tweets')

PATH_SAVES = os.path.join(WS, f'saves/{TODAY}_playlist.json')
PATH_TWEETS = os.path.join(WS, f'tweets/{TODAY}.json')


# ADD PATH TO THE CREDENTIALS FILE (LIKE: ~/.googleapi/client_secret.json)
GOOGLE_API_SECRET_FILE = ''

try:
    os.makedirs(FOLDER_IMAGES, exist_ok=True)
    os.makedirs(FOLDER_SAVES, exist_ok=True)
    os.makedirs(FOLDER_TWEETS, exist_ok=True)
except Exception as e:
    print('Failed to create workspace folders. exiting...', e)
    exit(2)
