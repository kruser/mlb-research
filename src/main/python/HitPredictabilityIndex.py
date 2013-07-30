'''
Created on Jul 28, 2013

Hit Predictability Index describes hits that go where they are expected. For example, an outside pitch should be hit to the opposite
field.

A lower value, means you're a more predictable hitter.

@author: kruser
'''
from kruser.mlb.EntityBattingStats import EntityBattingStats
from kruser.mlb.PlateEventsEnum import PlateEventsEnum
from pymongo import MongoClient
from datetime import datetime
from numpy import mean
from numpy import std
from numpy import array
from matplotlib import pyplot 
from scipy import stats
import argparse
import re

def make_date(datestr):
    return datetime.strptime(datestr, '%m/%d/%Y')

# setup the args.
parser = argparse.ArgumentParser(description='Analyze baseball data for Hit Predictability. Results are presented to STDOUT in CSV format.')
parser.add_argument('--stats', dest='stats', action='store_true', help='If set, some stats about the qualifying RMIs will be printed at the end of the results')
parser.add_argument('--start', dest='start', type=make_date, metavar='MM/DD/YYYY', required=True, help='The start of your date range')
parser.add_argument('--end', dest='end', type=make_date, metavar='MM/DD/YYYY', required=True, help='The end of your date range')
args = parser.parse_args()

# Setup the database connection
client = MongoClient()
db = client.mlbatbat

def get_player(playerId):
    '''
    Retrieve a single player from the database, given an ID
    :param playerId: the AtBatID for the player
    '''
    playersCollection = db.players
    return playersCollection.find_one({"id":playerId})

pitchesCollection = db.pitches

playersOrTeams = {}
hitPitches = pitchesCollection.find({'hip.angle':{'$exists':True},'tfs_zulu':{'$gte':args.start, '$lt':args.end}})
for pitch in hitPitches:
    print '.' 


    