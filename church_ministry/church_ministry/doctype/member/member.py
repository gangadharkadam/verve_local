# Copyright (c) 2013, New Indictrans Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import json
from frappe.model.document import Document
from frappe import throw, _, msgprint
from frappe.utils import getdate, validate_email_add, cint,cstr,now
import base64

class Member(Document):

        def validate(self):
            self.validate_phone()

        def on_update(self):
                # pass
                usr_id=frappe.db.sql("select name from `tabUser` where name='%s'"%(self.email_id),as_list=1)
                if self.flag=='not' and self.email_id:
                        # frappe.errprint("user creation")
                        # if  self.member_designation=='PCF Leader':
                        #       c_user = self.pcf
                        #       r_user = 'PCF Leader'
                        #       perm = 'PCFs'
                        # elif self.member_designation=='Sr.Cell Leader':
                        #       c_user = self.senior_cell
                        #       r_user = 'Senior Cell Leader'
                        #       perm = 'Senior Cells'
                        # elif self.member_designation=='Cell Leader':
                        #       c_user = self.cell
                        #       r_user = 'Cell Leader'
                        #       perm = 'Cells'
                        # elif self.member_designation=='Member':
                        #       c_user = self.name
                        #       r_user = 'Member'
                        #       perm = 'Member'
                        # elif self.member_designation=='Bible Study Class Teacher':
                        #       c_user = self.church
                        #       r_user = 'Bible Study Class Teacher'
                        #       perm = 'Churches'

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

        def validate_phone(self):
            if self.get("__islocal"):
                phone_list=frappe.db.sql("select phone_1 from `tabMember`",as_list=1)
                for phone in phone_list:
                    if self.phone_1:
                        if self.phone_1==phone[0]:
                            frappe.throw(_("Duplicate entry for phone no..."))
                        else:
                            if self.phone_1.isdigit() and len(self.phone_1)>9 and len(self.phone_1)<11:
                                pass    
                            else:
                                frappe.throw(_("Please enter valid 10 digits phone no."))
           
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
                #       if not doc.baptism_when or not doc.baptism_where :
                #               frappe.throw(_("When and Where is Mandatory if 'Baptisum Status' is 'Yes'..!"))

                if doc.email_id:
                        if not validate_email_add(doc.email_id):
                                frappe.throw(_('{0} is not a valid email id').format(doc.email_id))



### web sevices
# gangadhar

@frappe.whitelist(allow_guest=True)
def user_roles(data):
	"""
	Get user name and password from user and returns roles and its def key and defvalue
	"""
	dts=json.loads(data)
	qry="select user from __Auth where user='"+cstr(dts['username'])+"' and password=password('"+cstr(dts['userpass'])+"') "
	valid=frappe.db.sql(qry)
	if not valid:
		return {
			"status":"401",
			"message":"User name or Password is incorrect"
		}
	else:
		data={}
		roles=frappe.db.sql("select role from `tabUserRole` where parent=%(user)s", {"user":dts['username']},as_dict=True)
		data['roles']=roles
		user_values=frappe.db.sql("select defkey,defvalue from `tabDefaultValue`  where parent=%(user)s", {"user":dts['username']},as_dict=True)
		data['user_values']=user_values
		return data


@frappe.whitelist(allow_guest=True)
def create_senior_cells(data):
	"""
	Need to check validation/ duplication  etc

	"""
        dts=json.loads(data)
        qry="select user from __Auth where user='"+cstr(dts['username'])+"' and password=password('"+cstr(dts['userpass'])+"') "
        valid=frappe.db.sql(qry)
        if not valid:
                return {
                  "status":"401",
                  "message":"User name or Password is incorrect"
                }
               
        if not frappe.has_permission(doctype="Senior Cells", ptype="create",user=dts['username']):
                return {
                  "status":"403",
                  "message":"You have no permission to create Senior Cell"
                }
                
        obj=frappe.new_doc("Senior Cells")
        obj.senior_cell_name=dts['senior_cell_name']
        obj.senior_cell_code=dts['senior_cell_code']
        obj.meeting_location=dts['meeting_location']
        obj.zone=dts['zone']
        obj.region=dts['region']
        obj.church_group=dts['church_group']
        obj.church=dts['church']
        obj.pcf=dts['pcf']
        obj.contact_phone_no=dts['contact_phone_no']
        obj.contact_email_id=dts['contact_email_id']
        obj.insert(ignore_permissions=True)
        return "Successfully created senior Cell '"+obj.name+"'"

@frappe.whitelist(allow_guest=True)
def create_cells(data):
	"""
	Need to check validation/ duplication  etc
	"""
        dts=json.loads(data)
        qry="select user from __Auth where user='"+cstr(dts['username'])+"' and password=password('"+cstr(dts['userpass'])+"') "
        valid=frappe.db.sql(qry)
        if not valid:
                return {
                  "status":"401",
                  "message":"User name or Password is incorrect"
                }
        if not frappe.has_permission(doctype="Cells", ptype="create",user=dts['username']):
                return {
                  "status":"403",
                  "message":"You have no permission to create Cell"
                }
        else:
                obj=frappe.new_doc("Cells")
                obj.cell_name=dts['cell_name']
                obj.cell_code=dts['cell_code']
                obj.meeting_location=dts['meeting_location']
                obj.address=dts['address']
                obj.senior_cell=dts['senior_cell']
                obj.zone=dts['zone']
                obj.region=dts['region']
                obj.church_group=dts['church_group']
                obj.church=dts['church']
                obj.pcf=dts['pcf']
                obj.contact_phone_no=dts['contact_phone_no']
                obj.contact_email_id=dts['contact_email_id']
                obj.insert(ignore_permissions=True)
                ret={
                        "message":"Successfully created Cell '"+obj.name+"'"
                }
                return ret


@frappe.whitelist(allow_guest=True)
def create_event(data):
        """
        Need to check validation/ duplication  etc
        """
        dts=json.loads(data)
        qry="select user from __Auth where user='"+cstr(dts['username'])+"' and password=password('"+cstr(dts['userpass'])+"') "
        valid=frappe.db.sql(qry)
        if not valid:
                return {
                  "status":"401",
                  "message":"User name or Password is incorrect"
                }
        if not frappe.has_permission(doctype="Event", ptype="create",user=dts['username']):
                return {
                  "status":"403",
                  "message":"You have no permission to create Cell"
                }
        else:
                obj=frappe.new_doc("Event")
                obj.subject=dts['subject']
                obj.type=dts['type']
                obj.starts_on=dts['starts_on']
                obj.ends_on=dts['ends_on']
                obj.address=dts['address']
                obj.description=dts['description']
                obj.insert(ignore_permissions=True)
                ret={
                        "message":"Successfully created Event '"+obj.name+"'"
                }
                return ret

