from .. import utils, loader
from gtts import gTTS
from pydub import AudioSegment
from io import BytesIO
import requests

@loader.tds
class BNewsMod(loader.Module):
	"""Делает срочные новости из вашего текста"""

	strings = {
		'name': 'BreakingNews'
	}

	async def client_ready(self, client, db):
		self.client = client
		self.db = db

	async def bnewscmd(self, message):
		"""указываем аргсы и палетели"""
		args = utils.get_args_raw(message)

		if args:
			await utils.answer(message, '<b>ждемс...</b>')
			sound = BytesIO(requests.get('https://x0.at/ZzO.mp3').content)
			sound = AudioSegment.from_file(sound) - 10
			first_part, sound, end_part = sound[:2350], sound[2350:119160], sound[119160:123710]
			voice = BytesIO()
			gTTS(args, lang='ru').write_to_fp(voice)
			voice.seek(0)
			voice = AudioSegment.from_file(voice, format='mp3')
			combined = first_part + voice.overlay(sound) + end_part
			result = BytesIO()
			result.name = 'breaking_news.ogg'
			result = combined.export(result, format="ogg", bitrate="64k", codec="libopus")
			result.seek(0)
			await message.client.send_file(message.to_id, result, voice_note=True, duration=len(combined)/1000)
			await message.delete()
		else:
			await utils.answer(message, '<b>срочные новости!</b>')
