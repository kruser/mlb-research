'''
Created on Jul 3, 2013

@author: kruser
'''
class RMI:
    '''
    RMI is a container for runners moved statistic
    '''
    
    def __init__(self):
        '''
        Constructor
        '''
        self.potentialBases = 0;
        self.actualBases = 0;
        self.rbi = 0;
        
    def __str__( self ):
        return str(self.get_rmi()) + ' - moved ' + str(self.actualBases) + ' of ' + str(self.potentialBases) + ' bases';
        
    def add_potential_bases_moved(self, potentialBases):
        '''
        :param potentialBases: integer for the number of potential bases moved
        '''
        self.potentialBases += potentialBases;
        
    def add_actual_bases_moved(self, actualBases):
        '''
        :param actualBases: integer for the number of actual bases moved
        '''
        self.actualBases += actualBases;
        
    def add_rbi(self, rbis):
        '''
        Add RBI to the counter
        :param rbis: the number of RBI to increment
        '''
        self.rbi += rbis;
        
    def get_rmi(self):
        '''
        @return: returns a float for the RMI
        '''
        return float(self.actualBases) / float(self.potentialBases);
        
        