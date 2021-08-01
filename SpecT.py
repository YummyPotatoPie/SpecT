import configparser

config = configparser.ConfigParser()
config.read("config.ini")

api_id      = config["Telegram"]["api_id"]
api_hash    = config["Telegram"]["api_hash"]
username    = config["Telegram"]["username"]

