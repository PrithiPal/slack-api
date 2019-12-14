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


    
def get_channel_id(channel_name,is_public):
    
    if is_public : 
        channel = client.conversations_list(types="public_channel")["channels"]
    else:
        channel = client.conversations_list(types="private_channel")["channels"]
        
    #print(channel)
    
    current_channel_id = [i["id"] for i in channel if i["name"]==channel_name][0]
    return current_channel_id
    
def get_channel_members_ids(channel_name,is_public):
    
    channel_id = get_channel_id(channel_name,is_public)
    channel_members = client.conversations_members(channel=channel_id,limit=10)["members"]
    print(channel_members)
    return channel_members
    
def get_member_info(member_id) : 
    
    conv_info = client.users_conversations(user=member_id)
        
    


def main():
    
    get_channel_members_ids("mentors",False)
    return 0
    

if __name__=="__main__" : 
    main()
    