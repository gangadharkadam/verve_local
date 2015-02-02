# Copyright (c) 2013, New Indictrans technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe import throw, _, msgprint

class SeniorCellMaster(Document):
	pass


def validate_duplicate(doc,method):
	if doc.get("__islocal"):
		res=frappe.db.sql("select name from `tabSenior Cell Master` where senior_cell_name='%s' and senior_cell_code='%s' and pcf='%s'"%(doc.senior_cell_name,doc.senior_cell_code,doc.pcf))
		if res:
			frappe.throw(_("Another Senior Cell '{0}' With Senior Cell Name '{1}' and Senior Cell Code '{2}' exist in PCF '{3}'..!").format(res[0][0],doc.senior_cell_name,doc.senior_cell_code,doc.pcf))

