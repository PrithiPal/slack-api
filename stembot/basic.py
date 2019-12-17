import os 
import slack 
from slack import WebClient as slack_client

## DEFAULT CONFIGURATIONS DEFINITIONS

MENTOR_CHANNEL_NAME="mentors"
MY_STEMBOT_TOKEN=os.getenv("STEMBOT_TOKEN")
CHANNEL_NUM = 500

client = slack_client(token=MY_STEMBOT_TOKEN)

def post_message_to_slack(channel_name,text_to_post) : 
    response = client.chat_postMessage(
            channel=channel_name,
            text=text_to_post
    )
    assert response["ok"]
    assert response["message"]["text"] == "Hello world!"


def get_channel_id(channel_name,is_public):
    
    if is_public : 
        channel = client.conversations_list(types="public_channel",limit=CHANNEL_NUM)["channels"]
    else:
        channel = client.conversations_list(types="private_channel",limit=CHANNEL_NUM)["channels"]
        
    #print(channel)
    
    current_channel_id = [i["id"] for i in channel if i["name"]==channel_name]
    
    if(len(current_channel_id)>1) : 
        print("--> get_channel_id : Multiple channels returned\nargs={},{} gnoring..".format(channel_name,is_public))
        return ""
    elif current_channel_id==[]:
        print("--> get_channel_id : Multiple channels returned\nargs={},{} gnoring..".format(channel_name,is_public))
        return ""
    else : 
        return current_channel_id[0]
    

def get_channel_members_ids(channel_name,is_public):
    
    channel_id = get_channel_id(channel_name,is_public)
    channel_members = client.conversations_members(channel=channel_id,limit=100)["members"]
    #print(channel_members)
    return channel_members
    

def get_member_info(member_id) : 
    
    presence_info = client.users_getPresence(user=member_id)
    user_identity = client.users_info(user=member_id)

    #print(user_identity)
   
    for user in user_identity : 
        user_team_id = user["user"]["team_id"]
        user_real_name = user["user"]["real_name"]
    
    return {"team_id":user_team_id,"real_name":user_real_name}
    

def get_channel_info(channel_name,is_public) : 

    channel_id = get_channel_id(channel_name,is_public=is_public)
    public_channel_info = client.conversations_info(channel=channel_id)
    channel_member_ids = get_channel_members_ids(channel_name,is_public=is_public)
    #print(public_channel_info)
    chan_creator = public_channel_info["channel"]["creator"]
    team_id = public_channel_info["channel"]["shared_team_ids"]
    return {'creator':chan_creator,'team_id':team_id,'members':channel_member_ids}

def channel_message_analysis(channel_name,is_public) : 
    print("chan : {}".format(channel_name))
    try : 
        chan_id = get_channel_id(channel_name,is_public=is_public)
        user_history = {}
        PAGINATION_LIMIT=200
        chan_history = client.conversations_history(channel=chan_id,limit=PAGINATION_LIMIT)
        #print(chan_history.__dict__.["data"].keys())
        #print(chan_history)
        
        
        if "response_metadata" in chan_history.__dict__["data"].keys() : 
            #print("Second")
            cursor = chan_history["response_metadata"]["next_cursor"]
            i = 0 
            while(True) : 
                chan_message = chan_history["messages"]
                for message in chan_message : 
                    message_user = message["user"] 
                    if message_user not in user_history : 
                        user_history[message_user]=1
                    else:
                        user_history[message_user]+=1

                if "response_metadata" not in chan_history.__dict__["data"].keys() : 
                    break
                else:
                    cursor = chan_history["response_metadata"]["next_cursor"]

                chan_history = client.conversations_history(channel=chan_id,limit=PAGINATION_LIMIT,cursor=cursor)
                i+=1
                print("{} {}".format(i,cursor))
        else:
            #print("First")
            chan_message = chan_history["messages"]
            for message in chan_message : 
                #print(message)
                message_user = message["user"] 
                if message_user not in user_history : 
                    user_history[message_user]=1
                else:
                    user_history[message_user]+=1 


        names = list(map(lambda x:get_member_info(x)["real_name"],user_history))
        returnval = list(zip(names,user_history.values()))
        return returnval

    except Exception as e : 
        print("--> channel_message_analysis : Error : {} . Exiting..".format(e))
        return {}


def generate_num_messages_all() : 
    
   all_public_channels =  [i["name"] for i in client.conversations_list(types="public_channel",limit=CHANNEL_NUM)["channels"]]
   all_private_channels = [i["name"] for i in client.conversations_list(types="private_channel",limit=CHANNEL_NUM)["channels"]] 

   public_chan_data = [channel_message_analysis(c,is_public=True) for c in all_public_channels]
   private_chan_data = [channel_message_analysis(c,is_public=False) for c in all_private_channels]
   

   return {**public_chan_data,**private_chan_data}



def main():

    #val=get_channel_info("lawrence_park_ci_team",is_public=True)
    #val = get_member_info("UMRV5AK16")
    #val = channel_message_analysis("fridge",is_public=False)
    val = generate_num_messages_all()
    print(val)
    return 0
    

if __name__=="__main__" : 
    main()
    