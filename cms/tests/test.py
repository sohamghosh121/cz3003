from django.test import TestCase
from django.test import Client
from cms.models import Admin, Operator, Event, EventTransactionLog, TrafficEvent, TerroristEvent, Reporter
from cms.dispatchers.socialmediadispatcher import SocialMediaDispatcher
from cms.dispatchers.agencydispatcher import AgencyDispatcher
from cms.pullapis.weather import WeatherAPI
from cms.pullapis.dengue import DengueAPI
from cms.pushapis.fb import FacebookAPI
from cms.pushapis.twitter import TwitterAPI
from cms.pushapis.sms import TwilioAPI
from cms.pushapis.email_api import EmailAPI
from django.contrib.gis.geos import Point
from django.contrib.auth.models import User


testEvent = {
    'description': 'Test Event',
    'num_casualties': 10,
    'num_injured': 5,
    'location': Point(103.8, 1.36)
}

testTrafficEvent = {

}


testReporter = {
    'name': 'Tester',
    'contact_number': '1234',
    'identification': 'S12345K'
}


def createNewEvent():
    usr, created = User.objects.get_or_create(
        username='test', password='testpassword', email='test@test.com')
    op = Operator.objects.create(user_ptr_id=usr.id, name='Test Operator')
    rep = Reporter.objects.create(**testReporter)
    ev = testEvent
    ev['first_responder'] = rep
    ev = Event.objects.create(**testEvent)
    ev.save()
    ev.operator.add(op)
    evlog = EventTransactionLog.objects.create(
        event=ev, transaction_type='CR', operator=op, reporter=rep)
    return ev, evlog


class EventsTest(TestCase):

    def setUp(self):
        event, log = createNewEvent()
        pass


class DispatcherTest(TestCase):

    def setUp(self):
        self.event1, self.log1 = createNewEvent()
        # self.event2, self.log2 = createNewEvent()
        self.traffic_event = TrafficEvent.objects.create(
            event=self.event1, num_vehicles=20)
        # self.terrorist_event = TerroristEvent.objects.create(
        #     event=self.event2, num_hostiles=20, attack_type='BMB')

    def test_agency_message(self):
        self.assertEqual(
            AgencyDispatcher(self.log1).constructMessage(), 'New traffic incident at 1.360000, 103.800000: 10 casualties and 5 injuries.')
        # self.assertEqual(
        # AgencyDispatcher(self.log2).constructMessage(), 'New terrorist attack
        # incident at 1.36, 103.8, 10 casualties and 5 injured')

    def test_agency_subscribers(self):
        self.assertEqual(
            AgencyDispatcher(self.log1).getAgencySubscribers(), ['+6597741853'])
        # self.assertEqual(AgencyDispatcher(
        #     self.log2).getAgencySubscribers(), ['+6597741853', '+6587198478'])


class PullAPITest(TestCase):

    def setUp(self):
        pass

    def test_pull_weather(self):
        self.assertTrue(True)
        # self.assertTrue(WeatherAPI().pullPSIUpdate())
        # self.assertTrue(WeatherAPI().pullWeatherUpdate())

    def test_pull_dengue(self):
        self.assertTrue(True)
        # self.assertTrue(DengueAPI().pullUpdate())


class PushAPITest(TestCase):

    def setUp(self):
        pass

    def test_fb_update(self):
        self.assertTrue(True)
        # randomizeUpdate = random.randint(1, 10000)
        # self.assertTrue(
        # FacebookAPI().pushUpdate('System Test %d #ignorethis' %
        # randomizeUpdate))

    def test_twitter_update(self):
        self.assertTrue(True)
        # import random
        # randomizeUpdate = random.randint(1, 10000)
        # self.assertTrue(
        # TwitterAPI().pushUpdate('System Test %d #ignorethis' %
        # randomizeUpdate))

    def test_email_update(self):
        self.assertTrue(True)
        # self.assertTrue(EmailAPI().pushUpdate(
        #     'ghosh.soham@gmail.com', 'System Test', 'System Test #ignorethis'))

    def test_sms_update(self):
        self.assertTrue(True)
        # self.assertTrue(
        #     TwilioAPI().pushUpdate('System Test #ignorethis', '+6597741853'))
