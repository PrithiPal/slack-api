import os 
import slack 
from slack import WebClient as slack_client

## DEFAULT CONFIGURATIONS DEFINITIONS

MENTOR_CHANNEL_NAME="mentors"
MY_STEMBOT_TOKEN=os.getenv("STEMBOT_TOKEN")
CHANNEL_NUM = 150

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
        print("Multiple channels returned. Ignoring..")
        return ""
    elif current_channel_id==[]:
        print("Empty channel list. Ignoring..")
        return ""
    else : 
        return current_channel_id[0]
    
## untested 
def get_channel_members_ids(channel_name,is_public):
    
    channel_id = get_channel_id(channel_name,is_public)
    channel_members = client.conversations_members(channel=channel_id,limit=100)["members"]
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
    
    return {"team_id":user_team_id,"real_name":user_real_name}
    
## untested
def get_channel_info(channel_name,is_public) : 

    channel_id = get_channel_id(channel_name,is_public=is_public)
    public_channel_info = client.conversations_info(channel=channel_id)
    channel_member_ids = get_channel_members_ids(channel_name,is_public=is_public)
    #print(public_channel_info)
    chan_creator = public_channel_info["channel"]["creator"]
    team_id = public_channel_info["channel"]["shared_team_ids"]
    return {'creator':chan_creator,'team_id':team_id,'members':channel_member_ids}


def main():

    #val=get_channel_info("lawrence_park_ci_team",is_public=True)
    val = get_member_info("UMRV5AK16")
    print(val)
    return 0
    

if __name__=="__main__" : 
    main()
    