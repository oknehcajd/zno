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

api_id = 3273854
api_hash = 'c8fdebeabd4f011e30dd9a62ee37218d'
client = TelegramClient('anon', api_id, api_hash)
botusername = 'HNEU_ZNO_math_bot'
path = '/Users/aroslav/Desktop/zno/'
reviews = ['Був близько', 'Ой, точно', 'Зовсім забув']
reviews2 = ['Дуже просто', 'Трішки задумався', 'Активно розмірковував']
possible_answers = ['А', 'Б', 'В', 'Г', 'Д']
ntests = 1500
test_number = 587
losestrick = 0

client.start()

while test_number <= ntests:
	print('test_number = ', test_number)
	bot_messages = client.get_messages(botusername, 2)
	cpath = path + 'images/img' + str(test_number) + '.jpg'
	bot_messages[1].download_media(cpath)
	time.sleep(1)
	img_hash = imagehash.average_hash(Image.open(cpath))
	img_hash2 = hashlib.md5(Image.open(cpath).tobytes())
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
			ihash2 = hashlib.md5(Image.open(cpath).tobytes())
			if img_hash2.hexdigest() == ihash2.hexdigest():
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
		losestrick+=1
		if ok == True:
			review_text = reviews[review_ind]
		else:
			review_text = reviews[0]

		if bot_messages[0].buttons != None:
			answer = answer_string[len(answer_string) - 2]
		else:
			answer = answer_string.split(' ')[-1][:-1]
	else:
		losestrick = 0
		if ok == True:
			review_text = reviews2[review_ind]
		else:
			review_text = reviews2[0]
		answer = answer_string.split('**')[1]
	print('answer = ', answer)
	if "Правильно!" not in answer_string:
		if ok == False:
			cpath = path + 'answers/ans' + str(cimage_index) + '.txt'
			f = open(cpath, 'w+')
			f.write(answer)
			f.close()
	if ok == True:
		cpath = path + 'answers/ans' + str(test_number) + '.txt'
		f = open(cpath, 'w+')
		f.write(answer)
		f.close()
		test_number+=1
	last_bot_messages[0].click(text = review_text)
	if losestrick > 10:
		break
	