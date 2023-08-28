// Copyright (c) 2019, Tech Station and contributors
// For license information, please see license.txt

frappe.ui.form.on("Processing", "onload", function (frm) {
    if (frm.doc.docstatus == 0) {
        set_field_options("processing", ["Draft", "Processed", "Processing Rejected"])
    }
    if (frm.doc.send_for_material_transfer == 1) {
        frm.set_df_property('transfer_to_warehouse', 'read_only', 0);
        frm.set_df_property('transfer_to_warehouse', 'reqd', 1);
    }
    if (frm.doc.send_for_material_transfer === 0) {
        frm.set_df_property('transfer_to_warehouse', 'read_only', 1);
        frm.set_df_property('transfer_to_warehouse', 'reqd', 0);
    }
    if (frm.doc.docstatus == 1 && frm.doc.processing == "Released") {
        frm.dirty();
    }
});

frappe.ui.form.on('Processing', {
    validate: function (frm) {
        if ((frm.doc.hold_order === 0) && (frm.doc.processing == 'Draft' || frm.doc.processing == 'Source Received' || frm.doc.processing == 'Delivered' ||
            frm.doc.processing == 'Delivery Rejected' || frm.doc.processing == 'Delivery Delay')) {
            msgprint("Status Can Not Be Draft, Source Received, Delivered, Delivery Rejected,It Should Be Processed Or Processing Rejected");
            validated = false;
        }
    }
});

frappe.ui.form.on('Processing', {
    refresh: function (frm) {
        getStockBalance(frm);
        if(frm.doc.docstatus === 0){
            getStockBalance(frm);
        }    
        if (frm.doc.docstatus == 1 && frm.doc.processing != "Hold") {
            frm.set_df_property('shipping_by', 'read_only', 1);
            frm.set_df_property('source', 'read_only', 1);
            frm.set_df_property('delivery_car', 'read_only', 1);
            frm.set_df_property('car_drivers', 'read_only', 1);
            frm.set_df_property('delivery_date', 'read_only', 1);
        }
        if (frm.doc.docstatus == 1 && frm.doc.processing == "Hold") {
            frm.set_df_property('shipping_by', 'read_only', 0);
            frm.set_df_property('source', 'read_only', 0);
            frm.set_df_property('rejection_reason', 'reqd', 0);
            frm.set_df_property('shipping_by', 'reqd', 1);
            frm.set_df_property('source', 'reqd', 1);
            frm.set_df_property('warehouse', 'reqd', 1);
        }
        if (frm.doc.docstatus == 1 && frm.doc.processing == "Released") {
            frappe.msgprint({
                title: __('Alert'),
                indicator: 'red',
                message: __('This Order was on Hold and now it has been Released For Next Stage<br><br> \
                Please Add Required Data to process it for next stage.')
            });
            frm.set_df_property('shipping_by', 'read_only', 0);
            frm.set_df_property('source', 'read_only', 0);
            frm.set_df_property('hold_reason', 'read_only', 0);
            frm.set_df_property('shipping_by', 'reqd', 1);
            frm.set_df_property('shipping_by', 'reqd', 1);
            frm.set_df_property('hold_reason', 'reqd', 1);
        }
    },
    processing: function (frm) {
        if (frm.doc.processing == 'Draft') {
            frm.set_df_property('shipping_by', 'reqd', 0);
            frm.set_df_property('source', 'reqd', 0);
            frm.set_df_property('rejection_reason', 'reqd', 0);
        }

        if (frm.doc.processing == 'Processed') {
            frm.set_df_property('shipping_by', 'reqd', 1);
            frm.set_df_property('source', 'reqd', 1);
            frm.set_df_property('rejection_reason', 'reqd', 0);
            frm.set_df_property('delivery_date', 'read_only', 0);
            frm.set_df_property('shipping_by', 'read_only', 0);
            frm.set_df_property('source', 'read_only', 0);
            frm.set_df_property('delivery_car', 'read_only', 0);
            frm.set_df_property('car_drivers', 'read_only', 0);
        }
        if (frm.doc.processing == 'Processing Rejected') {
            frm.set_df_property('shipping_by', 'reqd', 0);
            frm.set_df_property('source', 'reqd', 0);
            frm.set_df_property('rejection_reason', 'reqd', 1);
            frm.set_df_property('delivery_date', 'read_only', 1);
        }
    },
    modify: function (frm) {
        if (frm.doc.modify && (frm.doc.processing == "Processed" || frm.doc.processing == "Delivery Delay")) {
            frm.set_df_property('shipping_by', 'read_only', 0);
            frm.set_df_property('source', 'read_only', 0);
            frm.set_df_property('delivery_car', 'read_only', 0);
            frm.set_df_property('car_drivers', 'read_only', 0);
            frm.set_df_property('delivery_date', 'read_only', 0);
        }
        if (!frm.doc.modify) {
            frm.set_df_property('shipping_by', 'read_only', 1);
            frm.set_df_property('source', 'read_only', 1);
            frm.set_df_property('delivery_car', 'read_only', 1);
            frm.set_df_property('car_drivers', 'read_only', 1);
            frm.set_df_property('delivery_date', 'read_only', 1);
        }
    },
    send_for_material_transfer: function (frm) {
        if (frm.doc.send_for_material_transfer == 1) {
            frm.set_df_property('transfer_to_warehouse', 'read_only', 0);
            frm.set_df_property('transfer_to_warehouse', 'reqd', 1);
        }
        if (frm.doc.send_for_material_transfer === 0) {
            frm.set_df_property('transfer_to_warehouse', 'read_only', 1);
            frm.set_df_property('transfer_to_warehouse', 'reqd', 0);
        }
    }
});

