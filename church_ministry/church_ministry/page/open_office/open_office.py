from __future__ import unicode_literals
import frappe
import frappe.defaults
from frappe.utils import cstr,now,add_days,nowdate


@frappe.whitelist()
def process(data):
	dts=[x for x in data[1:-1].split(',')]
	for item in dts:
		itm=item.replace('"','').strip()
		qry="select first_name,ifnull(last_name,'') from tabUser where name='"+itm+"'"
		result=frappe.db.sql(qry)
		import requests
		import xmltodict ,json
		req1 = requests.get('http://localhost:5080/openmeetings/services/UserService/getSession')
		req2="http://localhost:5080/openmeetings/services/UserService/loginUser?SID="+req1.text.split('ax28:session_id>')[1][:-2]+"&username="+result[0][0].replace(' ','')+"&userpass="+result[0][0].replace(' ','')
		res2=requests.get(req2)
		#frappe.errprint(res2.text)
		req3="http://localhost:5080/openmeetings/services/UserService/setUserObjectAndGenerateRoomHashByURLAndRecFlag?SID="+req1.text.split('ax28:session_id>')[1][:-2]+"&username="+result[0][0]+"&firstname="+result[0][0]+"&lastname="+result[0][1]+"&profilePictureUrl=http://www.fnordware.com/superpng/pnggrad16rgb.png&email=email.kadam@gmail.com&externalUserId=5&externalUserType=gangadhar&room_id=13&becomeModeratorAsInt=1&showAudioVideoTestAsInt=1&allowRecording=1"
		#frappe.msgprint(req3)
		res3=requests.get(req3)
		#frappe.errprint(res3.text)
		hashid=res3.text.split('ns:return>')[1][:-2]
		url="http://localhost:5080/openmeetings/?secureHash="+hashid
		frappe.get_doc({
		"doctype": "ToDo",
		"description": url,
		"owner":itm
		}).insert(ignore_permissions=True)
		frappe.sendmail(recipients=itm+',gangadhar.k@indictranstech.com', content=url, subject='Audio meeting url')
	return "done"
	# req4 = requests.get('http://localhost:5080/openmeetings/services/UserService/getSession')
	# req5="http://localhost:5080/openmeetings/services/UserService/loginUser?SID="+req4.text.split('ax28:session_id>')[1][:-2]+"&username=priya&userpass=priya"
	# res5=requests.get(req5)
	# req6="http://localhost:5080/openmeetings/services/UserService/setUserObjectAndGenerateRoomHashByURLAndRecFlag?SID="+req4.text.split('ax28:session_id>')[1][:-2]+"&username=priya&firstname=priya&lastname=shitole&profilePictureUrl=http://www.fnordware.com/superpng/samples.html&email=priya.s@indictranstech.com.com&externalUserId=3&externalUserType=gangadhar&room_id=13&becomeModeratorAsInt=1&showAudioVideoTestAsInt=1&allowRecording=1"
	# res6=requests.get(req6)
	# hashid1=res6.text.split('ns:return>')[1][:-2]
	# return  {  
	#             "user1" :"http://localhost:5080/openmeetings/?secureHash="+hashid,
	#             "user2" :"http://localhost:5080/openmeetings/?secureHash="+hashid1
	# }


@frappe.whitelist()
def get_users():
	res=frappe.db.sql("select a.name,CONCAT(ifnull(a.first_name,''),' ',ifnull(a.last_name,'')) as full_name from tabUser  a,tabUserRole r where a.name=r.parent and r.role in ('Regional Pastor','Zonal Pastor','Group Church Pastor','Church Pastor','Cell Leader','Senior Cell Leader','PCF Leader','Bible Study Class Teacher','System Manager') order by a.name" ,as_dict=1)	
	return res


@frappe.whitelist()
def invite_meeting(data):
	from church_ministry.church_ministry.page.open_office.open_office import process
	process(user_list)
	frappe.msgprint("invited members for meeting")
	return data
	
			
