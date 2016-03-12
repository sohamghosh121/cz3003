from ..tabview import TabView, TabViews, MapView, ListView



class AdminLogView(TabView):
    tab_id = 'log'
    url = 'admin/log'
    template = 'admin/log.html'
    title = 'TransactionLog'
    icon = 'book'

class AdminCrisisView(TabView):
	tab_id = 'crisis'
	url = 'admin/crisis'
	template = 'admin/crisis.html'
	title = 'Crisis Manager'
	icon = 'warning'


class AdminTabViews(TabViews):

    def __init__(self):
        self.tabs = [AdminLogView(), AdminCrisisView()]
