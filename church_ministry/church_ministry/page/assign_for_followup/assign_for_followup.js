frappe.pages['assign-for-followup'].onload = function(wrapper) {
	frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Assign For Followup',
		single_column: true
	});    
	$("<div class='assign' style='min-height: 400px; padding: 15px;'></div>").appendTo($(wrapper).find('.layout-main-section'));
	new frappe.assign(wrapper);
}	

frappe.assign = Class.extend({
	init: function(wrapper) {
		this.wrapper = wrapper;
		this.body = $(this.wrapper).find(".assign");
		this.make();
	},
	make: function() {
		var me = this;
		return frappe.call({
			module:"church_ministry.church_ministry",
			page:"assign_for_followup",
			method: "ftv",
			callback: function(r) {
				me.options = r.message;
				me.setup_page();
			}
		});
	},
	setup_page: function() {
		var me = this;
		this.doctype_select
			= this.wrapper.page.add_select(__("Document Types"),
				[{value: "", label: __("Select FTV")+"..."}].concat(this.options.ftv))
				.change(function() {
					me.show_members();
					//console.log("changed");
				});
	},
	show_members: function(){
		//console.log("show members");
		var me = this;
		$(me.wrapper).find('.assign').empty();
		frappe.call({
				method:"church_ministry.church_ministry.page.assign_for_followup.assign_for_followup.loadmembers",
				callback: function(r) {
					if (r.message.members){
						console.log(r.message.members);
						var h = "<table class='members' border='1' style='width:100%;background-color: #f9f9f9;'><thead style='padding=0px;width=100%'><tr style='padding=0px;'><th>#</th><th>Member ID</th><th>Member Name</th><th>Gender</th></tr></thead><tbody style='padding=0px;'></table>"
			                    //$(h).appendTo($(me.wrapper).find('.customercl2'))
			                    h1="<table class='members1' border='1' style='width:100%;background-color: #f9f9f9;'>"
			                    for (i=1;i<r.message.members[0][0].length;i++){
			                    	console.log(r.message.members[0][i][0]);
			                        var j=i+1
			                        h1 += '<tr style="padding=0px;">'
			                        h1 += '<td >'+j+'</td>'
			                        h1 += '<td >'+r.message.members[0][i][0]+'</td>'
			                        h1 += '<td >'+r.message.members[0][i][1]+'</td>'
			                        h1 += '<td align="right">'+r.message.members[0][i][2]+'</td></tr></tbody>'                      
			                    }        
			                    console.log(h1)   ;         
			                    $(h1).appendTo($(me.wrapper).find('.assign'))        
					}
			 	}
	    }); 
	}   
});
