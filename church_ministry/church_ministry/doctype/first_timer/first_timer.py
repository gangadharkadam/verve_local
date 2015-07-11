# Copyright (c) 2015, New Indictrans Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.utils import getdate, validate_email_add, cint
from frappe import throw, _, msgprint
from frappe.model.mapper import get_mapped_doc
from frappe import msgprint, _
import frappe, os, json

class FirstTimer(Document):
	# pass
	def validate(self):
		if self.date_of_birth and self.date_of_visit and getdate(self.date_of_birth) >= getdate(self.date_of_visit):		
			frappe.throw(_("Date of First Visit '{0}' must be greater than Date of Birth '{1}'").format(self.date_of_visit, self.date_of_birth))

		# if self.baptisum_status=='Yes':
		# 	if not self.baptism_when or not self.baptism_where :
		# 		frappe.throw(_("When and Where is Mandatory if 'Baptisum Status' is 'Yes'..!"))

		if self.email_id:
			if not validate_email_add(self.email_id):
				frappe.throw(_('{0} is not a valid email id').format(self.email_id))

		self.validate_phone()

	def validate_phone(self):
            if self.get("__islocal"):
                phone_list=frappe.db.sql("select phone_1 from `tabFirst Timer`",as_list=1)
                for phone in phone_list:
					if self.phone_1:
						if self.phone_1==phone[0]:
							frappe.throw(_("Duplicate entry for phone no..."))
						else:
							if self.phone_1.isdigit() and len(self.phone_1)>9 and len(self.phone_1)<11:
								pass    
							else:
								frappe.throw(_("Please enter valid 10 digits phone no."))
@frappe.whitelist()
def make_member(source_name, target_doc=None):
	return _make_member(source_name, target_doc)

def _make_member(source_name, target_doc=None, ignore_permissions=False):
	def set_missing_values(source, target):
		pass

	doclist = get_mapped_doc("First Timer", source_name,
		{"First Timer": {
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
		# if doc.baptisum_status=='Yes':
		# 	if not doc.when or doc.where :
		# 		frappe.throw(_("When and Where is Mandatory if 'Baptisum Status' is 'Yes'..!"))

@frappe.whitelist()
def ismember(name):
	converted=frappe.db.sql("select name from `tabMember` where ftv_id_no='%s'"%(name))
	if converted:
		return "Yes"
	else:
		return "No"


@frappe.whitelist()
def set_higher_values(args):
    args = json.loads(args)
    keys = ["region", "zone", "church_group", "church", "pcf", "senior_cell", "name"]
    out = frappe.db.get_all("Cells", fields=keys, filters={'name':args['name']})
    if out:
          return out[0]
