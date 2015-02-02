# Copyright (c) 2013, New Indictrans Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe import throw, _, msgprint

class ZoneMaster(Document):
	pass


def validate_duplicate(doc,method):
	if doc.get("__islocal"):
		res=frappe.db.sql("select name from `tabZone Master` where zone_name='%s' and zone_code='%s' and region='%s'"%(doc.zone_name,doc.zone_code,doc.region))
		if res:
			frappe.throw(_("Another Zone '{0}' With Zone Name '{1}' and Zone Code '{2}' exist in Region '{3}'..!").format(res[0][0],doc.zone_name,doc.zone_code,doc.region))
