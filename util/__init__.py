import logging

withFile = False

def logWithFile(logWithFile=False):
    global withFile
    withFile = logWithFile

def getLogger():
    if withFile:
        logging.basicConfig(format='%(asctime)s - %(levelname)s : %(message)s', filename='main.log',
                            datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)
    else:
        logging.basicConfig(format='%(asctime)s - %(levelname)s : %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)
    return logging.getLogger()
