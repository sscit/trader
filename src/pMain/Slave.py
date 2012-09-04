'''
Created on 25.08.2012

@author: Stefan
'''

from pData.Stock import CStock
from pIndicator.Indicator import CIndicator 

class CSlave(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        
    def run(self, listImporter, listIndicator):
        l = listImporter.getListOfStocks()
        
        for stock in l:
            
            print stock.Name
            summe = 0
            
            for indicator in listIndicator:
                summe += indicator.getPoints(stock)
                
            print summe
        
        
        
        
        