# Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
# MIT License. See license.txt

from __future__ import unicode_literals
import frappe
import frappe.defaults

@frappe.whitelist()
def ftv():
	return {
		"ftv": [d[0] for d in frappe.db.sql("""select name from `tabFirst Time Visitor` """)]
	}

@frappe.whitelist()
def ftvdetails(ftv):
	query="select ftv_name,sex,YEAR(CURDATE()) - YEAR(date_of_birth)- (DATE_FORMAT(CURDATE(), '%m%d') < DATE_FORMAT(date_of_birth, '%m%d')) as age,address from `tabFirst Time Visitor` where name='"+ftv+"'"
	return {
		"ftv": [frappe.db.sql(query)]
	}

@frappe.whitelist()
def loadmembers(ftv):
	a="select b.name,b.member_name,b.sex,YEAR(CURDATE()) - YEAR(b.date_of_birth)- (DATE_FORMAT(CURDATE(), '%m%d') < DATE_FORMAT(b.date_of_birth, '%m%d')) as age,6371 * 2 * ASIN(SQRT(POWER(SIN((a.lat - abs(b.lat)) * pi()/180 / 2),2) + COS(a.lat * pi()/180 ) * COS(abs(b.lat) * pi()/180) * POWER(SIN((a.lon - a.lon) * pi()/180 / 2), 2) )) as distance from  `tabFirst Time Visitor` a,`tabMember` b where a.name='"+ftv+"' order by distance asc ,age desc "
	#frappe.errprint(a)
	return {
		"members": [frappe.db.sql(a)]
	}

@frappe.whitelist()
def assignmember(memberid,ftv):
	frappe.db.sql("""update `tabFirst Time Visitor` set ftv_owner='%s' where name='%s' """ % (memberid,ftv))
	recipients='gangadhar.k@indictranstech.com'
	member=frappe.db.sql("select member_name,email_id from `tabMember` where name='%s'"%(memberid))
	ftvdetails=frappe.db.sql("select ftv_name,email_id from `tabFirst Time Visitor` where name='%s'"%(ftv))
	msg_member="""Hello %s,<br>
	The First Time visitor '%s' name: '%s' Email ID: '%s' is assigned to you for follow up <br>Regrds,<br>Varve
	"""%(member[0][0],ftv,ftvdetails[0][0],ftvdetails[0][0])
	msg_ftv="""Hello %s,<br>
	The Member '%s' name: '%s' Email ID: '%s' is assigned to you for follow up <br>Regrds,<br>Varve
	"""%(ftvdetails[0][0],memberid,member[0][0],member[0][0])
	frappe.sendmail(recipients=member[0][1], sender='gangadhar.k@indictranstech.com', content=msg_member, subject='Assign for follow up')
	frappe.sendmail(recipients=ftvdetails[0][1], sender='gangadhar.k@indictranstech.com', content=msg_ftv, subject='Assign for follow up')
	return "Done"
