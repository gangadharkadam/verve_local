# Copyright (c) 2013, New Indictrans Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe import throw, _, msgprint

class PCFMaster(Document):
	pass


def validate_duplicate(doc,method):
	if doc.get("__islocal"):
		res=frappe.db.sql("select name from `tabPCF Master` where pcf_name='%s' and pcf_code='%s' and church='%s'"%(doc.pcf_name,doc.pcf_code,doc.church))
		if res:
			frappe.throw(_("Another PCF '{0}' With PCF Name '{1}' and PCF Code '{2}' exist in Church '{3}'..!").format(res[0][0],doc.pcf_name,doc.pcf_code,doc.church))
