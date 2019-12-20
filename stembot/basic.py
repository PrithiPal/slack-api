import os 
import slack 
import time 
import pickle
import pandas as pd 
import numpy as np 
from typing import Dict, List
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

client = slack_client(token=MY_STEMBOT_TOKEN)

## CACHED DATA (things that takes too much time to call each time.)

PUBLIC_CHANNELS=client.conversations_list(types="public_channel",limit=CHANNEL_NUM)["channels"]
PRIVATE_CHANNELS=client.conversations_list(types="private_channel",limit=CHANNEL_NUM)["channels"]
NUM_REQUESTS+=2

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


client = slack_client(token=MY_STEMBOT_TOKEN)

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
    global NUM_REQUESTS
    channel_members = client.conversations_members(channel=channel_id,limit=MAX_CHANNEL_NUM)["members"]
    NUM_REQUESTS+=1
    return channel_members
    
## test type checking
@recored_function_calls
def get_member_info(member_id : str ) -> Dict[str,str] : 
    global NUM_REQUESTS
    
    presence_info = client.users_getPresence(user=member_id)
    user_identity = client.users_info(user=member_id)
    NUM_REQUESTS+=2

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
    global NUM_REQUESTS
    

    public_channel_info = client.conversations_info(channel=channel_id)
    NUM_REQUESTS+=1
    channel_member_ids = get_channel_members_ids(channel_id,is_public=is_public)

    chan_creator = public_channel_info["channel"]["creator"]
    team_id = public_channel_info["channel"]["shared_team_ids"]
    return {'creator':chan_creator,'members':channel_member_ids,'channel_id':channel_id}

## add type checking and test type checking
@recored_function_calls
def channel_message_analysis(channel_name,is_public) : 
    
    global NUM_REQUESTS
    print("channel : #{}".format(channel_name))
    try : 
        chan_id = get_channel_id(channel_name,is_public=is_public)
        user_history = {}
        chan_history = client.conversations_history(channel=chan_id,limit=PAGINATION_LIMIT)
        NUM_REQUESTS+=1

            
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

    df = pd.DataFrame({'user_id':list(all_data.keys()),'num_messages':list(all_data.values())})
    df['name'] = df.apply(lambda x:get_member_info(x["user_id"])["real_name"],axis=1)
    df['team']
    


    if to_pickle : 
        pickle.dump(all_data,open("generate_num_messages_all.p","wb"))
        pickle.dump(missed_channels,open("general_num_messag_all_missed_channels.p","wb"))
    
    if to_csv : 
        df = pd.DataFrame({'name':list(all_data.keys()),'number_of_messages':list(all_data.values())})
        df.to_csv('general_num_messages_all.csv')

    
    return all_data 


def main():

    val = generate_num_messages_all()
    print(val)

    
    return 0
    

if __name__=="__main__" : 
    main()
    