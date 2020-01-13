import logging

comArquivo = False

def logComArquivo(valor=False):
    global comArquivo
    comArquivo = valor

def getLogger():
    if comArquivo:
        logging.basicConfig(format='%(asctime)s - %(levelname)s : %(message)s', filename='main.log',
                            datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)
    else:
        logging.basicConfig(format='%(asctime)s - %(levelname)s : %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)
    return logging.getLogger()
