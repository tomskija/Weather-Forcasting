##########################################################
import numpy as np
import pandas as pd
import warnings
import json
from urllib.request import urlopen
from bs4 import BeautifulSoup
from utils.utils import writeToJson
warnings.filterwarnings("ignore")

##########################################################
def parserFun(inputData={}, dirname=''):
    """
    This function needs to be cleaned up. It does what it is meant to at the moment, but it is slow
    and not built optimally. Plus, can probably use ascyio.gather() to run all possible years (i.e.,
    inputData["idealDates"]) in parallel. Also would like to get rid of hard coding variable columns below.
    """
    dfDict = {}
    for varTime in range(0, len(inputData["idealDates"])):
        url = "https://www.ncei.noaa.gov/pub/data/uscrn/products/hourly02/" + str(inputData["idealDates"][varTime]) + "/"
        html = urlopen(url).read()
        soup = BeautifulSoup(html, features="html.parser")
        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split(".txt"))
        text = ' '.join(chunk for chunk in chunks if chunk)
        text = text.split(' ')
        text = [x for x in text if x]  # Delete '' from list after parsing
        textL = []
        for s in text:
            if s.find('CRNH') != -1: textL.append(s + '.txt')
        dfDict[str(inputData["idealDates"][varTime])] = textL
    #######################################################
    dictAllData = {}
    for varTime in range(0, len(inputData["idealDates"])):
        thisYear = str(inputData["idealDates"][varTime])
        print(thisYear)
        dictStations = {}
        for j in range(0, len(dfDict[thisYear])):
            stationAtThisYear = dfDict[thisYear][j]
            url = "https://www.ncei.noaa.gov/pub/data/uscrn/products/hourly02/" + thisYear + "/" + stationAtThisYear
            html = urlopen(url).read()
            soup = BeautifulSoup(html, features="html.parser")
            text = soup.get_text()
            valSplit = text.split('\n')
            val = [x for x in valSplit if x]
            textLineList = []
            for k in range(0, len(val)):
                textLine = val[k].split(' ')
                textLine = [x for x in textLine if x]
                textLineList.append(textLine)
            textLineArray = np.array(textLineList).flatten().reshape(-1, 38)
            stationLabel = stationAtThisYear.replace('.txt', '').replace('CRNH0203-' + str(inputData["idealDates"][varTime]) + '-', '')
            if len(stationLabel) > 31: stationLabel = stationLabel[:31]
            print(j, stationLabel)
            columns = ["WBANNO", "UTC_DATE", "UTC_TIME", "LST_DATE", "LST_TIME", "CRX_VN", "LONGITUDE", "LATITUDE", "T_CALC", "T_HR_AVG", "T_MAX", "T_MIN", "P_CALC", "SOLARAD", "SOLARAD_FLAG", "SOLARAD_MAX", "SOLARAD_MAX_FLAG", "SOLARAD_MIN", "SOLARAD_MIN_FLAG", "SUR_TEMP_TYPE", "SUR_TEMP", "SUR_TEMP_FLAG", "SUR_TEMP_MAX", "SUR_TEMP_MAX_FLAG", "SUR_TEMP_MIN", "SUR_TEMP_MIN_FLAG", "RH_HR_AVG", "RH_HR_AVG_FLAG", "SOIL_MOISTURE_5", "SOIL_MOISTURE_10", "SOIL_MOISTURE_20", "SOIL_MOISTURE_50", "SOIL_MOISTURE_100", "SOIL_TEMP_5", "SOIL_TEMP_10", "SOIL_TEMP_20", "SOIL_TEMP_50", "SOIL_TEMP_100"]
            dataFrameTemp = pd.DataFrame(textLineArray, columns=columns)
            dictNew = {}
            for col in dataFrameTemp.columns: dictNew[col] = dataFrameTemp.loc[:, col].values.tolist()
            dictStations[stationLabel] = dictNew
        dictAllData[thisYear] = dictStations
    # Commenting this out for now as file is over 2GB in size when saved...
    # additionally, json object is not being saved formatted correctly to open later
    # writeToJson(data=dictAllData, outFileName=dirname+'/weatherDataJSONObject.json')
    print("Successfully generated dictionary of all weather stations and saved to JSON")
    return dictAllData

def updateAndCleanUpDictionary(weatherDataDictObjectAll={}):
    ''' Hard Coded Version'''
    # print("BEFORE")
    # print(len(list(weatherDataDictObjectAll['2018'].keys())))
    # unionList = list(set(list(weatherDataDictObjectAll['2018'].keys())).union(
    #     set(list(weatherDataDictObjectAll['2019'].keys())),
    #     set(list(weatherDataDictObjectAll['2020'].keys())),
    #     set(list(weatherDataDictObjectAll['2021'].keys())),
    #     set(list(weatherDataDictObjectAll['2022'].keys()))
    # ))
    # weatherDataDictObjectAll['2018'] = {key: value for key, value in weatherDataDictObjectAll['2018'].items() if key in unionList}
    # weatherDataDictObjectAll['2019'] = {key: value for key, value in weatherDataDictObjectAll['2019'].items() if key in unionList}
    # weatherDataDictObjectAll['2020'] = {key: value for key, value in weatherDataDictObjectAll['2020'].items() if key in unionList}
    # weatherDataDictObjectAll['2021'] = {key: value for key, value in weatherDataDictObjectAll['2021'].items() if key in unionList}
    # weatherDataDictObjectAll['2022'] = {key: value for key, value in weatherDataDictObjectAll['2022'].items() if key in unionList}
    # print("AFTER")
    # print(len(list(weatherDataDictObjectAll['2018'].keys())))
    ''' Generic Coded Version'''
    print(weatherDataDictObjectAll.keys())
    print("BEFORE")
    print(len(list(weatherDataDictObjectAll['2018'].keys())))
    # Get all keys from all nested dictionaries and create union
    ListOfAllkeys = []
    for nested_dict in weatherDataDictObjectAll.values():
        if isinstance(nested_dict, dict):
            ListOfAllkeys.extend(nested_dict.keys())
    unionList = list(set(ListOfAllkeys))
    print('len(ListOfAllkeys): ', len(ListOfAllkeys))
    print(ListOfAllkeys[:10])
    print('len(unionList):     ', len(unionList))
    print(unionList[:10])
    # Filter each nested dictionary to only contain keys in the union
    for key, nested_dict in weatherDataDictObjectAll.items():
        if isinstance(nested_dict, dict):
            weatherDataDictObjectAll[key] = {k: v for k, v in nested_dict.items() if k in unionList}
    print("AFTER")
    print(len(list(weatherDataDictObjectAll['2018'].keys())))
    print(weatherDataDictObjectAll.keys())
    return weatherDataDictObjectAll

##########################################################
def getCleanedDataStructure(inputData={}, dirname=''):
    ######################################################
    if inputData["parseDataBool"] == 0:
        weatherDataDictObjectAll = json.loads(dirname + '/weatherDataJSONObject.json')
    else:
        weatherDataDictObjectAll = parserFun(inputData=inputData, dirname=dirname)
    ######################################################
    # Once below function is debugged, place this in the parsing function above prior to saving final dictionary to a json
    weatherDataDictObjectCleaned = updateAndCleanUpDictionary(weatherDataDictObjectAll=weatherDataDictObjectAll)
    ######################################################
    return weatherDataDictObjectCleaned

##########################################################