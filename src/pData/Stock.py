'''
Created on 25.08.2012

@author: Stefan
'''
class CStock(object):
   
    def __init__(self, pISIN=None, pName=None, pFinanzenNetId=None, pOnvistaId=None, isLargeCap=None, strBoerseFinanzenNet=None, strIndex=None):
        self.ISIN = pISIN
        self.Name = pName
        self.FinanzenNetId = pFinanzenNetId
        self.OnvistaId = pOnvistaId
        '''
        falls marktkapitalisierung > X Mrd euro, dann zaehlt die firma als large cap, 
        z.b. BMW ist ein large cap
        '''
        self.isLargeCap = isLargeCap 
        
        self.strBoerseFinanzenNet = strBoerseFinanzenNet
        
        # Der Indexstring von Finanzen.net, in dem diese Aktie gelistet ist.
        self.strIndexFinanzenNet = strIndex
        