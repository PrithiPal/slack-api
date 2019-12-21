import os 
import slack 
import time 
import pickle
import pandas as pd 
import numpy as np 
from typing import Dict, List
from pymongo import MongoClient
from slack import WebClient as slack_client
from parameters import *


## WRAPPER FUNCTIONS 
def measure_time(func):
    def wrapper(*args,**kwargs):
        start = time.time()
        returnval = func(*args,**kwargs)
        end = time.time() 
        print("Time taken by {} is {}".format(func.__name__,end-start))
        return returnval
    return wrapper

def recored_function_calls(func) : 
    def wrapper(*args,**kwargs) : 
        global NUM_FUNC_CALLS 
        NUM_FUNC_CALLS+=1
        returnval = func(*args,**kwargs)
        return returnval
    return wrapper




def add_dicts(d1,d2) : 

    d3={}
    k1 = d1.keys()
    k2  = d2.keys()

    all_keys=set(k1).union(k2)
    for k in all_keys : 
        sum=0
        if k in k1 : 
            sum+=d1[k]
        if k in k2 : 
            sum+=d2[k]
        d3[k]=sum

    return d3 

@recored_function_calls
def post_message_to_slack(channel_name,text_to_post) : 
    response = client.chat_postMessage(
            channel=channel_name,
            text=text_to_post
    ) 
    assert response["ok"]
    assert response["message"]["text"] == "Hello world!"

## test type checking
@recored_function_calls
def get_channel_id(channel_name : str,is_public : bool) -> int:
    
    #t1 = time.time()
    if is_public : 
        channel = PUBLIC_CHANNELS
    else:
        channel = PRIVATE_CHANNELS

    current_channel_id = [i["id"] for i in channel if i["name"]==channel_name]

    if(len(current_channel_id)>1) : 
        print("--> get_channel_id : Multiple channels returned\nargs={},{} Ignoring..".format(channel_name,is_public))
        return ""
    elif current_channel_id==[]:
        print("--> get_channel_id : Channel {} , {} not found. ".format(channel_name,is_public))
        return ""
    else : 
        return current_channel_id[0]

## test type checking
@recored_function_calls
def get_channel_members_ids(channel_id : str , is_public : bool ) -> List[int] :

    channel_members = client.conversations_members(channel=channel_id,limit=MAX_CHANNEL_NUM)["members"]

    return channel_members

## test type checking
@recored_function_calls
def get_member_info(member_id : str ) -> Dict[str,str] : 

    
    presence_info = client.users_getPresence(user=member_id)
    user_identity = client.users_info(user=member_id)


    try : 
        for user in user_identity : 
            user_real_name=""
            user_team_id = user["user"]["team_id"]
            if "real_name" in user["user"] : 
                user_real_name = user["user"]["real_name"]
            else:
                user_real_name = user["user"]["name"]
    except : 
        print("[err] : real_name not a key. skipping... ")
    
    return {"real_name":user_real_name}

## add type checking and test type checking
def get_channel_info(channel_id : str,is_public : bool) -> Dict[str,str] : 

    public_channel_info = client.conversations_info(channel=channel_id)

    channel_member_ids = get_channel_members_ids(channel_id,is_public=is_public)

    chan_creator = public_channel_info["channel"]["creator"]
    team_id = public_channel_info["channel"]["shared_team_ids"]
    return {'creator':chan_creator,'members':channel_member_ids,'channel_id':channel_id}


def db_add_members_channel_info() : 
    
    for chan in PRIVATE_CHANNELS : 
        chan_name = chan["name"]
        chan_id = chan["id"]
        chan_is_public = not chan["is_private"]
        members = get_channel_members_ids(chan_id,is_public=chan_is_public)
        #member_names = list(map(lambda x:get_member_info(x),members))

        
        channel_table.insert_one({
            "name" : chan_name ,
            "id" : chan_id,
            "is_public" : True,
            #"members" : members
        })


        ## time consuming.
        #member_table.insert_many(
        #    [{"name":x["real_name"],"id":y} for x,y in zip(member_names,members) ]
        #)

def db_testing() : 
    data = {"col1":"something","col2":"something2"}
    member_table.insert_one(data)
    pass


def db_cache_create() : 
    
    PUBLIC_CHANNELS=client.conversations_list(types="public_channel",limit=CHANNEL_NUM)["channels"]
    PRIVATE_CHANNELS=client.conversations_list(types="private_channel",limit=CHANNEL_NUM)["channels"]

    for chan in PUBLIC_CHANNELS : 
        
        conversations_list_table.insert_one(chan)
        try : 
            chan_mem = client.conversations_members(channel=chan["id"],limit=MAX_CHANNEL_NUM)
            payload = {"channel_id":chan["id"],"channel_name":chan["name"],"members":chan_mem.__dict__["data"]["members"]}
            conversations_members_table.insert_one(payload)

        except Exception as e : 
            print("Error : {}".format(e.args))


    for chan in PRIVATE_CHANNELS : 
        conversations_list_table.insert_one(chan)
        try : 
            chan_mem = client.conversations_members(channel=chan["id"],limit=MAX_CHANNEL_NUM)
            payload = {"channel_id":chan["id"],"channel_name":chan["name"],"members":chan_mem.__dict__["data"]["members"]}
            conversations_members_table.insert_one(payload)
        except Exception as e : 
            
            print("Error : {}".format(e.args))



