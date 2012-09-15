'''
Created on 25.08.2012

@author: Stefan

This indicator evaluates KBV for the current year
'''
from pIndicator.Indicator import CIndicator
from pDataInterface.FinanzenNet import CFinanzenNet

class CIndicatorKBV(CIndicator):

    def __init__(self):
        CIndicator.__init__(self)
        self.__FinanzenNet = CFinanzenNet()
        self.__StockDict = dict()
        self._Name = str(self.__class__)
        
    def getPoints(self, stock):    
        
        '''
        check if this stock has already been processed
        '''
        
        if stock in self.__StockDict:
            kbv= self.__StockDict[stock]
        else:    
            self.__FinanzenNet.parseFinanzenNet(stock)
            kbv = self.__FinanzenNet.KBV
            self.__StockDict[stock] = kbv
        
        result = 0
        
        if kbv == "NA":
            result = 0
            print "Warnung: " + self._Name + ": " + stock.Name + ": Wert nicht verfuegbar"
        elif kbv < 0.6:
            result = 2
        elif (kbv < 0.9 and kbv >= 0.6):
            result = 1
        elif (kbv < 1.3 and kbv >= 0.9):
            result = 0
        else:
            result = -1
        
        
        return result
    