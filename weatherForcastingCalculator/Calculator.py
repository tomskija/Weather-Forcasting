##########################################################
import time
import numpy as np
import logging
import asyncio
from utils.dataPrepAndParser import getCleanedDataStructure
from utils.utils import generateInputFileDict
from os.path import dirname

##########################################################
async def calculate(dirname=''):
    try:
        inputData = generateInputFileDict()
        startTime = time.time()
        weatherDataDictObjectCleaned = await getCleanedDataStructure(inputData=inputData, dirname=dirname)
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