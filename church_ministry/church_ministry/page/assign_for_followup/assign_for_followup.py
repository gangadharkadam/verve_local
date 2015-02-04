# Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
# MIT License. See license.txt

from __future__ import unicode_literals
import frappe
import frappe.defaults

@frappe.whitelist()
def ftv():
	return {
		"ftv": [d[0] for d in frappe.db.sql("""select name from `tabFirst Time Visitor` """)]
	}

@frappe.whitelist()
def loadmembers():
	return {
		"members": [frappe.db.sql("""select name,member_name,sex from `tabMember` """)]
	}
