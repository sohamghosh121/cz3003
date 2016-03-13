from ..tabview import TabView, TabViews, MapView, ListView


class OperatorMapView(MapView):
    url = 'operator/map'
    template = 'common/map.html'


class NewEventView(TabView):
    tab_id = 'newevent'
    icon = 'plus-square'
    url = 'operator/new'
    title = 'New Request'
    template = 'operator/new_event.html'


class OperatorListEvents(ListView):
    url = 'operator/list'
    template = 'operator/list.html'


class OperatorTabViews(TabViews):

    def __init__(self):
        self.tabs = [NewEventView(), OperatorMapView(), OperatorListEvents()]
