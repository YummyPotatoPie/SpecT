import configparser

from telethon.sync import TelegramClient
from telethon import connection
from telethon.tl.types import ChannelParticipantsSearch
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch
from telethon.tl.functions.messages import GetHistoryRequest

config = configparser.ConfigParser()
config.read("config.ini")

api_id      = config["Telegram"]["api_id"]
api_hash    = config["Telegram"]["api_hash"]
username    = config["Telegram"]["username"]

client = TelegramClient(username, api_id, api_hash)
client.start()

async def main():
	"""Main script"""
	channel = await channel_input()
	participants = await dump_all_participants(channel)

	# Temporary code
	for i in range(len(participants)):
		await client.send_message(channel, participants[i].stringify())
	# Temporary code


async def channel_input():
	"""The function that requests the url of the channel from which its participants will be read"""
	while True:
		try:
			channel_url = input("Enter url of the channel: ")
			channel = await client.get_entity(channel_url)
		except Exception:
			print("\nInvalid url, please try again.")
			continue
		return channel


async def dump_all_participants(channel):
	"""Function that gets all participants of the channel"""
	offset_user = 0   
	limit_user = 100  

	all_participants = []  
	filter_user = ChannelParticipantsSearch('')

	while True:
		participants = await client(GetParticipantsRequest(channel, filter_user, offset_user, limit_user, hash=0))
		if not participants.users:
			break
		all_participants.extend(participants.users)
		offset_user += len(participants.users)

	return all_participants

with client:
	client.loop.run_until_complete(main())