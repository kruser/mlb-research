'''
Created on Jul 6, 2013

@author: kruser
'''
from kruser.mlb.RMI import RMI;

class TeamRMI(RMI):
    '''
    Used for calculating RMI on a team
    '''

    def __init__(self, team):
        self.team = team
        self.rbi = 0
        super(TeamRMI, self).__init__()
        
    def add_rbi(self, rbi):
        self.rbi += rbi
        