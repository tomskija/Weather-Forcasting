##########################################################
import time
import numpy as np
import asyncio
from utils.dataPrepAndParser import getCleanedDataStructure
from utils.utils import generateInputFileDict
from os.path import dirname
##########################################################
"""
Think about updating repo to Weather Forcasting and Geospatial Modeling
For graduate school jupyter notebooks, think about finding more on personal laptop and push to show more

Outside working devconatiner and this continuosuly developing backend, create UI and get it production ready
    This would be its own repo, but getting working first, and then can make this more generic as needed
"""
##########################################################
async def calculate(dirname=''):
    try:
        inputData = generateInputFileDict()
        inputData["problemType"] = 'PROB01'
        startTime = time.time()
        weatherDataDictObjectCleaned = await getCleanedDataStructure(inputData=inputData, dirname=dirname)
        if inputData["problemType"] == "PROB01":
            # this will be like data clean up code and corrolation/uncertainity plots based on user chosen target feature
            print("HERE 01")
        if inputData["problemType"] == "PROB02":
            # this will be like geospatial modeling to get a 2D/3D map of chosen target feature... similar to thesis, could then
            # use this plus ground truth data (i.e.,  weather station data points) to predict value at various time stamps
            print("HERE 02")
        if inputData["problemType"] == "PROB03":
            # this could be time series forcasting using standard ML approaches (could spice it up if want)
            print("HERE 03")
        if inputData["problemType"] == "PROB04":
            # at this point, could start using some cool methods, like physics informed NNs in a Bayesian framework. etc...
            # i.e., expand problem types 4-10 etc. of various methods outside problem type 1-3
            print("HERE 04")
        endTime = time.time()
        print("The total numerical time to parse data is " + str(np.round(endTime - startTime, 5)) + " seconds")
        print("Completed Calculation")
    except Exception as e:
        print('\nError Message: ' + str(e) + '\n')
        return str(e)
    return weatherDataDictObjectCleaned

##########################################################
async def main():
    ######################################################
    weatherDataDictObjectCleaned = await calculate(dirname=dirname(__file__) + '/Data')
##########################################################

######################################################
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    print("Done")
######################################################