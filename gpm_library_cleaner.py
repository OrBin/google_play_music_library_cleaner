from gmusicapi import Mobileclient
import sys
from datetime import datetime
import time
import logging
import os

# CONSTANTS
RATING_DOWNVOTE = "1"
CONFIG_FILE_NAME = os.path.join(os.path.abspath(os.path.dirname(__file__)), ".google_play_music_cleaner_config")

logging.basicConfig(filename=os.path.join(os.path.abspath(os.path.dirname(__file__)), 'log.txt'),level=logging.INFO, format="%(asctime)s %(levelname)s %(module)s %(message)s", datefmt='%Y-%m-%d %H:%M:%S %Z')
api = Mobileclient()


with open(CONFIG_FILE_NAME) as conf_file:
	username, password = conf_file.read().split("\n")[:2]
	if not api.login(username, password, Mobileclient.FROM_MAC_ADDRESS):
		logging.error("Error: could not log in.")
		sys.exit(1)

all_songs = api.get_all_songs()
downvoted_songs = [song for song in all_songs if song["rating"] == RATING_DOWNVOTE]

if len(downvoted_songs) == 0:
	logging.info("No downvoted songs")
else:
	logging.info("Deleting %s downvoted songs:", len(downvoted_songs))
	for song in downvoted_songs:
		logging.info("%s - %s", song["artist"], song["title"])
	api.delete_songs([song["id"] for song in downvoted_songs])
