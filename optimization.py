from PIL import Image
import imagehash
import hashlib
import telethon.sync
import os
import time
from telethon import TelegramClient
from random import randint
from telethon import functions, types
import logging
logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)

api_id = 3383391
api_hash = 'ae4aa759b03f4476301f5b9a4dfd5574'
client = TelegramClient('anon', api_id, api_hash)
botusername = 'HNEU_ZNO_math_bot'
path = '/Users/aroslav/Desktop/zno/'
reviews = ['Був близько', 'Ой, точно', 'Зовсім забув']
reviews2 = ['Дуже просто', 'Трішки задумався', 'Активно розмірковував']
possible_answers = ['А', 'Б', 'В', 'Г', 'Д']
ntests = 500
test_number = # TO DO
prevOK = -1
bounds = 0
client.start()

while True:
	print('test_number = ', test_number)
	bot_messages = client.get_messages(botusername, 2)
	cpath = path + 'images/img' + str(test_number) + '.jpg'
	bot_messages[1].download_media(cpath)
	time.sleep(1)
	img_hash = imagehash.average_hash(Image.open(cpath))
	# print('img_hash = ', img_hash)
	cimage_index = test_number - 1
	ok = True
	correct_answer = ''
	for i in range(1, test_number):
		ipath = path + 'hashes/hash' + str(cimage_index) + '.txt'
		f = open(ipath, 'r')
		ihash = f.read()
		# print('ihash = ', ihash)
		f.close()
		if str(ihash) == str(img_hash):
			print('cimage_index = ', cimage_index)
			cpath = path + 'answers/ans' + str(cimage_index) + '.txt'
			f = open(cpath, 'r')
			correct_answer = f.read()
			f.close()
			ok = False
			break
		cimage_index-=1
	print('correct_answer = ', correct_answer)
	if ok == True:
		cpath = path + 'hashes/hash' + str(test_number) + '.txt'
		f = open(cpath, 'w+')
		shash = str(img_hash)
		# print('hash gone to file : ', shash)
		f.write(shash)
		f.close()
	else:
		cpath = path + 'images/img' + str(test_number) + '.jpg'
		os.remove(cpath)
	if bot_messages[0].buttons != None:
		if ok == False:
			bot_messages[0].click(text = str(correct_answer))
		else:
			bot_messages[0].click(text = possible_answers[randint(0, 4)])
	else:
		if ok == False:
			client.send_message(botusername, str(correct_answer))
		else:
			client.send_message(botusername, str(randint(0, 100)))
	time.sleep(1)
	last_bot_messages = client.get_messages(botusername, 3)
	if bot_messages[0].buttons != None:
		answer_string = last_bot_messages[1].text
	else:
		answer_string = last_bot_messages[2].text
	print('answer_string = ', answer_string)
	review_ind = randint(0, 2)
	if "Правильно!" not in answer_string:
		if ok == True:
			review_text = reviews[review_ind]
		else:
			review_text = reviews[0]
		if bot_messages[0].buttons != None:
			answer = answer_string[len(answer_string) - 2]
		else:
			answer = answer_string.split(' ')[-1][:-1]
	else:
		if ok == True:
			review_text = reviews2[review_ind]
		else:
			review_text = reviews2[0]
		answer = answer_string.split('**')[1]
	print('answer = ', answer)
	if ok == True:
		cpath = path + 'answers/ans' + str(test_number) + '.txt'
		f = open(cpath, 'w+')
		f.write(answer)
		f.close()
		test_number+=1
	last_bot_messages[0].click(text = review_text)
	if prevOK == -1:
		prevOK = ok
	else:
		if ok != prevOK:
			if ok == False:
				prevOK = ok
				bounds = 19
				break
			else:
				prevOK = -1

