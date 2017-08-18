import logging

import Config

logging.basicConfig(
    level=logging.DEBUG,
    format="[%(asctime)s] %(name)s:%(levelname)s: %(message)s"
)

def debug(str):
    if Config.degbugMode:
        logging.debug(str);