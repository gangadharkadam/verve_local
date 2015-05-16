//cur_frm.add_fetch("church", "church_group", "church_group");
cur_frm.add_fetch("church", "region", "region");
cur_frm.add_fetch("church", "zone", "zone");

frappe.ui.form.on("Foundation School Attendance", "onload", function(frm,cdt,cdn,doc) {
	if(frm.doc.__islocal){
    cur_frm.fields_dict["attendance"].grid.set_column_disp("attendance",false );
  	}
  	cur_frm.cscript.toggle_related_fields(frm.doc);

  	if(frm.doc.__islocal && frm.doc.cell ){   
    argmnt={
              // "region": frm.doc.region,
              // "zone": frm.doc.zone,
              // "church_group": frm.doc.church_group,
              // "church": frm.doc.church ,
              // "pcf": frm.doc.pcf,
              // "senior_cell": frm.doc.senior_cell,
              "name": frm.doc.cell  
            }
 
    frappe.call({
        method:"church_ministry.church_ministry.doctype.first_timer.first_timer.set_higher_values",
        args:{"args":argmnt},
        callback: function(r) {
          if (r.message){
            frm.doc.region=r.message.region
            frm.doc.zone=r.message.zone
            frm.doc.church_group=r.message.church_group
            frm.doc.church=r.message.church
            frm.doc.pcf=r.message.pcf
            frm.doc.senior_cell=r.message.senior_cell
            //frm.doc.cell=r.message.name
            refresh_field('region');              
            refresh_field('zone');
            refresh_field('church_group');              
            refresh_field('church');
            refresh_field('pcf');              
            refresh_field('senior_cell');
           // refresh_field('cell');
          }
        }
      });
  }
});

frappe.ui.form.on("Foundation School Attendance", "refresh", function(frm,cdt,cdn,doc) {
    cur_frm.fields_dict["attendance"].grid.set_column_disp("attendance",true );
    cur_frm.cscript.toggle_related_fields(frm.doc);
});

frappe.ui.form.on("Foundation School Attendance", "church", function(frm,cdt,cdn,doc) {
	    //console.log("in church trigger");
		var d = locals[cdt][cdn];
		frappe.call({
				method:"church_ministry.church_ministry.doctype.foundation_school_attendance.foundation_school_attendance.loadftv",
				args:{
	        	"church":frm.doc.church,
	        	"visitor_type":frm.doc.visitor_type,
	        	"foundation__exam" : frm.doc.fc_class
	        	},
				callback: function(r) {
					if (r.message.ftv[0].length>0){
			           for (i=0;i<r.message.ftv[0].length;i++){
			           	    var child = frappe.model.add_child(frm.doc,"Foundation School Exam Details","attendance");
			           	    if (frm.doc.visitor_type=='FTV'){
			           	    	child.ftv_id=r.message.ftv[0][i][0];
			           	    }
			           	    else{
			           	    	child.member_id=r.message.ftv[0][i][0];
			           	    }
			           	    child.ftv_name=r.message.ftv[0][i][1];
			           	    child.cell=r.message.ftv[0][i][2];
			           }
			           cur_frm.refresh_fields();
			        }
			 }
	    })
});

frappe.ui.form.on("Foundation School Attendance", "visitor_type", function(frm,doc) {
	frappe.model.clear_table(frm.doc, "attendance");
	cur_frm.cscript.toggle_related_fields(frm.doc);
});

cur_frm.cscript.toggle_related_fields = function(doc) {
	if (doc.visitor_type=='FTV'){
		cur_frm.fields_dict["attendance"].grid.set_column_disp("member_id",false );
		cur_frm.fields_dict["attendance"].grid.set_column_disp("ftv_id", true);
		cur_frm.fields_dict["attendance"].grid.set_column_disp("score", false);
		cur_frm.fields_dict["attendance"].grid.set_column_disp("remarks", false);
		cur_frm.fields_dict["attendance"].grid.set_column_disp("baptism_when", false);
		cur_frm.fields_dict["attendance"].grid.set_column_disp("baptism_where", false);
		cur_frm.refresh_fields();
	}
	else {
		cur_frm.fields_dict["attendance"].grid.set_column_disp("member_id",true );
		cur_frm.fields_dict["attendance"].grid.set_column_disp("ftv_id", false);
		cur_frm.fields_dict["attendance"].grid.set_column_disp("score", false);
		cur_frm.fields_dict["attendance"].grid.set_column_disp("remarks", false);
		cur_frm.fields_dict["attendance"].grid.set_column_disp("baptism_when", false);
		cur_frm.fields_dict["attendance"].grid.set_column_disp("baptism_where", false);
		cur_frm.refresh_fields();
	}
}

cur_frm.add_fetch("ftv_id", "ftv_name", "ftv_name");