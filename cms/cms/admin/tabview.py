"""
    View module for admin
"""
from ..tabview import TabView, TabViews, MapView, ListView


class AdminLogView(TabView):

    """
        Admin Log View
    """
    tab_id = 'log'
    url = 'admin/log'
    template = 'admin/log.html'
    title = 'Transaction Log'
    icon = 'book'


class AdminCrisisView(TabView):

    """
        View for admin to see the crisis level
    """
    tab_id = 'crisis'
    url = 'admin/crisis'
    template = 'admin/crisis.html'
    title = 'Crisis Manager'
    icon = 'warning'


class AdminMapView(MapView):

    """
        View for admin to see the map
    """
    url = 'admin/map'
    template = 'common/map.html'


class AdminListEvents(ListView):

    """
        View for admin to see a list of AdminListEvents
    """
    url = 'admin/list'
    template = 'admin/list.html'


class AdminReport(TabView):

    """
        View for admin to see a list of AdminListEvents
    """
    tab_id = 'reportmanager'
    url = 'admin/report'
    template = 'admin/report.html'
    title = 'Report Manager'
    icon = 'file-text'


class AdminSuggestedCrisis(TabView):

    """
        View for admin to view suggested crisis levels by our system
    """
    tab_id = 'calculator'
    url = 'admin/suggestedcrisis'
    template = 'admin/crisiscalculator.html'
    title = 'Crisis Calculator'
    icon = 'calculator'


class AdminTabViews(TabViews):

    """
        Tab view to switch between different views for admin
    """

    def __init__(self):
        self.tabs = [
            AdminLogView(), AdminCrisisView(), AdminMapView(), AdminListEvents(), AdminReport(), AdminSuggestedCrisis()]
