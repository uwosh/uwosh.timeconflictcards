if hasattr(context, 'portal_type') and context.portal_type == 'TimeConflictCard' and hasattr(context, 'instructorID2'):
  return context.getInstructorID2()
else:
  return None
