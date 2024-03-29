# Copyright (c) 2013, New Indictrans Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc

class EventAttendance(Document):
	def  load_table(self):
		if self.region:
			key='region'
			value=self.region

		elif self.zone:
			key='zone'
			value=self.zone

		elif self.church_group:
			key='church_group'
			value=self.church_group

		elif self.church:
			key='church'
			value=self.church

		elif self.pcf:
			key='pcf'
			value=self.pcf

		elif self.senior_cell:
			key='senior_cell'
			value=self.senior_cell

		elif self.cell:
			key='cell'
			value=self.cell

		self.set('event_attendace_details', [])
		member_ftv = frappe.db.sql("select name,ftv_name from `tabFirst Timer` where %s='%s' union select \
		name,member_name from `tabMember` where %s='%s' union select name,invitee_contact_name from `tabInvitees and Contacts` where %s='%s'"%(key,value,key,value,key,value))
		for d in member_ftv:
			child = self.append('event_attendace_details', {})
			child.id = d[0]
			child.person_name = d[1]

@frappe.whitelist()
def create_event_attendance(source_name, target_doc=None):
	def postprocess(source, doc):
		pass

	doc = get_mapped_doc("Event", source_name, {
		"Event": {
			"doctype": "Event Attendance",
			# "validation": {
			# 	"docstatus": ["=", 1]
			# }
		},
		"Event Attendace Details": {
			"doctype": "Event Attendace Details",
			"field_map": {
				# "parent": "sales_order_no",
				# "stock_uom": "uom"
			}
		}
	}, target_doc, postprocess)

	return doc

