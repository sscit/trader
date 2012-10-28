'''
Created on 25.08.2012

@author: Stefan
'''
class CImporter(object):
    '''
    classdocs
    '''


    def __init__(self):
        self._strIndexFinanzenNet = "undef"
        pass
    
    def getName(self):
        return self._strIndexFinanzenNet
    
    def getListOfStocks(self):    
        pass
    
    def validateListeLaenge(self, Liste, l, caller):
        if len(Liste) == 0 or len(Liste) != l:
            raise NameError('Error: Importer ' + caller + ': Laenge Aktienliste: ' + str(len(Liste)) + ' != ' + str(l))    
        