## Script (Python) "hackTimeConflictCard"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=testmode=0
##title=
from Products.CMFCore.utils import getToolByName
pm = getToolByName(context, 'portal_membership', None)
if not pm:
    print 'unable to check login'
    return printed

m = pm.getAuthenticatedMember()
if not m or m.id == 'Anonymous User':
    print 'not logged in'
    return printed

if m.id <> 'kimadmin':
    print 'unauthorized'
    return printed

context.setInstructorID1('kimtestinstructor1')
context.setInstructorID2('kimtestinstructor2')
context.reindexObject()
print "set instructorID1 to %s and instructorID2 to %s" % (context.getInstructorID1(), context.getInstructorID2())
return printed
