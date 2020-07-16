from aiogram import types, Bot, Dispatcher, executor
import logging
import asyncio
from data import Subs
import youtube_dl as ydl
import requests
import os
import pygame
import time
from mutagen.mp3 import MP3


API_TOKEN = os.environ.get('BOT_TOKEN')
logging.basicConfig(level=logging.INFO)
bot = Bot(API_TOKEN)
dp = Dispatcher(bot)
sub = Subs()
pygame.mixer.init()


@dp.message_handler(commands=['start'])
async def say_hello(message):
	global check
	check = sub.check_subscribe(message.from_user.id)
	if check:
		await message.answer('Привет! Смотри что я умею:\n\t/download_music - для скачивания музыки\n\t/info если хотите увидеть список функций')
	else:
		await message.answer('Чтобы продолжить подпишитесь!\nДля этого введите "/subscribe"')


@dp.message_handler(commands=['subscribe'])
async def add_subscriber(message):
	if sub.check_user(message.from_user.id):
		sub.update_status_subscribe(message.from_user.id, True)
	else:
		sub.subscribe(message.from_user.id)
	await message.answer('Вы успешно подписались!\nДля получения списка функций воспользуйтесь: /info')


@dp.message_handler(commands=['unsubscribe'])
async def del_subscriber(message):
	sub.unsubscribe(message.from_user.id)
	await message.answer('Вы отписались(')


@dp.message_handler(lambda message: message.text == 'фон')
async def send_background(message: types.Message):
	photo = open('D:\\Загрузки\\36464-playstation_djoystik.jpg', 'rb')
	if sub.check_subscribe(message.from_user.id) == 1:
		await message.answer_photo(photo=photo)
	else:
		await message.answer('Подпишитесь: "/subscribe"')
	logging.info(message.text)


@dp.message_handler(commands=['download_music'])
async def music_downloader(message):
	if sub.check_subscribe(message.from_user.id):
		await message.answer('Вставьте ссылку на трек')
		global save_last_mess
		save_last_mess = message.text
	else:
		await message.answer('Подпишитесь: "/subscribe"')



@dp.message_handler(commands=['info'])
async def say_hello(message):
	if sub.check_subscribe(message.from_user.id):
		await message.answer('''Если вы используете бота через пк:\nДоступные функции:\n\t/download_music - для скачивания музыки\n\t/play_music   ... - для прослушивания трека(на месте троеточия название трека)\n\t
			/pause - для приостановки трека\n\t/unpause - для возобновления проигрывания трека\n\t/repeat - для повторного проигрывания в данный момент играющего трека\n
			Также вы можете создать плейлист и слушать музыку\n\t/create_playlist - создание плейлиста\n\t/play_playlist - начать проигрывать плейлист\n\t/repeat_playlist - слушать плейлист на репите\n
			Если вы используете бота через мобильное устройство:\n\t/download_music - для скачивания музыки, когда бот попросит вставить ссылку сделайте это так - "ссылка" и добавьте mobile(между ними должен быть пробел!!!)\n\t
			Пока что это все функции для моб.устройства''')
	else:
		await message.answer('Подпишитесь: "/subscribe"')


@dp.message_handler(lambda message: message.text.startswith('https'))
async def wasd(message):
	if save_last_mess == '/download_music':
		ydl_opts = {
			'format': 'bestaudio/best',
    		'postprocessors': [{
        		'key': 'FFmpegExtractAudio',
        		'preferredcodec': 'mp3',
        		'preferredquality': '192',
			}],
		}
		if 'mobile' in message.text:
			lst = message.text.split()
			messag = lst[0]
		else:
			messag = message.text
		with ydl.YoutubeDL(ydl_opts) as f:
			await message.answer('Загрузка началась...')
			f.download([messag])
			await message.answer('Загрузка завершена')
			if 'mobile' in message.text:
				for i, j in enumerate(os.listdir('C:\\Users\\zhern\\')):
					if j.endswith('.mp3'):
						await message.answer('Ожидайте')
						music = open('C:\\Users\\zhern\\' + j, 'rb')
						await message.answer_audio(audio=music)
						break
	logging.info(message.text)


