import json
import os.path
import re
from webvtt import WebVTT
from subprocess import call

# This program outputs the closed caption associated 
# with an youtube video, it primarily uses the 
# youtube-dl library - https://github.com/rg3/youtube-dl

# this version takes a folder under which there are multiple subdirectories,
# and each of those subdirectories contains list of json files of an youtube API response
# from https://www.googleapis.com/youtube/v3/videos

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


def convertVTTtoTXT(filename):
	file = open(filename + '.txt', 'w')
	for caption in WebVTT().read(filename+'.en.vtt'):
		file.write(caption.text + '\n')
	file.close()
	print('subtitle generated for '+ filename)


def extractCC(title, vid, cc_path):
	print (bcolors.OKBLUE + '---------------- EXTRACT CC START------------------' + bcolors.ENDC)
	command = 'youtube-dl --sub-lang en --write-sub --write-auto-sub --skip-download \
		 -o '+ cc_path +'/'+title +' https://www.youtube.com/watch?v='+vid
	call(command.split(), shell=False)
	if(os.path.isfile(cc_path +'/'+title+'.en.vtt')):
		convertVTTtoTXT(cc_path +'/'+title)
	else:
		print('cc do not exists for '+title+ ' ; ' + vid)
	
	print (bcolors.OKBLUE + '---------------- EXTRACT CC ENDS------------------'+ bcolors.ENDC)


def exportclosedcaption(json_data, export_folder):
	post = json_data['items'][0]
	title = post['snippet']['title']
	title = re.sub('[^A-Za-z0-9]+', '', title).lower()
	video_id = post['id']
	print(title, video_id)
	if video_id:
		# we found a video
		if os.path.isfile(export_folder +'/'+title +'_'+ video_id +'.txt'):
			print(bcolors.OKGREEN+ 'cc already downloaded'+bcolors.ENDC)
		else:
			extractCC(title+'_' +video_id, video_id, export_folder)


def main():
	dirname = 'youtube_export/fashion2'
	subdirs = [dI for dI in os.listdir(dirname) if os.path.isdir(os.path.join(dirname,dI))]
	file_no = 1

	for subdir in subdirs:
		for file in os.listdir(os.path.join(dirname,subdir)):
			
			if file.endswith(".json"):
				print(str(file_no), file)
				file_no = file_no +1

				json_file_path = os.path.join(os.path.join(dirname,subdir), file)
				with open(json_file_path) as json_data:
					d = json.load(json_data)
					exportclosedcaption(d, os.path.join(dirname,subdir))

if __name__ == "__main__":
	main()
	