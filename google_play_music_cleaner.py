from gmusicapi import Mobileclient
import sys
from datetime import datetime
import time
import logging

# CONSTANTS
HOURS_INTERVAL = 1 # Will run every hour
RATING_DOWNVOTE = "1"
CONFIG_FILE_NAME = ".google_play_music_cleaner_config"

logging.basicConfig(filename='log.txt',level=logging.INFO, format="%(asctime)s %(levelname)s %(module)s %(message)s", datefmt='%Y-%m-%d %H:%M:%S %Z')
api = Mobileclient()
global last_login_data
global logged_in
last_login_data = open(CONFIG_FILE_NAME).read().split("\n")
logged_in = api.login(last_login_data[0], last_login_data[1])

# This procedure will perform a clean process
def perform_iteration():
	global last_login_data
	global logged_in

	# Re-fetch login data
	curr_login_data = open(CONFIG_FILE_NAME).read().split("\n")

	# If the login data have changed, logging out and in and saving the new login data
	if last_login_data != curr_login_data:
		last_login_data = curr_login_data
		api.logout()
		logged_in = api.login(curr_login_data[0], curr_login_data[1])
	
	logging.info("Started iteration")
	#print "--"
	#print datetime.now()

	if not logged_in:
		logging.error("Error: could not log in.")
		#print "Error: could not log in."
		return
	
	all_songs = api.get_all_songs()
	downvoted_songs = [song for song in all_songs if song["rating"]  == RATING_DOWNVOTE]
	
	if len(downvoted_songs) == 0:
		logging.info("No downvoted songs")
		#print "No downvoted songs"
	else:
		logging.info("Deleting %s downvoted songs:", len(downvoted_songs))
		#print "Deleting %s downvoted songs:" % len(downvoted_songs)
		for song in downvoted_songs:
			logging.info("%s - %s", song["artist"], song["title"])
			#print "%s - %s" % (song["artist"], song["title"])
		api.delete_songs([song["id"] for song in downvoted_songs])

while True:
	try:
		perform_iteration()
	except Exception, e:
		logging.exception(e)
	
	time.sleep(60 * 60 * HOURS_INTERVAL)
