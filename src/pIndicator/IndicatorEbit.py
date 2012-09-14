'''
Created on 25.08.2012

@author: Stefan

This indicator evaluates EBIT marge for the current year
'''
from pIndicator.Indicator import CIndicator
from pDataInterface.Onvista import COnvista

class CIndicatorEbit(CIndicator):

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
            ekr= self.__StockDict[stock]
        else:    
            ekr = self.__Onvista.getEbitMargeAktJahrProzent(stock)
            self.__StockDict[stock] = ekr
        
        result = 0
        
        if ekr == "NA":
            result = 0
            print "Warnung: " + self._Name + ": " + stock.Name + ": Wert nicht verfügbar"
        elif ekr > 12:
            result = 1
        elif (ekr >= 6 and ekr <= 12):
            result = 0
        else:
            result = -1
        
        
        return result
    