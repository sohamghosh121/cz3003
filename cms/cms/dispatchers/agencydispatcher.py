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

    def get_agency_subscribers(self):
        """
            Returns phone numbers of agencies to be contacted for a certain event
        """
        subscribers = []
        sub_class_event = self.get_event_subclass_object()
        if isinstance(sub_class_event, TerroristEvent):
            subscribers.extend(['SCDF', 'SAF'])
        elif isinstance(sub_class_event, TrafficEvent):
            subscribers.extend(['SCDF'])
        return [AGENCIES[key] for key in subscribers]

    def get_event_subclass_object(self):
        """
            Looks in the database for the subclass object to return
        """
        if TrafficEvent.objects.filter(event=self.transaction.event).exists():
            return TrafficEvent.objects.get(event=self.transaction.event)
        elif TerroristEvent.objects.filter(event=self.transaction.event).exists():
            return TerroristEvent.objects.get(event=self.transaction.event)
        else:
            return None

    def construct_message(self):
        """
            Logic to construct SMS update for the agency
        """
        def get_pretty_location(location):
            return '%f, %f' % (location.y, location.x)

        if self.transaction.transaction_type == 'CR':
            fmt = 'New {0} incident at {1}: {2} casualties and {3} injuries.'
        elif self.transaction.transaction_type == 'ED':
            fmt = 'Ongoing {0} incident at {1}: {2} casualties and {3} injuries.'
        else:
            return 'blank'
        sub_class_event = self.get_event_subclass_object()
        if isinstance(sub_class_event, TerroristEvent):
            self.event_type = 'terrorist attack'
        elif isinstance(sub_class_event, TrafficEvent):
            self.event_type = 'traffic'
        return fmt.format(self.event_type, get_pretty_location(self.transaction.event.location), self.transaction.event.num_casualties, self.transaction.event.num_injured)

    def dispatch(self):
        """
            Constructs the message and sends it to subscribed agencies
        """
        message = self.construct_message()
        for agency_phone_number in self.get_agency_subscribers():
            TwilioAPI().push_update(message, agency_phone_number)
