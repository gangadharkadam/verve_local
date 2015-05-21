# Copyright (c) 2013, New Indictrans Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe import throw, _, msgprint
import json
from frappe.utils import getdate, validate_email_add, cint

class Member(Document):

	
	def on_update(self):
		# pass
		usr_id=frappe.db.sql("select name from `tabUser` where name='%s'"%(self.email_id),as_list=1)
		if self.flag=='not' and self.email_id:
			# frappe.errprint("user creation")
			# if  self.member_designation=='PCF Leader':
			# 	c_user = self.pcf
			# 	r_user = 'PCF Leader'
			# 	perm = 'PCFs'
			# elif self.member_designation=='Sr.Cell Leader':
			# 	c_user = self.senior_cell
			# 	r_user = 'Senior Cell Leader'
			# 	perm = 'Senior Cells'
			# elif self.member_designation=='Cell Leader':
			# 	c_user = self.cell
			# 	r_user = 'Cell Leader'
			# 	perm = 'Cells'
			# elif self.member_designation=='Member':
			# 	c_user = self.name
			# 	r_user = 'Member'
			# 	perm = 'Member'
			# elif self.member_designation=='Bible Study Class Teacher':
			# 	c_user = self.church
			# 	r_user = 'Bible Study Class Teacher'
			# 	perm = 'Churches'

			if not usr_id:
				u = frappe.new_doc("User")
				u.email=self.email_id
				u.first_name = self.member_name
				u.new_password = 'password'
				frappe.flags.mute_emails = False
				u.insert()
				frappe.flags.mute_emails = True
			r=frappe.new_doc("UserRole")
			r.parent=self.email_id
			r.parentfield='user_roles'
			r.parenttype='User'
			r.role='Member'
			r.insert()
			v = frappe.new_doc("DefaultValue")
			v.parentfield = 'system_defaults'
			v.parenttype = 'User Permission'
			v.parent = self.email_id
			v.defkey = 'Member'
			v.defvalue = self.name 
			v.insert()
			frappe.db.sql("update `tabMember` set flag='SetPerm' where name='%s'"%(self.name))
			frappe.db.commit()
			self.user_id = self.email_id

def get_list(doctype, txt, searchfield, start, page_len, filters):
	conditions=get_conditions(filters)
	if conditions:
		value=frappe.db.sql("select name from `tab%s` where %s"%(filters.get('doctype'),conditions))
		return value
	else :
		value=frappe.db.sql("select name from `tab%s`"%(filters.get('doctype')))
		return value

def get_conditions(filters):
	cond=[]
	if filters.get('cell'):
		cond.append('cell="%s"'%(filters.get('cell')))
	elif filters.get('senior_cell'):
		cond.append('senior_cell="%s"'%(filters.get('senior_cell')))
	elif filters.get('pcf'):
		cond.append('pcf="%s"'%(filters.get('pcf')))
	elif filters.get('church'):
		cond.append('church="%s"'%(filters.get('church')))
	elif filters.get('church_group'):
		cond.append('church_group="%s"'%(filters.get('church_group')))
	elif filters.get('zone'):
		cond.append('zone="%s"'%(filters.get('zone')))
	elif filters.get('region'):
		cond.append('region="%s"'%(filters.get('region')))
	return ' or '.join(cond)  


def validate_birth(doc,method):
		#frappe.errprint("in date of birth ")
		if doc.date_of_birth and doc.date_of_join and getdate(doc.date_of_birth) >= getdate(doc.date_of_join):		
			frappe.throw(_("Date of Joining '{0}' must be greater than Date of Birth '{1}'").format(doc.date_of_join, doc.date_of_birth))
		
		# if doc.baptisum_status=='Yes':
		# 	if not doc.baptism_when or not doc.baptism_where :
		# 		frappe.throw(_("When and Where is Mandatory if 'Baptisum Status' is 'Yes'..!"))

		if doc.email_id:
			if not validate_email_add(doc.email_id):
				frappe.throw(_('{0} is not a valid email id').format(doc.email_id))

