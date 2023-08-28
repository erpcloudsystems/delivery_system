frappe.ui.form.on('Delivery Note', {
    "refresh": function(frm) {
		if(!frm.doc.set_source_warehouse){
		   frm.set_df_property('set_source_warehouse', 'read_only', 0);
		}
		else{
		    $.each(frm.doc.items || [], function(i, d) {
		    d.warehouse = "";
		    d.warehouse = frm.doc.set_source_warehouse;
		    });
		    refresh_field("items");
		   frm.set_df_property('set_source_warehouse', 'read_only', 1);
		   var d = frappe.meta.get_docfield("Delivery Note Item", "warehouse", cur_frm.doc.name);
           d.read_only = 1;
		}
},
	"validate": function(frm) {
		$.each(frm.doc.items || [], function(i, d) {
                    d.cost_center = frm.doc.cost_center;
                    });
		var so = frm.doc.items;
		var so_no = "";
		for (var j in so){
			so_no = so[j].against_sales_order;
			}
		frm.set_value("sales_order",so_no);
		cur_frm.refresh();
},
    "onload": function(frm) {
		if(frm.doc.order_review_status == 'order_review_status' || frm.doc.order_processing == 'Confirmed'){
		   frm.set_df_property('set_source_warehouse', 'read_only', 1);
		   frm.get_field("items").grid.only_sortable();
		   $(".grid-add-row").hide();
		   $(".grid-add-multiple-rows").hide();
		   $(".grid-download").hide();
		   $(".grid-upload").hide();
		}
		if(!frm.doc.set_source_warehouse){
		   frm.set_df_property('set_source_warehouse', 'read_only', 0);
		}
		else{
		    $.each(frm.doc.items || [], function(i, d) {
		    d.warehouse = frm.doc.set_source_warehouse;
		    });
		    refresh_field("items");
		   frm.set_df_property('set_source_warehouse', 'read_only', 1);
		   var d = frappe.meta.get_docfield("Delivery Note Item", "warehouse", cur_frm.doc.name);
           d.read_only = 1;
		}
}
});

