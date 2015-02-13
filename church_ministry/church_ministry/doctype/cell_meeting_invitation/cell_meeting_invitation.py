# Copyright (c) 2013, New Indictrans Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class CellMeetingInvitation(Document):
	# pass
	def __init__(self):
		pass
	
	def get_members(self):
		members=frappe.db.sql("select name,member_name,email_id from `tabMember`",as_list=1)
		frappe.errprint(members)
		return {
			'members' : members
		}
