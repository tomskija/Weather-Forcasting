##########################################################
import time
import numpy as np
import asyncio
from utils.dataPrepAndParser import getCleanedDataStructure
from utils.utils import generateInputFileDict
from os.path import dirname

##########################################################
async def calculate(dirname=''):
    try:
        inputData = generateInputFileDict()
        inputData["problemType"] = 'PROB01'
        startTime = time.time()
        weatherDataDictObjectCleaned, dfStations = await getCleanedDataStructure(inputData=inputData, dirname=dirname)
        if inputData["problemType"] == "PROB01":
            # This could be data generating further feature information (i.e., correlation/uncertainty/feature importance, etc. stats and plots)
            print("HERE 01")
        if inputData["problemType"] == "PROB02":
            # This could be geospatial modeling to get a 2D/3D map.
            # Could then use this map as ground truth data and predict other features away from stations and at various time stamps
            print("HERE 02")
        if inputData["problemType"] == "PROB03":
            # This could be Time Series Forecasting using standard ML approaches (could spice it up if want)
            print("HERE 03")
        if inputData["problemType"] == "PROB04":
            # At this point, could start using some cool methods, like physics informed NNs in a Bayesian framework. etc...
            print("HERE 04")
        endTime = time.time()
        print("The total numerical time to parse data is " + str(np.round(endTime - startTime, 5)) + " seconds")
        print("Completed Calculation")
    except Exception as e:
        print('\nError Message: ' + str(e) + '\n')
        return str(e)
    return weatherDataDictObjectCleaned, dfStations

##########################################################
async def main():
    ######################################################
    weatherDataDictObjectCleaned, dfStations = await calculate(dirname=dirname(__file__))
##########################################################

######################################################
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    print("Done")
######################################################