'''
Created on 25.08.2012

@author: Stefan

This indicator evaluates Eigenkapitalrendite / RoE for the current year
'''
from pIndicator.Indicator import CIndicator
from pDataInterface.Onvista import COnvista

class CIndicatorEKR(CIndicator):

    def __init__(self):
        CIndicator.__init__(self)
        self.__Onvista = COnvista()
        self.__StockDict = dict()
        self._Name = str(self.__class__)
        
    def getPoints(self, stock):    
        
        '''
        check if this stock has already been processed
        '''
        
        if stock in self.__StockDict:
            ekr = self.__StockDict[stock]
        else:
            ekr = self.__Onvista.getEKRAktJahrProzent(stock)
            self.__StockDict[stock] = ekr
        
        result = 0
        
        if ekr == "NA":
            result = 0
            print "Warnung: " + self._Name + ": " + stock.Name + ": Wert nicht verfügbar"
        elif ekr > 20:
            result = 1
        elif (ekr >= 10 and ekr <= 20):
            result = 0
        else:
            result = -1
        
        
        return result
        
        
        
    