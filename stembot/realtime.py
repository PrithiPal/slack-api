import os 
import slack 
import time 
import pickle
import pandas as pd 
import numpy as np 
import re 
from typing import Dict, List
from pymongo import MongoClient

import helper_functions as hf 
from parameters import *

import requests 
from random import random,seed 
from datetime import datetime 
from math import ceil 
import time 

import os
from slack import RTMClient
from slack.errors import SlackApiError

def post_message_to_slack(channel_name,text_to_post) : 
    response = client.chat_postMessage(
            channel=channel_name,
            text=text_to_post
    ) 
    assert response["ok"]

def send_message_all_students_accounts() : 
    
    general_chan_id = hf.get_channel_id("general",True)
    resp=hf.get_channel_members_ids(general_chan_id,True)

    #STUDENT_IDS = list(set(resp).difference(set(ADMIN_USERIDS)))
    #for student in STUDENT_IDS : 

    MYID=['U013ALLGH8E']
    for userid in MYID : 
       resp = client.conversations_open(users=userid)
       ret = client.chat_postMessage(text="Hello from Bot. Ignore Me.",channel=resp['channel']['id'])

       print(resp)
       print(ret)

    







