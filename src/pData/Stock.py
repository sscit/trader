'''
Created on 25.08.2012

@author: Stefan
'''
class CStock(object):

    def __init__(self, pWKN, pName, pFinanztreffId, pOnvistaId, isLargeCap, strBoerseFinanzenNet, strIndex):
        self.WKN = pWKN
        self.Name = pName
        self.FinanztreffId = pFinanztreffId
        self.OnvistaId = pOnvistaId
        '''
        falls marktkapitalisierung > X Mrd euro, dann zählt die firma als large cap, 
        z.b. BMW ist ein large cap
        '''
        self.isLargeCap = isLargeCap 
        
        self.strBoerseFinanzenNet = strBoerseFinanzenNet
        
        # Der Indexstring von Finanzen.net, in dem diese Aktie gelistet ist.
        self.strIndexFinanzenNet = strIndex
        