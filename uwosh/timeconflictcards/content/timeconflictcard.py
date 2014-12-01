"""Definition of the TimeConflictCard content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.Archetypes.Field import ComputedField
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata
import datetime
from Products.ATVocabularyManager import NamedVocabulary
# -*- Message Factory Imported Here -*-
from uwosh.timeconflictcards import timeconflictcardsMessageFactory as _
from uwosh.timeconflictcards.interfaces import ITimeConflictCard
from uwosh.timeconflictcards.config import PROJECTNAME
from Products.CMFCore.utils import getToolByName
import xmlrpclib
import socket
from Products.Archetypes.utils import DisplayList
from Products.PlonePAS.interfaces import group as igroup


# from Products.validation import validation 
# from uwosh.timeconflictcards import validators
# validation.register(validators.CourseNumberValidator('CourseNumberValidator'))


# webServiceBaseURL = 'https://ws.it.uwosh.edu/'
webServiceBaseURL = 'http://ws.it.uwosh.edu:8081/ws'
webService = xmlrpclib.Server(webServiceBaseURL, allow_none=1)
# WEBSERVICETESTMODE=0

TimeConflictCardSchema = schemata.ATContentTypeSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-

    ComputedField('title',
        searchable=1,
        expression='context._computeTitle()',
        accessor='Title',
    ),

    atapi.StringField(
        'studentemail',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Your (the student's) UW Oshkosh email address"),
            description=_(u""),
        ),
        default_method="setDefaultEmail",
        required=True,
        validators=('isEmail'),
    ),
                                                                             
    atapi.StringField(
        'fullname',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Your full name"),
            description=_(u""),
        ),
        default_method="setDefaultFullName",
        required=True,
    ),

    ComputedField('studentemplid',
        searchable=0,
        expression='context._computeStudentEmplid()',
        accessor='getStudentemplid',
    ),

    atapi.StringField(
        'creditaudit',
        storage=atapi.AnnotationStorage(),
        widget=atapi.SelectionWidget(
            label=_(u"Credit or Audit"),
            description=_(u"Please select whether you are taking this class for credit or audit"),
        ),
        vocabulary=("Credit", "Audit",),
        required=True,
        default="Credit",
   ),

    atapi.StringField(
        'psterm',
        storage=atapi.AnnotationStorage(),
        widget=atapi.SelectionWidget(
            label=_(u"Academic term"),
            description=_(u"Please select the academic term for your conflict"),
        ),
        vocabulary=NamedVocabulary("PSSemesters"),
        # vocabulary="getPSSemesters",
        default_method="setDefaultPsterm",
        required=True,
   ),

    atapi.StringField(
        'subject1',
        storage=atapi.AnnotationStorage(),
        widget=atapi.SelectionWidget(
            label='Subject 1',
            description=_(u"Please choose the subject for your first conflicting class, e.g. HISTORY"),
        ),
        required=1,
        vocabulary=NamedVocabulary("PSSubjects"),
        searchable=True,
        ),
        
                                                                                                                                                              
    atapi.StringField(
        'catalognumber1',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label='Catalog Number 1',
            description=_(u"Please select the catalog number for your first conflicting class, e.g. 101"),
        ),
        required=1,
        searchable=True,
    ),       

    atapi.StringField(
        'sectionnumber1',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label='Section Number 1',
            description=_(u"Please select the section number for your first conflicting class, e.g. 001"),
        ),
        required=1,
        searchable=True,
    ),      
    
    atapi.StringField(
        'classnumber1',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Class Number 1"),
            description=_(u"This is the five (5) digit class number for your first conflicting class, e.g. 50123, and is for your information only"),
        ),
        required=1,
    ),

    
                                                                                                                                                             
    atapi.StringField(
        'instructorID1',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Instructor 1's ID"),
            description=_(u"This is the user ID of the instructor for your first conflicting class, and is for your information only"),
        ),
        required=True,
        searchable=True,
    ),

                                                                                 
    atapi.StringField(
        'subject2',
        storage=atapi.AnnotationStorage(),
        widget=atapi.SelectionWidget(
            label='Subject 2',
            description=_(u"Please choose the subject for your second conflicting class, e.g. HISTORY"),
        ),
        required=1,
        vocabulary=NamedVocabulary("PSSubjects"),
        searchable=True
        ),
        
                                                                                                                                                              
    atapi.StringField(
        'catalognumber2',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label='Catalog Number 2',
            description=_(u"Please select the catalog number for your first conflicting class, e.g. 101"),
        ),
        required=1,
        searchable=True,
    ),        


    atapi.StringField(
        'sectionnumber2',
         storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label='Section Number 2',
            description=_(u"Please select the section number for your first conflicting class, e.g. 001"),
        ),
        required=1,
        searchable=True,   
    ),        
                                                                             

     atapi.StringField(
        'classnumber2',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label='Class Number 2',
            description=_(u"This is the five (5) digit class number for your second conflicting class, e.g. 50123, and is for your information only"),
        ),
        required=1,
    ),


    atapi.StringField(
        'instructorID2',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Instructor 2's ID"),
            description=_(u"This is the user ID of the instructor for your second conflicting class, and is for your information only"),
        ),
        searchable=True,
        required=True,        
    ),


    atapi.StringField(
        'comments',
        storage=atapi.AnnotationStorage(),
        widget=atapi.TextAreaWidget(
            label=_(u"Explanation"),
            description=_(u"Please explain your schedule conflict"),
        ),
        required=True,
    ),

    atapi.StringField(
        'legallabel',
        storage=atapi.AnnotationStorage(),
        widget=atapi.BooleanWidget(
            label=_(u"ATTENTION STUDENT"),
            description=_(u"By checking the box on the left, I (Student) agree to pay all costs associated with my enrollment at the University.  Furthermore, I agree to pay all collection expenses, including reasonable attorney's fees, which the University may incur if I do not fulfill my payment obligations.  Time Conflict Cards are not official until they are processed by the Registrar's Office."),
        ),
        required=True,
    ),


))

# Set storage on fields copied from ATContentTypeSchema, making sure
# they work well with the python bridge properties.

TimeConflictCardSchema['title'].storage = atapi.AnnotationStorage()
TimeConflictCardSchema['title'].required = 0
TimeConflictCardSchema['title'].widget.visible = {'edit': 'hidden', 'view': 'invisible'}

TimeConflictCardSchema['description'].storage = atapi.AnnotationStorage()
TimeConflictCardSchema['description'].widget.visible = {'edit': 'hidden', 'view': 'invisible'}


schemata.finalizeATCTSchema(TimeConflictCardSchema, moveDiscussion=False)


class TimeConflictCard(base.ATCTContent):
    """Implementation of Time Conflict Card"""
    implements(ITimeConflictCard)

    meta_type = "TimeConflictCard"
    schema = TimeConflictCardSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')


    def setDefaultEmail(self):
        pm = getToolByName(self, "portal_membership", None)
        if pm:
            member = pm.getAuthenticatedMember()
            if member:
                return member.getProperty('email')


    def setDefaultFullName(self):
        pm = getToolByName(self, "portal_membership", None)
        if pm:
            member = pm.getAuthenticatedMember()
            if member:
                return member.getProperty('fullname')         


    def setDefaultPsterm(self):
        # psterm = ""
        # try:
        #     psterm = webService.getCurrentOrNextSemesterCX(WEBSERVICETESTMODE)
        # except Exception, e:
        #     pass
        psterm = webService.getCurrentOrNextSemesterCX()
        return psterm
    

    # def getPSSemesters(self):
    #     threesems = webService.getThreeSemestersCX(WEBSERVICETESTMODE)
    #     threesemstuple =xmlrpclib.loads(threesems)
    #     dl = DisplayList([(x, y) for x, y in threesemstuple])
    #     import pdb; pdb.set_trace( )
    #     return threesemstuple


    def getPsterm(self):
        vocab = NamedVocabulary("PSSemesters")
        try:
            displayval = vocab.getVocabularyDict(self)[self.psterm]
        except KeyError, e:
            retstr = ""
        else:
            retstr = "%s (%s)" % (displayval, self.psterm)
        return retstr


    def getRawPsterm(self):
        return self.psterm


    def _huntUserFolder(self, member_id, context):
        """Find userfolder containing user in the hierarchy
           starting from context
        """
        uf = context.acl_users
        while uf is not None:
            user = uf.getUserById(member_id)
            if user is not None:
                return uf
            container = aq_parent(aq_inner(uf))
            parent = aq_parent(aq_inner(container))
            uf = getattr(parent, 'acl_users', None)
        return None


    def _huntUser(self, member_id, context):
        """Find user in the hierarchy of userfolders
           starting from context
        """
        uf = self._huntUserFolder(member_id, context)
        if uf is not None:
            return uf.getUserById(member_id)


    def getMemberEmail(self, id):
        """ Need this because portal_membership.getMemberById() is for Manager role only.
            This code is based on getMemberById but doesn't use wrapUser().
        """
        user = self._huntUser(id, self)
        if user is not None:
            email = user.getProperty('email', None)
            return email
        # otherwise just return the userid with a domain name appended
        # return id + '@uwosh.edu'


    def getRegistrarGroupMemberEmails(self):
        """ Need this because portal_groups.getGroupMembers() is protected.
        """
        return [self.getMemberEmail(m) for m in self.getGroupMembers('Registrar')]


    def getGroupMembers(self, group_id):
        members = set()
        introspectors = self._getGroupIntrospectors()
        for iid, introspector in introspectors:
            members.update(introspector.getGroupMembers(group_id))
        return list(members)


    def _getGroupIntrospectors(self):
        return self._getPlugins().listPlugins(
            igroup.IGroupIntrospection
            )


    def _getPlugins(self):
        return self.acl_users.plugins


    def _computeTitle(obj):
        """Get object's title."""
        title = " ".join([obj.fullname or '?', obj.psterm or '?', obj.classnumber1 or '?', obj.classnumber2 or '?',])
        return title


    def _computeStudentEmplid(obj):
        """Get student's emplid via web service"""
        # emplid = ''
        # try:
        #     emplid = webService.getEmplidFromEmailAddressCX(obj.studentemail, WEBSERVICETESTMODE)
        # except xmlrpclib.ResponseError, e:
        #     pass
        # except socket.error, e:
        #     pass
        emplid = webService.getEmplidFromEmailAddressCX(obj.studentemail)
        return emplid

    # -*- Your ATSchema to Python Property Bridges Here ... -*-

    instructorID1 = atapi.ATFieldProperty('instructorID1')

    instructorID2 = atapi.ATFieldProperty('instructorID2')

    classnumber1 = atapi.ATFieldProperty('classnumber1')
    
    sectionnumber1 = atapi.ATFieldProperty('sectionnumber1')

    classnumber2 = atapi.ATFieldProperty('classnumber2')

    sectionnumber2 = atapi.ATFieldProperty('sectionnumber2')

    catalognumber1 = atapi.ATFieldProperty('catalognumber1')

    catalognumber2 = atapi.ATFieldProperty('catalognumber2')

    creditaudit = atapi.ATFieldProperty('creditaudit')
    
    subject1 = atapi.ATFieldProperty('subject1')

    subject2 = atapi.ATFieldProperty('subject2')
    
    psterm = atapi.ATFieldProperty('psterm')

    fullname = atapi.ATFieldProperty('fullname')

    comments = atapi.ATFieldProperty('comments')

    topic = atapi.ATFieldProperty('topic')

    studentemail = atapi.ATFieldProperty('studentemail')


def objectSetTitle(obj, event):
    title = " ".join([obj.fullname or '?', obj.psterm or '?', obj.classnumber1 or '?', obj.classnumber2 or '?',])
    if obj.Title() != title:
        obj.Title(title)
        obj.reindexObject()


def objectInitialized(obj, event):
    objectSetTitle(obj, event)
   

def objectEdited(obj, event):
    objectSetTitle(obj, event)
    changed = False
    pm = getToolByName(obj, "portal_membership", None)
    if pm:
        id1 = obj.getInstructorID1()
        if pm.getMemberById(id1):
            obj.manage_setLocalRoles(id1, ('Instructor',))
            changed = True
        id2 = obj.getInstructorID2()
        if pm.getMemberById(id2):
            obj.manage_setLocalRoles(id2, ('Instructor',))
            changed = True
        if changed:
            obj.reindexObjectSecurity()


atapi.registerType(TimeConflictCard, PROJECTNAME)
