'''
Created on 25.08.2012

@author: Stefan

necessary packages:
- python 2.7
- installation of libxml2
-- download from http://stackoverflow.com/questions/3520826/installing-libxml2-on-python-2-7-windows
- installation of libxml2dom
-- http://mail.python.org/pipermail/xml-sig/2005-December/011407.html

'''
from pImport.ImporterDummy import CImporterDummy
from Slave import CSlave

from pIndicator.IndicatorEbit import CIndicatorEbit
from pIndicator.IndicatorEigenkapital import CIndicatorEigenkapital
from pIndicator.IndicatorEKR import CIndicatorEKR
from pIndicator.IndicatorKGV import CIndicatorKGV, CIndicatorKGVMean

if __name__ == '__main__':
    
    imp = CImporterDummy()
    sl = CSlave()
    
    listIndicator = list()
    #listIndicator.append( CIndicatorEbit() )
    #listIndicator.append( CIndicatorEigenkapital() )
    #listIndicator.append( CIndicatorEKR() )
    listIndicator.append( CIndicatorKGV() )
    #listIndicator.append( CIndicatorKGVMean() )
    
    sl.run(imp, listIndicator)
    
    
    '''
        TODO
       
        - nacheinander die indikatorklassen erstellen
        - auch ein interface fuer finanzen.net schreiben, fuer den POST kram
        
        - presenter schreiben
        - weitere importer schreiben
        
        - TESTS machen, welche alle indikatoren testen und die einzelnen interface klassen
        
        
        
        '''