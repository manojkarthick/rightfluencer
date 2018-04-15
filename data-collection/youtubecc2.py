from subprocess import call
from webvtt import WebVTT
from os import remove
from os import path

import re

def convertVTTtoTXT(filename):

	file = open(filename + '.txt', 'w')
	for caption in WebVTT().read(filename+'.en.vtt'):
		file.write(caption.text)
	file.close()
	print('subtitle generated for '+ filename)

def extractCC(title, id, cc_path):
	command = 'youtube-dl --sub-lang en --write-sub --write-auto-sub --skip-download \
		 -o '+ cc_path +'/'+title +' https://www.youtube.com/watch?v='+id

	print(command)
	call(command.split(), shell=False)
	
	if(path.isfile(cc_path +'/'+title+'.en.vtt')):
		convertVTTtoTXT(cc_path +'/'+title)
	else:
		print('cc do not exists for '+title+ ' ; ' + id)

cc_export_folder = 'youtube_export/JamieOliver'
cc_filename = 'cc'
video_title = 'Live with Jamie Oliver | Behind the Scenes.'
video_title = re.sub('[^A-Za-z0-9]+', '', video_title).lower()
print(video_title)

extractCC(video_title, 'HtWfl4FR0sk', cc_export_folder)