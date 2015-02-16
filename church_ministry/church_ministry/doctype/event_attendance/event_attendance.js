cur_frm.cscript.cell = function(doc, cdt, cdn) {
		var d = locals[cdt][cdn];
		frappe.call({
				method:"church_ministry.church_ministry.doctype.event_attendance.event_attendance.loadtable",
				args:{
	        	"cell":doc.cell
	        	},
				callback: function(r) {
					if (r.message.ftv[0].length>0){
						frappe.model.clear_table(doc, "event_attendace_details");
			           for (i=0;i<r.message.ftv[0].length;i++){
			           	    var child = frappe.model.add_child(doc,"Event Attendance","event_attendace_details");
			           	    child.id=r.message.ftv[0][i][0];			           	    
			           	    child.person_name=r.message.ftv[0][i][1];
			           } 
			           refresh_field("event_attendace_details");
			        }
			 }
	    });
}