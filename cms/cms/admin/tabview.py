from ..tabview import TabView, TabViews, MapView, ListView

class AdminLogView(TabView):
    tab_id = 'log'
    url = 'admin/log'
    template = 'admin/log.html'
    title = 'Transaction Log'
    icon = 'book'

class AdminCrisisView(TabView):
	tab_id = 'crisis'
	url = 'admin/crisis'
	template = 'admin/crisis.html'
	title = 'Crisis Manager'
	icon = 'warning'

class AdminMapView(MapView):
    url = 'admin/map'
    template = 'common/map.html'

class AdminListEvents(ListView):
    url = 'admin/list'
    template = 'admin/list.html'

class AdminTabViews(TabViews):

    def __init__(self):
        self.tabs = [AdminLogView(), AdminCrisisView(), AdminMapView(), AdminListEvents()]
