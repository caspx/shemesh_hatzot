# Shemesh Hatzot

Automatically generate a youtube playlist from a tracklist image uploaded to twitter. 


The script downloads the tracklist images from twitter, converts them to text, and creates (using Google API) a Youtube playlist in your account.

### Usage

Create a python3 virtual environment
```sh
$ python3 -m venv /path/to/new/virtual/environment
```
Install requirements
```sh
$ pip install -r requirements.txt
```

The script uses google api to create/edit playlists, so to use it you'll need to edit the "config.py" file with the location of your credentials file
```py
# ADD PATH TO THE CREDENTIALS FILE (LIKE: ~/.googleapi/client_secret.json)
GOOGLE_API_SECRET_FILE = ''
```

### Examples
Using twitter
```sh
python playlist_maker.py --from-date "2018-03-11 00:00:00"
```
From local file containing tweets with images
```sh
python playlist_maker.py --tweets-file PATH_TO_FILE
```
