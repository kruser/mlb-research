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
import pprint;

'''
@param players: hashtable of players stats, key is their playerId
@param atbat: an atbat object
'''
def adjustRmi(players, atbat):
    pprint.pprint(atbat);
    '''
    if players[atbat.batter]:
        players[atbat.batter] += 1;
    else:
        players[atbat.batter] = 1;
        '''

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
    adjustRmi(players, atbat);
    
print players;