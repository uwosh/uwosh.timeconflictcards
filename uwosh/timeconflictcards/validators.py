#from Products.validation.interfaces import ivalidator
from Products.validation.interfaces.IValidator import IValidator
from zope.interface import implements
import xmlrpclib
import socket

webServiceBaseURL = 'http://ws.it.uwosh.edu:8080/ws/'
webService = xmlrpclib.Server(webServiceBaseURL, allow_none=1)

class CourseNumberValidator:

    implements(IValidator)

    # __implements__ = (IValidator,)

    def __init__(self, name="CourseNumberValidator"):
        self.name = name

    #def __call__(self, value, instance, field, *args, **kwargs):
    def __call__(self, value, *args, **kwargs):
        psterm = 0660
        subject1 = 'ENGLISH'
        import pdb; pdb.set_trace()
    	class_info = webService.getCatalogNumbersAndSectionsByTermAndSubjectCX(psterm, subject1)
        import pdb; pdb.set_trace()

        for i in class_info:
            if value in [class_info.keys()[0] for i in class_info]:
                pass
        else:
            return "No way!"