"""
    View modules for admin
"""
from ..tabview import TabView, TabViews, MapView, ListView



class AdminLogView(TabView):
    """
        Transaction Log View for admin
    """

    tab_id = 'log'
    url = 'admin/log'
    template = 'admin/log.html'
    title = 'Transaction Log'
    icon = 'book'

class AdminCrisisView(TabView):
    """
        Crisis View for admin
    """

	tab_id = 'crisis'
	url = 'admin/crisis'
	template = 'admin/crisis.html'
	title = 'Crisis Manager'
	icon = 'warning'

class AdminMapView(MapView):
    """
        Map View for admin
    """

    url = 'admin/map'
    template = 'common/map.html'

class AdminListEvents(ListView):
    """
        List of events for admin
    """

    url = 'admin/list'
    template = 'admin/list.html'

class AdminTabViews(TabViews):
    """
        Module to switch between tab views
    """

    def __init__(self):
        self.tabs = [AdminLogView(), AdminCrisisView(), AdminMapView(), AdminListEvents()]
