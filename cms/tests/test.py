from django.test import TestCase
from django.test import Client
from cms.models import Admin, Operator, Event, EventTransactionLog, TrafficEvent, TerroristEvent, Reporter, CrisisTransactionLog
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


testReporter = {
    'name': 'Tester',
    'contact_number': '1234',
    'identification': 'S12345K'
}


def createNewEvent():
    usr, created = User.objects.get_or_create(
        username='test', password='testpassword', email='test@test.com')
    usr.save()
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


class AgencyDispatcherTest(TestCase):

    def setUp(self):
        self.event, self.log = createNewEvent()

    def test_agency_message_traffic(self):
        self.traffic_event = TrafficEvent.objects.create(
            event=self.event, num_vehicles=20)
        self.assertEqual(
            AgencyDispatcher(self.log).constructMessage(), 'New traffic incident at 1.360000, 103.800000: 10 casualties and 5 injuries.')
        self.traffic_event.delete()

    def test_agency_message_terrorist(self):
        self.terrorist_event = TerroristEvent.objects.create(
            event=self.event, num_hostiles=20, attack_type='BMB')
        self.assertEqual(
            AgencyDispatcher(self.log).constructMessage(), 'New terrorist attack incident at 1.360000, 103.800000: 10 casualties and 5 injuries.')

    def test_agency_subscribers_traffic(self):
        self.traffic_event = TrafficEvent.objects.create(
            event=self.event, num_vehicles=20)
        self.assertEqual(
            AgencyDispatcher(self.log).getAgencySubscribers(), ['+6597741853'])
        self.traffic_event.delete()

    def test_agency_subscribers_terrorist(self):
        self.terrorist_event = TerroristEvent.objects.create(
            event=self.event, num_hostiles=20, attack_type='BMB')
        self.assertEqual(AgencyDispatcher(
            self.log).getAgencySubscribers(), ['+6597741853', '+6587198478'])
        self.terrorist_event.delete()


class SocialDispatcherTest(TestCase):

    def setUp(self):
        self.usr, created = User.objects.get_or_create(
            username='test', password='testpassword', email='test@test.com')
        self.adm = Admin.objects.create(
            user_ptr_id=self.usr.id, name='Test Admin')
        self.crisisLog = CrisisTransactionLog.objects.create(
            new_crisis=4, admin=self.adm, district='Bishan')

    def test_social_dispatcher_message(self):
        self.assertEqual(SocialMediaDispatcher(self.crisisLog).constructMessage(
        ), 'Crisis level in Bishan has been changed to Level 4. Please take care.')


class PullAPITest(TestCase):

    def setUp(self):
        pass

    def test_pull_weather(self):
        self.assertTrue(WeatherAPI().pullPSIUpdate())
        self.assertTrue(WeatherAPI().pullWeatherUpdate())

    def test_pull_dengue(self):
        self.assertTrue(DengueAPI().pullUpdate())


class PushAPITest(TestCase):

    def setUp(self):
        pass

    def test_fb_update(self):
        randomizeUpdate = random.randint(1, 10000)
        self.assertTrue(
            FacebookAPI().pushUpdate('System Test %d #ignorethis' %
                                     randomizeUpdate))

    def test_twitter_update(self):
        import random
        randomizeUpdate = random.randint(1, 10000)
        self.assertTrue(
            TwitterAPI().pushUpdate('System Test %d #ignorethis' %
                                    randomizeUpdate))

    def test_email_update(self):
        self.assertTrue(EmailAPI().pushUpdate(
            'ghosh.soham@gmail.com', 'System Test', 'System Test #ignorethis'))

    def test_sms_update(self):
        self.assertTrue(
            TwilioAPI().pushUpdate('System Test #ignorethis', '+6597741853'))
