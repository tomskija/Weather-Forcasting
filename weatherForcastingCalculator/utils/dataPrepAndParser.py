##########################################################
import numpy as np
import pandas as pd
import warnings
import json
import asyncio
import aiohttp
from urllib.request import urlopen
from bs4 import BeautifulSoup
from utils.utils import writeToJson
warnings.filterwarnings("ignore")

##########################################################
def updateAndCleanUpDictionaryWithStats(weatherDataDictObjectAll={}):    
    # Get all years that contain dictionaries
    yearKeys = [str(year) for year in weatherDataDictObjectAll.keys() if isinstance(weatherDataDictObjectAll.get(str(year)), dict)]    
    # Collect statistics before cleanup
    original_stats = {}
    all_stations = set()
    for year in yearKeys:
        stations = set(weatherDataDictObjectAll[year].keys())
        original_stats[year] = len(stations)
        all_stations.update(stations)
    # Find intersection of all station keys
    station_sets     = [set(weatherDataDictObjectAll[year].keys()) for year in yearKeys]
    common_stations  = set.intersection(*station_sets) if station_sets else set()
    removed_stations = all_stations - common_stations
    # Filter each year to only include common stations
    for year in yearKeys:
        weatherDataDictObjectAll[year] = {station: data for station, data in weatherDataDictObjectAll[year].items() if station in common_stations}
    # Prepare statistics
    statsDict = {
        'Years Processed:              ': yearKeys,
        'Original Station Counts:      ': original_stats,
        'Total Unique Stations:        ': len(all_stations),
        'Common Stations Count:        ': len(common_stations),
        # 'Common Stations:              ': sorted(common_stations),
        'Removed Stations Count:       ': len(removed_stations),
        'Removed Stations:             ': sorted(removed_stations),
        'Final Station Count per Year: ': len(common_stations)
    }
    print("\n" + "="*60)
    print("Parsed Weather Data into Dictionary with Statistics:")
    listOfKeys = list(statsDict.keys())
    for i in range(0, len(listOfKeys)):
        print(listOfKeys[i], statsDict[listOfKeys[i]])
    print("="*60)
    return weatherDataDictObjectAll

##########################################################
async def fetchURLContent(session='', url=''):
    """Fetch content from URL asynchronously"""
    # try:
    async with session.get(url) as response:
        if response.status == 200:
            return await response.text()
        else:
            print("Failed to fetch:", url)
            print("Status:", response.status)
            return
    # except Exception as e:
    #     print("Error fetching:", url, e)
    #     return

##########################################################
async def getStationFiles(session='', year=''):
    """Get list of station files for a given year"""
    url = f"https://www.ncei.noaa.gov/pub/data/uscrn/products/hourly02/{year}/"
    html_content = await fetchURLContent(session=session, url=url)    
    soup = BeautifulSoup(html_content, features="html.parser")
    text = soup.get_text()
    # Extract .txt files containing 'CRNH'
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split(".txt"))
    text_parts = ' '.join(chunk for chunk in chunks if chunk).split(' ')
    text_parts = [x for x in text_parts if x]  # Remove empty strings
    station_files = [s + '.txt' for s in text_parts if 'CRNH' in s]
    return station_files

##########################################################
async def processStationData(session='', year='', stationFile=''):
    """Process individual station data file"""
    url = f"https://www.ncei.noaa.gov/pub/data/uscrn/products/hourly02/{year}/{stationFile}"
    html_content = await fetchURLContent(session=session, url=url)    
    soup = BeautifulSoup(html_content, features="html.parser")
    text = soup.get_text()
    # Parse data lines
    val_split = text.split('\n')
    val = [x for x in val_split if x]
    text_line_list = []
    for line in val:
        text_line = line.split(' ')
        text_line = [x for x in text_line if x]
        if text_line:  # Only add non-empty lines
            text_line_list.append(text_line)    
    # Define columns as a constant to avoid hardcoding
    weatherDataColumns = [
        "WBANNO", "UTC_DATE", "UTC_TIME", "LST_DATE", "LST_TIME", "CRX_VN", "LONGITUDE", "LATITUDE", "T_CALC", "T_HR_AVG", \
        "T_MAX", "T_MIN", "P_CALC", "SOLARAD", "SOLARAD_FLAG", "SOLARAD_MAX", "SOLARAD_MAX_FLAG", "SOLARAD_MIN", "SOLARAD_MIN_FLAG", \
        "SUR_TEMP_TYPE", "SUR_TEMP", "SUR_TEMP_FLAG", "SUR_TEMP_MAX", "SUR_TEMP_MAX_FLAG", "SUR_TEMP_MIN", "SUR_TEMP_MIN_FLAG", \
        "RH_HR_AVG", "RH_HR_AVG_FLAG", "SOIL_MOISTURE_5", "SOIL_MOISTURE_10", "SOIL_MOISTURE_20", "SOIL_MOISTURE_50", \
        "SOIL_MOISTURE_100", "SOIL_TEMP_5", "SOIL_TEMP_10", "SOIL_TEMP_20", "SOIL_TEMP_50", "SOIL_TEMP_100"
    ]
    # Convert to numpy array and reshape
    textLineArray = np.array(text_line_list).flatten().reshape(-1, len(weatherDataColumns))
    # Create station label
    stationLabel = (stationFile.replace('.txt', '').replace(f'CRNH0203-{year}-', ''))
    if len(stationLabel) > 31: stationLabel = stationLabel[:31]
    # Create DataFrame and convert to JSON-serializable format
    dfTemp = pd.DataFrame(textLineArray, columns=weatherDataColumns)
    # Convert DataFrame to dictionary with JSON-serializable values
    stationData = {}
    for col in dfTemp.columns:
        # Convert numpy arrays to lists for JSON serialization
        column_data = dfTemp[col].values.tolist()
        # Ensure all values are JSON serializable
        stationData[col] = [str(val) if val is not None else None for val in column_data]
    return stationLabel, stationData

