# Copyright (c) 2013, New Indictrans Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class CellMeetingInvitation(Document):
	
	def  load_table(self):
		self.set('invitation_member_details', [])
		if self.cell:
			member_ftv = frappe.db.sql("select name,member_name,email_id from `tabMember` where cell='%s'"%(self.cell))
		elif self.church:
			member_ftv = frappe.db.sql("select name,member_name,email_id from `tabMember` where church='%s'"%(self.church))
		for d in member_ftv:
			child = self.append('invitation_member_details', {})
			child.member = d[0]
			child.member_name = d[1]
			child.email_id = d[2]



