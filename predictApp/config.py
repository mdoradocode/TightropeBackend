#Ticketmaster API Keys
from boto.s3.connection import S3Connection

TICKETMASTER_API_KEY = S3Connection(os.environ['TICKETMASTER_API_KEY'])
TICKETMASTER_SECRET_KEY = S3Connection(os.environ['TICKETMASTER_SECRET_KEY'])