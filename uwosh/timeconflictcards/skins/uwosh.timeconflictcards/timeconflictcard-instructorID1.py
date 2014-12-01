if hasattr(context, 'portal_type') and context.portal_type == 'TimeConflictCard' and hasattr(context, 'instructorID1'):
  return context.getInstructorID1()
else:
  return None
