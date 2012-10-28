'''
Created on 25.08.2012

@author: Stefan
'''

from pData.Stock import CStock
from pIndicator.Indicator import CIndicator 
from time import *

class CSlave(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        
    def run(self, Importer, listIndicator, Presenter):
        
        print "Starte Verarbeitung..."
        
        l = Importer.getListOfStocks()
        pointList = list()
        
        for stock in l:
            print "Starte Aktie: " + stock.Name
            summe = 0
            
            for indicator in listIndicator:
                print "Starte Indicator " + indicator.getName()
                t1 = clock()
                summe += indicator.getPoints(stock)
                t2 = clock()
                print "Dauer: " + str(t2-t1)
                
            pointList.append(summe)
            
            
        print "Verarbeitung ENDE ....."    
        print ""
        
        Presenter.printData(l, pointList, listIndicator, Importer)
        
        
        
        
        