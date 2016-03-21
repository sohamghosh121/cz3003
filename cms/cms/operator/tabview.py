"""
    Module that display views for operator
"""
from ..tabview import TabView, TabViews, MapView, ListView

class OperatorMapView(MapView):
    """
        Display map for operator
    """
    url = 'operator/map'
    template = 'common/map.html'


class NewEventView(TabView):
    """
        View for operator to create a new event
    """
    tab_id = 'newevent'
    icon = 'plus-square'
    url = 'operator/new'
    title = 'New Request'
    template = 'operator/new_event.html'


class OperatorListEvents(ListView):
    """
        List of events for operator
    """
    url = 'operator/list'
    template = 'operator/list.html'


class OperatorTabViews(TabViews):
    """
        Module to switch between tab views for operator
    """
    def __init__(self):
        self.tabs = [NewEventView(), OperatorMapView(), OperatorListEvents()]
