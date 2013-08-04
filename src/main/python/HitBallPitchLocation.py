'''
Created on Jul 28, 2013

Show a histogram of all hit balls and their horizontal location on the plate

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

def standard_stats(array, heading):
    '''
    simple function to print the mean, max, min and standard deviation of a set of data points
    
    :param array: an array of data
    :param heading: a heading string
    '''
    average = mean(array);
    deviation = std(array);
    
    print heading
    print 'Mean: {}'.format(average)
    print 'Max: {}'.format(max(array))
    print 'Min: {}'.format(min(array))
    print 'STD: {}'.format(deviation)
    print 'Boundaries: {} to {}'.format(average + (deviation*2), average - (deviation*2))
    print ''
    
# setup the args.
parser = argparse.ArgumentParser(description='Shows horizontal pitch location on the plate for all hit balls.')
parser.add_argument('--start', dest='start', type=make_date, metavar='MM/DD/YYYY', required=True, help='The start of your date range')
parser.add_argument('--end', dest='end', type=make_date, metavar='MM/DD/YYYY', required=True, help='The end of your date range')
args = parser.parse_args()

# Setup the database connection
client = MongoClient()
db = client.mlbatbat

pitchesCollection = db.pitches

locationsLeft = []
locationsRight = []

hitPitches = pitchesCollection.find({'hip':{'$exists':True},'tfs_zulu':{'$gte':args.start, '$lt':args.end}})
for pitch in hitPitches:
    if 'px' in pitch:
        if pitch['atbat']['stand'] == 'R':
            locationsRight.append(pitch['px'])
        else:
            locationsLeft.append(pitch['px'])

standard_stats(locationsRight, 'Right Handed Batter Hit Balls')
standard_stats(locationsLeft, 'Left Handed Batter Hit Balls')

pyplot.figure()
pyplot.hist(locationsRight, bins=20, histtype='stepfilled', color='black', alpha=0.8, label='Righties')
pyplot.hist(locationsLeft, bins=20, histtype='stepfilled', color='red', alpha=0.3, label='Lefties')
pyplot.legend()
pyplot.title('Pitch Horizontal Location on Hit Balls (Catcher View) - {} through {}'.format(args.start.date().isoformat(), args.end.date().isoformat()))
pyplot.xlabel('Distance from center of plate (feet)')
pyplot.show()
 
    