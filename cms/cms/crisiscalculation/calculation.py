from ..models import TrafficEvent, TerroristEvent, Singapore, Districts


class CrisisCalculator:
    SEVERITY_THRESHOLD_BINS = [100, 150, 300, 500, 750, 1000, 2000]

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
        return 0

    def getEvents(self, geom):
        events = []
        events.extend(TrafficEvent.objects.filter(location__within=geom))
        events.extend(TerroristEvent.objects.filter(location__within=geom))

    def checkCrisis(self):
        singaporeObj = Singapore.objects.all()
        for geom in geoms:
            totalSeverity = sum([eventSeverityCalculator(event)
                                 for event in self.getEvents(singaporeObj.geom)])
            crisisLevel = self.getCrisisLevel(totalSeverity)
            district = Districts.objects.get(district=singaporeObj.name_1)
            # if district.crisis <= crisisLevel:
