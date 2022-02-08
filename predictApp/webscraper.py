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
import config
from datetime import datetime
from datetime import timedelta

def find_events(categories = '', city='Reno'):

    """
    Usage: find_events(categories = '{categories list}', city='{city name}')

    Must have a config file that specififes the ticketmaster_api_key.

    This may be shared upon request.

    """

    # Set up essential variables
    currentDate = datetime.now()
    endDate = datetime.now() + timedelta(days=8)
    currentDate = currentDate.strftime("%Y-%m-%dT%H:%M:%SZ")
    endDate = endDate.strftime("%Y-%m-%dT%H:%M:%SZ")

    tm_client = ticketpy.ApiClient(config.ticketmaster_api_key)
    

    pages = tm_client.events.find(
        classification_name=categories,
        city=city,
        start_date_time=currentDate,
        end_date_time=endDate
    )

    for page in pages:
        for event in page:
            print(event.name)
            print(event.local_start_time)
    return pages

find_events()