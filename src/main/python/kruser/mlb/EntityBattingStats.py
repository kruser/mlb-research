'''
Created on Jul 6, 2013

@author: kruser
'''
from kruser.mlb.RMI import RMI;
from kruser.mlb.PlateEventsEnum import PlateEventsEnum

class EntityBattingStats(RMI):
    '''
    Used for calculating RMI and other batting stats on a single player or team
    '''

    def __init__(self, entityId, name):
        '''
        :param entityId: ID of this thing, either a playerId or team ID
        :param name: the name to display for this entity
        '''
        self.entityId = entityId
        self.name = name 
        self.rbi = 0
        self.atBats = 0
        self.singles = 0
        self.doubles = 0
        self.triples = 0
        self.homeruns = 0
        self.walks = 0
        self.hitByPitch = 0
        self.sacrifices = 0
        self.runs = 0
        super(EntityBattingStats, self).__init__()
        
    def add_rbi(self, rbi):
        self.rbi += rbi
        
    def add_runs(self, runs):
        self.runs += runs
        
    def add_plate_event(self, plateEvent):
        '''
        :param plateEvent: use PlateEventsEnum values for this
        '''
        if (plateEvent == PlateEventsEnum.SINGLE):
            self.singles += 1;
            self.atBats += 1;
        elif (plateEvent == PlateEventsEnum.DOUBLE):
            self.doubles += 1;
            self.atBats += 1;
        elif (plateEvent == PlateEventsEnum.TRIPLE):
            self.triples += 1;
            self.atBats += 1;
        elif (plateEvent == PlateEventsEnum.HOMERUN):
            self.homeruns += 1;
            self.atBats += 1;
        elif (plateEvent == PlateEventsEnum.OTHER):
            self.atBats += 1;
        elif (plateEvent == PlateEventsEnum.WALK or plateEvent == PlateEventsEnum.CATCHER_INTERFERENCE or plateEvent == PlateEventsEnum.INTENTIONAL_WALK):
            self.walks += 1;
        elif (plateEvent == PlateEventsEnum.HIT_BY_PITCH):
            self.hitByPitch += 1;
        elif (plateEvent == PlateEventsEnum.SACRIFICE):
            self.sacrifices += 1;
        
    def get_hits(self):
        return self.singles + self.doubles + self.triples + self.homeruns
    
    def get_batting_average(self):
        if self.atBats > 0:
            return float(self.get_hits()) / float(self.atBats)
        else:
            return 0.0

    def get_on_base_percentage(self):
        return float(self.get_hits() + self.walks + self.hitByPitch) / float(self.atBats + self.walks + self.hitByPitch + self.sacrifices)
    
    def get_slugging_percentage(self):
        if self.atBats > 0:
            return float(self.singles + self.doubles*2 + self.triples*3 + self.homeruns*4) / float(self.atBats)
        else:
            return 0.0
    