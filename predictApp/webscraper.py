"""

This is a webscraper that will find events in a user's city. The categories will hopefully be inputs from a user, and the city will be selected by the user.

If there are no categoires, don't worry about it. It should be fine.

This webscraper uses Ticketpy, a wrapper of the TicketMaster API, to find events near a user in the categories they like.

The Ticketpy library was created by Edward Wells and can be found here:
    https://github.com/arcward/ticketpy

This library can be installed using pip:
    pip install ticketpy

It utilizes the TicketMaster API, which can be found here:
    https://developer.ticketmaster.com/products-and-docs/apis/discovery/v2/

This was built by Cooper Flourens

"""

import ticketpy
import os
from datetime import datetime
from datetime import timedelta

#Use the following lines whenever pushing to the Git
#TICKETMASTER_API_KEY = os.environ['TICKETMASTER_API_KEY']
#TICKETMASTER_SECRET_KEY = os.environ['TICKETMASTER_SECRET_KEY']

#Use the following lines for local development
TICKETMASTER_API_KEY = 'dpffBCJurjKsU2MGMshICDYFMXLEbl9d'
TICKETMASTER_SECRET_KEY='16OzXMilxrP3uyIb'

def find_events(categories = '', city='Reno',  startDate = datetime.now().date(), endDate = datetime.now().date() + timedelta(days=7)):

    """
    Usage: find_events(categories = '{categories list}', city='{city name}')

    Must have a config file that specififes the ticketmaster_api_key.

    This may be shared upon request.

    """

    # Set up essential variables
    startDate = startDate.strftime("%Y-%m-%dT%H:%M:%SZ")
    endDate = endDate.strftime("%Y-%m-%dT%H:%M:%SZ")

    tm_client = ticketpy.ApiClient(TICKETMASTER_API_KEY)

    pages = tm_client.events.find(
        classification_name=categories,
        city=city,
        start_date_time=startDate,
        end_date_time=endDate
    )
    events = []
    for page in pages:
        for event in page:
            print(event)
            if event.local_start_time == None: continue
            start_time = datetime.strptime(event.local_start_date + "T" + event.local_start_time + "Z", "%Y-%m-%dT%H:%M:%SZ")
            end_time = start_time+timedelta(hours=3)
            formatted = {
                "EventName": event.name,
                "StartDate": start_time,
                "EndDate": end_time,
                "Location": event.venues[0].address,
                "EventType": 1,
                "StressLevel": 0,
                "Notes": event.json['url']
            }
            events.append(formatted)

    return events