@frappe.whitelist(allow_guest=True)
def update_event(data):
        """
        Need to check validation/ duplication  etc
        """
        dts=json.loads(data)
        qry="select user from __Auth where user='"+cstr(dts['username'])+"' and password=password('"+cstr(dts['userpass'])+"') "
        valid=frappe.db.sql(qry)
        if not valid:
                return {
                  "status":"401",
                  "message":"User name or Password is incorrect"
                }
        if not frappe.has_permission(doctype="Event", ptype="create",user=dts['username']):
                return {
                  "status":"403",
                  "message":"You have no permission to create Cell"
                }
        else:
                obj=frappe.get_doc("Event",dts['name'])
                obj.subject=dts['subject']
                obj.type=dts['type']
                obj.starts_on=dts['starts_on']
                obj.ends_on=dts['ends_on']
                obj.address=dts['address']
                obj.description=dts['description']
                obj.save(ignore_permissions=True)
                ret={
                        "message":"Successfully updated Event '"+obj.name+"'"
                }
                return ret


@frappe.whitelist(allow_guest=True)
def create_meetings(data):

        """
        No Need to send sms,push notification and email , it should be on attendence update on every user.
                Need to check validation/ duplication  etc
        """
        dts=json.loads(data)
        qry="select user from __Auth where user='"+cstr(dts['username'])+"' and password=password('"+cstr(dts['userpass'])+"') "
        valid=frappe.db.sql(qry)
        if not valid:
        	return {
        		"status":"401",
        		"message":"User name or Password is incorrect"
        	}
        res=frappe.db.sql("select name from `tabAttendance Record` where (cell='%s' or church='%s') and from_date like '%s%%' and to_date like '%s%%'"%(dts['cell'],dts['church'],dts['from_date'],dts['to_date']))
        # if res:
        if not frappe.has_permission(doctype="Attendance Record", ptype="create",user=dts['username']):
                return {
        		"status":"403",
        		"message":"You have no permission to create Meeting Attendance Record"
                }
        fdate=dts['from_date'].split(" ")
        f_date=fdate[0]
        tdate=dts['to_date'].split(" ")
        t_date=tdate[0]
        res=frappe.db.sql("select name from `tabAttendance Record` where (cell='%s' or church='%s') and from_date like '%s%%' and to_date like '%s%%'"%(doc.cell,doc.church,f_date,t_date))
        if res:
            return {
                "status":"401",
                "message":"Attendance Record is already created for same details on same date "
                }
        if doc.from_date and doc.to_date:
            if doc.from_date >= doc.to_date:
                return {
                "status":"402",
                "message":"To Date should be greater than From Date..!"
                }

		obj=frappe.new_doc("Attendance Record")
		obj.meeting_category=dts['meeting_category']
		if dts['meeting_category']=="Cell Meeting":
			obj.meeting_subject=dts['meeting_sub']
		else:
		        obj.meeting_sub=dts['meeting_sub']
		obj.from_date=dts['from_date']
		obj.to_date=dts['to_date']
		obj.venue=dts['venue']
		obj.cell=dts['cell']
		obj.senior_cell=dts['senior_cell']
		obj.zone=dts['zone']
		obj.region=dts['region']
		obj.church_group=dts['church_group']
		obj.church=dts['church']
		obj.pcf=dts['pcf']
		obj.insert(ignore_permissions=True)
		member_ftv=''
		if dts['meeting_category']=="Cell Meeting":
			member_ftv = frappe.db.sql("select name,ftv_name,email_id from `tabFirst Timer` where cell='%s' and approved=0 union select name,member_name,email_id from `tabMember` where cell='%s' "%(dts['cell'],dts['cell']))
		else:
			member_ftv = frappe.db.sql("select name,ftv_name,email_id from `tabFirst Timer` where church='%s' and approved=0 union select name,member_name,email_id from `tabMember` where church='%s'"%(dts['church'],dts['church']))	
		for d in member_ftv:
			child = frappe.new_doc('Invitation Member Details')
			child.member = d[0]
			child.member_name = d[1]
			child.email_id = d[2]
			child.parent=obj.name
			child.parentype="Attendance Record"
			child.parentfield="invitation_member_details"
			child.insert(ignore_permissions=True)
		ret={
			"message":"Successfully created Cell '"+obj.name+"'"
		}
		return ret

@frappe.whitelist(allow_guest=True)
def meetings_list(data):
	"""
	Need to add filter of permitted records for user
	"""
        dts=json.loads(data)
        qry="select user from __Auth where user='"+cstr(dts['username'])+"' and password=password('"+cstr(dts['userpass'])+"') "
        valid=frappe.db.sql(qry)
        if not valid:
                return {
                  "status":"401",
                  "message":"User name or Password is incorrect"
                }
        else:
               qry="select name as meeting_name,meeting_subject , from_date as meeting_date ,venue from `tabAttendance Record`"
               data=frappe.db.sql(qry,as_dict=True)
               return data


@frappe.whitelist(allow_guest=True)
def meetings_members(data):
	"""
	Get all participents of selected meeting
	"""
        dts=json.loads(data)
        qry="select user from __Auth where user='"+cstr(dts['username'])+"' and password=password('"+cstr(dts['userpass'])+"') "
        valid=frappe.db.sql(qry)
        if not valid:
                return {
                  "status":"401",
                  "message":"User name or Password is incorrect"
                }
        else:
                data=frappe.db.sql("select name,member,member_name,present from `tabInvitation Member Details` where parent=%s",dts['meeting_id'],as_dict=True)
                return data


@frappe.whitelist(allow_guest=True)
def meetings_attendance(data):
	"""
	Need to add provision to send sms,push notification and emails on present and absent
	"""
        dts=json.loads(data)
        qry="select user from __Auth where user='"+cstr(dts['username'])+"' and password=password('"+cstr(dts['userpass'])+"') "
        valid=frappe.db.sql(qry)
        if not valid:
                return {
                  "status":"401",
                  "message":"User name or Password is incorrect"
                }
        else:
                for record in dts['records']:
                        if record['present']=='0' or record['present']=='1' :
                                frappe.db.sql("update `tabInvitation Member Details` set present=%s where name=%s",(record['present'],record['name']))
                return "Updated Attendance"


