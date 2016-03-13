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

    def __init__(self, eventtransaction):
        self.transaction = eventtransaction

    def getAgencySubscribers(self):
        """
            Returns phone numbers of agencies to be contacted for a certain event
        """
        subscribers = []
        subClassEvent = self.getEventSubclassObject()
        if isinstance(subClassEvent, TerroristEvent):
            subscribers.extend(['SCDF', 'SAF'])
        elif isinstance(subClassEvent, TrafficEvent):
            subscribers.extend(['SCDF'])
        return [AGENCIES[key] for key in subscribers]

    def getEventSubclassObject(self):
        """
            Looks in the database for the subclass object to return
        """
        if TrafficEvent.objects.filter(event=self.transaction.event).exists():
            return TrafficEvent.objects.get(event=self.transaction.event)
        elif TerroristEvent.objects.filter(event=self.transaction.event).exists():
            return TerroristEvent.objects.get(event=self.transaction.event)
        else:
            return None

    def constructMessage(self):
        """
            Logic to construct SMS update for the agency
        """
        def getPrettyLocation(location):
            return '%f, %f' % (location.y, location.x)

        if self.transaction.transaction_type == 'CR':
            fmt = 'New {0} incident at {1}: {2} casualties and {3} injuries.'
        elif self.transaction.transaction_type == 'ED':
            fmt = 'Ongoing {0} incident at {1}: {2} casualties and {3} injuries.'
        else:
            return 'blank'
        subClassEvent = self.getEventSubclassObject()
        if isinstance(subClassEvent, TerroristEvent):
            self.eventtype = 'terrorist attack'
        elif isinstance(subClassEvent, TrafficEvent):
            self.eventtype = 'traffic'
        return fmt.format(self.eventtype, getPrettyLocation(self.transaction.event.location), self.transaction.event.num_casualties, self.transaction.event.num_injured)

    def dispatch(self):
        """
            Constructs the message and sends it to subscribed agencies
        """
        message = self.constructMessage()
        for agencyPhoneNumber in self.getAgencySubscribers():
            TwilioAPI().pushUpdate(message, agencyPhoneNumber)
