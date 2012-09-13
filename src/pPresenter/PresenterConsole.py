'''
Created on 13.09.2012

@author: Stefan

This presenter prints all stocks to the console
'''
from Presenter import CPresenter
from pDataInterface.FinanzenNet import CFinanzenNet
from pData.Stock import CStock

class CPresenterConsole(CPresenter):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        
    def printData(self, StockList, PointList):
        
        finanzenNet = CFinanzenNet()
        
        print "Aktie \t Punkte \t KBV"
        
        c = 0
        for i in StockList:
            print i.Name + " \t " + str(PointList[c]) + " \t\t " + str(finanzenNet.getKBV(i))  
            c =c + 1
        

if __name__ == '__main__':
        xx = CPresenterConsole()
        s = list()
        p = list()
        
        s.append(CStock("BASF11", "BASF", 59905, 34694526, 1, 'FSE', 'DAX'))
        p.append(2)
        
        xx.printData(s, p)
        
        
        
        