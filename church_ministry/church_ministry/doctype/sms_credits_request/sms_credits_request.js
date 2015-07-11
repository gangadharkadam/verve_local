cur_frm.cscript.onload = function(doc, dt, dn) {
	if (doc.__islocal){
		set_field_permlevel('allocated_credits',2);
		set_field_permlevel('unit_value',2);
		set_field_permlevel('currency',2);
	}
	for (i=0;i<user_roles.length;i++){
		if( user_roles[i]=='Cell Leader' || user_roles[i]=='PCF Leader' || user_roles[i]=='Senior Cell Leader' || user_roles[i]=='Church Pastor' || user_roles[i]=='Group Church Pastor' || user_roles[i]=='Zonal Pastor' || user_roles[i]=='Regional Pastor') {
			doc.designation=user_roles[i];
		}
	}	
	if (has_common(user_roles, ["Administrator", "System Manager"])){
		set_field_permlevel('allocated_credits',0);
		set_field_permlevel('requested_credits',1);
		set_field_permlevel('unit_value',0);
		set_field_permlevel('currency',0);
	}
	else if (doc.allocated_credits>=1 ) {
		set_field_permlevel('allocated_credits',1);
		set_field_permlevel('unit_value',1);
		set_field_permlevel('currency',1);
	}
	else{
		set_field_permlevel('allocated_credits',2);
		set_field_permlevel('unit_value',2);
		set_field_permlevel('currency',2);
	}
}

cur_frm.cscript.allocated_credits = function(doc) {
	frappe.call({
			method:"church_ministry.church_ministry.doctype.sms_credits_request.sms_credits_request.check_balance",
			callback: function(r) {
				if (r.message[0][0]< doc.allocated_credits){
				  doc.allocated_credits=null;
				  alert("You do not have sufficient sms to credit");
                  refresh_field("allocated_credits");
				}
			}
		});
	
}