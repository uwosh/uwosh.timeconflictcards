## Script (Python) "grantLocalInstructorRoleProxied"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=state_change
##title=
##
from Products.CMFCore.utils import getToolByName
import logging
logger = logging.getLogger('grantLocalInstructorRoleProxied')

#logger.info('hello - context is %s and state_change is %s' % (context, state_change))
logger.info('hello - state_change is %s' % (state_change))
obj = state_change.object
#logger.info('hello - context is %s and state_change is %s and obj is %s' % (context, state_change, obj))
logger.info('hello - obj is %s' % (obj))

changed = False
pm = getToolByName(obj, "portal_membership", None)
if pm:
    id1 = obj.getInstructorID1()
    if pm.getMemberById(id1):
        obj.manage_setLocalRoles(id1, ('Instructor',))
        logger.info('set local role for %s' % id1)
        changed = True
    id2 = obj.getInstructorID2()
    if pm.getMemberById(id2):
        obj.manage_setLocalRoles(id2, ('Instructor',))
        logger.info('set local role for %s' % id2)
        changed = True
    if changed:
        obj.reindexObjectSecurity()
        logger.info('called reindexObjectSecurity')
