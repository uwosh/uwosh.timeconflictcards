from Products.CMFCore.utils import getToolByName
# from Products.ATVocabularyManager.config import *
from uwosh.timeconflictcards.config import PROJECTNAME
"""Test setup for integration and functional tests.

When we import PloneTestCase and then call setupPloneSite(), all of
Plone's products are loaded, and a Plone site will be created. This
happens at module level, which makes it faster to run each test, but
slows down test runner startup.
"""

from Products.Five import zcml
from Products.Five import fiveconfigure

from Testing import ZopeTestCase as ztc

import Products.ATVocabularyManager

from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import onsetup

import uwosh.timeconflictcards


# When ZopeTestCase configures Zope, it will *not* auto-load products
# in Products/. Instead, we have to use a statement such as:
#   ztc.installProduct('SimpleAttachment')
# This does *not* apply to products in eggs and Python packages (i.e.
# not in the Products.*) namespace. For that, see below.
# All of Plone's products are already set up by PloneTestCase.


@onsetup
def setup_product():
    """Set up the package and its dependencies.

    The @onsetup decorator causes the execution of this body to be
    deferred until the setup of the Plone site testing layer. We could
    have created our own layer, but this is the easiest way for Plone
    integration tests.
    """

    # Load the ZCML configuration for the example.tests package.
    # This can of course use <include /> to include other packages.

    fiveconfigure.debug_mode = True
    zcml.load_config('configure.zcml', Products.ATVocabularyManager)
    zcml.load_config('configure.zcml', uwosh.timeconflictcards)
    fiveconfigure.debug_mode = False

    # We need to tell the testing framework that these products
    # should be available. This can't happen until after we have loaded
    # the ZCML. Thus, we do it here. Note the use of installPackage()
    # instead of installProduct().
    # This is *only* necessary for packages outside the Products.*
    # namespace which are also declared as Zope 2 products, using
    # <five:registerPackage /> in ZCML.

    # We may also need to load dependencies, e.g.:
    #   ztc.installPackage('borg.localrole')

    ztc.installProduct('ATVocabularyManager')
    ztc.installPackage('uwosh.timeconflictcards')

# The order here is important: We first call the (deferred) function
# which installs the products we need for this product. Then, we let
# PloneTestCase set up this product on installation.

setup_product()
ptc.setupPloneSite(products=['ATVocabularyManager', 'uwosh.timeconflictcards'])
# ptc.setupPloneSite()
ztc.installProduct('ATVocabularyManager')
ztc.installProduct('uwosh.timeconflictcards')
ptc.installProduct('ATVocabularyManager')
ptc.installProduct('uwosh.timeconflictcards')


class TestCase(ptc.PloneTestCase):
    """We use this base class for all the tests in this package. If
    necessary, we can put common utility or setup code in here. This
    applies to unit test cases.
    """


class FunctionalTestCase(ptc.FunctionalTestCase):
    """We use this class for functional integration tests that use
    doctest syntax. Again, we can put basic common utility or setup
    code in here.
    """

    def afterSetUp(self):
        roles = ('Member', 'Contributor')
        self.portal.portal_membership.addMember('contributor',
                                                'secret',
                                                roles, [])


def installWithinPortal(portal):
    qi = getToolByName(portal, 'portal_quickinstaller')
    qi.installProduct(PROJECTNAME)


def getATVM(portal):
    return portal[TOOL_NAME]
