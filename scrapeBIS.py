import time
import re
import requests
from bs4 import BeautifulSoup

def get_soup_from_BIS(baseURL, parameters, tries = 10, wait = 1):
    for i in range(tries):
        r = requests.get(baseURL,params = parameters)
        if (r.text.find('Visitor Prioritization') == -1 
            & r.text.find('NOT IN PROPERTY FILE') == -1) :
            return BeautifulSoup(r.text)
        time.sleep(wait)
    return BeautifulSoup('')
    
def get_property_profile(parameters, tries = 10, wait = 1):
    baseURL='http://a810-bisweb.nyc.gov/bisweb/PropertyProfileOverviewServlet'
    return get_soup_from_BIS(baseURL, parameters, tries, wait)
    
#Three primary BIS Profile query functions
def get_address_profile(boro, houseno, street, tries = 10, wait = 1):
    parameters = {'boro':boro,
                  'houseno':houseno,
                  'street':street}
    return get_property_profile(parameters, tries, wait)

def get_BBL_profile(boro, block, lot, tries = 10, wait = 1):
    parameters = {'boro':boro,
                  'block':block,
                  'lot':lot}
    return get_property_profile(parameters, tries, wait)
    
def get_BIN_profile(bin, tries = 10, wait = 1):
    parameters = {'bin':bin}
    return get_property_profile(parameters, tries, wait)
    
def get_DOB_data_from_soup(soup):
    landmarkStatus = ''
    crossStreets = ''
    buildingClass = ''
    if(soup):
        #get Landmark data
        precursor = soup.find_all('td', 
                                  text = re.compile('Landmark Status'))
        if precursor:
            landmarkStatus = precursor[0].find_next('td').text
        #get Cross Street data
        precursor = soup.find_all('td', 
                                  text = re.compile('Cross Street'))
        if precursor:
            crossStreets = precursor[0].find_next('td').text
        #get Building Class data
        precursor = soup.find_all('td', 
                                 text = re.compile('Building Classification'))
        if precursor:
            buildingClass = precursor[0].find_next('td').text
    return {'landmarkStatus':landmarkStatus,
            'crossStreets':crossStreets,
            'buildingClass':buildingClass}        
            