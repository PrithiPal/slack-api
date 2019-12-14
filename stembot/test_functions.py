import unittest
import basic as api
import os 
import slack 
from slack import WebClient as slack_client

MY_STEMBOT_TOKEN=os.getenv("STEMBOT_TOKEN")
client = slack_client(token=MY_STEMBOT_TOKEN)

class TestSlackFunctions(unittest.TestCase) : 

    
    def setUp(self) : 
        print("TEST FIXTURE SETUP")
        self.all_public_channels_names = [i["name"] for i in client.conversations_list(types="public_channel")["channels"]]
        self.all_public_channels_ids = [i["id"] for i in client.conversations_list(types="public_channel")["channels"]]

        self.all_private_channels_names = [i["name"] for i in client.conversations_list(types="private_channel")["channels"]]
        self.all_private_channels_ids = [i["id"] for i in client.conversations_list(types="private_channel")["channels"]]
        
        print("# of public channels = {}".format(len(self.all_public_channels_names)))
        print("# of private channels = {}".format(len(self.all_private_channels_names)))

    def test_get_channel_id(self) : 
        ind=0
        self.assertEqual(api.get_channel_id(self.all_public_channels_names[ind],is_public=True),
                            self.all_public_channels_ids[ind])

        public_chan_name = "olots_of_data"
        self.assertEqual(api.get_channel_id(public_chan_name,is_public=True),"CP6S1LT5Y")

        private_chan_name = "4guyswhoeatpie"
        self.assertEqual(api.get_channel_id(private_chan_name,is_public=False),"CQ5H42XGE")


if __name__ == "__main__" : 
    unittest.main()