@frappe.whitelist(allow_guest=True)
def meetings_list_member(data):
	"""
	Meeting list of member user
	"""
        dts=json.loads(data)
        qry="select user from __Auth where user='"+cstr(dts['username'])+"' and password=password('"+cstr(dts['userpass'])+"') "
        valid=frappe.db.sql(qry)
        if not valid:
                return {
                  "status":"401",
                  "message":"User name or Password is incorrect"
                }
        else:
                data=frappe.db.sql("select a.name as meeting_name,a.meeting_category as meeting_category, a.meeting_subject as meeting_subject,a.from_date as from_date,a.to_date as to_date,a.venue as venue,b.name as name,ifnull(b.present,0) as present from `tabAttendance Record`  a,`tabInvitation Member Details` b where a.name=b.parent and b.email_id=%s",dts['username'],as_dict=True)
                return data
                
                
@frappe.whitelist(allow_guest=True)
def mark_my_attendance(data):
	"""
	Member can mark their attandence of meeting
	"""
        dts=json.loads(data)
        qry="select user from __Auth where user='"+cstr(dts['username'])+"' and password=password('"+cstr(dts['userpass'])+"') "
        valid=frappe.db.sql(qry)
        if not valid:
                return {
                  "status":"401",
                  "message":"User name or Password is incorrect"
                }
        else:
                for record in dts['records']:
                        if not record['present'] :
                                record['present']=0
                        frappe.db.sql("update `tabInvitation Member Details` set present=%s where name=%s",(record['present'],record['name']))
                return "Updated Attendance"



@frappe.whitelist(allow_guest=True)
def get_masters(data):
	"""
	Member can mark their attandence of meeting
	"""
	dts=json.loads(data)
	from frappe.model.db_query import DatabaseQuery
	qry="select user from __Auth where user='"+cstr(dts['username'])+"' and password=password('"+cstr(dts['userpass'])+"') "
	valid=frappe.db.sql(qry)
	if not valid:
		return {
				"status":"401",
				"message":"User name or Password is incorrect"
		}
	meta = frappe.get_meta(dts['tbl'])
	role_permissions = frappe.permissions.get_role_permissions(meta, dts['username'])
	user_permissions = frappe.defaults.get_user_permissions(dts['username'])
	match_conditions = []
	for doctypes in user_permissions:
		for df in meta.get_fields_to_check_permissions(doctypes):
			match_conditions.append("""(ifnull(`tab{doctype}`.`{fieldname}`, "")=""
					or `tab{doctype}`.`{fieldname}` in ({values}))""".format(doctype=dts['tbl'],fieldname=df.fieldname,values=", ".join([('"'+v+'"') for v in user_permissions[df.options]])
			))
	cond = ''
	user_roles = frappe.get_roles(dts['username'])
	if match_conditions   :
		cond = 'where ' + ' or '.join(match_conditions)
		return frappe.db.sql("""select name from `tab%s` where %s"""%(dts['tbl'], ' or '.join(match_conditions)), as_dict=1)
	elif ("System Manager" in user_roles ):
		return frappe.db.sql("""select name from `tab%s` """%(dts['tbl']), as_dict=1)
	else:
		return {
				"status":"200",
				"message":"No Records Found"
		}
	

@frappe.whitelist(allow_guest=True)
def event_list(data):
    """
    Event List for user
    """
    dts=json.loads(data)
    from frappe.model.db_query import DatabaseQuery
    qry="select user from __Auth where user='"+cstr(dts['username'])+"' and password=password('"+cstr(dts['userpass'])+"') "
    valid=frappe.db.sql(qry)
    if not valid:
        return {
                "status":"401",
                "message":"User name or Password is incorrect"
        }    
    from frappe.desk.doctype.event.event import get_permission_query_conditions
    qry=" select name as event_name,address,starts_on as event_date,subject from tabEvent where "+get_permission_query_conditions(dts['username'])
    #return qry
    data=frappe.db.sql(qry,as_dict=True)
    return data

        
@frappe.whitelist(allow_guest=True)
def event_participents(data):
    """
    Event details og selected event
    """
    dts=json.loads(data)
    qry="select user from __Auth where user='"+cstr(dts['username'])+"' and password=password('"+cstr(dts['userpass'])+"') "
    valid=frappe.db.sql(qry)
    if not valid:
        return {
                "status":"401",
                "message":"User name or Password is incorrect"
        }       
    data=frappe.db.sql("select a.name,a.person_name,ifnull(a.present,0) as present,a.comments from `tabEvent Attendace Details`  a,`tabEvent Attendance` b ,`tabEvent` c  where a.parent=b.name and b.event_name=c.name and c.name=%s",dts['event_id'],as_dict=True)
    return data
                



@frappe.whitelist(allow_guest=True)
def event_attendance(data):
    """
    Give provisin for sms email and push notification
    update Event attendance
    """
    dts=json.loads(data)
    qry="select user from __Auth where user='"+cstr(dts['username'])+"' and password=password('"+cstr(dts['userpass'])+"') "
    valid=frappe.db.sql(qry)
    if not valid:
        return {
                "status":"401",
                "message":"User name or Password is incorrect"
        }   
    for record in dts:
        if not record['present'] :
            record['present']=0
        frappe.db.sql("update `tabEvent Attendace Details` set present=%s,comments=%s where name=%s",(record['present'],record['comments'],record['name']))
    return "Updated Attendance"

@frappe.whitelist(allow_guest=True)
def my_event_list(data):
    """
    Member Event list
    """
    dts=json.loads(data)
    qry="select user from __Auth where user='"+cstr(dts['username'])+"' and password=password('"+cstr(dts['userpass'])+"') "
    valid=frappe.db.sql(qry)
    if not valid:
        return {
                "status":"401",
                "message":"User name or Password is incorrect"
        }       
    data=frappe.db.sql("select a.subject ,a.starts_on as event_date, a.address,c.name,c.person_name,ifnull(c.present,0) as present,comments from `tabEvent` a, `tabEvent Attendance` b,`tabEvent Attendace Details` c \
                         where a.name=b.event_name and b.name=c.parent and c.id in (select a.name from tabMember a,tabUser b where a.email_id=b.name and b.name=%s) ",dts['username'],as_dict=True)
    return data

