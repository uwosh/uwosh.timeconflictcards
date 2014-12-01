from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.Five.browser import BrowserView

class TimeConflictCardView(BrowserView):

    # This may be overridden in ZCML
    index = ViewPageTemplateFile("timeconflictcard_view.pt")

    def render(self):
        return self.index()

    def __call__(self):
        return self.render()