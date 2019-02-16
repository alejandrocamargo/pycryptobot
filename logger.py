import logging
import datetime

def configure_logger():
    # Logger
    log = logging.getLogger("Bot")
    log.setLevel(logging.INFO)

    # create file handler which logs even debug messages
    fh = logging.FileHandler(str(datetime.datetime.now())+ ".log")
    fh.setLevel(logging.DEBUG)

    # create console handler with a log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # create formatter and add it to the handlers
    formatter = logging.Formatter('( %(asctime)s )( %(levelname)s ): %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    # add the handlers to the logger
    log.addHandler(fh)
    log.addHandler(ch)
