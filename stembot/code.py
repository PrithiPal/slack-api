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


def main():
    create_team("sample-team","sample-team")
    


if __name__=="__main__" : 
    main()

    