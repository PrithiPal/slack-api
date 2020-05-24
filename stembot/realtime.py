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


def message_all_mentors(text_message) : 
    


    with open(STUDENT_MENTOR_MATCH_LIST) as mentor_file : 
    
        csv_reader = csv.reader(mentor_file,delimiter=",")
        line_count = 0 
        for row in csv_reader : 
            
            
            if line_count!=0 and row[0] != "": 
                mentor_name = row[0]
                mentor_email = row[1]
                
                try : 
                
                    mentor_userid = client.users_lookupByEmail(email=mentor_email)['user']['id']
                    print("{} - {}".format(mentor_name,mentor_userid))
                    
                    resp = client.conversations_open(users=userid)
                    ret = client.chat_postMessage(text=text_message,channel=resp['channel']['id'])
                   

            line_count += 1


def validate_mentor_info() : 

    CHANNELS_LIST={}

    with open(STUDENT_MENTOR_MATCH_LIST) as mentor_file : 
    
        csv_reader = csv.reader(mentor_file,delimiter=",")
        line_count = 0 
        for row in csv_reader : 
            
            
            if line_count!=0 and row[0] != "": 
                mentor_name = row[0]
                mentor_email = row[1]
                team1_name = row[2]
                team2_name = row[3]
                team3_name = row[4]
                team4_name = row[5]
                team5_name = row[6]  

                if team1_name in CHANNELS_LIST : 
                    print("duplicate : {} already exists".format(team1_name))
                else:
                    CHANNELS_LIST[team1_name]=1
                
                if team2_name in CHANNELS_LIST : 
                    print("duplicate : {} already exists".format(team2_name))
                else:
                    CHANNELS_LIST[team2_name]=1
                
                if team3_name in CHANNELS_LIST : 
                    print("duplicate : {} already exists".format(team3_name))
                else:
                    CHANNELS_LIST[team3_name]=1
                
                if team4_name in CHANNELS_LIST : 
                    print("duplicate : {} already exists".format(team4_name))
                else:
                    CHANNELS_LIST[team4_name]=1
                
                if team5_name in CHANNELS_LIST : 
                    print("duplicate : {} already exists".format(team5_name))
                else:
                    CHANNELS_LIST[team5_name]=1

            line_count += 1


def assign_mentors_to_channels() : 
    FAILED_MENTORS=[]

    with open(STUDENT_MENTOR_MATCH_LIST) as mentor_file : 
        
        csv_reader = csv.reader(mentor_file,delimiter=",")
        line_count = 0 
        for row in csv_reader : 
            #print("row = ",row)
            
            if line_count!=0 and row[0] != "": 
                mentor_name = row[0]
                mentor_email = row[1]
                team1_name = row[2]
                team2_name = row[3]
                team3_name = row[4]
                team4_name = row[5]
                team5_name = row[6]
                
                try : 
                
                    print("{}".format(mentor_name))
                    mentor_userid = client.users_lookupByEmail(email=mentor_email)['user']['id']
                    print("{} - {}".format(mentor_name,mentor_userid))

                    try : 
                        if team1_name != "" : 
                            sf.assign_members(hf.get_channel_id(team1_name, False),mentor_userid)
                            #time.sleep(1)
                    except Exception as e :
                        print("User1 error ",e)

                    try:
                        if team2_name != "" : 
                            sf.assign_members(hf.get_channel_id(team2_name, False),mentor_userid)
                            #time.sleep(1)
                    except Exception as e :
                            print("User 2 error ",e)
                    
                    try:
                        if team3_name != "" : 
                            sf.assign_members(hf.get_channel_id(team3_name, False),mentor_userid)
                            #time.sleep(1)
                    except Exception as e :
                        print("User 3 error ",e)

                    try:
                        if team4_name != "" : 
                            sf.assign_members(hf.get_channel_id(team4_name, False),mentor_userid)
                            #time.sleep(1)
                    except Exception as e :
                        print("User 4 error ",e)
                    try: 
                        if team5_name != "" : 
                            sf.assign_members(hf.get_channel_id(team5_name, False),mentor_userid)
                            #time.sleep(1)
                    except Exception as e :
                        print("User 5 error ",e)

                    time.sleep(2)
                except Exception as e :
                    print("Error : {}".format(e))

                

            line_count += 1
 