'''
Created on Jul 6, 2013

@author: kruser
'''
from kruser.mlb.RMI import RMI;

class EntityRMI(RMI):
    '''
    Used for calculating RMI on a single player or team
    '''

    def __init__(self, entityId, name):
        '''
        :param entityId: ID of this thing, either a playerId or team ID
        :param name: the name to display for this entity
        '''
        self.entityId = entityId
        self.name = name 
        self.rbi = 0
        super(EntityRMI, self).__init__()
        
    def add_rbi(self, rbi):
        self.rbi += rbi
        