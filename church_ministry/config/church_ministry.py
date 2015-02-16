from frappe import _

def get_data():
	return [
		{
			"label": _("Documents"),
			"icon": "icon-star",
			"items": [
				{
					"type": "page",
					"name": "Assign For Followup",
					"icon": "icon-sitemap",
					"label": _("Assign For Followup"),
					"route": "assign-for-followup",
					"description": _("Assign Members For FTV Followup."),
					"doctype": "Member",
				},
				{
					"type":"doctype",
					"name": "Foundation School Exam",
					"description": _("Foundation School Exam Attendance/Results")
				},
				{
					"type":"doctype",
					"name": "Event Attendance",
					"description": _("Event Attendance")
				},
			]
		},
	]
