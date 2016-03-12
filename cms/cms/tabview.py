class TabView:
    tab_id = ''
    url = ''
    is_active = False
    tab_title = ''
    template = ''
    icon = ''


class MapView(TabView):
    tab_id = 'map'
    icon = 'map'
    url = 'map'
    title = 'Map'


class OperatorMapView(MapView):
    template = 'operatormapview.html'


class PublicMapView(MapView):
    template = 'publicmapview.html'


class AdminMapView(MapView):
    template = 'adminmapview.html'


class NewEventView(TabView):
    tab_id = 'newevent'
    icon = 'plus-square'
    url = 'new'
    title = 'New Request'
    template = 'new_event.html'


class ListView(TabView):
    tab_id = 'listevents'
    icon = 'list'
    url = 'listEvents'
    title = 'List'


class OperatorListEvents(ListView):
    template = 'operator_list_events.html'


class AdminListTransactions(ListView):
    template = 'admin_list_transactions.html'


class TabViews:

    def __init__(self):
        # add tabs in order here
        self.tabs = []

    def set_active_tab(self, tab_id):
        for tab in self.tabs:
            if tab_id == tab.tab_id:
                tab.is_active = True
            else:
                tab.is_active = False

    def get_active_tab(self):
        for tab in self.tabs:
            if tab.is_active:
                return tab


class OperatorTabViews(TabViews):

    def __init__(self):
        self.tabs = [NewEventView(), MapView(), OperatorListEvents()]
