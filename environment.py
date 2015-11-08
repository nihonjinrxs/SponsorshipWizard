LOGFILE = "sponsor_wizard.log"
FLASKPORT = 8000
DEBUG = True
SUPPORTEMAIL = "secretary@datacommunitydc.org"


# Application threads. A common general assumption is
# using 2 per available processor cores - to handle
# incoming requests using one and performing background
# operations using the other.
# THREADS_PER_PAGE = 2