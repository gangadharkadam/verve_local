# Copyright (c) 2013, New Indictrans Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class EventAttendance(Document):
	pass



@frappe.whitelist()
def loadtable(cell):
	return {
		"ftv": [frappe.db.sql("select name,ftv_name from `tabFirst Time Visitor` where cell='%s' union select name,member_name from `tabMember` where cell='%s'"%(cell,cell))]
		}