@frappe.whitelist()
def dashboard(user):
	#frappe.errprint(user)
	data={}
	new_visitor=frappe.db.sql("select count(name) from `tabFirst Timer` where creation between date_sub(now(),INTERVAL 1 YEAR) and now()")
	if new_visitor :
		data['new_visitor']=new_visitor[0][0] 
	else:
		data['new_visitor']='0'
	first_timers=frappe.db.sql("select count(name) from `tabFirst Timer` where creation between date_sub(now(),INTERVAL 1 YEAR) and now()")
	if first_timers:
		data['first_timers']=first_timers[0][0]
	else:
		data['first_timers']='0'
	visitor_last_months=frappe.db.sql("select count(name) from `tabFirst Timer` where creation between date_sub(now(),INTERVAL 1 WEEK) and now()")
	if visitor_last_months:
		data['visitor_last_months']=visitor_last_months[0][0]
	else:
		data['visitor_last_months']='0'
	membership_strength=frappe.db.sql("select MONTHNAME(creation) as Month, count(name) as `New Users`,count(name) as Revisited from `tabFirst Timer` where creation between date_sub(now(),INTERVAL 1 Year) and now() group by year(creation), MONTH(creation)",as_list=1)
	if membership_strength:
		data['membership_strength']=membership_strength
	else:
		data['membership_strength']='0'
	partnership=frappe.db.sql("select MONTHNAME(creation) as Month, count(name) as `New Users`,count(name) as Revisited from `tabFirst Timer` where creation between date_sub(now(),INTERVAL 1 Year) and now() group by year(creation), MONTH(creation)",as_list=1)
	if partnership:
		data['partnership']=partnership
	else:
		data['partnership']='0'
	return data


@frappe.whitelist()
def user_roles(user):
	data={}
	roles=frappe.db.sql("select role from `tabUserRole` where parent=%(user)s", {"user":user},as_dict=True)
	data['roles']=roles
	user_values=frappe.db.sql("select defkey,defvalue from `tabDefaultValue`  where parent=%(user)s", {"user":user},as_dict=True)
	data['user_values']=user_values
	return data


@frappe.whitelist()
def create_meeting(user,data,_type='POST'):
		ma = frappe.get_doc(json.loads(data))
		ma.insert()
		frappe.db.commit()
		return ma.name

@frappe.whitelist()
def meetings_list(user):
	from erpnext.controllers.queries import get_match_cond
	qry="select name as `Meeting Name`,meeting_subject as `Meeting Subject`,from_date as `Meeting Date`,venue from `tabAttendance Record` where 1=1 "+ get_match_cond('Attendance Record').replace('\n','').replace("\"","'").replace('\t','')
	#frappe.errprint(qry)
	data=frappe.db.sql(qry,as_dict=True)
	return data

@frappe.whitelist()
def meetings_details():
	data=frappe.db.sql(qry,as_dict=True)
	return data


@frappe.whitelist()
def meetings_members(meeting_id):
	data=frappe.db.sql("select name,member,member_name,present from `tabInvitation Member Details` where parent=%s",meeting_id,as_dict=True)
	return data


@frappe.whitelist()
def meetings_attendance(data):
	for record in json.loads(data):
		if not record['present'] : 
			record['present']=0
		frappe.db.sql("update `tabInvitation Member Details` set present=%s where name=%s",(record['present'],record['name']))
	return "Updated Attendance"


@frappe.whitelist()
def meetings_list_member(user):
	data=frappe.db.sql("select a.name as `Meeting Name`,a.meeting_category as `Meeting Category`, a.meeting_subject as `Meeting Subject`,a.from_date as `From Date`,a.to_date,a.venue,b.name,ifnull(b.present,0) as `present` from `tabAttendance Record`  a,`tabInvitation Member Details` b where a.name=b.parent and b.email_id=%s",user,as_dict=True)
	return data


@frappe.whitelist()
def mark_my_attendance(data):
	for record in json.loads(data):
		if not record['present'] : 
			record['present']=0
		frappe.db.sql("update `tabInvitation Member Details` set present=%s where name=%s",(record['present'],record['name']))
	return "Updated Attendance"













