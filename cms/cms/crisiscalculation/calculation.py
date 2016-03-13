from ..models import TrafficEvent, TerroristEvent, Singapore, Districts
from ..dispatchers.pmodispatcher import PMODispatcher


class CrisisCalculator:
    SEVERITY_THRESHOLD_BINS = [100, 150, 300, 500, 750, 1000]

    def eventSeverityCalculator(self, event):
        severity = 20 * event.event.num_casualties + \
            10 * event.event.num_injured
        if isinstance(event, TrafficEvent):
            severity += 8 * event.num_vehicles
        elif isinstance(event, TerroristEvent):
            severity += 20 * event.num_hostiles
        else:
            return 0.0
        return severity

    def getCrisisLevel(self, severity):
        for i in range(len(self.SEVERITY_THRESHOLD_BINS)):
            if severity < self.SEVERITY_THRESHOLD_BINS[i]:
                return i
        return 5

    def getEvents(self, geom):
        events = []
        events.extend(TrafficEvent.objects.filter(event__location__within=geom))
        events.extend(
            TerroristEvent.objects.filter(event__location__within=geom))
        return events

    def checkCrisis(self):
        singapore = Singapore.objects.all()
        new_crises = {}
        for singaporeObj in singapore:
            totalSeverity = sum([self.eventSeverityCalculator(event)
                                 for event in self.getEvents(singaporeObj.geom)])
            print singaporeObj.name_1, totalSeverity
            crisisLevel = self.getCrisisLevel(totalSeverity)
            district = Districts.objects.get(district=singaporeObj.name_1)
            if district.crisis >= crisisLevel:
                continue
            else:
                new_crises[district.district] = crisisLevel
        print new_crises
        # PMODispatcher().emergencyDispatch(new_crises)
