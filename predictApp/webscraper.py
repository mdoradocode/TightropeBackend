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
import predictApp.config
from datetime import datetime
from datetime import timedelta

def find_events(categories = '', city='Reno',  startDate = datetime.now().date(), endDate = datetime.now().date() + timedelta(days=7)):

    """
    Usage: find_events(categories = '{categories list}', city='{city name}')

    Must have a config file that specififes the ticketmaster_api_key.

    This may be shared upon request.

    """

    # Set up essential variables
    startDate = startDate.strftime("%Y-%m-%dT%H:%M:%SZ")
    endDate = endDate.strftime("%Y-%m-%dT%H:%M:%SZ")

    tm_client = ticketpy.ApiClient(predictApp.config.ticketmaster_api_key)

    pages = tm_client.events.find(
        classification_name=categories,
        city=city,
        start_date_time=startDate,
        end_date_time=endDate
    )
    events = []
    for page in pages:
        for event in page:
            events.append(event.json)

    return events
