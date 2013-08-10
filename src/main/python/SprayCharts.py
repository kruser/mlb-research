'''
Created on Aug 3, 2013

Utility to plot out spray charts for a player with a number of filters.

@author: kruser
'''
from pymongo import MongoClient
from datetime import datetime
import argparse
from matplotlib import pyplot
import re

def make_date(datestr):
    return datetime.strptime(datestr, '%m/%d/%Y')

# setup the args.
parser = argparse.ArgumentParser(description='Plot out a hit spray chart for a batter.')
parser.add_argument('--start', dest='start', type=make_date, metavar='MM/DD/YYYY', required=True, help='The start of your date range')
parser.add_argument('--end', dest='end', type=make_date, metavar='MM/DD/YYYY', required=True, help='The end of your date range')
parser.add_argument('--player', required=True, nargs=2, help='The full name of the player to analyze')
parser.add_argument('--pitchType', metavar='PITCH', nargs='*', choices=['FA', 'FF', 'FT', 'FC', 'FS', 'FO', 'SI', 'SL', 'CU', 'KC', 'EP', 'CH', 'SC', 'KN', 'UN'], help='Filter on pitch types. This is the short name of the pitch type from PitchFX. Examples are FF, FC, FA, SL')
parser.add_argument('--pxRange', metavar='0.0', nargs=2, help='Filter on the horizontal range of the pitch in feet, where 0 is the middle of the plate. Negative numbers to the left, positive to the right, both from the view of the catcher.')
args = parser.parse_args()

# Setup the database connection
client = MongoClient()
db = client.mlbatbat

def get_player_id():
    '''
    get the ID of the player based on their name as take from the argparse args
    :return the playerId
    '''
    playersCollection = db.players
    player = playersCollection.find_one({"first":args.player[0], 'last':args.player[1]})
    if player:
        return player['id']
    else:
        raise Exception('I cannot find a player named "{} {}". Check your spelling.'.format(args.player[0], args.player[1]))

playerId = get_player_id()

title = '{} {}: {} to {}'.format(args.player[0], args.player[1], args.start.strftime("%m/%d/%Y"), args.end.strftime("%m/%d/%Y"))

query = {'hip':{'$exists':True},'atbat.batter':playerId,'tfs_zulu':{'$gte':args.start, '$lt':args.end}}
if args.pxRange:
    query['px'] = {'$gte':float(args.pxRange[0]), '$lte':float(args.pxRange[1])}
    title += '\nPitch Placement - Horizontal Offset: {}ft to {}ft'.format(args.pxRange[0], args.pxRange[1])
    
if args.pitchType:
    query['pitch_type'] = {'$in':args.pitchType}
    title += '\nPitch Types: {}'.format(args.pitchType)
    
pitchesCollection = db.pitches
hitPitches = pitchesCollection.find(query)

groundersX = []
groundersY = []

linersX = []
linersY = []

flyballsX = []
flyballsY = []

popupsX = []
popupsY = []

for pitch in hitPitches:
    if re.search('pop up|pops out', pitch['atbat']['des'], re.IGNORECASE):
        popupsX.append(pitch['hip']['x']);
        popupsY.append(pitch['hip']['y']);
    elif re.search('line drive|lines out', pitch['atbat']['des'], re.IGNORECASE):
        linersX.append(pitch['hip']['x']);
        linersY.append(pitch['hip']['y']);
    elif re.search('fly ball|flies out', pitch['atbat']['des'], re.IGNORECASE):
        flyballsX.append(pitch['hip']['x']);
        flyballsY.append(pitch['hip']['y']);
    else:
        groundersX.append(pitch['hip']['x']);
        groundersY.append(pitch['hip']['y']);

pyplot.figure()
im = pyplot.imread('../../main/resources/stadiumImages/1.png')
implot = pyplot.imshow(im)
pyplot.scatter(groundersX, groundersY, marker='v', c="black", label="Grounder")
pyplot.scatter(linersX, linersY, marker='o', label="Liner")
pyplot.scatter(flyballsX, flyballsY, marker='^', c="r", label="Fly Ball")
pyplot.scatter(popupsX, popupsY, marker='s', label="Pop Up")
pyplot.legend()
pyplot.title(title)
pyplot.show()