@frappe.whitelist(allow_guest=True)
def my_event_attendance(data):
    dts=json.loads(data)
    qry="select user from __Auth where user='"+cstr(dts['username'])+"' and password=password('"+cstr(dts['userpass'])+"') "
    valid=frappe.db.sql(qry)
    if not valid:
        return {
                "status":"401",
                "message":"User name or Password is incorrect"
        }     
    for record in dts['records']:
        if not record['present'] :
            record['present']=0
        frappe.db.sql("update `tabEvent Attendace Details` set present=%s,comments=%s where name=%s",(record['present'],record['comments'],record['name']))
    return "Updated Your Event Attendance"

@frappe.whitelist(allow_guest=True)
def get_hierarchy(data):
    dts=json.loads(data)
    qry="select user from __Auth where user='"+cstr(dts['username'])+"' and password=password('"+cstr(dts['userpass'])+"') "
    valid=frappe.db.sql(qry)
    if not valid:
        return {
                "status":"401",
                "message":"User name or Password is incorrect"
        }
    dictnory={
        "Cells":"senior_cell,pcf,church,church_group,zone,region",
        "Senior Cells":"pcf,church,church_group,zone,region",
        "PCFs":"church,church_group,zone,region",
        "Churches":"church_group,zone,region",
        "Group Churches":"zone,region",
        "Zones":"region"
    }
    tablename=dts['tbl']
    res=frappe.db.sql("select %s from `tab%s` where name='%s'"  %(dictnory[tablename],dts['tbl'],dts['name']),as_dict=True)
    return res


@frappe.whitelist(allow_guest=True)
def get_lists(data):
    dts=json.loads(data)
    qry="select user from __Auth where user='"+cstr(dts['username'])+"' and password=password('"+cstr(dts['userpass'])+"') "
    valid=frappe.db.sql(qry)
    if not valid:
        return {
                "status":"401",
                "message":"User name or Password is incorrect"
        }
    wheres={
            "Senior Cells":"senior_cell",
            "PCFs":"pcf",
            "Churches":"church",
            "Group Churches":"church_group",
            "Zones":"zone",
            "Regions":"region"
    }
    tablename=dts['tbl']
    fields={
            "Senior Cells":"Cells",
            "PCFs":"Senior Cells",
            "Churches":"PCFs",
            "Group Churches":"Churches",
            "Zones":"Group Churches",
            "Regions":"Zones"
    }
    fieldname=dts['tbl']

    res=frappe.db.sql("select name from `tab%s` where %s='%s'"  %(fields[fieldname],wheres[tablename],dts['name']),as_dict=True)
    return res


@frappe.whitelist(allow_guest=True)
def task_list(data):
    dts=json.loads(data)
    qry="select user from __Auth where user='"+cstr(dts['username'])+"' and password=password('"+cstr(dts['userpass'])+"') "
    valid=frappe.db.sql(qry)
    if not valid:
        return {
                "status":"401",
                "message":"User name or Password is incorrect"
        }    
    data=frappe.db.sql("""select name ,subject ,exp_end_date,status,priority,description,cell from `tabTask` where status in ('Open','Working' ) and exp_start_date is not null and owner='%s' or _assign like '%%%s%%' """ %(dts['username'],dts['username']),as_dict=True)
    return data


@frappe.whitelist(allow_guest=True)
def task_update(data):
    dts=json.loads(data)
    qry="select user from __Auth where user='"+cstr(dts['username'])+"' and password=password('"+cstr(dts['userpass'])+"') "
    valid=frappe.db.sql(qry)
    if not valid:
        return {
                "status":"401",
                "message":"User name or Password is incorrect"
        }         
    if dts['followup_task']:
        dts['exp_start_date']=now()
        dts['doctype']='Task'
        dts['subject']='followup task for '+dts['name']
        del dts['assignee']
        ma = frappe.get_doc(dts)
        ma.insert(ignore_permissions=True)
        frappe.db.sql("update `tabTask` set description=%s,status='Closed',closing_date=%s where name=%s",('Closed the task and created followup task '+ma.name ,now(),dts['name']),as_dict=True)
        return "Created followup taks "+ma.name+" and closed old task "+dts['name']
    else:
        frappe.db.sql("update `tabTask` set description=%s,status=%s,_assign=%s where name=%s",(dts['description'],dts['status'],dts['_assign'],dts['name']),as_dict=True)
        return "Task Details updated Successfully"

@frappe.whitelist(allow_guest=True)
def cell_members(data):
    dts=json.loads(data)
    qry="select user from __Auth where user='"+cstr(dts['username'])+"' and password=password('"+cstr(dts['userpass'])+"') "
    valid=frappe.db.sql(qry)
    if not valid:
        return {
                "status":"401",
                "message":"User name or Password is incorrect"
        }  
    data=frappe.db.sql("select a.member_name from tabMember a,tabUser b where a.user_id=b.name and a.cell=%s",dts['cell'],as_dict=True)
    return data


@frappe.whitelist(allow_guest=True)
def create_task(data):
    dts=json.loads(data)
    qry="select user from __Auth where user='"+cstr(dts['username'])+"' and password=password('"+cstr(dts['userpass'])+"') "
    valid=frappe.db.sql(qry)
    if not valid:
        return {
                "status":"401",
                "message":"User name or Password is incorrect"
        }  
    dts['exp_start_date']=now()
    dts['doctype']='Task'
    del dts['assignee']
    del dts['name']
    ma = frappe.get_doc(dts)
    ma.insert(ignore_permissions=True)
    return ma.name+" created Successfully"



