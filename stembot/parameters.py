import os 
from slack import WebClient as slack_client
from pymongo import MongoClient

## DEFAULT CONFIGURATIONS DEFINITIONS

MENTOR_CHANNEL_NAME="mentors"
BOT_NAME="bdcbot"


#MY_STEMBOT_TOKEN=os.getenv("SAMPLE_SLACK_TOKEN")


SLACK_ADMIN_TOKEN=os.getenv("SLACK_ADMIN_TOKEN")
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")

# Turn false to use admin
USE_BOT_TOKEN=False


CHANNEL_NUM = 500
NUM_REQUESTS = 0
RATE_LIMIT_TIME_WAIT = 0

MAX_CHANNEL_NUM=600
NUM_FUNC_CALLS=0
PAGINATION_LIMIT=200
## slack API client settings 

client=""
if USE_BOT_TOKEN : 

    client = slack_client(token=SLACK_BOT_TOKEN)
    print("SLACK_BOT_TOKEN=",SLACK_BOT_TOKEN)
else:
    
    client = slack_client(token=SLACK_ADMIN_TOKEN)
    print("SLACK_ADMIN_TOKEN=",SLACK_ADMIN_TOKEN)

## INPUT CSV FILE

STUDENTS_CSV = "localfiles/dummy.csv"
STUDENT_INVITE_LIST = "localfiles/student_invite_list.txt"
STUDENT_READABLE_LIST = "localfiles/readable_student_invite_emails.txt"
STUDENT_SLACK_LIST = "localfiles/new_student_list.csv"
STUDENT_MENTOR_MATCH_LIST = "localfiles/mentor_match_channel.csv"

ADMIN_USERIDS=[
    "U0136DUHHPG",
    "U013D76B97D", 
    "U0136AJ7Y86",
    "U013ALLGH8E", 
    "U013D76B97D",
]

## MONGO DB settings 

mongo_client = MongoClient('mongodb://localhost:27017')
mongodb = mongo_client.pymongo_test

## MONGO DB TABLE LIST 


## RAW TABLES 
conversations_list_table_raw = mongodb.conversations_list_raw
conversations_members_table_raw = mongodb.conversations_members_raw
students_table = mongodb.students_raw
member_table_raw = mongodb.member_raw
user_table_raw = mongodb.user_raw
conversation_history_table_raw = mongodb.conversations_history_raw

## STRUCTURED TABLES 
num_messages_members_table = mongodb.num_messages_members
num_messages_members2_table = mongodb.num_messages_members2
num_message_user_info_table = mongodb.num_message_user_info



## WORKSPACE CREATION TABLES 
students_table_raw = mongodb.students_table_raw

## CACHED DATA (things that takes too much time to call each time.)

PUBLIC_CHANNELS=client.conversations_list(types="public_channel",limit=CHANNEL_NUM)["channels"]
PRIVATE_CHANNELS=client.conversations_list(types="private_channel",limit=CHANNEL_NUM)["channels"]





