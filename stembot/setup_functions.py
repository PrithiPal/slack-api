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

## HELPER FUNCTIONS for SETUP
def create_channel(chan_name,chan_private,user_id_list) : 
    response = client.conversations_create(name=chan_name,is_private=chan_private)
    # print(response)
    response2 = client.conversations_invite(channel=response['channel']['id'],users=user_id_list)
    
    return response

def get_users_all() : 
    response = client.users_list()
    return response 


def slugify(string) : 
    new_string = re.sub("\-","_",string)
    new_string = re.sub("\ ","_",new_string)
    new_string = re.sub("\.","_",new_string)
    return new_string

def create_student_invite_list() : 

    df=pd.read_csv(STUDENTS_CSV,parse_dates=['Submission Time'])
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

    sample_file=open("student_invite_emails.txt","w")
    sample_file.write(",".join(EMAIL_LIST))
    sample_file.close()
    print("Output to {}".format(STUDENT_INVITE_LIST))



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