## Script (Python) "createTimeConflictCard"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
##
request = container.REQUEST
response =  request.response

pm=context.portal_membership
if pm.isAnonymousUser():
    context.plone_utils.addPortalMessage("Please log in first")
    response.redirect("%s?came_from=%s" % ('login_form', context.absolute_url()))
    return

member = pm.getAuthenticatedMember()
homeFolder = pm.getHomeFolder()
theTime = str(int(context.ZopeTime()))
appId = 'timeconflictcard_' + member.getId() + theTime
homeFolder.invokeFactory("TimeConflictCard", appId)
msg = "A new time conflict card has been created for you.  You may now fill in the details by clicking on the purple 'Edit request' button below." 

context.plone_utils.addPortalMessage(msg)
#state.setNextAction('redirect_to:string:%s'%homeFolder.absolute_url())
response.redirect("%s/%s?portal_status_message=%s" % (homeFolder.absolute_url(), appId, msg))
#return state
