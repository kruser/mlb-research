'''
Created on Jul 3, 2013

@author: kruser
'''
class RMI(object):
    '''
    RMI is a container for runners moved statistic
    '''
    
    def __init__(self):
        '''
        Constructor
        '''
        self.potentialBases = 0;
        self.actualBases = 0;
        self.rmi = 0.0;
        
    def __str__( self ):
        return str(self.rmi) + ' - moved ' + str(self.actualBases) + ' of ' + str(self.potentialBases) + ' bases';
        
    def add_potential_bases_moved(self, potentialBases):
        '''
        :param potentialBases: integer for the number of potential bases moved
        '''
        self.potentialBases += potentialBases;
        self._calculate_rmi();
        
    def add_actual_bases_moved(self, actualBases):
        '''
        :param actualBases: integer for the number of actual bases moved
        '''
        self.actualBases += actualBases;
        self._calculate_rmi();
        
    def _calculate_rmi(self):
        '''
        Calculate the RMI and store it as a property on the object
        '''
        self.rmi = float(self.actualBases) / float(self.potentialBases);
        