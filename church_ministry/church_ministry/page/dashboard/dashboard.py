# Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
# MIT License. See license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils import cstr,now,add_days

@frappe.whitelist()
def get_revenue():
	return {
		"get_revenue": frappe.db.sql("select name,round(lat) from `tabMember` ",as_list=1)
	}

@frappe.whitelist()
def get_todo():
	return {
		"get_todo": frappe.db.sql("select name,status,priority,date,description from `tabToDo` limit 10",as_list=1)
	}


@frappe.whitelist()
def get_event():
	return {
		"get_event": frappe.db.sql("select name,subject,address,starts_on from `tabEvent` limit 3",as_list=1)
	}

@frappe.whitelist()
def get_meter():
	result={}
	members=frappe.db.sql("select ifnull(count(name),0 )from `tabMember` ")
	ftvcl=frappe.db.sql("select ifnull(count(name),0 ) from `tabFirst Time Visitor` where ftv_type='Cell' ")
	ftvch=frappe.db.sql("select ifnull(count(name),0 ) from `tabFirst Time Visitor` where ftv_type='Church' ")
	nccl=frappe.db.sql("select ifnull(count(name),0 ) from `tabFirst Time Visitor` where ftv_type='Cell' and is_new_born=1 ")
	ncch=frappe.db.sql("select ifnull(count(name),0 ) from `tabFirst Time Visitor` where ftv_type='Church' and is_new_born=1 ")
	result['members']=members
	result['ftvcl']=ftvcl
	result['ftvch']=ftvch
	result['nccl']=nccl
	result['ncch']=ncch
	return {
		"result": result
	}