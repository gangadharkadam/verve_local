# Copyright (c) 2015, New Indictrans Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc
from frappe import throw, _, msgprint
import frappe.share
from frappe.utils import cstr,now,add_days,nowdate

class AttendanceRecord(Document):
	def autoname(self):
		from frappe.model.naming import make_autoname
		if self.meeting_category=='Cell Meeting':
			self.name = make_autoname(self.cell + '/' + 'CELL' + 'ATT' + '.####')
		else:
			sub=self.meeting_sub[:3].upper()
			self.name = make_autoname(self.cell + '/' + sub + 'ATT' + '.####')
	
	def load_participents(self):
		self.set('invitation_member_details', [])
		member_ftv=''
		if self.cell:
			member_ftv = frappe.db.sql("select name,ftv_name,email_id from `tabFirst Timer` where cell='%s' and approved=0 union select name,member_name,email_id from `tabMember` where cell='%s' "%(self.cell,self.cell))
		elif self.church:
			member_ftv = frappe.db.sql("select name,ftv_name,email_id from `tabFirst Timer` where church='%s' and approved=0 union select name,member_name,email_id from `tabMember` where church='%s'"%(self.church,self.church))	
		for d in member_ftv:
			child = self.append('invitation_member_details', {})
			child.member = d[0]
			child.member_name = d[1]
			child.email_id = d[2]

def validate_duplicate(doc,method):
	if doc.get("__islocal"):
		fdate=doc.from_date.split(" ")
		f_date=fdate[0]
		tdate=doc.to_date.split(" ")
		t_date=tdate[0]
		res=frappe.db.sql("select name from `tabAttendance Record` where (cell='%s' or church='%s') and from_date like '%s%%' and to_date like '%s%%'"%(doc.cell,doc.church,f_date,t_date))
		frappe.errprint(res)
		if res:
			frappe.throw(_("Attendance Record '{0}' is already created for same details on same date '{1}'").format(res[0][0],f_date))

		if doc.from_date and doc.to_date:
			if doc.from_date >= doc.to_date:
				frappe.throw(_("To Date should be greater than From Date..!"))

		if len(doc.invitation_member_details)<1:
			frappe.throw(_("Attendance Member table is empty.There should be at least 1 member in attendance list. Please load members in table."))
