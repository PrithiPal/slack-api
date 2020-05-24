import unittest
import time

import helper_functions as hf
import db_functions as df
import setup_functions as sf 
import realtime as rt 
import csv 
from parameters import *
import basic as ba
import os
import slack
import numpy as np
import pandas as pd
from slack import WebClient as slack_client
import copy 

from random import random,seed 
from datetime import datetime 
from math import ceil 

def measure_time(func):
    def wrapper(*args,**kwargs):
        start = time.time()
        returnval = func(*args,**kwargs)
        end = time.time()
        print("Time taken by {} is {}".format(func.__name__,end-start))
        return returnval
    return wrapper


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


        pass

    #def setUp(self) :
    #    print("TEST PER FUNCTION SETUP .. ")

    @measure_time
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
        pass

        #chan_id = hf.get_channel_id(chan_name,is_public=is_public)
        #print(chan_id)

    @measure_time
    def test_get_channel_id(self) :
        print("-- > test_get_channel_id()")
        ind=0
        self.assertEqual(hf.get_channel_id(self.all_public_channels_names[ind],is_public=True),
                            self.all_public_channels_ids[ind])

        self.assertEqual(hf.get_channel_id(self.public_chan_name,is_public=True),self.public_chan_id)

        self.assertEqual(hf.get_channel_id(self.private_chan_name,is_public=False),self.private_chan_id)
        pass

    @measure_time
    def test_get_channel_members_ids(self) :
        print("-- > test_get_channel_members_ids()")

        #print(hf.get_channel_members_ids(self.public_chan_name,is_public=True))
        #print(hf.get_channel_members_ids(self.private_chan_name,is_public=False))

        sol1=['UMRV5AK16', 'UPCDVB3DX', 'UPKS6TRQ8', 'UPUGK9M8D', 'UQ0S162TH', 'UQ30NAU8J', 'UQ99FQWRJ', 'UQBE4GPA5', 'UQBVABEA2', 'UQC6DRSTZ', 'UQKBT6H16', 'UQKC9EBT7']
        sol2=['UMRV5AK16', 'UP5BWTWGZ', 'UPB0D7892', 'UPBEANB37', 'UPBQHEZCG', 'UPN3DUTRC']

        self.assertEqual(hf.get_channel_members_ids(self.public_chan_id,is_public=True),sol1)
        self.assertEqual(hf.get_channel_members_ids(self.private_chan_id,is_public=False),sol2)
        pass

    @measure_time
    def test_get_member_info(self) :
        print("-- > test_get_member_info()")
        val = hf.get_member_info(self.user1)
        sol = {'real_name': 'BDC Admin'}
        self.assertEqual(val,sol)

        pass

    @measure_time
    def test_channel_message_analysis(self) :
        print("-- > test_channel_message_analysis()")
        SAMPLE_CHAN_NAME="earlhaig-bdc1"
        IS_PUBLIC=True
        missed_channels=[('4guyswhoeatpie', False), ('stembot_test', False)]
        all_data={}
        for c in missed_channels :
            chan_name = c[0]
            is_public = c[1]
            output = ba.channel_message_analysis(chan_name,is_public=is_public)
            if output == {}:
                print("{} unprocessed ".format(chan_name))
            else :
                try :
                    all_data = hf.add_dicts(all_data,output)
                except Exception as err :
                    print('err : {}',err.args)

        response = ba.channel_message_analysis(SAMPLE_CHAN_NAME,is_public=IS_PUBLIC)
        print(response)
        pass

    @measure_time
    def test_db(self) :
        print("-- > test_db()")

        #df.db_cache_create()
        df.db_create_report_num_messages()

    @measure_time 
    def test_channel_creation(self) : 
        print("-- > test_channel_creation()")

        CHANNEL_NAME="modest_northcutt_904049_c013nhlkmfh"
        IS_PRIVATE=False

        SAMPLE_ID1="U0136DUHHPG"
        SAMPLE_ID2="U013D76B97D"
        SAMPLE_ID3="U0136DUHHPG"
        SAMPLE_ID4="U0136AJ7Y86"
        SAMPLE_ID5="U013LFVGVLP"
        SAMPLE_ID5="U0141EEFBSP"

        USER_LIST=[
            SAMPLE_ID2,
            SAMPLE_ID1,
            SAMPLE_ID3,
            SAMPLE_ID4,
            SAMPLE_ID5
        ]

        # channel_id = sf.create_channel( CHANNEL_NAME, IS_PRIVATE)['channel']['id']
        # print("Created channel {} [{}]".format(CHANNEL_NAME,channel_id))
        
        
        sf.assign_members(CHANNEL_NAME[-11:].upper(),USER_LIST)
        
        
        # print("Assigned Members ")

        #for channel_id in CHANS : 
        #    sf.delete_channel(channel_id)
        
        #print("Archived Channel")

    @measure_time 
    def test_generate_team_name(self) : 
        print("-- > test_generate_team_name()")
        for i in range(100) : 
            name = sf.generate_team_name('sample')
            seed_value = datetime.timestamp(datetime.now())
            seed(seed_value)
            randval = ceil(random()*1000000)
            print("{}_{}".format(name,randval))

    @measure_time
    def test_create_all_student_channels(self) : 
        print("-- > test_create_all_student_channels()")
        sf.create_all_student_channels()


    @measure_time
    def test_realtime_functions(self) : 

        




def suite() :
    suite = unittest.TestSuite()
    #suite.addTest(TestSlackFunctions('test_channel_exists'))
    #suite.addTest(TestSlackFunctions('test_get_channel_id'))
    #suite.addTest(TestSlackFunctions('test_get_channel_members_ids'))
    #suite.addTest(TestSlackFunctions('test_get_member_info'))
    #suite.addTest(TestSlackFunctions('test_channel_message_analysis'))
    #suite.addTest(TestSlackFunctions('test_db'))
    #suite.addTest(TestSlackFunctions('test_channel_creation'))
    #suite.addTest(TestSlackFunctions('test_generate_team_name'))
    #suite.addTest(TestSlackFunctions('test_create_all_student_channels'))
    
    
    #suite.addTest(TestSlackFunctions('test_generate_team_name'))
    suite.addTest(TestSlackFunctions('test_realtime_functions'))
    return suite


if __name__ == "__main__" :
    #unittest.main()
    runner = unittest.TextTestRunner()
    runner.run(suite())
