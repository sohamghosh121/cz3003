from ..pushapis.sms import TwilioAPI
from ..models import TrafficEvent, TerroristEvent

AGENCIES = {
    'SAF': '+6587198478',
    'SCDF': '+6597741853'
}

import geocoder


class AgencyDispatcher:

    """
        Implements methods for dispatching SMS to Agencies when appropriate
    """

    def __init__(self, event, transaction):
        self.event = event
        self.transaction = transaction

    def getAgencySubscribers(self):
        """
            Returns phone numbers of agencies to be contacted for a certain event
        """
        subscribers = []
        if isinstance(self.event, TerroristEvent):
            subscribers.extend(['SCDF', 'SAF'])
        elif isinstance(self.event, TrafficEvent):
            subscribers.extend(['SCDF'])
        return [AGENCIES[key] for key in subscribers]

    def constructMessage(self):
        """
            Logic to construct SMS update for the agency
        """
        def getPrettyLocation(location):
            return '%f, %f' % (location.y, location.x)

        if self.transaction == 'NEW':
            fmt = 'New {0} incident at {1}, {2} casualties and {3} injuries.'
        elif self.transaction == 'EDIT':
            fmt = 'Ongoing {0} incident at {1}, {2} casualties and {3} injuries.'
        else:
            return 'blank'
        if isinstance(self.event, TerroristEvent):
            eventtype = 'terrorist attack'
        elif isinstance(self.event, TrafficEvent):
            eventtype = 'traffic'
        return fmt.format(eventtype, getPrettyLocation(self.event.event.location), self.event.event.num_casualties, self.event.event.num_injured)

    def dispatch(self):
        """
            Constructs the message and sends it to subscribed agencies
        """
        message = self.constructMessage()
        for agencyPhoneNumber in self.getAgencySubscribers():
            TwilioAPI().pushUpdate(message, agencyPhoneNumber)
