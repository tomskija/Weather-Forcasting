##########################################################
from utils.dataPrepAndParser import getCleanedDataStructure
from utils.utils import generateInputFileDict
from os.path import dirname
##########################################################
"""
Side project efforts:
    1. Keep working on and cleaning up getCleanedDataStructure() and all its calls before going any further
    2. Take all old Jupyter notebooks and place into a single project named like "Jupyter notebooks" and or
        "Graduate School Jupyter Notebook Projects" such that people know its old skills/work.
"""
##########################################################
def calculate(dirname=''):
    try:
        inputData = generateInputFileDict()
        weatherDataDictObjectCleaned = getCleanedDataStructure(inputData=inputData, dirname=dirname)
        # once have it in the format wanted, then can perform further data clean up
        # once clean up all the array data, then can perform analysis
        return weatherDataDictObjectCleaned
    except Exception as e:
        print(e)
        return e

##########################################################
if __name__ == '__main__':
    ######################################################
    weatherDataDictObjectCleaned = calculate(dirname=dirname(__file__) + '/Data')
    print("Completed Calculation")
    ######################################################