##########################################################
import json

##########################################################
def writeToJson(data="", outFileName=''):
    jsonOut = json.dumps(data)#, indent=4, sort_keys=True)
    file1 = open(outFileName, "w")
    file1.write(jsonOut)
    file1.close()
    return

##########################################################
def generateInputFileDict():
    # for later, can create a sandox.py for inputs to map
    parseBoolean = 1
    inputData = {}
    inputData["parseDataBool"] = [0, 1][parseBoolean]
    if inputData["parseDataBool"] == 1:
        inputData["idealDates"] = [2018, 2019]# [2018, 2019, 2020, 2021, 2022] # user specify years
    return inputData

##########################################################