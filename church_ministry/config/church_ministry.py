from frappe import _

def get_data():
	return [
		{
			"label": _("Documents"),
			"icon": "icon-star",
			"items": [
				
				{
					"type":"doctype",
					"name": "Member",
					"description": _("Member Database")
				},	
				{
					"type":"doctype",
					"name": "First Timer",
					"description": _("First Timer Database")
				},
		        {
					"type":"doctype",
					"name": "Invitees and Contacts",
					"description": _("Invitees & Contacts")
				},								
				# {
				# 	"type":"doctype",
				# 	"name": "Cell Meeting Invitation",
				# 	"description": _("Cell Meeting Invitation Database")
				# },
				{
					"type":"doctype",
					"name": "Attendance Record",
					"label": _("Attendance Records"),
					"description": _("Meeting Attendance Records Database")
				},	
				{
					"type":"doctype",
					"name": "Foundation School Attendance",
					"description": _("Foundation School Attendance")
				},											

				{
					"type":"doctype",
					"name": "Foundation School Exam",
					"description": _("Foundation School Exam Attendance/Results")
				},
				{
					"type":"doctype",
					"name": "Partnership Record",
					"description": _("Partnership Record")
				},
				{
					"type":"doctype",
					"name": "Event",
					"description": _("Event")
				},
				{
					"type":"doctype",
					"name": "Task",
					"description": _("Task Database")
				},				
				{
					"type":"doctype",
					"name": "SMS Credits Request",
					"description": _("SMS Credits Request and Approval ")
				},
			]
		},
		{
			"label": _("Tools"),
			"icon": "icon-star",
			"items": [
				{
					"type": "page",
					"name": "assign-for-followup",
					"label": _("Assign For Followup"),
					"icon": "icon-bar-chart",
					"description": _("Assign For Followup")
				},
				{
					"type": "page",
					"name": "convert-invitees-and",
					"label": _("Convert Invitees & Contacts to FT"),
					"icon": "icon-bar-chart",
					"description": _("Convert Invitees & Contacts to FT")
				},

				{
					"type": "page",
					"name": "approve-ftv-to-membe",
					"label": _("Eligible FT List  for Membership"),
					"icon": "icon-bar-chart",
					"description": _("Eligible FT List  for Membership")
				},
				{
					"type": "page",
					"name": "open-office",
					"label": _("Audio meeting"),
					"icon": "icon-bar-chart",
					"description": _("Audio meeting")
				},
				# {
				# 	"type": "page",
				# 	"name": "convert-ftv-to-membe",
				# 	"label": _("Convert FTV to Member"),
				# 	"icon": "icon-bar-chart",
				# 	"description": _("Convert FTV to Member")
				# },
				{
					"type":"doctype",
					"name": "Event Attendance",
					"description": _("Event Attendance Database")
				},
				{
					"type": "page",
					"name": "convert-invitees-and",
					"label": _("Convert Invitees & Contacts to FT"),
					"icon": "icon-bar-chart",
					"description": _("Convert Invitees & Contacts to FT")
				},
				{
					"type": "page",
					"name": "send-sms",
					"label": _("Send SMS"),
					"icon": "icon-bar-chart",
					"description": _("Send SMS")
				},		
				{
					"type": "page",
					"name": "data-import-tool",
					"label": _("Import / Export Data"),
					"icon": "icon-bar-chart",
					"description": _("Import / Export Data from .csv files.")
				},	
			]
		},


		{
			"label": _("Setup"),
			"icon": "icon-star",
			"items": [
				{
					"type":"doctype",
					"name": "Regions",
					"description": _("Regions")
				},
				{
					"type":"doctype",
					"name": "Zones",
					"description": _("Zones")
				},
				{
					"type":"doctype",
					"name": "Group Churches",
					"description": _("Group Churches")
				},
				{
					"type":"doctype",
					"name": "Churches",
					"description": _("Churches")
				},				
				{
					"type":"doctype",
					"name": "PCFs",
					"description": _("PCFs")
				},
				{
					"type":"doctype",
					"name": "Senior Cells",
					"description": _("Senior Cells")
				},
				{
					"type":"doctype",
					"name": "Cells",
					"description": _("Cells")
				},				
				{
					"type":"doctype",
					"name": "Foundation School Exams",
					"description": _("Foundation School Exams")
				},							
				{
					"type":"doctype",
					"name": "Foundation School Grades",
					"description": _("Foundation School Grades")
				},				
				{
					"type":"doctype",
					"name": "Partnership Arms",
					"description": _("Partnership Arms Master")
				},
			]
		},
	]
