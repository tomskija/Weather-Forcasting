##########################################################
import numpy as np
import pandas as pd
import requests
import matplotlib.pyplot as plt

##########################################################
def getElevations(lat=0, lon=0):
    ######################################################
    try:
        url = f"https://api.open-elevation.com/api/v1/lookup"
        params = {'locations': f"{lat},{lon}"}
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            elevation = data['results'][0]['elevation']
            return float(elevation)
        return np.nan
    except Exception as e:
        print(f"Error getting elevation for {lat}, {lon}: {e}")
        return np.nan
    
##########################################################
def getElevationAndDataFrameOfDesiredWeatherStations(weatherDataDictObjectAll={}, dirname=''):
    ######################################################
    cityList              = []
    longitudeList         = []
    latitudeList          = []
    elevationList         = []
    ######################################################
    for i in range(0, len(list(weatherDataDictObjectAll))):
        city = list(weatherDataDictObjectAll)[i]
        longitude = np.float64(weatherDataDictObjectAll[city]['LONGITUDE'][0])
        latitude  = np.float64(weatherDataDictObjectAll[city]['LATITUDE'][0])
        elevation = getElevations(lat=latitude, lon=longitude)
        if (longitude >= -130): # i.e., stations not part of the continental US
            cityList.append(city)
            longitudeList.append(longitude)
            latitudeList.append(latitude)
            elevationList.append(elevation)
    ######################################################
    npArray = np.vstack([cityList, longitudeList, latitudeList, elevationList]).T
    dfStations = pd.DataFrame(npArray, columns=['City', 'Longitude', 'Latitude', 'Elevation'])
    ######################################################
    generatePlotOfContinentalUS(dfStations=dfStations, dirname=dirname)
    dfStations.to_csv(dirname + '/Data/Weather Stations Info.csv', index=False)
    ######################################################
    return dfStations

##########################################################
def generatePlotOfContinentalUS(dfStations=[], dirname=''):
    ######################################################
    plt.figure(figsize=(14, 8))
    cm = plt.cm.get_cmap('terrain')
    sc = plt.scatter(
        np.float64(dfStations['Longitude'].values.flatten()), 
        np.float64(dfStations['Latitude'].values.flatten()), 
        c=np.float64(dfStations['Elevation'].values.flatten()), 
        cmap=cm,
        s=50,
        alpha=0.8,
        edgecolors='black',
        linewidth=0.3,
    )
    ######################################################
    cbar = plt.colorbar(sc, label='Elevation (ft)', shrink=0.8, aspect=30)
    cbar.ax.tick_params(labelsize=10)
    ######################################################
    xticks = np.round(np.linspace(-130, -60, 20), 3).tolist()
    yticks = np.round(np.linspace(20, 60, 20), 3).tolist()
    plt.xlim([min(xticks), max(xticks)]) # Longitude
    plt.ylim([min(yticks), max(yticks)]) # Latitude
    plt.xticks(xticks, rotation=45)
    plt.yticks(yticks, rotation=45)
    plt.xlabel('Longitude (°W)', fontsize=12, fontweight='bold')
    plt.ylabel('Latitude (°N)', fontsize=12, fontweight='bold')
    plt.title('Weather Stations across Continental US\n(Colored by Elevation)', fontsize=14, fontweight='bold', pad=20)
    plt.grid(True, alpha=0.3, linestyle='--')
    plt.tight_layout()
    plt.savefig(dirname + '/Figures/Weather Stations Map.png', dpi=300, bbox_inches='tight')
    ######################################################

##########################################################
def replaceInvalidDataWithNaN(stationDict={}, keysList=[], i=0):
    try:
        valRawDataFloat = np.array(stationDict[keysList[i]]).flatten().astype(float)
        valCleanDataPartI = np.where((valRawDataFloat == -99.0) | (valRawDataFloat == -9999.0), np.nan, valRawDataFloat)
        stationDict[keysList[i]] = valCleanDataPartI
    except: # i.e., cannot convert valRawDataFloat to float
        stationDict[keysList[i]] = np.array(stationDict[keysList[i]]).flatten()
    return stationDict

##########################################################
def cleanData(weatherDataDictObjectAll={}, dirname=''):
    ######################################################
    # Initial Clean up of each data
    stationsKeysList = list(weatherDataDictObjectAll.keys())
    for j in range(0, len(stationsKeysList)):
        stationDict = weatherDataDictObjectAll[stationsKeysList[j]]
        keysList = list(stationDict.keys())
        for i in range(0, len(keysList)):
            # adding data cleaning functions here
            stationDict = replaceInvalidDataWithNaN(stationDict=stationDict, keysList=keysList, i=i)
        weatherDataDictObjectAll[stationsKeysList[j]] = stationDict
    ######################################################
    print("Done Cleaning")
    dfStations = getElevationAndDataFrameOfDesiredWeatherStations(weatherDataDictObjectAll=weatherDataDictObjectAll, dirname=dirname)
    print("Done Getting Unique Weather Station Info and Putting in DataFrame")
    return weatherDataDictObjectAll, dfStations
##########################################################