frappe.ui.form.on("Processing", "refresh", function (frm) {
    frm.set_query("delivery_car", function () {
        return {
            "filters": {
                "company": frm.doc.company,
                "enabled": 1
            }
        };
    });

    frm.set_query("car_drivers", function () {
        return {
            "filters": {
                "company": frm.doc.company,
                "enabled": 1
            }
        };
    });

    frm.set_query("territory_group", function () {
        return {
            "filters": {
                "company": frm.doc.company,
                "is_group": 1
            }
        };
    });

    frm.set_query("transfer_to_warehouse", function () {
        return {
            filters: [
                ['Warehouse', 'company', '=', frm.doc.company],
				['Warehouse', 'name', '!=', frm.doc.warehouse],
				['Warehouse', 'is_group', '=', 0]
			]
        };
    });

});

frappe.ui.form.on("Processing", {
    source: function (frm) {
        if (frm.doc.source && frm.doc.docstatus === 0) {
            frappe.call({
                "method": "delivery_system.utils.get_contact.getShippingContact",
                args: {
                    shipping_by: frm.doc.shipping_by,
                    source: frm.doc.source
                },
                callback: function (r) {
                    var len = r.message.length;
                    for (var i = 0; i < len; i++) {
                        frm.set_value("mobile_number", r.message[i][0]);
                    }
                    frm.refresh_fields();
                }
            });
        }
    }
});


frappe.ui.form.on("Processing", "shipping_by", function (frm) {
    frm.set_value("source","");
    frm.set_value("user","");
    frm.set_value("warehouse","");
    cur_frm.set_query("source", function () {
        return {
            "filters": {
                "company": frm.doc.company,
                "enabled": 1
            }
        };
    });
});

/*******************************************************************************/

frappe.ui.form.on("Processing", {
    "cancel_order": function (frm) {
        if (!frm.doc.order_review && frm.doc.processing == "Processed") {
            frappe.confirm(
                'Are You Sure ?',
                function () {
                    frappe.call({
                        "method": "delivery_system.delivery_system.doctype.processing.processing.cancel_order_1",
                        args: {
                            so: frm.doc.sales_order_1,
                            doc: frm.doc.sales_order_1
                        },
                        callback: function (r) {
                            frm.refresh();
                        }
                    })
                },
                function () {
                    show_alert('Thanks!')
                }
            )
        }
    }
});

frappe.ui.form.on("Processing", {
    "cancel_order": function (frm) {
        if (frm.doc.order_review && frm.doc.processing == "Processed") {
            frappe.confirm(
                'Are You Sure ?',
                function () {
                    frappe.call({
                        "method": "delivery_system.delivery_system.doctype.processing.processing.cancel_order",
                        args: {
                            so: frm.doc.sales_order_1,
                            order: frm.doc.order_review,
                            doc: frm.doc.sales_order_1
                        },
                        callback: function (r) {
                            frm.refresh();
                        }
                    })
                },
                function () {
                    show_alert('Thanks!')
                }
            )
        }
    }
});

/***********************************************************************************/

frappe.ui.form.on("Processing", {
    "cancel_order": function (frm) {
        if (!frm.doc.order_review && frm.doc.processing == "Delivery Delay") {
            frappe.confirm(
                'Are You Sure ?',
                function () {
                    frappe.call({
                        "method": "delivery_system.delivery_system.doctype.processing.processing.CanDelay",
                        args: {
                            so: frm.doc.sales_order_1,
                            order: frm.doc.order_review
                        },
                        callback: function (r) {
                            frm.refresh();
                        }
                    })
                },
                function () {
                    show_alert('Thanks!')
                }
            )
        }
    }
});

