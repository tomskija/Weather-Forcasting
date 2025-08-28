##########################################################
import json
import numpy as np

##########################################################
class NumpyEncoder(json.JSONEncoder):
    """Custom JSON encoder for numpy data types"""
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super().default(obj)

##########################################################
def writeToJson(data="", outFileName=''):
    # 1.3GB atm with parallized vs. 2GB... so something wrong with parallel parser
    jsonOut = json.dumps(data, cls=NumpyEncoder) # indent=2, ensure_ascii=False, sort_keys=True)
    file1 = open(outFileName, "w")
    file1.write(jsonOut)
    file1.close()
    return

##########################################################
def generateInputFileDict():
    # for later, can create a sandox.py for inputs to map
    inputData = {}
    inputData["booleanRunSeriesVsParallel"] = 0
    inputData["parseDataBool"] = [0, 1][1]
    if inputData["parseDataBool"] == 1:
        inputData["idealDates"] = [2018, 2019, 2020, 2021, 2022] # user specify years
        if inputData["booleanRunSeriesVsParallel"] == 0:
            inputData["batchSize"] = 10
    return inputData

##########################################################