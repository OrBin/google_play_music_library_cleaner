from gmusicapi import Mobileclient
import sys
from datetime import datetime
import time

# CONSTANTS
HOURS_INTERVAL = 1 # Will run every hour
RATING_DOWNVOTE = "1"
CONFIG_FILE_NAME = ".google_play_music_cleaner_config"


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
	
	print "--"
	print datetime.now()

	if not logged_in:
		print "Error: could not log in."
		return
	
	all_songs = api.get_all_songs()
	downvoted_songs = [song for song in all_songs if song["rating"]  == RATING_DOWNVOTE]
	
	if len(downvoted_songs) == 0:
		print "No downvoted songs"
	else:
		print "Deleting %s downvoted songs:" % len(downvoted_songs)
		for song in downvoted_songs:
			print "%s - %s" % (song["artist"], song["title"])
		api.delete_songs([song["id"] for song in downvoted_songs])

while True:
	perform_iteration()
	time.sleep(60 * 60 * HOURS_INTERVAL)
