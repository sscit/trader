'''
Created on 25.08.2012

@author: Stefan

necessary packages:
- python 2.7
- installation of libxml2
-- download from http://stackoverflow.com/questions/3520826/installing-libxml2-on-python-2-7-windows
- installation of libxml2dom
-- http://mail.python.org/pipermail/xml-sig/2005-December/011407.html
- installation of xlwt 
-- http://www.python-excel.org/

'''
from pImport.ImporterTECDAX import *
from pImport.ImporterDAX import *
from pImport.ImporterMDAX import *
from pImport.ImporterATX import *
from pImport.ImporterEuroStoxx import CImporterEuroStoxx50
from Slave import CSlave
from pPresenter.PresenterConsole import CPresenterConsole
from pPresenter.PresenterExcel import CPresenterExcel

from pIndicator.Indicator3MonatsReversal import CIndicator3MonatsReversal
from pIndicator.IndicatorEbit import CIndicatorEbit
from pIndicator.IndicatorEigenkapital import CIndicatorEigenkapital
from pIndicator.IndicatorEKR import CIndicatorEKR
from pIndicator.IndicatorKBV import CIndicatorKBV
from pIndicator.IndicatorKGV import CIndicatorKGV, CIndicatorKGVMean
from pIndicator.IndicatorKursmomentum import CIndicatorKursMomentum
from pIndicator.IndicatorKursVor12M import CIndicatorKursVor12M
from pIndicator.IndicatorKursVor6M import CIndicatorKursVor6M

if __name__ == '__main__':
    
    #imp = CImporterATX()
    imp = CImporterMDAX()
    present = CPresenterExcel()
    sl = CSlave()
    
    listIndicator = list()
    listIndicator.append( CIndicator3MonatsReversal() )
    listIndicator.append( CIndicatorEbit() )
    listIndicator.append( CIndicatorEigenkapital() )
    listIndicator.append( CIndicatorEKR() )
    listIndicator.append( CIndicatorKBV() )
    listIndicator.append( CIndicatorKGV() )
    listIndicator.append( CIndicatorKGVMean() )
    listIndicator.append ( CIndicatorKursMomentum() )
    listIndicator.append ( CIndicatorKursVor12M() )
    listIndicator.append ( CIndicatorKursVor6M() )
    
    sl.run(imp, listIndicator, present)
    
    
    '''
        TODO
              
        - presenter excel noch tunen, mit farben oder so
        - restliche indikatoren machen
        . auch andere indizes mit reinbringen
        -- fuer FTSE100 einfach folgende url nehmen http://www.finanzen.net/index/FTSE_100@intpagenr_2 und z.b. alles hinter dem "@"
            in irngend einer form in ein array packe? damit N seiten abgerufen werden beim einlesen
        - mal alle indikatoren durchgehen und genau dokumentieren und verstehen, was die jetzt eigentlich machen
        
        - TESTS machen, welche alle indikatoren testen und die einzelnen interface klassen
        
        
        
        '''