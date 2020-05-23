import os 
import slack 
import time 
import pickle
import pandas as pd 
import numpy as np 
from pymongo import MongoClient
from typing import Dict, List
from slack import WebClient as slack_client

from parameters import *
from setup_functions import *
from db_functions import * 
from realtime import * 

import time 
def main():
    
    # print(get_users_all())

    ## DB FUNCTIONS 


    #db_cache_create()
    
    time.sleep(2)
    
    #db_create_report_num_messages()
    db_students_table_raw()


    ## WORKSPACE CREATION 


    #create_student_invite_list()
    #create_all_student_channels()
    
    ## MESSAGING CREATION 

    #post_message("#general","Hello there!")


    return  0 

if __name__=="__main__" : 
    main()

    