frappe.ui.form.on("Processing", {
    "cancel_order": function (frm) {
        if (frm.doc.order_review && frm.doc.processing == "Delivery Delay") {
            frappe.confirm(
                'Are You Sure ?',
                function () {
                    frappe.call({
                        "method": "delivery_system.delivery_system.doctype.processing.processing.CanDelay_1",
                        args: {
                            so: frm.doc.sales_order_1,
                            order: frm.doc.order_review
                        },
                        callback: function (r) {
                            frm.refresh();
                        }
                    })
                },
                function () {
                    show_alert('Thanks!')
                }
            )
        }
    }
});

frappe.ui.form.on('Processing', {
    onload: function (frm) {
        if ((frm.doc.processing == "Processed" || frm.doc.processing == "Delivery Delay") && frm.doc.docstatus == 1) {
            frm.set_df_property('cancel_order', 'hidden', 0);
            frm.set_df_property('modify', 'hidden', 0);
        }
        if (frm.doc.processing == "Draft" || frm.doc.docstatus == 0) {
            frm.set_df_property('cancel_order', 'hidden', 1);
            frm.set_df_property('modify', 'hidden', 1);
        }
    }
});

frappe.ui.form.on('Processing', {
    hold_order: function (frm) {
        if (frm.doc.hold_order == 1) {
            frm.set_df_property('hold_reason', 'reqd', 1);
            frm.set_df_property('hold_release_date', 'reqd', 1);
            frm.set_value("processing", "Hold");
            frm.set_df_property('processing', 'read_only', 1);
            frm.set_df_property('delivery_car', 'reqd', 0);
            frm.set_df_property('car_drivers', 'reqd', 0);
        }
        if (frm.doc.hold_order === 0) {
            frm.set_df_property('hold_reason', 'reqd', 0);
            frm.set_df_property('hold_release_date', 'reqd', 0);
            frm.set_value("processing", "Draft");
            frm.set_df_property('processing', 'read_only', 0);
        }
    },
    continue_hold_order: function (frm) {
        frappe.call({
            "method": "re_process_hold_order",
            doc: frm.doc,
            callback: function (r) {
                
            }
        })
    }
});


frappe.ui.form.on('Processing', {
    warehouse: function (frm) {
        if (frm.doc.warehouse) {
            $.each(frm.doc.items || [], function (i, d) {
                d.warehouse = frm.doc.warehouse;
            });
            refresh_field("items");
        }
    }
});

function update_multipayment_status(frm) {
	$.each(frm.doc.multiple_payment,  function(i,  d) {
		if(!frm.is_new()){
		frappe.call({
			method: "delivery_system.hook.sales_order.get_PaymentEntry_data",
			args: {
				order_no: frm.doc.so,
				mode_of_payment: d.payment_method,
				paid_amount: d.amount,
			},
			callback: function (r) {
				if (r.message == 1 && d.create_payment_entry_on_delivery === 0){
					d.status = "<span class=\"indicator-pill whitespace-nowrap green\"> <span>Paid</span></span>";
				}
				else{
					d.status = "<span class=\"indicator-pill whitespace-nowrap orange\"> <span>Unpaid</span></span>";
				}
				frm.refresh_fields();
			}
		});
		}
        if(d.create_payment_entry_on_delivery === 0 && d.create_payment_entry_on_so == 0){
			d.payment_stage = "<span class=\"indicator-pill whitespace-nowrap red\"><span>Payment Not Specified</span></span>";
		}
		if(d.create_payment_entry_on_delivery === 0 && d.create_payment_entry_on_so == 1){
			d.payment_stage = "<span class=\"indicator-pill whitespace-nowrap green\"><span>Advance Payment</span></span>";
		}
		if(d.create_payment_entry_on_delivery === 1 && d.create_payment_entry_on_so == 0){
			d.payment_stage = "<span class=\"indicator-pill whitespace-nowrap orange\"><span>Payment With Delivery</span></span>";
		}
	});
}

function getStockBalance(frm) {
	$.each(frm.doc.items,  function(i,  d) {
		if(d.warehouse && d.item_code){
	    frappe.call({
		"method": "delivery_system.delivery_system.doctype.processing.processing.get_balance_qty_from_sle",
		    args: {
			    item_code: d.item_code,
		    	warehouse: d.warehouse
		    },
		    callback:function(r){
                console.log(r.message)
		        frappe.model.set_value(d.doctype, d.name, "stock_quantity", r.message);
            }
        });
    }
});
    frm.refresh_fields("item_stock_table");
}