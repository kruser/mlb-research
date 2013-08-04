'''
Created on Jul 28, 2013

Hit Predictability Index describes hits that go where they are expected. For example, an outside pitch should be hit to the opposite
field.

A lower value, means you're a more predictable hitter.

@author: kruser
'''
from pymongo import MongoClient
from datetime import datetime
import argparse
from kruser.mlb.HitAngleAggregator import HitAngleAggregator

def make_date(datestr):
    return datetime.strptime(datestr, '%m/%d/%Y')

# setup the args.
parser = argparse.ArgumentParser(description='Analyze baseball data for Hit Predictability. Results are presented to STDOUT in CSV format.')
parser.add_argument('--stats', dest='stats', action='store_true', help='If set, some stats about the qualifying RMIs will be printed at the end of the results')
parser.add_argument('--start', dest='start', type=make_date, metavar='MM/DD/YYYY', required=True, help='The start of your date range')
parser.add_argument('--end', dest='end', type=make_date, metavar='MM/DD/YYYY', required=True, help='The end of your date range')
parser.add_argument('--plateSection', choices=['inside', 'outside'], help='The section of the plate to analyze')
args = parser.parse_args()

# The plate boundaries describe what we would consider a hittable
# ball based on the handedness of the hitter
# See the HitBallPitchLocation.py script for information on how this was
# captured
plateBoundaries = {'L':[-1.357, 0.891], 'R':[-1.129, 1.1769]}; 

# Setup the database connection
client = MongoClient()
db = client.mlbatbat

def get_expected_angle(hand, px):
    '''
    :param hand: L or R - the handedness of the hitter
    :param px: the px value from PitchFX, signifies the offset from the center of the plate, in feet
    '''
    boundaries = plateBoundaries[hand]
    if px < boundaries[0]:
        return 45 
    elif px > boundaries[1]:
        return 135
    else:
        platePercentage = (px - boundaries[0]) / (boundaries[1] - boundaries[0])
        fieldAngle = 90 * platePercentage + 45
        return fieldAngle 

def get_player(playerId):
    '''
    Retrieve a single player from the database, given an ID
    :param playerId: the AtBatID for the player
    '''
    playersCollection = db.players
    return playersCollection.find_one({"id":playerId})

def get_minimum_hit_balls(start, end):
    '''
    Gets the minimum number of potential hit balls required to be considered
    
    Must have 1 hit ball per game played. This is a general method that works
    on games per day and not games played by the batter.
    
    :param start: the starting date
    :param end: the ending date
    '''
    gamesCollection = db.games
    
    # take the max of the twins or cubs games for the time allotted and assume the league played about that many games
    # this isn't perfect as it assumes each team has played the same number of games over a time range, but it'll do 
    # for now.
    cubsGames = gamesCollection.find({'$or':[{'home_name_abbrev':'CHC'},{'away_name_abbrev':'CHC'}],'start':{'$gte':start, '$lt':end}}).count()
    twinsGames = gamesCollection.find({'$or':[{'home_name_abbrev':'MIN'},{'away_name_abbrev':'MIN'}],'start':{'$gte':start, '$lt':end}}).count()
    gameCount = max(cubsGames, twinsGames);
    if gameCount >= 5: 
        if args.plateSection:
            return gameCount / 2
        else:
            return gameCount
    else:
        return 0

pitchesCollection = db.pitches

players = {}

mongoFilter = {'hip.angle':{'$exists':True},'tfs_zulu':{'$gte':args.start, '$lt':args.end}}

middleL = ((plateBoundaries['L'][1] - plateBoundaries['L'][0]) / 2) + plateBoundaries['L'][0];
middleR = ((plateBoundaries['R'][1] - plateBoundaries['R'][0]) / 2) + plateBoundaries['R'][0];
if args.plateSection == 'outside':
    mongoFilter['$or'] = [{'atbat.stand':'L','px':{'$lt':middleL}},{'atbat.stand':'R','px':{'$gt':middleR}}]
elif args.plateSection == 'inside':
    mongoFilter['$or'] = [{'atbat.stand':'L','px':{'$gt':middleL}},{'atbat.stand':'R','px':{'$lt':middleR}}]

hitPitches = pitchesCollection.find(mongoFilter)
for pitch in hitPitches:
    if 'px' in pitch:
        batterId = pitch['atbat']['batter']
        if batterId in players:
            tracker = players[batterId]
        else:
            tracker = HitAngleAggregator(batterId)
            players[batterId] = tracker
            
        hand = pitch['atbat']['stand']
        px = pitch['px']
        hitAngle = pitch['hip']['angle']
        expectedFieldAngle = get_expected_angle(hand, px)
        tracker.add_hit_ball(hand, hitAngle, expectedFieldAngle)
        #print 'hand {}, px {}, angle {}, expected {}, score {}'.format(hand, px, hitAngle, expectedFieldAngle, tracker.get_score())


playerTrackers = players.values()
playerTrackers.sort(key=lambda tracker: tracker.get_score(), reverse=False)

minHitBalls = get_minimum_hit_balls(args.start, args.end)

print 'Batter,Absolute Score,Average Score,Standard Deviation,Hit Balls'
for tracker in playerTrackers:
    if tracker.get_hit_count() >= minHitBalls:
        player = get_player(tracker.batterId)
        print '{} {},{},{},{},{}'.format(player['first'], player['last'], tracker.get_score(), tracker.get_mean(), tracker.get_std(), tracker.get_hit_count())
    