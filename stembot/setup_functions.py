import os 
import slack 
import time 
import pickle
import pandas as pd 
import numpy as np 
from typing import Dict, List
from pymongo import MongoClient

from parameters import *

def create_team(team_domain,team_name) : 

    resp = client.admin_teams_create(
        team_domain=team_domain,
        team_name=team_name
        )
    return resp 
