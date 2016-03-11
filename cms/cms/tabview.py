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
