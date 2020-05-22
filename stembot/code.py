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


def main():
    
    # print(get_users_all())
    #db_cache_create()
    
    #db_create_report_num_messages()
    #db_students_table_raw()

    #create_student_invite_list()
    create_all_student_channels()
    
    #create_student_invite_list()


    return  0 

if __name__=="__main__" : 
    main()

    