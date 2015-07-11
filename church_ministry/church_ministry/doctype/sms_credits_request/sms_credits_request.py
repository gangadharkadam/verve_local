# -*- coding: utf-8 -*-
# Copyright (c) 2015, New Indictrans Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.utils import getdate, validate_email_add, cint,flt

class SMSCreditsRequest(Document):

	def validate(self):
		if not self.get("__islocal"):
			if not self.allocated_credits and frappe.session.user=='Administrator':
				frappe.throw("Please enter Allocated Credits before save..!")
		if self.requested_credits <=0  :
			frappe.throw("Please enter Valid Credits before save..!")
		if self.allocated_credits and self.allocated_credits <=0 :
			frappe.throw("Please enter Valid Credits before save..!")
		#frappe.sendmail(recipients="email.kadam@gmail.com", sender='gangadhar.k@indictranstech.com', content="msg_member", subject='')
	
	def on_submit(self):
		obj=frappe.get_doc("User",self.user_name)
		obj.sms_credits=cint(obj.sms_credits)+cint(self.allocated_credits)
		obj.save(ignore_permissions=True)
		obj1=frappe.get_doc("User","Administrator")
		obj1.sms_credits=cint(obj1.sms_credits)-cint(self.allocated_credits)
		obj1.save(ignore_permissions=True)


@frappe.whitelist()
def check_balance():
	return frappe.db.sql("select sms_credits from tabUser where name='Administrator'")


