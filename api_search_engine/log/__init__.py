import logging


def get_logger(with_file=False):
    if with_file:
        logging.basicConfig(format='%(asctime)s - %(levelname)s : %(message)s', filename='main.log',
                            datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)
    else:
        logging.basicConfig(format='%(asctime)s - %(levelname)s : %(message)s',
                            datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)
    return logging.getLogger()
