'''
Created on Jul 30, 2013

@author: kruser
'''
from numpy import mean
from numpy import std

class HitAngleAggregator(object):
    '''
    The HitAngleAggregator accumulates hit angles, pitch positions and expected hit angles to score
    the hitters ability to "go with the pitch".
    '''

    def __init__(self, batterId):
        '''
        Constructor
        '''
        self.batterId = batterId
        self.angleDifferences = [] 
    
    def add_hit_ball(self, hand, hitAngle, expectedAngle):
        '''
        Add a single hit ball to the aggregator for this batter
        :param hand: L or R
        :param hitAngle: the angle of the hit on the field, where the field is 45 degrees at the left field foul line and 135 degrees at the right field foul line
        :param expectedAngle: the angle we expected the ball to be hit
        :return the angle difference
        '''
        angleDifference = 0
        if hand == 'L':
            angleDifference = hitAngle - expectedAngle
        else:
            angleDifference = expectedAngle - hitAngle
        self.angleDifferences.append(angleDifference)
        return angleDifference
    
    def get_score(self):
        '''
        Gets the overall score for this batter, based on all hits added to the aggregator.
        '''
        return mean([abs(diff) for diff in self.angleDifferences])
    
    def get_mean(self):
        '''
        similar to get_score, but gets the true mean instead, so positive (right) and
        negative (left) angles will balance each other out. This is useful for finding
        the batters tendencies.
        '''
        return mean(self.angleDifferences)
    
    def get_std(self):
        '''
        Get the standard deviation of the values
        '''
        return std(self.angleDifferences)
    
    def get_hit_count(self):
        return len(self.angleDifferences)
    