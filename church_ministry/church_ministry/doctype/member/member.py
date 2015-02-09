# Copyright (c) 2013, New Indictrans Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe import throw, _, msgprint
from frappe.utils import getdate, validate_email_add, cint

class Member(Document):
	pass


def validate_birth(doc,method):
		#frappe.errprint("in date of birth ")
		if doc.date_of_birth and doc.date_of_join and getdate(doc.date_of_birth) >= getdate(doc.date_of_join):		
			frappe.throw(_("Date of Joining '{0}' must be greater than Date of Birth '{1}'").format(doc.date_of_join, doc.date_of_birth))
		if doc.baptisum_status=='Yes':
			if not doc.when or doc.where :
				frappe.throw(_("When and Where is Mandatory if 'Baptisum Status' is 'Yes'..!"))

