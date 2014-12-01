import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from Products.CMFCore.WorkflowCore import WorkflowException
from base import TestCase
from AccessControl import security
from AccessControl import getSecurityManager
from Products.MailHost.interfaces import IMailHost
from Products.CMFPlone.tests.utils import MockMailHost
from zope.component import getSiteManager



class CardTestCase(TestCase):
    """All our tests"""


    def createCard(self):
        """ creates a card or recreates if it already exists """
        pm = self.portal.portal_membership
        # login as student and create a card
        self.login('student')
        memberId = pm.getAuthenticatedMember().id
        # delete and recreate if already exists
        # import ipdb; ipdb.set_trace()
        if getattr(self.folder, 'card', None):
            self.folder.manage_delObjects('card')
        self.folder.invokeFactory('TimeConflictCard', 'card')
        self.card = self.folder.card
        self.card.setTitle('this is a card title')
        self.card.setDescription('a description')
        self.card.edit(studentemail='email@email.com', 
            fullname='Bob Bobster',
            psterm='0668',
            subject1='COMPUTER SCIENCE', 
            catalognumber1=' 101',
            sectionnumber1='001C', 
            classnumber1='44444',
            instructorID1='instructor1',
            subject2='MATH', 
            catalognumber2=' 102',
            sectionnumber2='002C', 
            classnumber2='55555',
            instructorID2='instructor2',
            comments='I need this class'
            )


    def afterSetUp(self):
        # add users and set their roles
        pm = self.portal.portal_membership
        workflow = self.portal.portal_workflow

        # set up fake mailhost
        self.portal._original_MailHost = self.portal.MailHost
        self.portal.MailHost = mailhost = MockMailHost('MailHost')
        sm = getSiteManager(context=self.portal)
        sm.unregisterUtility(provided=IMailHost)
        sm.registerUtility(mailhost, provided=IMailHost)
        # We need to fake a valid mail setup
        # self.portal.manage_changeProperties({'email_from_address':'siteowner@uwosh.edu'})
        self.portal.email_from_address = "siteowner@uwosh.edu"
        self.mailhost = self.portal.MailHost

        pm.addMember('student', 'secret', [], [], properties={'email':'student@uwosh.edu'})
        self.setRoles(['Contributor',], 'student')

        pm.addMember('instructor1', 'secret', [], [], properties={'email':'instructor1@uwosh.edu'})
        self.setRoles(['Instructor',], 'instructor1')

        pm.addMember('instructor2', 'secret', [], [], properties={'email':'instructor2@uwosh.edu'})
        self.setRoles(['Instructor',], 'instructor2')

        pm.addMember('registrar', 'secret', [], [], properties={'email':'registrar@uwosh.edu'})
        self.setRoles(['Registrar',], 'registrar')

        pm.addMember('joe_schmoe_contributor', 'secret', [], [], properties={'email':'joe_schmoe_contributor@uwosh.edu'})
        self.setRoles(['Contributor',], 'joeschmoe_contributor')

        pm.addMember('joe_schmoe_nobody', 'secret', [], [], properties={'email':'joe_schmoe_nobody@uwosh.edu'})
        self.setRoles([], 'joeschmoe_nobody')

        self.logout()
        self.createCard()

        # this would be preferable if only it showed all transitions
        # workflow.timeconflictcard.transitions is protected
        # self.ALL_STATES = [i[0] for i in workflow.timeconflictcard.items()]
        self.ALL_STATES = ('archived', 'completed', 'instructor1waitingforstudentresponse', 'instructor2waitingforstudentresponse', 'needinstructor1approval', 'needinstructor2approval', 'private', 'registrarprocessing', 'retracted', 'studenthasbeeninformedenrollmentdenied', )


    def test_create_and_set_attributes_and_initial_roles(self):
        card = self.card

        self.assertEqual(card.Title(), 'Bob Bobster 0668 44444 55555')
        self.assertEqual(card.Description(), 'a description')
        self.assertEqual(card.studentemail, 'email@email.com')
        self.assertEqual(card.fullname, 'Bob Bobster')
        self.assertEqual(card.psterm, '0668')
        self.assertEqual(card.subject1, 'COMPUTER SCIENCE')
        self.assertEqual(card.catalognumber1, ' 101')
        self.assertEqual(card.sectionnumber1, '001C')
        self.assertEqual(card.classnumber1, '44444')
        self.assertEqual(card.instructorID1, 'instructor1')
        self.assertEqual(card.subject2, 'MATH')
        self.assertEqual(card.catalognumber2, ' 102')
        self.assertEqual(card.sectionnumber2, '002C')
        self.assertEqual(card.classnumber2, '55555')
        self.assertEqual(card.instructorID2, 'instructor2')
        self.assertEqual(card.getComments(), 'I need this class')

        card.processForm()

        # import ipdb;ipdb.set_trace()
        # check various roles on the card
        localRoles2 = card.get_local_roles_for_userid('student')
        self.assertEqual(('Owner',), localRoles2)

        localRoles3 = card.get_local_roles_for_userid('instructor1')
        self.assertEqual((), localRoles3)

        localRoles4 = card.get_local_roles_for_userid('instructor2')
        self.assertEqual((), localRoles4)

        localRoles5 = card.get_local_roles_for_userid('registrar')
        self.assertEqual((), localRoles5)


    def _add_comment(self, state_title):
        workflow = self.portal.portal_workflow
        utils = self.portal.plone_utils

        self.logout()
        self.login('student')
        workflow.doActionFor(self.card, 'addcomment')
        self.assertEqual(utils.getReviewStateTitleFor(self.card), state_title)
        self.logout()
        self.login('instructor1')
        workflow.doActionFor(self.card, 'addcomment')
        self.assertEqual(utils.getReviewStateTitleFor(self.card), state_title)
        self.logout()
        self.login('instructor2')
        workflow.doActionFor(self.card, 'addcomment')
        self.assertEqual(utils.getReviewStateTitleFor(self.card), state_title)
        self.logout()
        self.login('registrar')
        workflow.doActionFor(self.card, 'addcomment')
        self.assertEqual(utils.getReviewStateTitleFor(self.card), state_title)
        self.logout()
        self.login('instructor1')


    def test_states(self):
        """
        States to test:

         archived   Archived 
            addcomment (Add a comment) 
         completed   Completed 
            addcomment (Add a comment) 
            archive (Archive this request) 
         instructor1waitingforstudentresponse   Instructor 1 waiting for student to respond to question 
            addcomment (Add a comment) 
            studentrespondstoinstructor1request (Respond to instructor request for more information) 
            retract (Retract this request) 
         instructor2waitingforstudentresponse   Instructor 2 waiting for student to respond to question 
            addcomment (Add a comment) 
            studentrespondstoinstructor2request (Respond to instructor request for more information) 
            retract (Retract this request) 
         needinstructor1approval   Needs instructor 1 approval 
            instructor1deniesenrollment (Deny request) 
            submitforinstructor2approval (Approve and send to other instructor for approval) 
            addcomment (Add a comment) 
            instructor1requestsmoreinformation (Request more information from student) 
            retract (Retract this request) 
         needinstructor2approval   Needs instructor 2 approval 
            instructor2requestsmoreinformation (Request more information from student) 
            instructor2deniesenrollment (Deny request) 
            submittoregistrarforprocessing (Approve and send to registrar) 
            addcomment (Add a comment) 
            retract (Retract this request) 
         * private   Private / not yet submitted 
            submitforinstructor1approval (Submit for approval) 
         registrarprocessing   Waiting for Registrar to process 
            addcomment (Add a comment) 
            registrarsofficecompletesprocessing (Complete processing) 
         retracted   Retracted 
            addcomment (Add a comment) 
         studenthasbeeninformedenrollmentdenied   The request has been denied 
            addcomment (Add a comment) 
            retract (Retract this request)

        workflow.doActionFor(self.card, '')
        self.assertEqual(utils.getReviewStateTitleFor(self.card), '')
         
        """

        workflow = self.portal.portal_workflow
        utils = self.portal.plone_utils

        # straight through approvals
        self.createCard()
        self.assertEqual(utils.getReviewStateTitleFor(self.card), 'Private / not yet submitted')
        workflow.doActionFor(self.card, 'submitforinstructor1approval')
        self.assertEqual(utils.getReviewStateTitleFor(self.card), 'Needs instructor 1 approval')
        # make sure can't do this as the student
        self.assertRaises(WorkflowException, workflow.doActionFor, self.card, 'submitforinstructor2approval')

        self.logout()
        self.login('instructor1')
        workflow.doActionFor(self.card, 'submitforinstructor2approval')
        self.assertEqual(utils.getReviewStateTitleFor(self.card), 'Needs instructor 2 approval')
        self.logout()
        self.login('instructor2')
        workflow.doActionFor(self.card, 'submittoregistrarforprocessing')
        self.assertEqual(utils.getReviewStateTitleFor(self.card), 'Waiting for Registrar to process')
        # make sure can't do this as the instructor
        self.assertRaises(WorkflowException, workflow.doActionFor, self.card, 'registrarsofficecompletesprocessing')

        self.logout()
        self.login('registrar')
        workflow.doActionFor(self.card, 'registrarsofficecompletesprocessing')
        self.assertEqual(utils.getReviewStateTitleFor(self.card), 'Completed')
        workflow.doActionFor(self.card, 'archive')
        self.assertEqual(utils.getReviewStateTitleFor(self.card), 'Archived')

        # instructor 1 denies
        self.createCard()
        self.assertEqual(utils.getReviewStateTitleFor(self.card), 'Private / not yet submitted')
        workflow.doActionFor(self.card, 'submitforinstructor1approval')
        self.assertEqual(utils.getReviewStateTitleFor(self.card), 'Needs instructor 1 approval')
        self.logout()
        self.login('instructor1')
        workflow.doActionFor(self.card, 'instructor1deniesenrollment')
        self.assertEqual(utils.getReviewStateTitleFor(self.card), 'The request has been denied')
        self.logout()
        self.login('student')
        workflow.doActionFor(self.card, 'retract')
        self.assertEqual(utils.getReviewStateTitleFor(self.card), 'Retracted')

        # instructor 2 denies
        self.createCard()
        self.assertEqual(utils.getReviewStateTitleFor(self.card), 'Private / not yet submitted')
        workflow.doActionFor(self.card, 'submitforinstructor1approval')
        self.assertEqual(utils.getReviewStateTitleFor(self.card), 'Needs instructor 1 approval')
        self.logout()
        self.login('instructor1')
        workflow.doActionFor(self.card, 'instructor1requestsmoreinformation')
        self.assertEqual(utils.getReviewStateTitleFor(self.card), 'Instructor 1 waiting for student to respond to question')
        self.logout()
        self.login('student')
        workflow.doActionFor(self.card, 'studentrespondstoinstructor1request')
        self.assertEqual(utils.getReviewStateTitleFor(self.card), 'Needs instructor 1 approval')
        self.logout()
        self.login('instructor1')
        workflow.doActionFor(self.card, 'submitforinstructor2approval')
        self.assertEqual(utils.getReviewStateTitleFor(self.card), 'Needs instructor 2 approval')
        self.logout()
        self.login('instructor2')
        workflow.doActionFor(self.card, 'instructor2requestsmoreinformation')
        self.assertEqual(utils.getReviewStateTitleFor(self.card), 'Instructor 2 waiting for student to respond to question')
        self.logout()
        self.login('student')
        workflow.doActionFor(self.card, 'studentrespondstoinstructor2request')
        self.assertEqual(utils.getReviewStateTitleFor(self.card), 'Needs instructor 2 approval')
        self.logout()
        self.login('instructor1')
        # should not be able to do this unless logged in as the instructorID2 (instructor2)
        self.assertRaises(WorkflowException, workflow.doActionFor, self.card, 'instructor2deniesenrollment')
        self.logout()
        self.login('instructor2')
        workflow.doActionFor(self.card, 'instructor2deniesenrollment')

        self.logout()
        self.login('instructor2')
        self.assertEqual(utils.getReviewStateTitleFor(self.card), 'The request has been denied')
        self.logout()
        self.login('student')
        workflow.doActionFor(self.card, 'retract')
        self.assertEqual(utils.getReviewStateTitleFor(self.card), 'Retracted')


    def test_can_retract(self):
        """ test can retract from anywhere """
        workflow = self.portal.portal_workflow
        utils = self.portal.plone_utils

        # retract from instructor 1
        self.createCard()
        self.assertEqual(utils.getReviewStateTitleFor(self.card), 'Private / not yet submitted')
        workflow.doActionFor(self.card, 'submitforinstructor1approval')
        self.assertEqual(utils.getReviewStateTitleFor(self.card), 'Needs instructor 1 approval')
        self.logout()
        self.login('student')
        workflow.doActionFor(self.card, 'retract')
        self.assertEqual(utils.getReviewStateTitleFor(self.card), 'Retracted')

        # retract from instructor 1 waiting
        self.createCard()
        self.assertEqual(utils.getReviewStateTitleFor(self.card), 'Private / not yet submitted')
        workflow.doActionFor(self.card, 'submitforinstructor1approval')
        self.assertEqual(utils.getReviewStateTitleFor(self.card), 'Needs instructor 1 approval')
        self.logout()
        self.login('instructor1')
        workflow.doActionFor(self.card, 'instructor1requestsmoreinformation')
        self.assertEqual(utils.getReviewStateTitleFor(self.card), 'Instructor 1 waiting for student to respond to question')
        self.logout()
        self.login('student')
        workflow.doActionFor(self.card, 'retract')
        self.assertEqual(utils.getReviewStateTitleFor(self.card), 'Retracted')

        # retract from instructor 2
        self.createCard()
        self.assertEqual(utils.getReviewStateTitleFor(self.card), 'Private / not yet submitted')
        workflow.doActionFor(self.card, 'submitforinstructor1approval')
        self.assertEqual(utils.getReviewStateTitleFor(self.card), 'Needs instructor 1 approval')
        self.logout()
        self.login('instructor1')
        workflow.doActionFor(self.card, 'submitforinstructor2approval')
        self.assertEqual(utils.getReviewStateTitleFor(self.card), 'Needs instructor 2 approval')
        self.logout()
        self.login('student')
        workflow.doActionFor(self.card, 'retract')
        self.assertEqual(utils.getReviewStateTitleFor(self.card), 'Retracted')

        # retract from instructor 2 waiting
        self.createCard()
        self.assertEqual(utils.getReviewStateTitleFor(self.card), 'Private / not yet submitted')
        workflow.doActionFor(self.card, 'submitforinstructor1approval')
        self.assertEqual(utils.getReviewStateTitleFor(self.card), 'Needs instructor 1 approval')
        self.logout()
        self.login('instructor1')
        workflow.doActionFor(self.card, 'submitforinstructor2approval')
        self.assertEqual(utils.getReviewStateTitleFor(self.card), 'Needs instructor 2 approval')
        self.logout()
        self.login('instructor2')
        workflow.doActionFor(self.card, 'instructor2requestsmoreinformation')
        self.assertEqual(utils.getReviewStateTitleFor(self.card), 'Instructor 2 waiting for student to respond to question')
        self.logout()
        self.login('student')
        workflow.doActionFor(self.card, 'retract')
        self.assertEqual(utils.getReviewStateTitleFor(self.card), 'Retracted')

        # retract from denied
        self.createCard()
        self.assertEqual(utils.getReviewStateTitleFor(self.card), 'Private / not yet submitted')
        workflow.doActionFor(self.card, 'submitforinstructor1approval')
        self.assertEqual(utils.getReviewStateTitleFor(self.card), 'Needs instructor 1 approval')
        self.logout()
        self.login('instructor1')
        workflow.doActionFor(self.card, 'instructor1deniesenrollment')
        self.assertEqual(utils.getReviewStateTitleFor(self.card), 'The request has been denied')
        self.logout()
        self.login('student')
        workflow.doActionFor(self.card, 'retract')
        self.assertEqual(utils.getReviewStateTitleFor(self.card), 'Retracted')


    def test_all_players_can_comment(self):
        """ test can add comment from anywhere """
        workflow = self.portal.portal_workflow
        utils = self.portal.plone_utils

        self.createCard()
        self.assertEqual(utils.getReviewStateTitleFor(self.card), 'Private / not yet submitted')
        workflow.doActionFor(self.card, 'submitforinstructor1approval')
        self.assertEqual(utils.getReviewStateTitleFor(self.card), 'Needs instructor 1 approval')
        self._add_comment(utils.getReviewStateTitleFor(self.card))
        self.logout()
        self.login('instructor1')
        workflow.doActionFor(self.card, 'instructor1requestsmoreinformation')
        self.assertEqual(utils.getReviewStateTitleFor(self.card), 'Instructor 1 waiting for student to respond to question')
        self._add_comment(utils.getReviewStateTitleFor(self.card))
        self.logout()
        self.login('student')
        workflow.doActionFor(self.card, 'studentrespondstoinstructor1request')
        self.assertEqual(utils.getReviewStateTitleFor(self.card), 'Needs instructor 1 approval')
        self.logout()
        self.login('instructor1')
        workflow.doActionFor(self.card, 'submitforinstructor2approval')
        self.assertEqual(utils.getReviewStateTitleFor(self.card), 'Needs instructor 2 approval')
        self._add_comment(utils.getReviewStateTitleFor(self.card))
        self.logout()
        self.login('instructor2')
        workflow.doActionFor(self.card, 'submittoregistrarforprocessing')
        self.assertEqual(utils.getReviewStateTitleFor(self.card), 'Waiting for Registrar to process')
        self._add_comment(utils.getReviewStateTitleFor(self.card))
        self.logout()
        self.login('registrar')
        workflow.doActionFor(self.card, 'registrarsofficecompletesprocessing')
        self.assertEqual(utils.getReviewStateTitleFor(self.card), 'Completed')
        self._add_comment(utils.getReviewStateTitleFor(self.card))
        self.logout()
        self.login('registrar')
        workflow.doActionFor(self.card, 'archive')
        self.assertEqual(utils.getReviewStateTitleFor(self.card), 'Archived')
        self._add_comment(utils.getReviewStateTitleFor(self.card))


    def check_user_cannot_view_or_edit(self, card, userid):
        " if userid then login as that user otherwise logout (use Anonymous User) "
        if userid:
            self.login(userid)
        else:
            self.logout()
        # some_retrieved_value = card.getComments() # no worky: this doesn't check security!
        # check if the card is viewable by anon
        self.assertEqual(security.checkPermission('zope2.View', card), False)
        # but can't find an equivalent zope2 permission for Modify so
        # try this way:
        self.assertEqual(getSecurityManager().checkPermission( "View", card), None)
        self.assertEqual(getSecurityManager().checkPermission( "Modify portal content", card), None)


    def generic_loop_user_cannot_view_or_edit(self, userid):
        """ for every state, check that the given user cannot view nor edit the item """
        workflow = self.portal.portal_workflow

        self.createCard()
        self.check_user_cannot_view_or_edit(self.card, userid)

        self.login('student')
        workflow.doActionFor(self.card, 'submitforinstructor1approval')
        self.check_user_cannot_view_or_edit(self.card, userid)

        self.login('instructor1')
        workflow.doActionFor(self.card, 'instructor1requestsmoreinformation')
        self.check_user_cannot_view_or_edit(self.card, userid)

        self.login('student')
        workflow.doActionFor(self.card, 'studentrespondstoinstructor1request')
        self.check_user_cannot_view_or_edit(self.card, userid)

        self.login('instructor1')
        workflow.doActionFor(self.card, 'submitforinstructor2approval')
        self.check_user_cannot_view_or_edit(self.card, userid)

        self.login('instructor2')
        workflow.doActionFor(self.card, 'instructor2requestsmoreinformation')
        self.check_user_cannot_view_or_edit(self.card, userid)

        self.login('student')
        workflow.doActionFor(self.card, 'studentrespondstoinstructor2request')
        self.check_user_cannot_view_or_edit(self.card, userid)

        self.login('instructor2')
        workflow.doActionFor(self.card, 'submittoregistrarforprocessing')
        self.check_user_cannot_view_or_edit(self.card, userid)

        self.login('registrar')
        workflow.doActionFor(self.card, 'registrarsofficecompletesprocessing')
        self.check_user_cannot_view_or_edit(self.card, userid)

        self.login('registrar')
        workflow.doActionFor(self.card, 'archive')
        self.check_user_cannot_view_or_edit(self.card, userid)


    def test_anonymous_cannot_view_or_edit(self):
        """ test that anonymous users can't see or do anything """
        self.generic_loop_user_cannot_view_or_edit(None)


    def test_joe_schmoe_contributor_cannot_view_or_edit(self):
        """ 
        a contributor on the site but not someone who should be reading
        anyone's time conflict cards
        """
        self.generic_loop_user_cannot_view_or_edit('joe_schmoe_contributor')


    def test_joe_schmoe_nobody_cannot_view_or_edit(self):
        """ 
        someone else on the site not involved in these time conflict cards 
        """
        self.generic_loop_user_cannot_view_or_edit('joe_schmoe_nobody')


    def check_user_can_view(self, card, userid):
        " if userid then login as that user otherwise logout (use Anonymous User) "
        if userid:
            self.login(userid)
        else:
            self.logout()
        # check if the card is viewable 
        self.assertEqual(security.checkPermission('zope2.View', card), 1)
        # but can't find an equivalent zope2 permission for Modify so
        # try this way:
        self.assertEqual(getSecurityManager().checkPermission( "View", card), 1)


    def generic_loop_user_can_view(self, userid, notinstates):
        """ for every state, check that the given user can view """
        workflow = self.portal.portal_workflow
        utils = self.portal.plone_utils

        self.createCard()
        if workflow.getInfoFor(self.card, 'review_state') not in notinstates:
            self.check_user_can_view(self.card, userid)

        self.login('student')
        workflow.doActionFor(self.card, 'submitforinstructor1approval')
        if workflow.getInfoFor(self.card, 'review_state') not in notinstates:
            self.check_user_can_view(self.card, userid)

        self.login('instructor1')
        workflow.doActionFor(self.card, 'instructor1requestsmoreinformation')
        if workflow.getInfoFor(self.card, 'review_state') not in notinstates:
            self.check_user_can_view(self.card, userid)

        self.login('student')
        workflow.doActionFor(self.card, 'studentrespondstoinstructor1request')
        if workflow.getInfoFor(self.card, 'review_state') not in notinstates:
            self.check_user_can_view(self.card, userid)

        self.login('instructor1')
        workflow.doActionFor(self.card, 'submitforinstructor2approval')
        if workflow.getInfoFor(self.card, 'review_state') not in notinstates:
            self.check_user_can_view(self.card, userid)

        self.login('instructor2')
        workflow.doActionFor(self.card, 'instructor2requestsmoreinformation')
        if workflow.getInfoFor(self.card, 'review_state') not in notinstates:
            self.check_user_can_view(self.card, userid)

        self.login('student')
        workflow.doActionFor(self.card, 'studentrespondstoinstructor2request')
        if workflow.getInfoFor(self.card, 'review_state') not in notinstates:
            self.check_user_can_view(self.card, userid)

        self.login('instructor2')
        workflow.doActionFor(self.card, 'submittoregistrarforprocessing')
        if workflow.getInfoFor(self.card, 'review_state') not in notinstates:
            self.check_user_can_view(self.card, userid)

        self.login('registrar')
        workflow.doActionFor(self.card, 'registrarsofficecompletesprocessing')
        if workflow.getInfoFor(self.card, 'review_state') not in notinstates:
            self.check_user_can_view(self.card, userid)

        self.login('registrar')
        workflow.doActionFor(self.card, 'archive')
        if workflow.getInfoFor(self.card, 'review_state') not in notinstates:
            self.check_user_can_view(self.card, userid)


    def check_user_cannot_view(self, card, userid):
        " if userid then login as that user otherwise logout (use Anonymous User) "
        if userid:
            self.login(userid)
        else:
            self.logout()
        # check if the card is viewable 
        self.assertEqual(security.checkPermission('zope2.View', card), False)
        # but can't find an equivalent zope2 permission for Modify so
        # try this way:
        self.assertEqual(getSecurityManager().checkPermission( "View", card), None)


    def generic_loop_user_cannot_view(self, userid, states):
        """ for every state, check that the given user can view """
        workflow = self.portal.portal_workflow
        utils = self.portal.plone_utils

        self.createCard()
        if workflow.getInfoFor(self.card, 'review_state') in states:
            self.check_user_cannot_view(self.card, userid)

        self.login('student')
        workflow.doActionFor(self.card, 'submitforinstructor1approval')
        if workflow.getInfoFor(self.card, 'review_state') in states:
            self.check_user_cannot_view(self.card, userid)

        self.login('instructor1')
        workflow.doActionFor(self.card, 'instructor1requestsmoreinformation')
        if workflow.getInfoFor(self.card, 'review_state') in states:
            self.check_user_cannot_view(self.card, userid)

        self.login('student')
        workflow.doActionFor(self.card, 'studentrespondstoinstructor1request')
        if workflow.getInfoFor(self.card, 'review_state') in states:
            self.check_user_cannot_view(self.card, userid)

        self.login('instructor1')
        workflow.doActionFor(self.card, 'submitforinstructor2approval')
        if workflow.getInfoFor(self.card, 'review_state') in states:
            self.check_user_cannot_view(self.card, userid)

        self.login('instructor2')
        workflow.doActionFor(self.card, 'instructor2requestsmoreinformation')
        if workflow.getInfoFor(self.card, 'review_state') in states:
            self.check_user_cannot_view(self.card, userid)

        self.login('student')
        workflow.doActionFor(self.card, 'studentrespondstoinstructor2request')
        if workflow.getInfoFor(self.card, 'review_state') in states:
            self.check_user_cannot_view(self.card, userid)

        self.login('instructor2')
        workflow.doActionFor(self.card, 'submittoregistrarforprocessing')
        if workflow.getInfoFor(self.card, 'review_state') in states:
            self.check_user_cannot_view(self.card, userid)

        self.login('registrar')
        workflow.doActionFor(self.card, 'registrarsofficecompletesprocessing')
        if workflow.getInfoFor(self.card, 'review_state') in states:
            self.check_user_cannot_view(self.card, userid)

        self.login('registrar')
        workflow.doActionFor(self.card, 'archive')
        if workflow.getInfoFor(self.card, 'review_state') in states:
            self.check_user_cannot_view(self.card, userid)


    def check_user_can_edit(self, card, userid):
        " if userid then login as that user otherwise logout (use Anonymous User) "
        if userid:
            self.login(userid)
        else:
            self.logout()
        # check if the card is viewable 
        self.assertEqual(security.checkPermission('zope2.View', card), 1)
        # but can't find an equivalent zope2 permission for Modify so
        # try this way:
        self.assertEqual(getSecurityManager().checkPermission( "Modify portal content", card), 1)


    def generic_loop_user_can_edit(self, userid, notinstates):
        """ for every state, check that the given user can view """
        workflow = self.portal.portal_workflow
        utils = self.portal.plone_utils

        self.createCard()
        if workflow.getInfoFor(self.card, 'review_state') not in notinstates:
            self.check_user_can_edit(self.card, userid)

        self.login('student')
        workflow.doActionFor(self.card, 'submitforinstructor1approval')
        if workflow.getInfoFor(self.card, 'review_state') not in notinstates:
            self.check_user_can_edit(self.card, userid)

        self.login('instructor1')
        workflow.doActionFor(self.card, 'instructor1requestsmoreinformation')
        if workflow.getInfoFor(self.card, 'review_state') not in notinstates:
            self.check_user_can_edit(self.card, userid)

        self.login('student')
        workflow.doActionFor(self.card, 'studentrespondstoinstructor1request')
        if workflow.getInfoFor(self.card, 'review_state') not in notinstates:
            self.check_user_can_edit(self.card, userid)

        self.login('instructor1')
        workflow.doActionFor(self.card, 'submitforinstructor2approval')
        if workflow.getInfoFor(self.card, 'review_state') not in notinstates:
            self.check_user_can_edit(self.card, userid)

        self.login('instructor2')
        workflow.doActionFor(self.card, 'instructor2requestsmoreinformation')
        if workflow.getInfoFor(self.card, 'review_state') not in notinstates:
            self.check_user_can_edit(self.card, userid)

        self.login('student')
        workflow.doActionFor(self.card, 'studentrespondstoinstructor2request')
        if workflow.getInfoFor(self.card, 'review_state') not in notinstates:
            self.check_user_can_edit(self.card, userid)

        self.login('instructor2')
        workflow.doActionFor(self.card, 'submittoregistrarforprocessing')
        if workflow.getInfoFor(self.card, 'review_state') not in notinstates:
            self.check_user_can_edit(self.card, userid)

        self.login('registrar')
        workflow.doActionFor(self.card, 'registrarsofficecompletesprocessing')
        if workflow.getInfoFor(self.card, 'review_state') not in notinstates:
            self.check_user_can_edit(self.card, userid)

        self.login('registrar')
        workflow.doActionFor(self.card, 'archive')
        if workflow.getInfoFor(self.card, 'review_state') not in notinstates:
            self.check_user_can_edit(self.card, userid)


    def check_user_cannot_edit(self, card, userid):
        " if userid then login as that user otherwise logout (use Anonymous User) "
        if userid:
            self.login(userid)
        else:
            self.logout()
        self.assertEqual(getSecurityManager().checkPermission( "Modify portal content", card), None)
        # if getSecurityManager().checkPermission( "Modify portal content", card):
        #     import ipdb; ipdb.set_trace( )
        #     pass


    def generic_loop_user_cannot_edit(self, userid, states):
        """ for every state, check that the given user cannot edit """
        workflow = self.portal.portal_workflow
        utils = self.portal.plone_utils
        # if userid == 'student':
            # import ipdb; ipdb.set_trace( )

        self.createCard()
        if workflow.getInfoFor(self.card, 'review_state') in states:
            self.check_user_cannot_edit(self.card, userid)

        self.login('student')
        workflow.doActionFor(self.card, 'submitforinstructor1approval')
        if workflow.getInfoFor(self.card, 'review_state') in states:
            self.check_user_cannot_edit(self.card, userid)

        self.login('instructor1')
        workflow.doActionFor(self.card, 'instructor1requestsmoreinformation')
        if workflow.getInfoFor(self.card, 'review_state') in states:
            self.check_user_cannot_edit(self.card, userid)

        self.login('student')
        workflow.doActionFor(self.card, 'studentrespondstoinstructor1request')
        if workflow.getInfoFor(self.card, 'review_state') in states:
            self.check_user_cannot_edit(self.card, userid)

        self.login('instructor1')
        workflow.doActionFor(self.card, 'submitforinstructor2approval')
        if workflow.getInfoFor(self.card, 'review_state') in states:
            self.check_user_cannot_edit(self.card, userid)

        self.login('instructor2')
        workflow.doActionFor(self.card, 'instructor2requestsmoreinformation')
        if workflow.getInfoFor(self.card, 'review_state') in states:
            self.check_user_cannot_edit(self.card, userid)

        self.login('student')
        workflow.doActionFor(self.card, 'studentrespondstoinstructor2request')
        if workflow.getInfoFor(self.card, 'review_state') in states:
            self.check_user_cannot_edit(self.card, userid)

        self.login('instructor2')
        workflow.doActionFor(self.card, 'submittoregistrarforprocessing')
        if workflow.getInfoFor(self.card, 'review_state') in states:
            self.check_user_cannot_edit(self.card, userid)

        self.login('registrar')
        workflow.doActionFor(self.card, 'registrarsofficecompletesprocessing')
        if workflow.getInfoFor(self.card, 'review_state') in states:
            self.check_user_cannot_edit(self.card, userid)

        self.login('registrar')
        workflow.doActionFor(self.card, 'archive')
        if workflow.getInfoFor(self.card, 'review_state') in states:
            self.check_user_cannot_edit(self.card, userid)


    # student
    def test_student_can_view(self):
        self.generic_loop_user_can_view('student', notinstates=())


    def test_student_can_edit(self):
        self.generic_loop_user_can_edit('student', notinstates=[s for s in self.ALL_STATES if s not in ('private',)])


    def test_student_cannot_edit(self):
        self.generic_loop_user_cannot_edit('student', states=[s for s in self.ALL_STATES if s != 'private'])


    # instructor1
    def test_instructor1_can_view(self):
        self.generic_loop_user_can_view('instructor1', notinstates=('private',))


    def test_instructor1_cannot_view(self):
        self.generic_loop_user_cannot_view('instructor1', states=('private',))


    def test_instructor1_cannot_edit(self):
        self.generic_loop_user_cannot_edit('instructor1', states=self.ALL_STATES)


    # instructor2
    def test_instructor2_can_view(self):
        self.generic_loop_user_can_view('instructor2', notinstates=('private',))


    def test_instructor2_cannot_view(self):
        self.generic_loop_user_cannot_view('instructor2', states=('private',))


    def test_instructor2_cannot_edit(self):
        self.generic_loop_user_cannot_edit('instructor2', states=self.ALL_STATES)


    # registrar
    def test_registrar_can_view(self):
        self.generic_loop_user_can_view('registrar', notinstates=('private',))


    def test_registrar_cannot_view(self):
        self.generic_loop_user_cannot_view('registrar', states=('private',))


    def test_registrar_cannot_edit(self):
        self.generic_loop_user_cannot_edit('registrar', states=('private',))


    def test_email_notifications(self):
        """ test that email notifications go out ok """
        workflow = self.portal.portal_workflow
        utils = self.portal.plone_utils
        raise NotImplemented


    def test_are_comments_displayed(self):
        """
        ipdb> self.portal.portal_workflow.getStatusOf('timeconflictcard', card)
        {'action': None, 'review_state': 'private', 'comments': '', 'actor': 'student', 'time': DateTime('2012/01/31 11:48:39.900125 US/Central')}

        ipdb> self.portal.portal_workflow.getHistoryOf('timeconflictcard', card)
        ({'action': None, 'review_state': 'private', 'comments': '', 'actor': 'student', 'time': DateTime('2012/01/31 11:48:39.900125 US/Central')},)

        """
        raise NotImplemented


    def test_non_players_cannot_comment(self):
        "Check that anon and non-involved users cannot comment"
        raise NotImplemented


    def test_case_student_is_not_owner(self):
        raise NotImplemented


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(CardTestCase))
    return suite


if __name__ == '__main__':
    framework()