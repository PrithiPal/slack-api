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
import helper_functions as hf 



## add type checking and test type checking
def get_conversation_history(channel_name,is_public) : 
    print("channel : #{}".format(channel_name))
    try : 
        chan_id = hf.get_channel_id(channel_name,is_public=is_public)
        user_history = {}
        chan_history = client.conversations_history(channel=chan_id,limit=PAGINATION_LIMIT)
        
        msg=chan_history.__dict__["data"]["messages"]
        payload={"channel_id":chan_id,"channel_name":channel_name,"messages":chan_history.__dict__["data"]["messages"]}
        
        conversation_history_table_raw.insert_one(payload)

        ## if the whole conversation_history_table is not loaded.(because data can't fit into PAGINATION_LIMIT pages)
        if "response_metadata" in chan_history.__dict__["data"].keys() : 
            #print("Second")
            cursor = chan_history["response_metadata"]["next_cursor"]
            i = 0 
            
            while(True) : 

                if "response_metadata" not in chan_history.__dict__["data"].keys() : 
                    break
                else:
                    cursor = chan_history["response_metadata"]["next_cursor"]

                chan_history = client.conversations_history(channel=chan_id,limit=PAGINATION_LIMIT,cursor=cursor)
                payload={"channel_id":chan_id,"channel_name":channel_name,"messages":chan_history.__dict__["data"]["messages"]}
                conversation_history_table_raw.insert_one(payload)
                
                i+=1
                print("{} {}".format(i,cursor))

        return user_history

    # most common excepts: 
    # User Not Found
    # Rate Limit Exceeded  
    # real_name 
    except Exception as e : 
        print("--> get_conversation_history : Error : {} . Exiting..".format(e))
        x = e.args
        #print("Exception args = {}".format(x))
        for err in e.args : 
            if 'user' in err : 
                print('--> Total requests made = {}'.format(NUM_REQUESTS))
                return {'error':'user'}
            if 'ratelimited' in err : 
                ## 10s sleep before making anyother request.
                ## Slack Api rate limit info can be found here : https://api.slack.com/docs/rate-limits
                print('--> Total requests made = {}'.format(NUM_REQUESTS))
                return {'error':'rate_limited'}
            if 'real_name' in err : 
                return {'error':'real_name'}
        return {}
"""
populates the tables : 
 - conversation_history_table_raw
"""
def db_conversation_history_table(to_pickle=False,to_csv=True) : 
    DO_PUBLIC=True
    DO_PRIVATE=True
    all_data = {}
    missed_channels = []

    if DO_PRIVATE : 

        all_private_channels = [i["name"] for i in PRIVATE_CHANNELS] 
        for c in all_private_channels : 
            output = get_conversation_history(c,is_public=False)
            
            if 'error' not in output : 
                all_data = hf.add_dicts(all_data,output)
            else:
                missed_channels.append((c,False))
        
    if DO_PUBLIC : 
        all_public_channels =  [i["name"] for i in PUBLIC_CHANNELS]
        
        for c in all_public_channels : 
            output = get_conversation_history(c,is_public=True)
            
            if 'error' not in output : 
                all_data = hf.add_dicts(all_data,output)
            else:
                missed_channels.append((c,True))
    
    #print("missed_channels={}".format(missed_channels))
    
    if missed_channels !=[] : 
        print("--> Waiting ({}s) and starting Missing Channels processing ".format(RATE_LIMIT_TIME_WAIT))
        
        time.sleep(RATE_LIMIT_TIME_WAIT)
        for c in missed_channels : 
            chan_name = c[0]
            is_public = c[1]
            output = get_conversation_history(chan_name,is_public=is_public)
            if output == {}:
                print("{} unprocessed ".format(chan_name))
            else : 
                all_data = hf.add_dicts(all_data,output)

    ## ADD MORE REQUIRED INFORMATION OVER HERE INTO THE general_num_messages_all.csv

    #df = pd.DataFrame({'user_id':list(all_data.keys()),'num_messages':list(all_data.values())})
    #df['name'] = df.apply(lambda x:get_member_info(x["user_id"])["real_name"],axis=1)
    #df['team']

    if to_pickle : 
        pickle.dump(all_data,open("generate_num_messages_all.p","wb"))
        pickle.dump(missed_channels,open("general_num_messag_all_missed_channels.p","wb"))
    
    if to_csv : 
        df = pd.DataFrame({'name':list(all_data.keys()),'number_of_messages':list(all_data.values())})
        df.to_csv('general_num_messages_all.csv')

    
    return all_data 


