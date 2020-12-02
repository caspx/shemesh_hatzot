# -*- coding: utf-8 -*-

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

from common.config import GOOGLE_API_SECRET_FILE
from . import safe_run

youtube_client = None


@safe_run
def googleapi_auth():
    global youtube_client

    if youtube_client is not None:
        return youtube_client

    scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]

    api_service_name = "youtube"
    api_version = "v3"

    client_secrets_file = GOOGLE_API_SECRET_FILE

    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    credentials = flow.run_console()
    youtube_client = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)

    return youtube_client


@safe_run
def search_video(query: str):
    youtube = googleapi_auth()
    request = youtube.search().list(
        part="snippet",
        maxResults=1,
        q=query
    )

    response = request.execute()
    v_id = response['items'][0]['id']['videoId']
    if v_id:
        return v_id
    else:
        print(f'ERROR: Track - {query} was not found!')
        print(f'Skipping...')


@safe_run
def create_new_playlist(name: str, description: str):
    youtube = googleapi_auth()

    request = youtube.playlists().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": name,
                "description": description,
                "defaultLanguage": "en"
            },
            "status": {
                "privacyStatus": "public"
            }
        }
    )
    response = request.execute()
    return response['id']


@safe_run
def add_video_2_playlist(video_id: str, playlist_id: str, position: int = 0):
    youtube = googleapi_auth()
    request = youtube.playlistItems().insert(
        part="snippet",
        body={
            "snippet": {
                "playlistId": playlist_id,
                "position": position,
                "resourceId": {
                    "kind": "youtube#video",
                    "videoId": video_id
                }
            }
        }
    )
    response = request.execute()
    return response



