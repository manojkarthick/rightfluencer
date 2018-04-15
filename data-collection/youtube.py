import json
import requests
import os.path
import re
import csv

# for a given youtube playlist ID, this script will collect all the 
# statistics for each and every videos and dump (export) them into json files
# then the script will download the closed caption and convert the vtt file to plaintext
# the files will be stored in this manner
# ./youtube_export/{channel_name}/title.json
# ./youtube_export/{channel_name}/title.txt
# NOTE:: all titles are striped off special chars and lowercased

# For example, here
# Jamie Oliver (All Uploads) https://www.youtube.com/user/JamieOliver/videos
# we can get the playlist ID using the following API call::
# https://www.googleapis.com/youtube/v3/channels?part=contentDetails&forUsername=JamieOliver&key= {API_KEY}

# for channel 
# https://www.googleapis.com/youtube/v3/search?key={API_KEY}&channelId={CHANNEL_ID}&part=snippet,id&order=date&maxResults=40

# INPUT : a csv file containing the 4 cols - category, Infl_name, channel_string_type, channel_type_value
# sample row:
# Food, Kevin Curry, user, fitmencook
# Food,Yolanda Gampp, channel, UCvM1hVcRJmVWDtATYarC0KA

# OUTPUT - folder with the same name as Infl_name, with n json response files, one for each video
# we feed this output folder(s) as the input to extractcc_single.py / extractcc_multiple.py

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

def dumpVideoStatistics(vid, title):
	videos_url= 'https://www.googleapis.com/youtube/v3/videos?part=snippet,contentDetails,statistics\
	&key=' + API_KEY +\
	'&id=' + vid
	
	response = requests.get(videos_url)
	json_data = json.loads(response.text)
	
	title = title + '.json'
	if not os.path.exists(export_folder):
         os.makedirs(export_folder)
	filename = os.path.join(export_folder, title)
	with open(filename, 'w') as outfile:
		json.dump(json_data, outfile, indent=4)
		print('JSON DUMP SUCCESS! :', filename, vid)


# position is the overall count of the videos processed so far across pages
def getYoutubeVideosList(url, pageToken = '', position = 0):
	if pageToken:
		url = (url + '&pageToken=' + pageToken)
	response = requests.get(url)
	json_data = json.loads(response.text)
	pageToken = json_data.get('nextPageToken')
	items = json_data['items']

	i = 0
	while (i <len(items)):
		print (bcolors.HEADER + 'processing video: ' + str(position+1) + bcolors.ENDC)

		title = json_data['items'][i]['snippet']['title']
		title = re.sub('[^A-Za-z0-9]+', '', title).lower()
		# description = json_data['items'][i]['snippet']['description']
		video_id = json_data['items'][i]['id'].get('videoId')

		if video_id:
			# we found a video
			dumpVideoStatistics(video_id, str(position)+ '_' + title)
			position = position + 1
		else:
			print('non video resource -- position not updated')
		
		i = i+1 # next item on the result json
		if (position == max_video_count):
			return()

	# pagination: continue to next page, if exists
	# there should be no pageToken if this is the last page
	if pageToken:
		getYoutubeVideosList(url= url, pageToken = pageToken, position = position)


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
	    start_row = 1
	    end_row = 1
	    
	    for row in list(readCSV)[start_row-1 : end_row]:
	        # category = row[0]
	        username = row[1].replace(" ", "")
	        input_type = row[2]
	        input_id = row[3]

	        channel_id = input_id if input_type == 'channel' else getChannelIDFromUserName(input_id)
	        global export_folder
	        export_folder = os.path.join('youtube_export', username)
	        
	        print('extracting :: ',username, channel_id)
	        getYoutubeVideosList(search_api_url + '&channelId='+ channel_id)

if __name__ == "__main__":
    main()
    