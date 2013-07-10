'''
Created on Jul 2, 2013

RMI is an alternative measure to the traditional Runs Batted In (RBI) statistic.
It measures potential runner movement and assigns a percentage success.

For example, if a batter comes up with a runner on 1st and 3rd, there is a potential
to move runners a total of 4 bases. In the event the batter advances the runner on 
1st to 2nd and the runner on 3rd to home, they will be credited with .500 RMI since
the runners moved 2 out of a potential 4 bases. 

@author: kruser
'''
from kruser.mlb.RMI import RMI
from kruser.mlb.EntityBattingStats import EntityBattingStats
from kruser.mlb.PlateEventsEnum import PlateEventsEnum
from pymongo import MongoClient
from datetime import datetime
from numpy import mean
from numpy import std
from matplotlib import pyplot 
from scipy import stats
import argparse

def make_date(datestr):
    return datetime.strptime(datestr, '%m/%d/%Y')

# setup the args.
parser = argparse.ArgumentParser(description='Analyze baseball data for RMI. Results are presented to STDOUT in CSV format.')
parser.add_argument('--team', dest='team', action='store_true', help='If set, the results will be by team instead of by player')
parser.add_argument('--stats', dest='stats', action='store_true', help='If set, some stats about the qualifying RMIs will be printed at the end of the results')
parser.add_argument('--start', dest='start', type=make_date, metavar='MM/DD/YYYY', required=True, help='The start of your date range')
parser.add_argument('--end', dest='end', type=make_date, metavar='MM/DD/YYYY', required=True, help='The end of your date range')
args = parser.parse_args()

# Setup the database connection
client = MongoClient()
db = client.mlbatbat

def adjust_rmi_for_runner(rmi, runner):
    '''
    Adjust the RMI given a single runner from the AtBat schema
    :param rmi: the starting RMI, can't be null
    :param runner: the runner data, can't be null
    '''
    if 'rbi' in runner:
        rbi = runner['rbi']
        if rbi == 'T':
            rmi.add_rbi(1)
            
    start = runner['start']
    startInt = 0
    if start == '':
        return
    elif start == '1B':
        startInt = 1 
    elif start == '2B':
        startInt = 2 
    elif start == '3B':
        startInt = 3 
    rmi.add_potential_bases_moved(4 - startInt)
    
    scored = ''
    if 'score' in runner: 
        scored = runner['score'] 
        
    end = runner['end']
    endInt = 0
    if end == '' and scored == 'T':
        endInt = 4 
    elif end == '':
        endInt = startInt 
    elif end == '3B':
        endInt = 3 
    elif end == '2B':
        endInt = 2 
    elif end == '1B':
        endInt = 1 
    rmi.add_actual_bases_moved(endInt - startInt)
    

def adjust_rmi(entities, atbat):
    '''
    Adjust the RMI for a player for a single AtBat
    :param entities: a dictionary of players or teams
    :param atbat:
    '''
    plateEvent = PlateEventsEnum.OTHER
    if 'event' in atbat:
        plateEvent = PlateEventsEnum.from_mlb_event(atbat['event'])
        
    if plateEvent == PlateEventsEnum.RUNNER_OUT:
        return;
    
    entityId = None
    if args.team:
        entityId = atbat['batter_team']
    else:
        entityId = atbat['batter']
    
    rmi = None
    if entityId in entities:
        rmi = entities[entityId]
    else:
        if args.team:
            rmi = EntityBattingStats(entityId, entityId)
            entities[entityId] = rmi
        else:
            player = get_player(entityId)
            if player:
                rmi = EntityBattingStats(entityId, player['first'] + ' ' + player['last'])
                entities[entityId] = rmi
    
    rmi.add_plate_event(plateEvent);
                
    if rmi and 'runner' in atbat:
        runners = atbat['runner']
        if runners:
            for runner in runners:
                adjust_rmi_for_runner(rmi, runner)
            
def get_player(playerId):
    '''
    Retrieve a single player from the database, given an ID
    :param playerId: the AtBatID for the player
    '''
    playersCollection = db.players
    return playersCollection.find_one({"id":playerId})

