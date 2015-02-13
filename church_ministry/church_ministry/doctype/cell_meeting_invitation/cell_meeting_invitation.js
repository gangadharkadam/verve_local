cur_frm.cscript.validate = function(doc,cdt,cdn) {
	console.log(doc.meeting_category);
	if(doc.meeting_category=="Cell Meeting"){
		if(!doc.meeting_subject){
			msgprint("Please enter cell 'Meeting Subject' before save..! ");
        	throw "Please enter Meeting Subject.!"
		}
	}
	else if(doc.meeting_category=="Church Meeting"){
		if(!doc.meeting_sub){
			msgprint("Please select church 'Meeting Subject' before save..! ");
        	throw "Please enter Meeting Subject.!"
		}
	}
}

cur_frm.cscript.invitation_to_members = function(doc,cdt,cdn) {
	console.log("hi")
	get_server_fields('get_members','','',doc, cdt, cdn, 1, function(r){
		console.log(r.message)
	}); 
}