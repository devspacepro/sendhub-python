# imports for dynamic constants
from logging import DEBUG, INFO
import platform

#------------------
# GLOBAL DEFAULTS
#------------------

DEFAULT_SERVER              = 'https://api.sendhub.com'
DEFAULT_VERSION             = 'v1'   # TODO: support dynamic version
RECORD_LIMIT                = 5000
MAX_API_RETRIES             = 1
DISABLE_API_RETRIES         = False  # disable during testing

#------------------
# LOGGING
#------------------

# whether or not to also log to stdout (will print
# a great deal if log level is DEBUG)
LOG_STDOUT                  = False

# location of file name to log to
LOG_FILE_LINUX              = '/tmp/sendhub.log'
LOG_FILE_WINDOWS            = r'C:\sendhub.log'

# log level, use DEBUG to see HTTP requests and 
# responses, and use INFO to see to just see
# method calls
LOG_LEVEL                   = DEBUG

#------------------
# TESTING
#------------------

# test api settings
TEST_USER                   = '5107551478'
TEST_KEY                    = 'e4a7247176c1ef1188a105c907e6a295b15a944d'
TEST_SERVER                 = DEFAULT_SERVER
TEST_VERSION                = DEFAULT_VERSION

# flag whether to cleanup test data
TEST_CLEANUP_PRE            = False
TEST_CLEANUP_POST           = False

#------------------
# URLS
#------------------

URL_INBOX                   = 'inbox'
URL_MESSAGES                = 'messages'
URL_THREADS                 = 'threads'
#------------------
# DYNAMIC SETTINGS
#------------------

# set log based on platform
if platform.system() == 'Windows':
    LOG_FILE = LOG_FILE_WINDOWS
else:
    LOG_FILE = LOG_FILE_LINUX
    