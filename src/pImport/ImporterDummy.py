'''
Created on 25.08.2012

@author: Stefan
'''
from Importer import CImporter
from pData.Stock import CStock

class CImporterDummy(CImporter):

    def __init__(self):
        self.__StockList = list()
        
        self.__StockList.append( CStock("BASF11", "BASF", 59905, 34694526, 1, 'FSE', 'DAX') )
        self.__StockList.append( CStock("DE000BAY0017", "Bayer", 689, 25272187, 1, 'FSE', 'DAX') )
        
        self._strIndexFinanzenNet = "DummyListe"
        
    def getListOfStocks(self):
        return self.__StockList    