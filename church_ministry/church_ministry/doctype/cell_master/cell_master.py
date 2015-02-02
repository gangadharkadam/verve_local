# Copyright (c) 2013, New Indictrans technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe import throw, _, msgprint

class CellMaster(Document):
	pass


def validate_duplicate(doc,method):
	if doc.get("__islocal"):
		res=frappe.db.sql("select name from `tabCell Master` where cell_name='%s' and cell_code='%s' and senior_cell='%s'"%(doc.cell_name,doc.cell_code,doc.senior_cell))
		if res:
			frappe.throw(_("Another Cell '{0}' With Cell Name '{1}' and Cell Code '{2}' exist in Senior Cell '{3}'..!").format(res[0][0],doc.cell_name,doc.cell_code,doc.senior_cell))

