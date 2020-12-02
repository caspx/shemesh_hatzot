#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import os
import pytesseract
import time
import twint

from PIL import Image
from datetime import datetime

from common.config import PATH_TWEETS
from common import utils, youtube_api


def get_tweets(from_date: str = None) -> None:
    # Configuration
    c = twint.Config()
    c.Username = "kereneubach"
    c.Search = 'רשימת הקטעים'
    c.Images = True
    c.Store_json = True
    c.Output = PATH_TWEETS
    if from_date is not None:
        c.Since = from_date
    # Run
    twint.run.Search(c)


def extract_playlists_from_tweets(path_tweets: str = PATH_TWEETS):
    tweets = utils.load_tweets_from_file(path_tweets, limit=2)
    if tweets is None:
        print('Was unable to scrap for tweets. exiting...')
        exit(2)
    play_lists = {}
    for t in tweets:
        image_url = t['photos'][0]
        image_path = utils.download_image(t['date'], image_url)
        # Extract playlist from image
        image_str = pytesseract.image_to_string(Image.open(image_path))
        print("Raw OCR output:")
        print(image_str + '\n\n')
        play_lists[t['date']] = dict(image=image_url, tracks=utils.clean_playlist(image_str))

    utils.save_playlist(play_lists)
    return play_lists


def upload_playlists(play_lists: dict):
    for pl in play_lists.items():
        pl_date = pl[0]
        pl_image = pl[1]['image']
        pl_tracks = pl[1]['tracks']

        # Create new playlist
        pl_name = f'Shemesh Hatzot - {pl_date}'
        pl_desc = f'Auto generated playlist from the {pl_date} prog.\n\n' \
                  f'Playlist image:\n\n {pl_image}'

        new_playlist_id = youtube_api.create_new_playlist(name=pl_name, description=pl_desc)
        print(f'New playlist has been created - {new_playlist_id}')

        # Search YouTube for the tracks in the playlist
        tracks_youtube_ids = utils.search_videos(pl_tracks)

        # Adding tracks to the new playlist
        # Reverse order because youtube api insert a new video at the top
        tracks_youtube_ids.reverse()
        for t_id in tracks_youtube_ids:
            youtube_api.add_video_2_playlist(t_id, new_playlist_id)
            print(f"Added {t_id} to {new_playlist_id}")
            time.sleep(1)


def main(args):
    if args.tweets_file is None:
        get_tweets(args.from_date)
        playlists = extract_playlists_from_tweets()
    else:
        playlists = extract_playlists_from_tweets(args.tweets_file)
    upload_playlists(playlists)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Playlist Maker for Shemesh Hatzot')
    parser.add_argument('--from-date', default=None, help='Scrape tweets from the specified date (Example: "2020-03-11 00:00:00")')
    parser.add_argument('--tweets-file', default=None, help='Path to local file containing saved tweets (skipping scraping)')

    args = parser.parse_args()
    main(args)