while test_number <= ntests:
	if prevOK == True:
		for counter in range(bounds):
			bot_messages = client.get_messages(botusername, 2)
			cpath = path + 'images/img' + str(test_number) + '.jpg'
			bot_messages[1].download_media(cpath)
			time.sleep(1)
			img_hash = imagehash.average_hash(Image.open(cpath))
			cpath = path + 'hashes/hash' + str(test_number) + '.txt'
			f = open(cpath, 'w+')
			shash = str(img_hash)
			f.write(shash)
			f.close()
			if bot_messages[0].buttons != None:
				bot_messages[0].click(text = possible_answers[randint(0, 4)])
			else:
				client.send_message(botusername, str(randint(0, 100)))
			time.sleep(1)
			last_bot_messages = client.get_messages(botusername, 3)
			if bot_messages[0].buttons != None:
				answer_string = last_bot_messages[1].text
			else:
				answer_string = last_bot_messages[2].text
			review_ind = randint(0, 2)
			if "Правильно!" not in answer_string:
				review_text = reviews[review_ind]
				if bot_messages[0].buttons != None:
					answer = answer_string[len(answer_string) - 2]
				else:
					answer = answer_string.split(' ')[-1][:-1]
			else:
				review_text = reviews2[review_ind]
				answer = answer_string.split('**')[1]
			cpath = path + 'answers/ans' + str(test_number) + '.txt'
			f = open(cpath, 'w+')
			f.write(answer)
			f.close()
			last_bot_messages[0].click(text = review_text)
		prevOK = False
		bounds = 20
	else:
		for counter in range(bounds):
			bot_messages = client.get_messages(botusername, 2)
			cpath = path + 'images/img' + str(test_number) + '.jpg'
			bot_messages[1].download_media(cpath)
			time.sleep(1)
			img_hash = imagehash.average_hash(Image.open(cpath))
			cimage_index = test_number - 1
			ok = True
			correct_answer = ''
			for i in range(1, test_number):
				ipath = path + 'hashes/hash' + str(cimage_index) + '.txt'
				f = open(ipath, 'r')
				ihash = f.read()
				# print('ihash = ', ihash)
				f.close()
				if str(ihash) == str(img_hash):
					print('cimage_index = ', cimage_index)
					cpath = path + 'answers/ans' + str(cimage_index) + '.txt'
					f = open(cpath, 'r')
					correct_answer = f.read()
					f.close()
					ok = False
					break
				cimage_index-=1
			for j in range(cimage_index + 1, cimage_index + 20):


while test_number <= ntests:
	print('test_number = ', test_number)
	bot_messages = client.get_messages(botusername, 2)
	cpath = path + 'images/img' + str(test_number) + '.jpg'
	bot_messages[1].download_media(cpath)
	time.sleep(1)
	img_hash = imagehash.average_hash(Image.open(cpath))
	# print('img_hash = ', img_hash)
	cimage_index = test_number - 1
	ok = True
	correct_answer = ''
	for i in range(1, test_number):
		ipath = path + 'hashes/hash' + str(cimage_index) + '.txt'
		f = open(ipath, 'r')
		ihash = f.read()
		# print('ihash = ', ihash)
		f.close()
		if str(ihash) == str(img_hash):
			print('cimage_index = ', cimage_index)
			cpath = path + 'answers/ans' + str(cimage_index) + '.txt'
			f = open(cpath, 'r')
			correct_answer = f.read()
			f.close()
			ok = False
			break
		cimage_index-=1
	print('correct_answer = ', correct_answer)
	if ok == True:
		cpath = path + 'hashes/hash' + str(test_number) + '.txt'
		f = open(cpath, 'w+')
		shash = str(img_hash)
		# print('hash gone to file : ', shash)
		f.write(shash)
		f.close()
	else:
		cpath = path + 'images/img' + str(test_number) + '.jpg'
		os.remove(cpath)
	if bot_messages[0].buttons != None:
		if ok == False:
			bot_messages[0].click(text = str(correct_answer))
		else:
			bot_messages[0].click(text = possible_answers[randint(0, 4)])
	else:
		if ok == False:
			client.send_message(botusername, str(correct_answer))
		else:
			client.send_message(botusername, str(randint(0, 100)))
	time.sleep(1)
	last_bot_messages = client.get_messages(botusername, 3)
	if bot_messages[0].buttons != None:
		answer_string = last_bot_messages[1].text
	else:
		answer_string = last_bot_messages[2].text
	print('answer_string = ', answer_string)
	review_ind = randint(0, 2)
	if "Правильно!" not in answer_string:
		if ok == True:
			review_text = reviews[review_ind]
		else:
			review_text = reviews[0]
		if bot_messages[0].buttons != None:
			answer = answer_string[len(answer_string) - 2]
		else:
			answer = answer_string.split(' ')[-1][:-1]
	else:
		if ok == True:
			review_text = reviews2[review_ind]
		else:
			review_text = reviews2[0]
		answer = answer_string.split('**')[1]
	print('answer = ', answer)
	if ok == True:
		cpath = path + 'answers/ans' + str(test_number) + '.txt'
		f = open(cpath, 'w+')
		f.write(answer)
		f.close()
		test_number+=1
	last_bot_messages[0].click(text = review_text)
	