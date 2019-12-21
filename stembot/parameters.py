import os 
from slack import WebClient as slack_client
from pymongo import MongoClient

## DEFAULT CONFIGURATIONS DEFINITIONS

MENTOR_CHANNEL_NAME="mentors"
MY_STEMBOT_TOKEN=os.getenv("STEMBOT_TOKEN")
CHANNEL_NUM = 500
NUM_REQUESTS = 0
RATE_LIMIT_TIME_WAIT = 120
MAX_CHANNEL_NUM=100
NUM_FUNC_CALLS=0
PAGINATION_LIMIT=200
## slack API client settings 

client = slack_client(token=MY_STEMBOT_TOKEN)

## MONGO DB settings 

mongo_client = MongoClient('mongodb://localhost:27017')
mongodb = mongo_client.pymongo_test

## DB TABLE LIST

conversations_list_table = mongodb.conversations_list
conversations_members_table = mongodb.conversations_members
channel_table = mongodb.channel_table
member_table = mongodb.member_table


## CACHED DATA (things that takes too much time to call each time.)

PUBLIC_CHANNELS=client.conversations_list(types="public_channel",limit=CHANNEL_NUM)["channels"]
PRIVATE_CHANNELS=client.conversations_list(types="private_channel",limit=CHANNEL_NUM)["channels"]

