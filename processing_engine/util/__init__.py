import logging

withFile = False


def log_with_file(logWithFile=False):
    global withFile
    withFile = logWithFile


def get_logger():
    if withFile:
        logging.basicConfig(format='%(asctime)s - %(levelname)s : %(message)s', filename='main.log',
                            datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)
    else:
        logging.basicConfig(format='%(asctime)s - %(levelname)s : %(message)s',
                            datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)
    return logging.getLogger()


def bounding_box_from_tuple(tuple_of_bbox):
    bbox = [float(tuple_of_bbox[0][0].split("BOX")[1].split(",")[0].split(" ")[0].split("(")[1]),
            float(tuple_of_bbox[0][0].split("BOX")[1].split(",")[0].split(" ")[1]),
            float(tuple_of_bbox[0][0].split("BOX")[1].split(",")[1].split(" ")[0]),
            float(tuple_of_bbox[0][0].split("BOX")[1].split(",")[1].split(" ")[1].split(")")[0])]
    return bbox


def process_escape_character(data):
    if data is not None:
        return data.replace('\'', '\'\'')
    return None