@frappe.whitelist(allow_guest=True)
def dashboard(data):
        dts=json.loads(data)
        qry="select user from __Auth where user='"+cstr(dts['username'])+"' and password=password('"+cstr(dts['userpass'])+"') "
        valid=frappe.db.sql(qry)
        
        if not valid:
            return {
                "status":"401",
                "message":"User name or Password is incorrect"
            }  
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

        new_born=frappe.db.sql("select count(name) from `tabMember` where creation between date_sub(now(),INTERVAL 1 YEAR) and now() and is_new_born='Yes'")
        if new_born:
                data['new_born']=new_born[0][0]
        else:
                data['new_born']='0'            

        visitor_last_months=frappe.db.sql("select count(name) from `tabFirst Timer` where creation between date_sub(now(),INTERVAL 1 WEEK) and now()")
        if visitor_last_months:
                data['visitor_last_months']=visitor_last_months[0][0]
        else:
                data['visitor_last_months']='0'

        membership_strength=frappe.db.sql("select a.month,a.total_member_count,b.conversion from ( SELECT COUNT(name) AS total_member_count,MONTHNAME(creation) as month FROM `tabMember` WHERE creation BETWEEN date_sub(now(),INTERVAL 1 YEAR) AND now() GROUP BY YEAR(creation),MONTH(creation)) a, (select MONTHNAME(creation) as month ,count(ftv_id_no) as conversion from tabMember where ftv_id_no is not null group by YEAR(creation), MONTH(creation)) b where a.month=b.month",as_dict=1)
        if membership_strength:
                data['membership_strength']=membership_strength
        else:
                data['membership_strength']='0'

        partnership=frappe.db.sql("SELECT CASE foo.week WHEN 1 THEN 'First Week' WHEN 2 THEN 'Second Week' WHEN 3 THEN 'Third Week' ELSE 'Last week' END AS Week, SUM(foo.Giving) AS Giving, sum(too.Pledge) AS Pledge FROM ( SELECT week(creation)mod 4 AS week, SUM(amount)AS 'Giving' FROM `tabPartnership Record` WHERE DATEDIFF(SYSDATE(),creation)<30 and giving_or_pledge='Giving' GROUP BY week )foo ,( SELECT week(creation)mod 4 AS week, SUM(amount)AS 'Pledge' FROM `tabPartnership Record` WHERE DATEDIFF(SYSDATE(),creation)<30 and giving_or_pledge='Pledge' GROUP BY week )too where foo.week=too.week group by foo.week",as_dict=1)
        if partnership:
                data['partnership']= partnership
        else:
                data['partnership']='0'

        return data

@frappe.whitelist(allow_guest=True)
def partnership_arm(data):
    dts=json.loads(data)
    qry="select user from __Auth where user='"+cstr(dts['username'])+"' and password=password('"+cstr(dts['userpass'])+"') "
    valid=frappe.db.sql(qry)
    if not valid:
        return {
                "status":"401",
                "message":"User name or Password is incorrect"
        }  
    data=frappe.db.sql("select church,giving_or_pledge,sum(amount) from `tabPartnership Record` group by church,giving_or_pledge ",as_dict=True)
    return data


@frappe.whitelist(allow_guest=True)
def search_glm(data):
        dts=json.loads(data)
        qry="select user from __Auth where user='"+cstr(dts['username'])+"' and password=password('"+cstr(dts['userpass'])+"') "
        valid=frappe.db.sql(qry)
        if not valid:
            return {
                "status":"401",
                "message":"User name or Password is incorrect"
            }         
        qry=''
        if dts['church']:
                key='church'
                value=dts['church']
                key1='church_name'
        elif dts['group_church']:
                key='group_church'
                value=dts['group']
                key1='church_group'
        elif dts['zone']:
                key='zone'
                value=dts['zone']
        elif dts['region']:
                key='region'
                value=dts['region']
        else:
                key='1'
                value=1
        if dts['search']=='Group':
                qry="select church,pcf,senior_cell,name as cell from tabCells where "+cstr(key)+"='"+cstr(value)+"'"
        elif dts['search']=='Leader':
                qry="SELECT ttl.church_name AS church,ttl.church_group AS group_type,ttl.member_name AS member_name,ttl.phone_no AS phone_no FROM ( SELECT cc.name AS church_name, cc.church_group AS church_group, mmbr.member_name AS member_name, mmbr.phone_1 AS phone_no, cc.zone As zone, cc.region as regin FROM tabChurches cc, ( SELECT m.member_name, m.phone_1, userrol.defvalue AS defvalue FROM tabMember m , ( SELECT a.name AS name, c.defvalue AS defvalue FROM tabUser a, tabUserRole b, tabDefaultValue c WHERE a.name=b.parent AND a.name=c.parent AND b.role='Church Pastor' AND c.defkey='Churches' ) userrol WHERE m.user_id=userrol.name) mmbr WHERE cc.name=mmbr.defvalue) ttl WHERE ttl."+key1+"='"+value+"'"
        else:
                qry="select name , member_name, church,church_group,zone,region,phone_1,email_id from tabMember where member_name like '%"+cstr(dts['member'])+"%'"
        #return qry
        data=frappe.db.sql(qry,as_dict=True)
        return data


@frappe.whitelist(allow_guest=True)
def file_upload(data):
        dts=json.loads(data)
        qry="select user from __Auth where user='"+cstr(dts['username'])+"' and password=password('"+cstr(dts['userpass'])+"') "
        valid=frappe.db.sql(qry)
        if not valid:
            return {
                "status":"401",
                "message":"User name or Password is incorrect"
            }
        from frappe.utils.file_manager import  save_file
        filedata=save_file(fname=dts['filename'],content=base64.b64decode(dts['fdata']),dt=dts['tbl'],dn=dts['name'])
        comment = frappe.get_doc(dts['tbl'], dts['name']).add_comment("Attachment",
            _("Added {0}").format("<a href='{file_url}' target='_blank'>{file_name}</a>".format(**filedata.as_dict())))
        if dts['tbl']=='Member':
             frappe.db.sql("update tabMember set image=%s where name=%s",(filedata.file_url,dts['name']))
        return {
            "name": filedata.name,
            "file_name": filedata.file_name,
            "file_url": filedata.file_url,
            "comment": comment.as_dict()
        }


@frappe.whitelist(allow_guest=True)
def list_members(data):
        dts=json.loads(data)
        qry="select user from __Auth where user='"+cstr(dts['username'])+"' and password=password('"+cstr(dts['userpass'])+"') "
        valid=frappe.db.sql(qry)
        if not valid:
            return {
                "status":"401",
                "message":"User name or Password is incorrect"
            }
        res=frappe.db.sql("select name from tabMember",as_dict=1)
        return res

@frappe.whitelist(allow_guest=True)
def list_members_details(data):
        dts=json.loads(data)
        qry="select user from __Auth where user='"+cstr(dts['username'])+"' and password=password('"+cstr(dts['userpass'])+"') "
        valid=frappe.db.sql(qry)
        if not valid:
            return {
                "status":"401",
                "message":"User name or Password is incorrect"
            }
        qr1="select * from tabMember where name='"+dts['name']+"'"
        res=frappe.db.sql(qr1,as_dict=1)
        return res

@frappe.whitelist(allow_guest=True)
def get_my_profile(data):
        dts=json.loads(data)
        qry="select user from __Auth where user='"+cstr(dts['username'])+"' and password=password('"+cstr(dts['userpass'])+"') "
        valid=frappe.db.sql(qry)
        if not valid:
            return {
                "status":"401",
                "message":"User name or Password is incorrect"
            }
        qr1="select name,member_name,date_of_birth,phone_1,phone_2,email_id,email_id2,address,office_address,employment_status,industry_segment,yearly_income,experience_years,core_competeance,educational_qualification,null AS `password`,image from tabMember where name='M00000007'"
        res=frappe.db.sql(qr1,as_dict=1)
        return res


