# -*- coding: utf-8 -*-

import json
import os
import re
import time
import urllib.request
from typing import List

from . import safe_run
from common import youtube_api
from common.config import PATH_SAVES, FOLDER_IMAGES


def save_playlist(playlist: dict):
    with open(PATH_SAVES, 'a') as save:
        json.dump(playlist, save)


def download_image(date: str, url: str) -> str:
    if not os.path.exists(FOLDER_IMAGES):
        os.makedirs(FOLDER_IMAGES)

    image_name = os.path.basename(url)
    image_path = os.path.join(FOLDER_IMAGES, f'{date}_{image_name}')
    urllib.request.urlretrieve(url, image_path)

    return image_path


@safe_run
def load_tweets_from_file(path: str, limit: int = None) -> List[dict]:
    with open(path, 'rb') as f:
        tweets = [json.loads(t) for t in f.readlines()]
    if limit is not None:
        tweets = tweets[:limit]
    print(f"Loaded {len(tweets)} tweets (playlists)")
    return tweets


def clean_playlist(play_list: str) -> List[str]:
    pat = '(.*)\s*\.\d+$'
    constraints = (' ', '-')
    clean_names = []
    names = [t for t in play_list.split('\n') if t]
    for n in names[1:]:
        if all(c not in n for c in constraints) or len(n) < 7:
            continue
        try:
            clean_name = re.search(pat, n).group(1)
            clean_names.append(clean_name.strip())
        except:
            print(f'using name: {n}')
            clean_names.append(n.strip())

    return clean_names


def search_videos(tracks: List[str]) -> List[str]:
    videos_ids = []
    for t in tracks:
        track = youtube_api.search_video(t)
        videos_ids.append(track)
        time.sleep(1)

    return videos_ids