"""
RAW TABLES CREATION 
populates the following tables : 

- member_table
- conversations_members
- conversations_list
- conversations_history 

"""
def db_cache_create() : 

    PUBLIC_CHANNELS=client.conversations_list(types="public_channel",limit=CHANNEL_NUM)["channels"]
    PRIVATE_CHANNELS=client.conversations_list(types="private_channel",limit=CHANNEL_NUM)["channels"]

    EXCLUDE_CHANNELS=["stembot_test"]
    
    ## Populates the students table
    chan_mem=client.conversations_members(channel=hf.get_channel_id("general",is_public=True),limit=MAX_CHANNEL_NUM)
    members = chan_mem.__dict__["data"]["members"]
    ## Populates the conversation_member table.

    for chan in PUBLIC_CHANNELS : 
        if chan not in EXCLUDE_CHANNELS : 
        
            conversations_list_table_raw.insert_one(chan)
            try : 
                chan_mem = client.conversations_members(channel=chan["id"],limit=MAX_CHANNEL_NUM)
                members = chan_mem.__dict__["data"]["members"]
                payload = {"channel_id":chan["id"],"channel_name":chan["name"],"members":members}
                conversations_members_table_raw.insert_one(payload)

            except Exception as e : 
                print("Error : {}".format(e.args))


    for chan in PRIVATE_CHANNELS : 
        if chan not in EXCLUDE_CHANNELS : 

            conversations_list_table_raw.insert_one(chan)
            try : 
                chan_mem = client.conversations_members(channel=chan["id"],limit=MAX_CHANNEL_NUM)
                payload = {"channel_id":chan["id"],"channel_name":chan["name"],"members":chan_mem.__dict__["data"]["members"]}
                conversations_members_table_raw.insert_one(payload)

            except Exception as e : 
                
                print("Error : {}".format(e.args))


    db_conversation_history_table()


def db_create_report_num_messages():
    
    val1=conversations_members_table_raw.aggregate([
        {"$unwind":"$members"},
        {"$project":
            {
            "_id":0,
            "channel_id":1,
            "channel_name":1,
            "user_id":"$members"
            }
        },
        {"$group":
            {
            "_id":{"user_id":"$user_id","channel_id":"$channel_id","channel_name":"$channel_name"}
            }
        }
    ])
    member_table_raw.insert_many(val1)
    
    distinct_users = conversations_members_table_raw.distinct("members")
    
    for user in distinct_users : 
        user_info = client.users_info(user=user).__dict__["data"]["user"]
        payload={
            "user_id":user,
            "user_name":user_info["name"],
            "user_real_name":user_info["real_name"]
        }
        print(payload)
        member_table_raw.update({"_id.user_id":user},{"$set":payload},multi=True)
    
 
    val=conversation_history_table_raw.aggregate([
        {"$unwind":"$messages"},
        {"$project":{"_id":0,"text":"$messages.text","user":"$messages.user"}},
        {"$group":{"_id":{'user':'$user','channel_id':'$channel_id','channel_name':'$channel_name'}, "num_messages" : {"$sum" : 1}}}])
    num_messages_members_table.insert_many(val)
    


    val1 = num_messages_members_table.aggregate([
        {"$lookup":
            {"from":"member_raw",
            "localField":"_id.user",
            "foreignField":"_id.user_id",
            "as":"russel_peters"
            }
        }
    ])

    num_messages_members2_table.insert_many(val1)
    

    val2 = num_messages_members2_table.aggregate([
        {"$project":
            {"num_messages":1,
             "user_id":{"$arrayElemAt":["$russel_peters.user_id",0]},
             "user_name":{"$arrayElemAt":["$russel_peters.user_name",0]},
             "user_real_name":{"$arrayElemAt":["$russel_peters.user_real_name",0]},
             "channel_ids":"$russel_peters._id.channel_id",
             "channel_names":"$russel_peters._id.channel_name"
            }
        }
    ])

    num_message_user_info_table.insert_many(val2)

    ## drop unnecessary tables.
    #num_messages_members_table.drop()

    

