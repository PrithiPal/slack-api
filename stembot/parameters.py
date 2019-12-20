import os 
from slack import WebClient as slack_client


## DEFAULT CONFIGURATIONS DEFINITIONS

MENTOR_CHANNEL_NAME="mentors"
MY_STEMBOT_TOKEN=os.getenv("STEMBOT_TOKEN")
CHANNEL_NUM = 500
NUM_REQUESTS = 0
RATE_LIMIT_TIME_WAIT = 120
MAX_CHANNEL_NUM=100
NUM_FUNC_CALLS=0
PAGINATION_LIMIT=200
MONGO_PORT=27017

client = slack_client(token=MY_STEMBOT_TOKEN)


## CACHED DATA (things that takes too much time to call each time.)

PUBLIC_CHANNELS=client.conversations_list(types="public_channel",limit=CHANNEL_NUM)["channels"]
PRIVATE_CHANNELS=client.conversations_list(types="private_channel",limit=CHANNEL_NUM)["channels"]
