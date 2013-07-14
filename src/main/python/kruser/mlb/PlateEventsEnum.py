'''
Created on Jul 8, 2013

@author: kruser
'''
import re

class PlateEventsEnum(object):
    '''
    Contains constants that represent and enum of plate events, like a single, double, triple, etc.
    '''
    SINGLE = 1
    DOUBLE = 2
    TRIPLE = 3
    HOMERUN = 4
    INTENTIONAL_WALK = 5
    WALK = 6
    HIT_BY_PITCH = 7
    CATCHER_INTERFERENCE = 8
    SACRIFICE = 9
    RUNNER_OUT = 10
    OTHER = 11 # for outs, fielder's choice, etck
    
    @staticmethod
    def from_mlb_event(event):
        if not event:
            return PlateEventsEnum.OTHER
        if re.search('^single$', event, re.IGNORECASE):
            return PlateEventsEnum.SINGLE
        elif re.search('^double$', event, re.IGNORECASE):
            return PlateEventsEnum.DOUBLE
        elif re.search('^triple$', event, re.IGNORECASE):
            return PlateEventsEnum.TRIPLE
        elif re.search('home', event, re.IGNORECASE):
            return PlateEventsEnum.HOMERUN
        elif re.search('intent walk', event, re.IGNORECASE):
            return PlateEventsEnum.INTENTIONAL_WALK
        elif re.search('walk', event, re.IGNORECASE):
            return PlateEventsEnum.WALK
        elif re.search('hit by pitch', event, re.IGNORECASE):
            return PlateEventsEnum.HIT_BY_PITCH
        elif re.search('interference', event, re.IGNORECASE):
            return PlateEventsEnum.CATCHER_INTERFERENCE
        elif re.search('sac', event, re.IGNORECASE):
            return PlateEventsEnum.SACRIFICE
        elif re.search('runner out', event, re.IGNORECASE):
            return PlateEventsEnum.RUNNER_OUT
        else:
            return PlateEventsEnum.OTHER
        