##########################################################
async def processYearData(session='', year=''):
    """ Process all station data for a given year """
    print("Processing year:", year)
    # Get station files for this year
    stationFiles = await getStationFiles(session=session, year=year)
    # Process all stations for this year in parallel
    tasks = [processStationData(session=session, year=year, stationFile=stationFile) for stationFile in stationFiles]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    # Collect valid results
    yearData = {}
    for i, result in enumerate(results):
        if isinstance(result, Exception):
            print("Exception processing station:", stationFiles[i], result)
            continue
        station_label, station_data = result
        if station_label and station_data:
            yearData[station_label] = station_data
            print("Processed station:", station_label)
    return yearData

##########################################################
async def parserFunParallelized(inputData={}, dirname=''):
    years = [str(year) for year in inputData["idealDates"]]
    # Create aiohttp session with connection limits
    connector = aiohttp.TCPConnector(limit=10, limit_per_host=5)
    timeout   = aiohttp.ClientTimeout(total=300)  # 5 minute timeout
    async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
        # Process all years in parallel
        tasks = [processYearData(session=session, year=year) for year in years]
        yearResults = await asyncio.gather(*tasks, return_exceptions=True)
        # Combine results
        dictAllData = {}
        for i, result in enumerate(yearResults):
            dictAllData[years[i]] = result
    # Save to JSON if dirname provided
    dictAllData = updateAndCleanUpDictionaryWithStats(weatherDataDictObjectAll=dictAllData)
    writeToJson(data=dictAllData, outFileName=dirname+'/weatherDataJSONObject.json')
    print("Successfully generated dictionary of all weather stations")
    return dictAllData

##########################################################
def parserFunSlowAndInSeries(inputData={}, dirname=''):
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
    dictAllData = updateAndCleanUpDictionaryWithStats(weatherDataDictObjectAll=dictAllData)
    writeToJson(data=dictAllData, outFileName=dirname+'/weatherDataJSONObject.json')
    print("Successfully generated dictionary of all weather stations and saved to JSON")
    return dictAllData
    
##########################################################
async def getCleanedDataStructure(inputData={}, dirname=''):
    ######################################################
    if inputData["parseDataBool"] == 0:
        with open(dirname + '/weatherDataJSONObject.json', 'r') as f:
            weatherDataDictObjectAll = json.load(f)
    else:
        if inputData["booleanRunSeriesVsParallel"] == 1: # parserFunSlowAndInSeries took apx 800 seconds to complete
            weatherDataDictObjectAll = parserFunSlowAndInSeries(inputData=inputData, dirname=dirname)
        elif inputData["booleanRunSeriesVsParallel"] == 0: # parserFunParallelized    took apx 400 seconds to complete
            weatherDataDictObjectAll = await parserFunParallelized(inputData=inputData, dirname=dirname)
    ######################################################
    """
    Correct Results Coming from series code
    ============================================================
    Parsed Weather Data into Dictionary with Statistics:
    Years Processed:               ['2018', '2019', '2020', '2021', '2022']
    Original Station Counts:       {'2018': 157, '2019': 157, '2020': 157, '2021': 157, '2022': 157}
    Total Unique Stations:         158
    Common Stations Count:         156
    Removed Stations Count:        2
    Removed Stations:              ['AK_Aleknagik_1_NNE', 'SA_Tiksi_4_SSE']
    Final Station Count per Year:  156
    ============================================================
    """
    return weatherDataDictObjectAll

##########################################################