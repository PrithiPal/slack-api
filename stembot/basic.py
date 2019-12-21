import os 
import slack 
import time 
import pickle
import pandas as pd 
import numpy as np 
from pymongo import MongoClient
from typing import Dict, List
from slack import WebClient as slack_client
from helper_functions import *
from parameters import *

## add type checking and test type checking
def channel_message_analysis(channel_name,is_public) : 
    print("channel : #{}".format(channel_name))
    try : 
        chan_id = get_channel_id(channel_name,is_public=is_public)
        user_history = {}
        chan_history = client.conversations_history(channel=chan_id,limit=PAGINATION_LIMIT)
            
        if "response_metadata" in chan_history.__dict__["data"].keys() : 
            #print("Second")
            cursor = chan_history["response_metadata"]["next_cursor"]
            i = 0 
            while(True) : 
                chan_message = chan_history["messages"]
                for message in chan_message : 
                    if "user" in message : 
                        message_user = message["user"] 
                        if message_user not in user_history : 
                            user_history[message_user]=1
                        else:
                            user_history[message_user]+=1
                    else:
                        print("[err] : User: not found, skipping..")

                if "response_metadata" not in chan_history.__dict__["data"].keys() : 
                    break
                else:
                    cursor = chan_history["response_metadata"]["next_cursor"]

                chan_history = client.conversations_history(channel=chan_id,limit=PAGINATION_LIMIT,cursor=cursor)
                NUM_REQUESTS+=1
                i+=1
                print("{} {}".format(i,cursor))
        else:
            #print("First")
            chan_message = chan_history["messages"]
            for message in chan_message : 
                if "user" in message : 
                    message_user = message["user"] 
                    if message_user not in user_history : 
                        user_history[message_user]=1
                    else:
                        user_history[message_user]+=1
                else:
                    print("[err] : User: not found, skipping..")


        return user_history

    # most common excepts: 
    # User Not Found
    # Rate Limit Exceeded  
    # real_name 
    except Exception as e : 
        print("--> channel_message_analysis : Error : {} . Exiting..".format(e))
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

@recored_function_calls
def generate_num_messages_all(to_pickle=False,to_csv=True) : 
    DO_PUBLIC=False
    DO_PRIVATE=True
    all_data = {}
    missed_channels = []

    if DO_PRIVATE : 

        all_private_channels = [i["name"] for i in PRIVATE_CHANNELS] 
        for c in all_private_channels : 
            output = channel_message_analysis(c,is_public=False)
            
            if 'error' not in output : 
                all_data = add_dicts(all_data,output)
            else:
                missed_channels.append((c,False))
        
    if DO_PUBLIC : 
        all_public_channels =  [i["name"] for i in PUBLIC_CHANNELS]
        
        for c in all_public_channels : 
            output = channel_message_analysis(c,is_public=True)
            
            if 'error' not in output : 
                all_data = add_dicts(all_data,output)
            else:
                missed_channels.append((c,True))
    
    #print("missed_channels={}".format(missed_channels))
    
    if missed_channels !=[] : 
        print("--> Waiting ({}s) and starting Missing Channels processing ".format(RATE_LIMIT_TIME_WAIT))
        
        time.sleep(RATE_LIMIT_TIME_WAIT)
        for c in missed_channels : 
            chan_name = c[0]
            is_public = c[1]
            output = channel_message_analysis(chan_name,is_public=is_public)
            if output == {}:
                print("{} unprocessed ".format(chan_name))
            else : 
                all_data = add_dicts(all_data,output)

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


def main():

    #val = generate_num_messages_all()
    #print(val)

    #db_add_members_channel_info()
    #db_testing()
    
    return 0
    

if __name__=="__main__" : 
    main()
    