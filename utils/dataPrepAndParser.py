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
    This function needs to be cleaned up. It does what it is meant to, but it is slow
    and not built optimally. Plus, can probably use ascyio.gather() to run all possible
    years (i.e., inputData["idealDates"]) in parallel
    Also would like to get rid of hard coding variable columns below
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
        # writer = pd.ExcelWriter(dirname+'/weatherDataFor' + thisYear + '.xlsx', engine='xlsxwriter')
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
            # new_df_file = pd.DataFrame(textLineArray, columns=columns)
            # new_df_file.to_excel(writer, sheet_name=stationLabel)
        # writer.save()
        dictAllData[thisYear] = dictStations
        # if thisYear == '2018': dfWeaterData2018 = pd.read_excel(dirname+'/weatherDataFor2018.xlsx').drop(columns=['Unnamed: 0'])
    writeToJson(data=dictAllData, outFileName=dirname+'/weatherDataJSONObject.json')
    return dictAllData

##########################################################
def updateAndCleanUpDictionary(weatherDataDictObjectAll={}):
    """
    This function needs to be more generic... get rid of any hard coding with dates
    """
    ##########################################################
    unionList = list(set(list(weatherDataDictObjectAll['2018'].keys())).union(
        set(list(weatherDataDictObjectAll['2019'].keys())),
        set(list(weatherDataDictObjectAll['2020'].keys())),
        set(list(weatherDataDictObjectAll['2021'].keys())),
        set(list(weatherDataDictObjectAll['2022'].keys()))
    ))
    print("BEFORE")
    print(len(list(weatherDataDictObjectAll['2018'].keys())))
    weatherDataDictObjectAll['2018'] = {key: value for key, value in weatherDataDictObjectAll['2018'].items() if key in unionList}
    weatherDataDictObjectAll['2019'] = {key: value for key, value in weatherDataDictObjectAll['2019'].items() if key in unionList}
    weatherDataDictObjectAll['2020'] = {key: value for key, value in weatherDataDictObjectAll['2020'].items() if key in unionList}
    weatherDataDictObjectAll['2021'] = {key: value for key, value in weatherDataDictObjectAll['2021'].items() if key in unionList}
    weatherDataDictObjectAll['2022'] = {key: value for key, value in weatherDataDictObjectAll['2022'].items() if key in unionList}
    print("AFTER")
    print(len(list(weatherDataDictObjectAll['2018'].keys())))
    return weatherDataDictObjectAll

##########################################################
def getCleanedDataStructure(inputData={}, dirname=''):
    ######################################################
    if inputData["parseDataBool"] == 0:
        # dfWeaterData2018 = pd.read_excel(dirname + '/weatherDataFor2018.xlsx').drop(columns=['Unnamed: 0'])
        weatherDataDictObjectAll = json.loads(dirname + '/weatherDataJSONObject.json')
        print("Read in json object successfully")
    else:
        weatherDataDictObjectAll = parserFun(inputData=inputData, dirname=dirname)
        print("Successfully generated dictionary of all weather stations")
    ######################################################
    # sheetNames2018      = getExcelSheetNames(file_path=dirname + "/weatherDataFor2018.xlsx")
    # listOfDfsAllData    = [dfWeaterData2018]
    # listOfSheetNamesAll = [sheetNames2018]
    print()
    print(weatherDataDictObjectAll.keys())
    print()
    f
    ######################################################
    weatherDataDictObjectCleaned = updateAndCleanUpDictionary(weatherDataDictObjectAll=weatherDataDictObjectAll)
    print(weatherDataDictObjectCleaned.keys())
    ######################################################
    return weatherDataDictObjectCleaned

##########################################################
# def getExcelSheetNames(file_path='):
#     sheets = []
#     with zipfile.ZipFile(file_path, 'r') as zip_ref: xml = zip_ref.read("xl/workbook.xml").decode("utf-8")
#     for s_tag in  re.findall("<sheet [^>]*", xml):sheets.append(re.search('name="[^"]*', s_tag).group(0)[6:])
#     return sheets

##########################################################