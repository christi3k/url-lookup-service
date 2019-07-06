import logging

# set up logging

# create new logger with library's name
logger = logging.getLogger(__package__)

# set null handler
logger.addHandler(logging.NullHandler())

def set_file_logger(name=__package__, level=logging.DEBUG, format_string=None):

    logger = logging.getLogger(name)

    # set logging level
    logger.setLevel(level)

    if format_string is None:
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', '%m/%d/%Y %I:%M:%S %p')
    else:
        formatter = format_string

    # create a fileHandler
    fileHandler = logging.FileHandler(filename=__package__+'.log')
    fileHandler.setLevel(logging.DEBUG)
    fileHandler.setFormatter(formatter)
    logger.addHandler(fileHandler)

    logger.debug('file handler added to logging')

