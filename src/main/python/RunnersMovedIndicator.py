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
from pymongo import MongoClient;
from datetime import datetime;
from kruser.mlb.RMI import RMI;
from pprint import pprint;

'''
@param players: hashtable of players stats, key is their playerId
@param atbat: an atbat object
'''


def adjust_rmi_for_runner(rmi, runner):
    '''
    Adjust the RMI given a single runner from the AtBat schema
    :param rmi: the starting RMI, can't be null
    :param runner: the runner data, can't be null
    '''
    start = runner['start'];
    startInt = 0;
    if start == '':
        return;
    elif start == '1B':
        startInt = 1; 
    elif start == '2B':
        startInt = 2; 
    elif start == '3B':
        startInt = 3; 
    rmi.add_potential_bases_moved(4 - startInt);
    
    end = runner['end'];
    endInt = 0;
    if end == '':
        endInt = 4; 
    elif end == '3B':
        endInt = 3; 
    elif end == '2B':
        endInt = 2; 
    elif end == '1B':
        endInt = 1; 
    rmi.add_actual_bases_moved(endInt - startInt);
    
    if 'rbi' in runner:
        rbi = runner['rbi'];
        if rbi == 'T':
            rmi.add_rbi(1);
    print rmi;

def adjust_rmi(players, atbat):
    '''
    Adjust the RMI for a player for a single AtBat
    :param players:
    :param atbat:
    '''
    batterId = atbat['batter'];
    
    rmi = RMI();
    if batterId in players:
        rmi = players[batterId];
    else:
        players[batterId] = rmi;
    
    if 'runner' in atbat:
        runners = atbat['runner'];
        for runner in runners:
            adjust_rmi_for_runner(rmi, runner);

# Setup the database connection
client = MongoClient();
db = client.mlbatbat;
atBatsCollection = db.atbats;

# Define the time range for our query
start = datetime(2013, 1, 1);
end = datetime(2014, 1, 1);

players = {};
atbatsWithRunners = atBatsCollection.find({"runner.start":{"$in":["1B","2B","3B"]}, "start_tfs_zulu":{"$gte":start, "$lt":end}});
for atbat in atbatsWithRunners:
    adjust_rmi(players, atbat);