#!/usr/bin/python
# -*- coding: utf-8 -*-

from fbchat import Client
from fbchat.models import *

import sys,os,requests,shutil,ntpath
from random import randint


from pprint import pprint
# Messenger images scraper
# usage: python messenger_scraper.py conversation_id

def downloadImage (author_uid, url, conversation_id, client):
	# first, let's check author's name
	user = client.fetchUserInfo(author_uid)[author_uid]
	filename = ntpath.basename(url).split('?')[0]

	user.name = user.name.encode('utf-8')
	
	print('Downloading {} from {}...'.format(filename, user.name))

	dir_name = conversation_id + '/' + user.name
	dir_name = dir_name.rsplit('?', 1)[0] # cut before ?
	
	try: 
		os.mkdir(dir_name)
	except OSError:
		pass
	
	r = requests.get(url)
	
	if r.status_code == 200:
		with open(dir_name.decode('utf-8') + '/' + filename, 'wb') as f:
			f.write(r.content)
	
	

def main ():
	if len(sys.argv) < 2: 
		print('Usage: python messenger_scraper.py conversation_id')
		return False

	conversation_id = sys.argv[1]

	client = Client(your username, your password)
	print('Attempting {}...'.format(conversation_id))
	# what the fuck fbchat, where is function to retrieve all images?
	# ehh I have to do everything by myself
	
	lastMessageTimestamp = None
	
	try: 
		os.mkdir(conversation_id)
	except OSError:
		print('Dir already exists!')
	
	try:
		while True:
			messages = client.fetchThreadMessages(conversation_id, 100, lastMessageTimestamp)
			lastMessageTimestamp = messages[len(messages)-1].timestamp
			endOfMessages = False
			for key,message in enumerate(messages):
				if message.attachments:
					for attachment in message.attachments:
						try:
							url = client.fetchImageUrl(attachment.uid)
						except: continue
						downloadImage(message.author, url, conversation_id, client)
				if key == len(messages)-1 and key < 99:
					endOfMessages = True
			if endOfMessages == True:
				break
	except KeyboardInterrupt:
		print('Downloading interrupted!')

	
	
if __name__ == '__main__':
	main()
