import json
import requests
import os.path
import re
import csv
import time
from time import gmtime, strftime

# from https://gist.github.com/dideler/3814182
class bcolors:
	HEADER = '\033[95m'
	OKBLUE = '\033[94m'
	OKGREEN = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	ENDC = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'


max_video_count = 100 # how many videos you want to process from this channel
results_per_page = 50 # pagination - how many video responses per page [0,50]
API_KEY = 'AIzaSyCLfn-5_GkQwxDlbua6SBRdV9CA1nul5W0'
export_folder = ''

search_api_url = 'https://www.googleapis.com/youtube/v3/search?part=snippet\
&order=date&maxResults=' + str(results_per_page) +\
'&key=' + API_KEY

def getYoutubeFollowersCount(channel_id):
  follower_count =1
  channel_url = 'https://www.googleapis.com/youtube/v3/channels?part=statistics&key=AIzaSyAvAQVvBy4H--aUNquBgzuOqvljQ4HPewg' \
  + '&id=' +channel_id
  response = requests.get(channel_url)
  json_data = json.loads(response.text)
  follower_count = json_data['items'][0]['statistics']['subscriberCount']
  return(follower_count)


def getChannelIDFromUserName(username):
	channel_url = 'https://www.googleapis.com/youtube/v3/channels?\
	&part=contentDetails\
	&key=' + API_KEY+'\
	&forUsername=' + username

	response = requests.get(channel_url)
	json_data = json.loads(response.text)
	# print(json_data)
	channel_id = json_data['items'][0]['id']
	return (channel_id)


def main():
	with open('youtubelist.csv') as csvfile:
		readCSV = csv.reader(csvfile, delimiter=',')
		
		for row in list(readCSV):
			# category = row[0]
			username = row[1].replace(" ", "")
			input_type = row[2]
			input_id = row[3]
			human_readable_time = strftime("%Y-%m-%d %H:%M:%S", gmtime())

			channel_id = input_id if input_type == 'channel' else getChannelIDFromUserName(input_id)
			# print('extracting :: ',username, channel_id)
			follower_count = getYoutubeFollowersCount(channel_id)

			with open('youtube-hist-follower.csv', 'a') as newFile:
				newFileWriter = csv.writer(newFile)
				newFileWriter.writerow([human_readable_time, time.time(), username, follower_count])

			print([human_readable_time, time.time(), username, follower_count])


if __name__ == "__main__":
	main()
 