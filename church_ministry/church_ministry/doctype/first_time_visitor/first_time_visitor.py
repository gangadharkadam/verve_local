# Copyright (c) 2013, New Indictrans Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.utils import getdate, validate_email_add, cint
from frappe import throw, _, msgprint
from frappe.model.mapper import get_mapped_doc

class FirstTimeVisitor(Document):
	pass


@frappe.whitelist()
def make_member(source_name, target_doc=None):
	return _make_member(source_name, target_doc)

def _make_member(source_name, target_doc=None, ignore_permissions=False):
	def set_missing_values(source, target):
		pass

	doclist = get_mapped_doc("First Time Visitor", source_name,
		{"First Time Visitor": {
			"doctype": "Member",
			"field_map": {				
				"name":"ftv_id_no",
				"ftv_name":"member_name"
			}
		}}, target_doc, set_missing_values, ignore_permissions=ignore_permissions)

	return doclist

def validate_birth(doc,method):
		if doc.date_of_birth and doc.date_of_visit and getdate(doc.date_of_birth) >= getdate(doc.date_of_visit):		
			frappe.throw(_("Date of Visit '{0}' must be greater than Date of Birth '{1}'").format(doc.date_of_visit, doc.date_of_birth))
		if doc.baptisum_status=='Yes':
			if not doc.when or doc.where :
				frappe.throw(_("When and Where is Mandatory if 'Baptisum Status' is 'Yes'..!"))