@frappe.whitelist(allow_guest=True)
def update_my_profile(data):
        dts=json.loads(data)
        qry="select user from __Auth where user='"+cstr(dts['username'])+"' and password=password('"+cstr(dts['userpass'])+"') "
        valid=frappe.db.sql(qry)
        if not valid:
            return {
                "status":"401",
                "message":"User name or Password is incorrect"
            }
        obj=frappe.get_doc('Member',dts['name'])
        obj.yearly_income=dts['yearly_income']
        obj.office_address=dts['office_address']
        #obj.email_id=dts['email_id']
        obj.industry_segment=dts['industry_segment']
        obj.employment_status=dts['employment_status']
        obj.address=dts['address']
        obj.image=dts['image']
        obj.date_of_birth=dts['date_of_birth']
        obj.educational_qualification=dts['educational_qualification']
        obj.core_competeance=dts['core_competeance']
        obj.member_name=dts['member_name']
        obj.email_id2=dts['email_id2']
        obj.phone_2=dts['phone_2']
        obj.experience_years=dts['experience_years']
        obj.phone_1=dts['phone_1']
        obj.save(ignore_permissions=True)
        obj1=frappe.get_doc('User',dts['username'])
        obj1.new_password=dts['password']
        obj.save(ignore_permissions=True)
        return "Your profile updated successfully"
























##########################################################################################################################

# # Copyright (c) 2013, New Indictrans Technologies Pvt. Ltd. and contributors
# # For license information, please see license.txt

# from __future__ import unicode_literals
# import frappe
# from frappe.model.document import Document
# from frappe import throw, _, msgprint
# import json
# from frappe.utils import getdate, validate_email_add, cint,now ,cstr

# class Member(Document):

	
# 	def on_update(self):
# 		# pass
# 		usr_id=frappe.db.sql("select name from `tabUser` where name='%s'"%(self.email_id),as_list=1)
# 		if self.flag=='not' and self.email_id:
# 			# frappe.errprint("user creation")
# 			# if  self.member_designation=='PCF Leader':
# 			# 	c_user = self.pcf
# 			# 	r_user = 'PCF Leader'
# 			# 	perm = 'PCFs'
# 			# elif self.member_designation=='Sr.Cell Leader':
# 			# 	c_user = self.senior_cell
# 			# 	r_user = 'Senior Cell Leader'
# 			# 	perm = 'Senior Cells'
# 			# elif self.member_designation=='Cell Leader':
# 			# 	c_user = self.cell
# 			# 	r_user = 'Cell Leader'
# 			# 	perm = 'Cells'
# 			# elif self.member_designation=='Member':
# 			# 	c_user = self.name
# 			# 	r_user = 'Member'
# 			# 	perm = 'Member'
# 			# elif self.member_designation=='Bible Study Class Teacher':
# 			# 	c_user = self.church
# 			# 	r_user = 'Bible Study Class Teacher'
# 			# 	perm = 'Churches'

# 			if not usr_id:
# 				u = frappe.new_doc("User")
# 				u.email=self.email_id
# 				u.first_name = self.member_name
# 				u.new_password = 'password'
# 				frappe.flags.mute_emails = False
# 				u.insert()
# 				frappe.flags.mute_emails = True
# 			r=frappe.new_doc("UserRole")
# 			r.parent=self.email_id
# 			r.parentfield='user_roles'
# 			r.parenttype='User'
# 			r.role='Member'
# 			r.insert()
# 			v = frappe.new_doc("DefaultValue")
# 			v.parentfield = 'system_defaults'
# 			v.parenttype = 'User Permission'
# 			v.parent = self.email_id
# 			v.defkey = 'Member'
# 			v.defvalue = self.name 
# 			v.insert()
# 			frappe.db.sql("update `tabMember` set flag='SetPerm' where name='%s'"%(self.name))
# 			frappe.db.commit()
# 			self.user_id = self.email_id

# def get_list(doctype, txt, searchfield, start, page_len, filters):
# 	conditions=get_conditions(filters)
# 	if conditions:
# 		value=frappe.db.sql("select name from `tab%s` where %s"%(filters.get('doctype'),conditions))
# 		return value
# 	else :
# 		value=frappe.db.sql("select name from `tab%s`"%(filters.get('doctype')))
# 		return value

# def get_conditions(filters):
# 	cond=[]
# 	if filters.get('cell'):
# 		cond.append('cell="%s"'%(filters.get('cell')))
# 	elif filters.get('senior_cell'):
# 		cond.append('senior_cell="%s"'%(filters.get('senior_cell')))
# 	elif filters.get('pcf'):
# 		cond.append('pcf="%s"'%(filters.get('pcf')))
# 	elif filters.get('church'):
# 		cond.append('church="%s"'%(filters.get('church')))
# 	elif filters.get('church_group'):
# 		cond.append('church_group="%s"'%(filters.get('church_group')))
# 	elif filters.get('zone'):
# 		cond.append('zone="%s"'%(filters.get('zone')))
# 	elif filters.get('region'):
# 		cond.append('region="%s"'%(filters.get('region')))
# 	return ' or '.join(cond)  


# def validate_birth(doc,method):
# 		#frappe.errprint("in date of birth ")
# 		if doc.date_of_birth and doc.date_of_join and getdate(doc.date_of_birth) >= getdate(doc.date_of_join):		
# 			frappe.throw(_("Date of Joining '{0}' must be greater than Date of Birth '{1}'").format(doc.date_of_join, doc.date_of_birth))
		
# 		# if doc.baptisum_status=='Yes':
# 		# 	if not doc.baptism_when or not doc.baptism_where :
# 		# 		frappe.throw(_("When and Where is Mandatory if 'Baptisum Status' is 'Yes'..!"))

# 		if doc.email_id:
# 			if not validate_email_add(doc.email_id):
# 				frappe.throw(_('{0} is not a valid email id').format(doc.email_id))


