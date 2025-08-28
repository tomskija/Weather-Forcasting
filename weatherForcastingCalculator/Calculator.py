##########################################################
import time
import numpy as np
from utils.dataPrepAndParser import getCleanedDataStructure
from utils.utils import generateInputFileDict
from os.path import dirname
##########################################################
"""
Showing the full stack effort (so will require to publish git images too):

Devcontainer Efforts:
    1. Get devcontainer working in a basic format through Docker
    2. See if any SQL scripts would be required or other efforts similar like using Node.js

Frontend UI Efforts:
    1. Can create a new repo for UI work that is simile and generic to show case CSS, HTML, and JavaScript skills

Backend Python Efforts for Project:
    1. Keep working on and cleaning up and debugging getCleanedDataStructure() and all its calls before going any further
    2. Once (1) is done and json is being saved or stored after parsing in correct formatted then can perform further data clean up
    3. Once clean up all the array data, then can perform analysis
    4. Then look into various ML methods or data analysis/interpolation techniques that can be used within project scope
"""
##########################################################
def calculate(dirname=''):
    # try:
    inputData = generateInputFileDict()
    startTime = time.time()
    weatherDataDictObjectCleaned = getCleanedDataStructure(inputData=inputData, dirname=dirname)
    endTime = time.time()
    print("The total numerical time to parse data is " + str(np.round(endTime - startTime, 5)) + " seconds")
    print("Completed Calculation")
    # except Exception as e:
    #     print('\nError Message: ' + str(e) + '\n')
    #     return str(e)
    return weatherDataDictObjectCleaned

##########################################################
if __name__ == '__main__':
    ######################################################
    weatherDataDictObjectCleaned = calculate(dirname=dirname(__file__) + '/Data')
    ######################################################