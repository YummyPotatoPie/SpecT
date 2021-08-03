import configparser
import os
import sys

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
	channel, channel_url = await channel_input()
	participants = await dump_all_participants(channel)
	write_csv_data(channel_url[13:len(channel_url)], participants)


def get_participant_name(participant):
	name = ""
	if (participant.first_name != None):
		name += participant.first_name
	if (participant.last_name != None):
		name += " " + participant.last_name
	return name


def get_participant_phone(participant):
	if participant.phone == None:
		return "None"
	return participant.phone


async def channel_input():
	"""The function that requests the url of the channel from which its participants will be read"""
	while True:
		try:
			channel_url = input("Enter url of the channel: ")
			channel = await client.get_entity(channel_url)
		except Exception:
			print("\nInvalid url, please try again.")
			continue
		return (channel, channel_url)


async def dump_all_participants(channel):
	"""Function that gets all participants of the channel"""
	offset_user = 0   
	limit_user = 100  

	all_participants = []  
	filter_user = ChannelParticipantsSearch('')

	while True:
		try:
			participants = await client(GetParticipantsRequest(channel, filter_user, offset_user, limit_user, hash=0))
			if not participants.users:
				break
			all_participants.extend(participants.users)
			offset_user += len(participants.users)
		except:
			print("For this action you need admin permission")
			input("Press any key to exit")
			sys.exit()

	return all_participants


def readable_info(participant):
	return str(participant.id) + "," + str(get_participant_name(participant)) + "," + \
		str(participant.scam) + "," + str(get_participant_phone(participant))


def write_mode():
	prompt = input("Write data about participant only if they has phone? Enter y (yes) or n (no): ")
	return prompt == 'y'


def writer(csv_file_name, participants, write_mode):
	with open(os.path.join("csv_data", csv_file_name + ".csv"), "w", encoding="utf-8") as csv_file:
		csv_file.write("id, name, is_scam, phone\n")
		for i in range(len(participants)):
			if participants[i].phone != None or not write_mode:
				csv_file.write(readable_info(participants[i]) + "\n")


def write_csv_data(csv_file_name, participants):
	write_if_has_phone = write_mode()
	writer(csv_file_name, participants, write_if_has_phone)


with client:
	client.loop.run_until_complete(main())

input("Press enter to exit")