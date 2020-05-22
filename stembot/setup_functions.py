import os 
import slack 
import time 
import pickle
import pandas as pd 
import numpy as np 
import re 
from typing import Dict, List
from pymongo import MongoClient
from parameters import *
import requests 
from random import random,seed 
from datetime import datetime 
from math import ceil 
import time 


## HELPER FUNCTIONS for SETUP
def create_channel(chan_name,chan_private) : 
    
    response = client.conversations_create(name=chan_name,is_private=chan_private)
    #print("Channel Created [{}] {}".format(chan_name,response['channel']['id']))
    return response

def assign_members(chan_id,user_id_list) : 
    response = client.conversations_invite(channel=chan_id,users=user_id_list)
    return response

def get_users_all() : 
    response = client.users_list()
    return response 

def delete_channel(chan_id) : 
    resp=client.conversations_archive(channel=chan_id)
    return resp 


def slugify(string) : 
    new_string = re.sub("\-","_",string)
    new_string = re.sub("\ ","_",new_string)
    new_string = re.sub("\.","_",new_string)
    return new_string

    
def generate_team_name(row) : 
    API_LINK = "https://frightanic.com/goodies_content/docker-names.php"
    resp=requests.get(API_LINK).text
    
    seed_value = datetime.timestamp(datetime.now())
    seed(seed_value)
    randval = ceil(random()*1000000)
    
    FINAL="{}_{}".format(resp[:-1],randval)
    #print(FINAL)
    return FINAL


df=pd.read_csv(STUDENTS_CSV,parse_dates=['Submission Time'],)


def create_student_invite_list() : 

    EMAIL_LIST=[]
    
    def gather_email(row) : 
        
        if row['Email Address'] is not np.nan : 
            EMAIL_LIST.append(str(row['Email Address']))
        if row['Email Address.1'] is not np.nan: 
            EMAIL_LIST.append(str(row['Email Address.1']))
        if row['Email Address.2'] is not np.nan: 
            EMAIL_LIST.append(str(row['Email Address.2']))
        if row["Email Address.3"] is not np.nan : 
            EMAIL_LIST.append(str(row['Email Address.3']))


    df.apply(gather_email,axis=1)

    sample_file=open(STUDENT_INVITE_LIST,"w")
    sample_file.write(",".join(EMAIL_LIST))
    sample_file.close()
    print("Output to {}".format(STUDENT_INVITE_LIST))

    readable_file = open(STUDENT_READABLE_LIST,"w")
    readable_file.write(",\n".join(EMAIL_LIST))
    readable_file.close()
    print("Readable output to {}".format(STUDENT_READABLE_LIST))



## AGGREGATE FUNCTIONS FOR WHOLE BDC WORKSPACE

def create_all_student_channels() : 

    TEAMS_PROCESSED = 0 

    def processTeam(row) : 

        GENERATE_TEAM_NAME = generate_team_name('random')
        chan_id = create_channel(GENERATE_TEAM_NAME,True)['channel']['id']
        #print("--> {}".format(chan_id))
        
        NEW_TEAM_NAME = "{}_{}".format(GENERATE_TEAM_NAME,chan_id)
        students_table_raw.insert_one({'channel_id':chan_id,'team_name':NEW_TEAM_NAME})
        
        print("NEW --> {}".format(NEW_TEAM_NAME))
        client.conversations_rename(channel=chan_id,name=NEW_TEAM_NAME.lower())

        # Assign student to Workspace
        STUDENT_USER_IDS=[]
        if row['Email Address'] is not np.nan : 
            user1=client.users_lookupByEmail(email=row['Email Address'])['user']['id']
            #print(user1)
            STUDENT_USER_IDS.append(user1)
        if row['Email Address.1'] is not np.nan: 
            user2=client.users_lookupByEmail(email=row['Email Address.1'])['user']['id']
            STUDENT_USER_IDS.append(user2)
        if row['Email Address.2'] is not np.nan: 
            user3=client.users_lookupByEmail(email=row['Email Address.2'])['user']['id']
            STUDENT_USER_IDS.append(user3)
        if row["Email Address.3"] is not np.nan : 
            user4=client.users_lookupByEmail(email=row['Email Address.3'])['user']['id']
            STUDENT_USER_IDS.append(user4)

    

        ## Assigns permissions to ADMINS
        
        assign_members(chan_id,STUDENT_USER_IDS)
        assign_members(chan_id,ADMIN_USERIDS)
        time.sleep(1)


    mydf=df
    mydf.apply(processTeam,axis=1)

def delete_all_student_channels() : 
        
    pass 


## DB CREATION FUNCTIONS 

def db_students_table_raw() : 
    df=pd.read_csv(STUDENTS_CSV,parse_dates=['Submission Time'])
    
    def processStudentRow(row) : 
        all_cols = df.columns.values.tolist()
        PAYLOAD={}
        for col in all_cols:
            PAYLOAD[slugify(col)]=row[col]
        students_table_raw.insert_one(PAYLOAD)


    df.apply(processStudentRow,axis=1)