# @frappe.whitelist(allow_guest=True)
# def create_senior_cells(data):
# 	dts=json.loads(data)
# 	qry="select user from __Auth where user='"+cstr(dts['username'])+"' and password=password('"+cstr(dts['userpass'])+"') "
# 	valid=frappe.db.sql(qry)
# 	if not valid:
# 		return {
# 		  "status":"401",
# 		  "message":"User name or Password is incorrect"
# 		}
# 	res=frappe.db.sql("select role from tabUserRole where parent=%s",dts['username'],as_list=1)
# 	#frappe.errprint(res)
# 	ur=["PCF Leader" , "Church Pastor" , "Zonal Pastor" , "Regional Pastor"]
# 	c3 = [val for val in res if val in ur]
# 	return c3
# 	if c3:
# 		return {
# 			  "status":"401",
# 			  "message":"You dont have privillages to create Senior Cell"
# 		}
# 	else:
# 		obj=frappe.new_doc("Senior Cells")
# 		obj.senior_cell_name=dts['senior_cell_name']
# 		obj.senior_cell_code=dts['senior_cell_code']
# 		obj.meeting_location=dts['meeting_location']
# 		obj.zone=dts['zone']
# 		obj.region=dts['region']
# 		obj.church_group=dts['church_group']
# 		obj.church=dts['church']
# 		obj.pcf=dts['pcf']
# 		obj.contact_phone_no=dts['contact_phone_no']
# 		obj.contact_email_id=dts['contact_email_id']
# 		obj.insert(ignore_permissions=True)
# 		ret={
# 			"message":"Successfully created senior Cell '"+obj.name+"'"
# 		}
# 		return ret                


# @frappe.whitelist(allow_guest=True)
# def create_cells(data):
# 	dts=json.loads(data)
# 	qry="select user from __Auth where user='"+cstr(dts['username'])+"' and password=password('"+cstr(dts['userpass'])+"') "
# 	valid=frappe.db.sql(qry)
# 	if not valid:
# 		return {
# 		  "status":"401",
# 		  "message":"User name or Password is incorrect"
# 		}
# 	else:
# 		obj=frappe.new_doc("Cells")
# 		obj.cell_name=dts['cell_name']
# 		obj.cell_code=dts['cell_code']
# 		obj.meeting_location=dts['meeting_location']
# 		obj.address=dts['address']
# 		obj.senior_cell=dts['senior_cell']
# 		obj.zone=dts['zone']
# 		obj.region=dts['region']
# 		obj.church_group=dts['church_group']
# 		obj.church=dts['church']
# 		obj.pcf=dts['pcf']
# 		obj.contact_phone_no=dts['contact_phone_no']
# 		obj.contact_email_id=dts['contact_email_id']
# 		obj.insert(ignore_permissions=True)
# 		ret={
# 			"message":"Successfully created Cell '"+obj.name+"'"
# 		}
# 		return ret



# @frappe.whitelist()
# def dashboard(user):
# 	#frappe.errprint(user)
# 	data={}
# 	new_visitor=frappe.db.sql("select count(name) from `tabFirst Timer` where creation between date_sub(now(),INTERVAL 1 YEAR) and now()")
# 	if new_visitor :
# 		data['new_visitor']=new_visitor[0][0] 
# 	else:
# 		data['new_visitor']='0'
# 	first_timers=frappe.db.sql("select count(name) from `tabFirst Timer` where creation between date_sub(now(),INTERVAL 1 YEAR) and now()")
# 	if first_timers:
# 		data['first_timers']=first_timers[0][0]
# 	else:
# 		data['first_timers']='0'
# 	visitor_last_months=frappe.db.sql("select count(name) from `tabFirst Timer` where creation between date_sub(now(),INTERVAL 1 WEEK) and now()")
# 	if visitor_last_months:
# 		data['visitor_last_months']=visitor_last_months[0][0]
# 	else:
# 		data['visitor_last_months']='0'
# 	membership_strength=frappe.db.sql("select MONTHNAME(creation) as Month, count(name) as `New Users`,count(name) as Revisited from `tabFirst Timer` where creation between date_sub(now(),INTERVAL 1 Year) and now() group by year(creation), MONTH(creation)",as_list=1)
# 	if membership_strength:
# 		data['membership_strength']=membership_strength
# 	else:
# 		data['membership_strength']='0'
# 	partnership=frappe.db.sql("select MONTHNAME(creation) as Month, count(name) as `New Users`,count(name) as Revisited from `tabFirst Timer` where creation between date_sub(now(),INTERVAL 1 Year) and now() group by year(creation), MONTH(creation)",as_list=1)
# 	if partnership:
# 		data['partnership']=partnership
# 	else:
# 		data['partnership']='0'
# 	return data


# @frappe.whitelist()
# def user_roles(user):
# 	data={}
# 	roles=frappe.db.sql("select role from `tabUserRole` where parent=%(user)s", {"user":user},as_dict=True)
# 	data['roles']=roles
# 	user_values=frappe.db.sql("select defkey,defvalue from `tabDefaultValue`  where parent=%(user)s", {"user":user},as_dict=True)
# 	data['user_values']=user_values
# 	return data


# @frappe.whitelist()
# def create_meeting(user,data,_type='POST'):
# 		ma = frappe.get_doc(json.loads(data))
# 		ma.insert()
# 		frappe.db.commit()
# 		return ma.name

# @frappe.whitelist()
# def meetings_list(user):
# 	from erpnext.controllers.queries import get_match_cond
# 	qry="select name as `Meeting Name`,meeting_subject as `Meeting Subject`,from_date as `Meeting Date`,venue from `tabAttendance Record` where 1=1 "+ get_match_cond('Attendance Record').replace('\n','').replace("\"","'").replace('\t','')
# 	#frappe.errprint(qry)
# 	data=frappe.db.sql(qry,as_dict=True)
# 	return data

# @frappe.whitelist()
# def meetings_details():
# 	data=frappe.db.sql(qry,as_dict=True)
# 	return data


# @frappe.whitelist()
# def meetings_members(meeting_id):
# 	data=frappe.db.sql("select name,member,member_name,present from `tabInvitation Member Details` where parent=%s",meeting_id,as_dict=True)
# 	return data


# @frappe.whitelist()
# def meetings_attendance(data):
# 	for record in json.loads(data):
# 		if not record['present'] : 
# 			record['present']=0
# 		frappe.db.sql("update `tabInvitation Member Details` set present=%s where name=%s",(record['present'],record['name']))
# 	return "Updated Attendance"


# @frappe.whitelist()
# def meetings_list_member(user):
# 	data=frappe.db.sql("select a.name as `Meeting Name`,a.meeting_category as `Meeting Category`, a.meeting_subject as `Meeting Subject`,a.from_date as `From Date`,a.to_date,a.venue,b.name,ifnull(b.present,0) as `present` from `tabAttendance Record`  a,`tabInvitation Member Details` b where a.name=b.parent and b.email_id=%s",user,as_dict=True)
# 	return data


