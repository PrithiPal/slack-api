import unittest
import basic as api
import os 
import slack 
from slack import WebClient as slack_client

MY_STEMBOT_TOKEN=os.getenv("STEMBOT_TOKEN")
client = slack_client(token=MY_STEMBOT_TOKEN)

class TestSlackFunctions(unittest.TestCase) : 

    @classmethod
    def setUpClass(self) : 
        print("--> TESTING GLOBAL SETUP .. ")
        self.all_public_channels_names = [i["name"] for i in client.conversations_list(types="public_channel",limit=300)["channels"]]
        self.all_public_channels_ids = [i["id"] for i in client.conversations_list(types="public_channel",limit=300)["channels"]]

        self.all_private_channels_names = [i["name"] for i in client.conversations_list(types="private_channel")["channels"]]
        self.all_private_channels_ids = [i["id"] for i in client.conversations_list(types="private_channel")["channels"]]
        
        print("# of public channels = {}".format(len(self.all_public_channels_names)))
        print("# of private channels = {}".format(len(self.all_private_channels_names)))      
        
        self.public_chan_name = "olots_of_data"
        self.private_chan_name = "4guyswhoeatpie"
        self.public_chan_id = "CP6S1LT5Y"
        self.private_chan_id = "CQ5H42XGE"

        self.user1 = "UMRV5AK16" 
        self.user2 = "UPB0D7892"
        self.user3 = "UQ99FQWRJ"

    #def setUp(self) : 
    #    print("TEST PER FUNCTION SETUP .. ")

    def test_channel_exists(self) : 
        print("-- > test_channel_exists()")
        
        chan_name = "lawrence_park_ci_team"
        is_public = True

        is_present = False
        if is_public : 
            is_present=chan_name in self.all_public_channels_names
        else:
            is_present=chan_name in self.all_private_channels_names
        #print("is_present = {}".format(is_present))

        self.assertTrue(is_present)
        
        #chan_id = api.get_channel_id(chan_name,is_public=is_public)
        #print(chan_id)


    def test_get_channel_id(self) : 
        print("-- > test_get_channel_id()")
        ind=0
        self.assertEqual(api.get_channel_id(self.all_public_channels_names[ind],is_public=True),
                            self.all_public_channels_ids[ind])

        self.assertEqual(api.get_channel_id(self.public_chan_name,is_public=True),self.public_chan_id)

        self.assertEqual(api.get_channel_id(self.private_chan_name,is_public=False),self.private_chan_id)

   
    def test_get_channel_members_ids(self) : 
        print("-- > test_get_channel_members_ids()")
        
        #print(api.get_channel_members_ids(self.public_chan_name,is_public=True))
        #print(api.get_channel_members_ids(self.private_chan_name,is_public=False))

        sol1=['UMRV5AK16', 'UPCDVB3DX', 'UPKS6TRQ8', 'UPUGK9M8D', 'UQ0S162TH', 'UQ30NAU8J', 'UQ99FQWRJ', 'UQBE4GPA5', 'UQBVABEA2', 'UQC6DRSTZ', 'UQKBT6H16', 'UQKC9EBT7']
        sol2=['UMRV5AK16', 'UP5BWTWGZ', 'UPB0D7892', 'UPBEANB37', 'UPBQHEZCG', 'UPN3DUTRC']
        
        self.assertEqual(api.get_channel_members_ids(self.public_chan_name,is_public=True),sol1)
        self.assertEqual(api.get_channel_members_ids(self.private_chan_name,is_public=False),sol2)

    def test_get_member_info(self) : 
        print("-- > test_get_member_info()")
        #print(api.get_member_info(self.user1))
        sol = {'team_id': 'TMU55JAQN', 'real_name': 'BDC Admin'}
        self.assertEqual(api.get_member_info(self.user1),sol)
       



if __name__ == "__main__" : 
    unittest.main()
