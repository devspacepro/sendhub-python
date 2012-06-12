import logging
import constants

'''

Setup basic logging mechanism.  This can easily be overridden
by the calling class to pipe logging to a custom location

'''


log = logging.getLogger("sendhub")
log.setLevel(constants.LOG_LEVEL)

# setup formatter
formatter = logging.Formatter("%(levelname)s %(asctime)s %(message)s")

# setup optional stdout logging
if constants.LOG_STDOUT:
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    log.addHandler(handler)

# setup file log
handler = logging.FileHandler(constants.LOG_FILE)
handler.setFormatter(formatter)
log.addHandler(handler)