# @frappe.whitelist()
# def mark_my_attendance(data):
# 	for record in json.loads(data):
# 		if not record['present'] : 
# 			record['present']=0
# 		frappe.db.sql("update `tabInvitation Member Details` set present=%s where name=%s",(record['present'],record['name']))
# 	return "Updated Attendance"


# @frappe.whitelist()
# def event_list(user):
# 	from erpnext.controllers.queries import get_match_cond
# 	qry="select name as `Event Name`,subject ,starts_on as `Event Date`,address from `tabEvent` where 1=1 "+ get_match_cond('Event')
# 	data=frappe.db.sql(qry,as_dict=True)
# 	return data


# @frappe.whitelist()
# def event_participents(event_id):
# 	data=frappe.db.sql("select name,person_name,ifnull(present,0) as present,comments from `tabEvent Attendace Details` where parent=%s",event_id,as_dict=True)
# 	return data


# @frappe.whitelist()
# def event_attendance(data):
# 	for record in json.loads(data):
# 		if not record['present'] : 
# 			record['present']=0
# 		frappe.db.sql("update `tabEvent Attendace Details` set present=%s,comments=%s where name=%s",(record['present'],record['comments'],record['name']))
# 	return "Updated Attendance"

# @frappe.whitelist()
# def my_event_list(user):
# 	data=frappe.db.sql("select a.subject ,a.starts_on as `Event Date`, a.address,c.name,c.person_name,ifnull(c.present,0) as present,comments from `tabEvent` a, `tabEvent Attendance` b,`tabEvent Attendace Details` c \
#                          where a.name=b.event_name and b.name=c.parent and c.id in (select a.name from tabMember a,tabUser b where a.email_id=b.name and b.name=%s) ",user,as_dict=True)
# 	return data

# @frappe.whitelist()
# def my_event_attendance(data):
# 	for record in json.loads(data):
# 		if not record['present'] : 
# 			record['present']=0
# 		frappe.db.sql("update `tabEvent Attendace Details` set present=%s,comments=%s where name=%s",(record['present'],record['comments'],record['name']))
# 	return "Updated Your Event Attendance"

# @frappe.whitelist()
# def task_list(user):
# 	from erpnext.controllers.queries import get_match_cond
# 	qry="select name ,subject ,exp_end_date,status,priority from `tabTask` where status in ('Open','Working' ) and exp_start_date is not null"+ get_match_cond('Task')+" order by exp_start_date ,priority asc"
# 	data=frappe.db.sql(qry,as_dict=True)
# 	return data

# @frappe.whitelist()
# def task_details(task_id):
# 	data=frappe.db.sql("select name ,subject ,exp_end_date,status,priority,description,cell,_assign from `tabTask` where name=%s",task_id,as_dict=True)
# 	return data


# @frappe.whitelist()
# def task_update(data):
# 	dts=json.loads(data)
# 	if dts['followup_task']:
# 		dts['exp_start_date']=now()
# 		dts['doctype']='Task'
# 		dts['subject']='followup task for '+dts['name']
# 		del dts['assignee']
# 		ma = frappe.get_doc(dts)
# 		ma.insert()
# 		frappe.db.sql("update `tabTask` set description=%s,status='Closed',closing_date=%s where name=%s",('Closed the task and created followup task '+ma.name ,now(),dts['name']),as_dict=True)
# 		return "create followup taks "+ma.name+" and closed old task "+dts['name']
# 	else:
# 		frappe.db.sql("update `tabTask` set description=%s,status=%s,_assign=%s where name=%s",(dts['description'],dts['status'],dts['_assign'],dts['name']),as_dict=True)
# 		return "Task Details updated Successfully"


# @frappe.whitelist()
# def cell_members(cell_id):
# 	data=frappe.db.sql("select a.member_name from tabMember a,tabUser b where a.user_id=b.name and a.cell=%s",cell_id,as_dict=True)
# 	return data

# @frappe.whitelist()
# def create_task(data):
# 	dts=json.loads(data)
# 	dts['exp_start_date']=now()
# 	dts['doctype']='Task'
# 	del dts['assignee']
# 	ma = frappe.get_doc(dts)
# 	ma.insert()
# 	return ma.name+" created Successfully"


# @frappe.whitelist()
# def partnership_arm(user):
# 	data=frappe.db.sql("select church,giving_or_pledge,sum(amount) from `tabPartnership Record` group by church,giving_or_pledge ",as_dict=True)
# 	return data

# @frappe.whitelist()
# def search_glm(data):
# 	dts=json.loads(data)
# 	qry=''
# 	if dts['church']:
# 		key='church' 
# 		value=dts['church']
# 	elif dts['group_church']:
# 		key='group_church' 
# 		value=dts['group']
# 	elif dts['zone']:
# 		key='zone' 
# 		value=dts['zone']
# 	elif dts['region']:
# 		key='region' 
# 		value=dts['region']
# 	else:
# 		key='1'
# 		value=1
# 	if dts['search']=='Group':
# 		qry="select church,pcf,senior_cell,name as cell from tabCells where "+cstr(key)+"='"+cstr(value)+"'"
# 	elif dts['search']=='Leader':
# 		qry="SELECT ttl.church_name AS church,ttl.church_group AS group_type,ttl.member_name AS member_name,ttl.phone_no AS phone_no FROM ( SELECT cc.name AS church_name, cc.church_group AS church_group, mmbr.member_name AS member_name, mmbr.phone_1 AS phone_no, cc.zone As zone, cc.region as regin FROM tabChurches cc, ( SELECT m.member_name, m.phone_1, userrol.defvalue AS defvalue FROM tabMember m , ( SELECT a.name AS name, c.defvalue AS defvalue FROM tabUser a, tabUserRole b, tabDefaultValue c WHERE a.name=b.parent AND a.name=c.parent AND b.role='Church Pastor' AND c.defkey='Churches' ) userrol WHERE m.user_id=userrol.name) mmbr WHERE cc.name=mmbr.defvalue) ttl WHERE ttl.zone='East Z'"	
# 	else:
# 		qry="select name as member_name, church,church_group,zone,region,phone_1,email_id from tabMember where member_name like '%"+cstr(dts['member'])+"%'"
# 	data=frappe.db.sql(qry,as_dict=True)
# 	return data











