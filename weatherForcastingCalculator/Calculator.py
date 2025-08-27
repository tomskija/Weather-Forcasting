##########################################################
from utils.dataPrepAndParser import getCleanedDataStructure
from utils.utils import generateInputFileDict
from os.path import dirname
##########################################################
"""
Current task efforts:
    1. Keep working on and cleaning up and debugging getCleanedDataStructure() and all its calls before going any further
    2. Once (1) is done and json is being saved or stored after parsing in correct formatted then can perform further data clean up
    3. Once clean up all the array data, then can perform analysis
    4. Then look into various ML methods or data analysis/interpolation techniques that can be used within project scope
"""
##########################################################
def calculate(dirname=''):
    try:
        inputData = generateInputFileDict()
        weatherDataDictObjectCleaned = getCleanedDataStructure(inputData=inputData, dirname=dirname)
    except Exception as e:
        print('\nError Message: ' + str(e) + '\n')
        return str(e)
    return weatherDataDictObjectCleaned

##########################################################
if __name__ == '__main__':
    ######################################################
    weatherDataDictObjectCleaned = calculate(dirname=dirname(__file__) + '/Data')
    print("Completed Calculation")
    ######################################################