import os 
import slack 
import time 
import pickle
import pandas as pd 
import numpy as np 
from typing import Dict, List
from pymongo import MongoClient
from parameters import client 


def create_channel(chan_name,chan_private) : 
    response = client.conversations_create(name=chan_name,is_private=chan_private)
    return response

def get_users_all() : 
    response = client.users_list()
    return response 


def read_users_csv() : 
    pd.read_csv(STUDENTS_CSV,delimiter=",")