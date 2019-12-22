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



def main():

    val = generate_num_messages_all()
    print(val)

    #db_add_members_channel_info()
    #db_testing()
    
    return 0
    

if __name__=="__main__" : 
    main()
    