def get_minimum_potential_bases(start, end):
    '''
    Gets the minimum number of potential bases required to be considered
    
    Currently this calculation determines how many game a given team has played within the range of dates provided
    and assumes that is roughly equal to the number of games each team has played. If there are less than 5 games,
    the return value is 0, otherwise it is 2 bases per game.
    
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
        return gameCount * 2
    else:
        return 0

def plot_linear_regression(x, xLabel, y, yLabel, start, end):
    '''
    Plot a linear regression with the r^2 listed in the chart
    :param x:
    :param xLabel:
    :param y:
    :param yLabel:
    '''
    
    slope, intercept, r_value, p_value, std_err = stats.linregress(x,y);
    print 'slope', slope
    print 'intercept', intercept
    print 'r^2', r_value**2
    
    rrrr = slope * x
    print 
    print rrrr
    line = intercept + slope * x
    pyplot.figure();
    pyplot.plot(x, y, 'o')
    #pyplot.plot(x, line, 'k-')

    pyplot.title("{} vs {}, {} to {}".format(xLabel, yLabel, start.date().isoformat(), end.date().isoformat()))
    pyplot.xlabel(xLabel)
    pyplot.ylabel(yLabel)
    
def show_distribution_chart(rmis, start, end):
    '''
    Shows a histogram to represent the frequency of occurrences of the different RMIs
    
    :param rmis: an array of RMI objects
    :param start: the starting date of the data, used for titles
    :param end: the ending date of the data, used for titles
    '''
    rmiList = []
    baList = []
    slgList = []
    obpList = []
    
    for rmiObj in rmis:
        rmiList.append(rmiObj.rmi)
        baList.append(rmiObj.get_batting_average())
        slgList.append(rmiObj.get_slugging_percentage())
        obpList.append(rmiObj.get_on_base_percentage())
        
    pyplot.figure();
    pyplot.hist(rmiList, bins=20, histtype='stepfilled', color='black', alpha=0.8)
    pyplot.title('RMI (Runners Moved Indicator) Distribution for {} through {}'.format(start.date().isoformat(), end.date().isoformat()))
    pyplot.xlabel('RMI')
    
    plot_linear_regression(rmiList, "RMI", baList, "Batting Average", start, end)
    plot_linear_regression(rmiList, "RMI", slgList, "Slugging Percentage", start, end)
    plot_linear_regression(rmiList, "RMI", obpList, "On Base Percentage", start, end)
    
    pyplot.show()

atBatsCollection = db.atbats

playersOrTeams = {}
atbatsWithRunners = atBatsCollection.find({'start_tfs_zulu':{'$gte':args.start, '$lt':args.end}})
for atbat in atbatsWithRunners:
    adjust_rmi(playersOrTeams, atbat)
    
allRMIs = playersOrTeams.values()
allRMIs.sort(key=lambda rmi: rmi.rmi, reverse=True)
    
minimumBases = get_minimum_potential_bases(args.start, args.end)
leagueRMI = RMI();

print ",Name,RMI,Actual Bases,Potential Bases,RBI,Hits,At-Bats,Batting Avg,OBP,SLG" 
    
i = 0
qualifyingRMIs = [] 
for rmi in allRMIs:
    leagueRMI.add_potential_bases_moved(rmi.potentialBases)
    leagueRMI.add_actual_bases_moved(rmi.actualBases)
    if rmi.potentialBases > minimumBases:
        i+=1
        print '{},{},{},{},{},{},{},{},{},{},{}'.format(i, rmi.name, rmi.rmi, rmi.actualBases, rmi.potentialBases, rmi.rbi, rmi.get_hits(), rmi.atBats, rmi.get_batting_average(), rmi.get_on_base_percentage(), rmi.get_slugging_percentage())
        qualifyingRMIs.append(rmi)

if args.stats:
    print ''
    print '#### STATS (*indicates computed against qualifiers) ####'
    print 'League RMI: {}'.format(leagueRMI.rmi)
    print 'Mean*: {}'.format(mean([rmiObj.rmi for rmiObj in qualifyingRMIs]))
    print 'Max*: {}'.format(max([rmiObj.rmi for rmiObj in qualifyingRMIs]))
    print 'Min*: {}'.format(min([rmiObj.rmi for rmiObj in qualifyingRMIs]))
    print 'STD*: {}'.format(std([rmiObj.rmi for rmiObj in qualifyingRMIs]))
    show_distribution_chart(qualifyingRMIs, args.start, args.end)
    