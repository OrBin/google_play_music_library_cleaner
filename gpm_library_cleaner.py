from gmusicapi import Mobileclient
from os.path import join, dirname, abspath
from datetime import datetime
from logging.handlers import RotatingFileHandler
import sys
import time
import logging
import os

RATING_DOWNVOTE = "1"
CONFIG_FILE_NAME = join(dirname(abspath(__file__)), "google_play_music_cleaner_config.txt")
LOGS_DIR_PATH = join(dirname(abspath(__file__)), 'logs')
LOG_FILE_NAME = join(LOGS_DIR_PATH, 'gpm_library_cleaner.log')

# Enable logging
os.makedirs(LOGS_DIR_PATH, exist_ok=True)
file_handler = RotatingFileHandler(LOG_FILE_NAME, maxBytes=(1048576 * 5), backupCount=7)
console_handler = logging.StreamHandler()
logging.basicConfig(format='%(asctime)s %(levelname)s %(module)s %(message)s',
                    level=logging.INFO,
                    handlers=[file_handler, console_handler],
                    datefmt='%Y-%m-%d %H:%M:%S %Z')

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
