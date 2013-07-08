'''
Created on Jul 6, 2013

@author: kruser
'''
from kruser.mlb.RMI import RMI;

class PlayerRMI(RMI):
    '''
    Used for calculating RMI on a single player
    '''

    def __init__(self, playerId, firstName, lastName):
        self.playerId = playerId
        self.firstName = firstName
        self.lastName = lastName
        self.rbi = 0
        super(PlayerRMI, self).__init__()
        
    def add_rbi(self, rbi):
        self.rbi += rbi
        