async def mus_play():
	global substraction1, length, the_song, start_play_music
	start_play_music = time.time()
	for i in os.listdir('C:\\Users\\zhern\\'):
		try:
			the_song = lst[1]
		except:
			pass
		if the_song in i:
			logging.info(lst[1])
			f = MP3('C:\\Users\\zhern\\' + i)
			length = f.info.length
			pygame.mixer.music.load(i)
			pygame.mixer.music.play()
			substraction = end - start
			await asyncio.sleep(length - substraction)


async def repeat_mus_play():
	global substraction1, length
	for j in os.listdir('C:\\Users\\zhern\\'):
		if the_song in j:
			f = MP3('C:\\Users\\zhern\\' + j)
			length = f.info.length
			pygame.mixer.music.load(j)
			pygame.mixer.music.play(-1)
			substraction1 = end - start
			await asyncio.sleep(length - substraction1)


@dp.message_handler(commands=['play_music', 'pause', 'unpause', 'repeat'])
async def play_music(message):
	if sub.check_subscribe(message.from_user.id):
		global lst, start, end
		lst = message.text.split()
		if '/play_music' in message.text:
			start, end = 0, 0
			await mus_play()

		elif message.text == '/repeat':
			start_press_reply = time.time()
			res = length - (start_press_reply - start_play_music)
			await asyncio.sleep(res)
			await repeat_mus_play()

		elif message.text == '/pause':
			start = time.time()
			pygame.mixer.music.pause()

		elif message.text == '/unpause':
			end = time.time()
			pygame.mixer.music.unpause()
	else:
		await message.answer('Подпишитесь: "/subscribe"')


@dp.message_handler(commands=['create_playlist', 'play_playlist', 'repeat_playlist'])
async def playlist(message):
	if sub.check_subscribe(message.from_user.id):
		if message.text == '/create_playlist':
			await message.answer('''Введите названия треков, которые вы хотите добавить в плейлист(через запятую)\nПример:\n\t
				!/трек1, трек2, ...''')

		elif message.text == '/play_playlist':
			await play_playlist_music()

		elif message.text == '/repeat_playlist':
			start_press_reply = time.time()
			count = 0
			for i in playlist:
				start, end = 0, 0
				for j in os.listdir('C:\\Users\\zhern\\'):
					if i in j:
						f = MP3('C:\\Users\\zhern\\' + j)
						length = f.info.length
						count += length
			res = count - (start_press_reply - start_play_music)
			await asyncio.sleep(res)
			await repeat_playlist_music()
	else:
		await message.answer('Подпишитесь: "/subscribe"')


async def play_playlist_music():
	global length, start_play_music
	start_play_music = time.time()
	for i in playlist:
		start, end = 0, 0
		for j in os.listdir('C:\\Users\\zhern\\'):
			if i in j:
				f = MP3('C:\\Users\\zhern\\' + j)
				length = f.info.length
				pygame.mixer.music.load(j)
				pygame.mixer.music.play()
			try:
				await asyncio.sleep(length - (end - start))
			except:
				pass



async def repeat_playlist_music():
	while True:
		for i in playlist:
			start, end = 0, 0
			for j in os.listdir('C:\\Users\\zhern\\'):
				if i in j:
					f = MP3('C:\\Users\\zhern\\' + j)
					length = f.info.length
					pygame.mixer.music.load(j)
					pygame.mixer.music.play()
					t = end - start
					await asyncio.sleep(length - t)
				try:
					await asyncio.sleep(length - (end - start))
				except:
					pass


@dp.message_handler(lambda message: message.text.startswith('!/'))
async def create_playlist(message):
	if sub.check_subscribe(message.from_user.id):
		global playlist
		playlist = message.text.lstrip('/!').split(',')
		await message.answer(playlist)
	else:
		await message.answer('Подпишитесь: "/subscribe"')


if __name__ == '__main__':
	executor.start_polling(dp, skip_updates=True)

