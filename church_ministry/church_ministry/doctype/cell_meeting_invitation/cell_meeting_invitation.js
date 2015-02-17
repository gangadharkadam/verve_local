frappe.ui.form.on("Cell Meeting Invitation", "validate", function(frm,doc) {
	if(frm.doc.meeting_category=="Cell Meeting"){
		if(!frm.doc.meeting_subject){
			msgprint("Please enter cell and 'Meeting Subject' before save..! ");
        	throw "Please enter cell and Meeting Subject.!"
		}
	}
	else if(frm.doc.meeting_category=="Church Meeting"){
		if(!frm.doc.meeting_sub){
			msgprint("Please select Church and 'Meeting Subject' before save..! ");
        	throw "Please enter Church and Meeting Subject.!"
		}
	}
});

frappe.ui.form.on("Cell Meeting Invitation", "meeting_category", function(frm,doc) {
	frappe.model.clear_table(frm.doc, "invitation_member_details");
	refresh_field("invitation_member_details");
});

