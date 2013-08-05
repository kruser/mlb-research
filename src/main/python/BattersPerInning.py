'''
Created on Jul 10, 2013

Calculates the number of batters per inning. Desgined to be used with the atbat-mongodb
database.

@author: kruser
'''
from pymongo import MongoClient
from datetime import datetime
from numpy import mean
from numpy import std
from matplotlib import pyplot 
import argparse

def make_date(datestr):
    return datetime.strptime(datestr, '%m/%d/%Y')

# setup the args.
parser = argparse.ArgumentParser(description='Calculate the at-bats per inning over a period of time.')
parser.add_argument('--start', dest='start', type=make_date, metavar='MM/DD/YYYY', required=True, help='The start of your date range')
parser.add_argument('--end', dest='end', type=make_date, metavar='MM/DD/YYYY', required=True, help='The end of your date range')
args = parser.parse_args()

# Setup the database connection
client = MongoClient()
db = client.mlbatbat
inningsAggregator = {}

def analyze_atbat(atbat):
    if 'inning' in atbat and 'game' in atbat:
        inning = atbat['inning']
        inningKey = atbat['game']['id'] + '_' + inning['type'] + '_' + str(inning['number'])
        if inningKey in inningsAggregator:
            inningsAggregator[inningKey] += 1
        else:
            inningsAggregator[inningKey] = 1
            
def show_distribution_chart():
    atbatList = inningsAggregator.values()
    print 'Mean: {}'.format(mean(atbatList))
    print 'Max: {}'.format(max(atbatList))
    print 'Min: {}'.format(min(atbatList))
    print 'STD: {}'.format(std(atbatList))
    
    threes = 0
    for atbatCount in atbatList:
        if atbatCount == 3:
            threes += 1
    
    inningCount = len(atbatList)
    print '{} of {} half innings included three batters'.format(threes, inningCount)
    print 'In a game with 18 half innings this equates to roughly {} half innings with 3 at-bats'.format(float(threes * 18) / float(inningCount))
    
    pyplot.figure();
    pyplot.hist(atbatList, bins=20, histtype='stepfilled', color='black', alpha=0.8)
    pyplot.title('Batters per Inning Distribution for {} through {}'.format(args.start.date().isoformat(), args.end.date().isoformat()))
    pyplot.xlabel('batters')
    pyplot.ylabel('frequency')
    pyplot.show()

atBatsCollection = db.atbats
atbatsWithRunners = atBatsCollection.find({'start_tfs_zulu':{'$gte':args.start, '$lt':args.end}})
for atbat in atbatsWithRunners:
    analyze_atbat(atbat)
    
show_distribution_chart()
    