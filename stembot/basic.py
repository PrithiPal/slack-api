import os 
import slack 
from slack import WebClient as slack_client

## DEFAULT CONFIGURATIONS DEFINITIONS

MENTOR_CHANNEL_NAME="mentors"
MY_STEMBOT_TOKEN=os.getenv("STEMBOT_TOKEN")

client = slack_client(token=MY_STEMBOT_TOKEN)

def post_message_to_slack(channel_name,text_to_post) : 
    response = client.chat_postMessage(
            channel=channel_name,
            text=text_to_post
    )
    assert response["ok"]
    assert response["message"]["text"] == "Hello world!"

## untested
def get_channel_id(channel_name,is_public):
    
    if is_public : 
        channel = client.conversations_list(types="public_channel")["channels"]
    else:
        channel = client.conversations_list(types="private_channel")["channels"]
        
    #print(channel)
    
    current_channel_id = [i["id"] for i in channel if i["name"]==channel_name][0]
    return current_channel_id
    
## untested 
def get_channel_members_ids(channel_name,is_public):
    
    channel_id = get_channel_id(channel_name,is_public)
    channel_members = client.conversations_members(channel=channel_id,limit=10)["members"]
    #print(channel_members)
    return channel_members
    
## untested
def get_member_info(member_id) : 
        
    USER_VARIABLES=["name"]
    
    presence_info = client.users_getPresence(user=member_id)
    user_identity = client.users_info(user=member_id)
   
    for user in user_identity : 
        user_team_id = user["user"]["team_id"]
        user_real_name = user["user"]["real_name"]
        user_team = user["user"]["profile"]["team"]
    
    return {"team_id":user_team_id,"real_name":user_real_name,"team":user_team}
    
## untested
def get_channel_info(channel_id) : 

    public_channel_info = client.channels_info(channel=channel_id)
    
    print(public_channel_info)
    #return public_channel_info

def main():


    #mentor_members = get_channel_members_ids("mentors",False)
    #info=get_member_info(mentor_members[2])
    #print(info)

    channel_id = get_channel_id("abbey_park",False)
    print(channel_id)
    return 0
    

if __name__=="__main__" : 
    main()
    