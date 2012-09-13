'''
Created on 25.08.2012

@author: Stefan

This indicator evaluates eigenkapitalquote for the current year
'''
from pIndicator.Indicator import CIndicator
from pDataInterface.Onvista import COnvista

class CIndicatorEigenkapital(CIndicator):

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
            ekr = self.__Onvista.getEigenkapitalquoteAktJahrProzent(stock)
            self.__StockDict[stock] = ekr
        
        result = 0
        
        if ekr > 25:
            result = 1
        elif (ekr >= 15 and ekr <= 25):
            result = 0
        else:
            result = -1
        
        
        return result
    