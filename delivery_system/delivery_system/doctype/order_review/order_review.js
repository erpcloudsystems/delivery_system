// Copyright (c) 2019, Tech Station and contributors
// For license information, please see license.txt

frappe.ui.form.on("Order Review", {
    onload: function (frm) {
        if (frm.doc.docstatus == 1 && frm.doc.status == "Hold") {
            frm.dirty();
        }

        if (frm.doc.docstatus === 0 && frm.doc.modify_address === 0) {
            frappe.call({
                "method": "delivery_system.utils.get_contact.getAPP",
                args: {
                    app_name: "customize_crm",
                },
                callback: function (r) {
                    if (r.message == 1) {
                        frm.set_df_property('house_number', 'hidden', 0);
                        frm.set_df_property('apartment_number', 'hidden', 0);
                        frm.set_df_property('floor', 'hidden', 0);
                        frm.set_df_property('way_to_climb', 'hidden', 0);
                        frm.set_df_property('special_marque', 'hidden', 0);
                        frm.set_df_property('preferred_method_of_communication', 'hidden', 0);
                        frm.set_df_property('watsapp', 'hidden', 0);
                        frm.set_df_property('telegram', 'hidden', 0);
                    }
                    else {
                        frm.set_df_property('house_number', 'hidden', 1);
                        frm.set_df_property('apartment_number', 'hidden', 1);
                        frm.set_df_property('floor', 'hidden', 1);
                        frm.set_df_property('way_to_climb', 'hidden', 1);
                        frm.set_df_property('special_marque', 'hidden', 1);
                        frm.set_df_property('preferred_method_of_communication', 'hidden', 1);
                        frm.set_df_property('watsapp', 'hidden', 1);
                        frm.set_df_property('telegram', 'hidden', 1);
                    }
                }
            });
        }
        if (frm.doc.customer && frm.doc.docstatus === 0 && frm.doc.modify_contact === 0) {
            frappe.call({
                "method": "delivery_system.utils.get_contact.getContact",
                args: {
                    customer: frm.doc.customer,
                    app_name: "customize_crm"
                },
                callback: function (r) {
                    if (r.message) {
                        var len = r.message.length;
                        for (var i = 0; i < len; i++) {
                            frm.set_value("preferred_method_of_communication", r.message[i][0]);
                            frm.set_value("phone", r.message[i][1]);
                            frm.set_value("mobile_no", r.message[i][2]);
                            frm.set_value("mobile_no_1", r.message[i][3]);
                            frm.set_value("watsapp", r.message[i][4]);
                            frm.set_value("telegram", r.message[i][5]);
                            frm.set_value("contact", r.message[i][6]);
                        }
                        frm.refresh_fields();
                    }
                }
            });
        }
        if (frm.doc.select_shipping_address && frm.doc.docstatus === 0 && frm.doc.modify_address === 0) {
            frappe.call({
                "method": "delivery_system.utils.get_contact.getORAddress",
                args: {
                    address: frm.doc.select_shipping_address,
                    app_name: "customize_crm"
                },
                callback: function (r) {
                    if (r.message) {
                        var len = r.message.length;
                        for (var i = 0; i < len; i++) {
                            frm.set_value("address", r.message[i][0]);
                            frm.set_value("citytown", r.message[i][1]);
                            frm.set_value("street", r.message[i][2]);
                            frm.set_value("country", r.message[i][3]);
                            frm.set_value("postal_code", r.message[i][4]);
                            frm.set_value("house_number", r.message[i][5]);
                            frm.set_value("apartment_number", r.message[i][6]);
                            frm.set_value("floor", r.message[i][7]);
                            frm.set_value("way_to_climb", r.message[i][8]);
                            frm.set_value("special_marque", r.message[i][9]);
                        }
                        frm.refresh_fields();
                    }
                }
            });
        }
        if (frm.doc.customer && frm.doc.docstatus === 0) {
            frappe.call({
                "method": "delivery_system.utils.customer_rating.sfRating",
                args: {
                    customer: frm.doc.customer,
                },
                callback: function (r) {
                    if (r.message) {
                        frm.set_value("total_successful_orders", r.message[0][0]);
                    }
                }
            });
        }
        if (frm.doc.customer && frm.doc.docstatus === 0) {
            frappe.call({
                "method": "delivery_system.utils.customer_rating.lastsucRating",
                args: {
                    customer: frm.doc.customer
                },
                callback: function (r) {
                    if (r.message) {
                        frm.set_value("successful_orders", r.message[0][0]);
                    }
                }
            });
        }
        if (frm.doc.customer && frm.doc.docstatus === 0) {
            frappe.call({
                "method": "delivery_system.utils.customer_rating.lastfailRating",
                args: {
                    customer: frm.doc.customer
                },
                callback: function (r) {
                    if (r.message) {
                        frm.set_value("failed_orders", r.message[0][0]);
                    }
                }
            });
        }
        if (frm.doc.customer && frm.doc.docstatus === 0) {
            frappe.call({
                "method": "delivery_system.utils.customer_rating.lastpendingRating",
                args: {
                    customer: frm.doc.customer
                },
                callback: function (r) {
                    if (r.message) {
                        frm.set_value("pending_order", r.message[0][0]);
                    }
                }
            });
        }
        if (frm.doc.customer && frm.doc.docstatus === 0) {
            frappe.call({
                "method": "delivery_system.utils.customer_rating.daysRating",
                args: {
                    customer: frm.doc.customer
                },
                callback: function (r) {
                    if (r.message) {
                        frm.set_value("last_order_before", r.message[0][0]);
                    }
                }
            });
        }
        if (frm.doc.customer && frm.doc.docstatus === 0) {
            frappe.call({
                "method": "delivery_system.utils.customer_rating.pendingRating",
                args: {
                    customer: frm.doc.customer
                },
                callback: function (r) {
                    if (r.message) {
                        frm.set_value("total_pending_order", r.message[0][0]);
                    }
                }
            });
        }
        if (frm.doc.customer && frm.doc.docstatus === 0) {
            frappe.call({
                "method": "delivery_system.utils.customer_rating.failRating",
                args: {
                    customer: frm.doc.customer
                },
                callback: function (r) {
                    if (r.message) {
                        frm.set_value("total_failed_orders", r.message[0][0]);
                    }
                }
            });
        }
        if (frm.doc.customer && frm.doc.docstatus === 0) {
            frappe.call({
                "method": "delivery_system.utils.customer_rating.totalRating",
                args: {
                    customer: frm.doc.customer
                },
                callback: function (r) {
                    if (r.message) {
                        frm.set_value("total_orders", r.message[0][0]);
                    }
                }
            });
        }
    }
});

frappe.ui.form.on('Order Review', {
    validate: function (frm) {
        if (frm.doc.status == 'Draft') {
            msgprint("Status Can Not Be Draft, It Should Be Confirmed Or Rejected");
            validated = false;
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

frappe.ui.form.on('Order Review', {
    refresh: function (frm) {
        frm.set_query("sub_territory", function () {
            return {
                "filters": {
                    "parent_territory": frm.doc.territory,
                    "enabled": 1
                }
            };
        });
        frm.set_df_property('status', 'reqd', 1);
        frm.set_df_property('rejection_reason', 'reqd', 0);
        update_multipayment_status(frm);
    },
    status: function (frm) {
        if (frm.doc.status == 'Confirmed') {
            frm.set_df_property('rejection_reason', 'reqd', 0);
        }
        if (frm.doc.status == 'Rejected') {
            frm.set_df_property('rejection_reason', 'reqd', 1);
        }
    }
});

frappe.ui.form.on('Order Review', 'warehouse', function (frm) {
    $.each(frm.doc.items || [], function (i, d) {
        d.warehouse = frm.doc.warehouse;
    });
    refresh_field("items");
});


frappe.ui.form.on("Order Review", "onload", function (frm) {
    cur_frm.set_query("warehouse", function () {
        return {
            "filters": {
                "company": frm.doc.company
            }
        };
    });
});

frappe.ui.form.on('Order Review', {
    shipping_type: function (frm) {
        if (frm.doc.shipping_type && frm.doc.territory) {
            frappe.call({
                "method": "delivery_system.delivery_system.doctype.shipping_type.shipping_type.getFee",
                args: {
                    shipping_type: frm.doc.shipping_type,
                    territory: frm.doc.territory
                },
                callback: function (r) {
                    if (frm.doc.grand_total < frm.doc.invoice_value_for_free_shipping) {
                        frm.set_value("shipping_fee", r.message);
                    }
                    else {
                        frm.set_value("shipping_fee", 0);
                    }
                    frm.set_value("outstanding_amount", (frm.doc.grand_total + frm.doc.shipping_fee + frm.doc.bank_fee) - frm.doc.advance_paid);
                }
            });
        }
    },
    territory: function (frm) {
        if (frm.doc.shipping_type && frm.doc.territory) {
            frappe.call({
                "method": "delivery_system.delivery_system.doctype.shipping_type.shipping_type.getFee",
                args: {
                    shipping_type: frm.doc.shipping_type,
                    territory: frm.doc.territory
                },
                callback: function (r) {
                    if (frm.doc.grand_total < frm.doc.invoice_value_for_free_shipping) {
                        frm.set_value("shipping_fee", r.message);
                    }
                    else {
                        frm.set_value("shipping_fee", 0);
                    }
                    frm.set_value("outstanding_amount", (frm.doc.grand_total + frm.doc.shipping_fee + frm.doc.bank_fee) - frm.doc.advance_paid);
                }
            });
        }
    }
});

frappe.ui.form.on('Order Review', {
    setup: function (frm) {
        frm.set_query('select_shipping_address', function (doc) {
            return {
                query: 'frappe.contacts.doctype.address.address.address_query',
                filters: {
                    link_doctype: 'Customer',
                    link_name: doc.customer
                }
            };
        });
    }
});

frappe.ui.form.on('Order Review', {
    modify_contact: function (frm) {
        contact_section(frm);
    },
    modify_address: function (frm) {
        address_section(frm);
    },
    refresh: function (frm) {
        address_section(frm);
        contact_section(frm);
    }
});

function update_multipayment_status(frm) {
	$.each(frm.doc.multiple_payment,  function(i,  d) {
		if(!frm.is_new()){
		frappe.call({
			method: "delivery_system.hook.sales_order.get_PaymentEntry_data",
			args: {
				order_no: frm.doc.sales_order,
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

function address_section(frm) {
	if (frm.doc.modify_address == 1) {
        frm.set_df_property('address', 'read_only', 0);
        frm.set_df_property('citytown', 'read_only', 0);
        frm.set_df_property('street', 'read_only', 0);
        frm.set_df_property('country', 'read_only', 0);
        frm.set_df_property('postal_code', 'read_only', 0);
        frm.set_df_property('house_number', 'read_only', 0);
        frm.set_df_property('apartment_number', 'read_only', 0);
        frm.set_df_property('floor', 'read_only', 0);
        frm.set_df_property('way_to_climb', 'read_only', 0);
        frm.set_df_property('number_of_stairs', 'read_only', 0);
        frm.set_df_property('special_marque', 'read_only', 0);
        frm.set_df_property('territory', 'read_only', 0);
        frm.set_df_property('sub_territory', 'read_only', 0);
    }
    if (frm.doc.modify_address === 0) {
        frm.set_df_property('address', 'read_only', 1);
        frm.set_df_property('citytown', 'read_only', 1);
        frm.set_df_property('street', 'read_only', 1);
        frm.set_df_property('country', 'read_only', 1);
        frm.set_df_property('postal_code', 'read_only', 1);
        frm.set_df_property('house_number', 'read_only', 1);
        frm.set_df_property('apartment_number', 'read_only', 1);
        frm.set_df_property('floor', 'read_only', 1);
        frm.set_df_property('way_to_climb', 'read_only', 1);
        frm.set_df_property('number_of_stairs', 'read_only', 1);
        frm.set_df_property('special_marque', 'read_only', 1);
        frm.set_df_property('territory', 'read_only', 1);
        frm.set_df_property('sub_territory', 'read_only', 1);
    }
}

function contact_section(frm) {
	if (frm.doc.modify_contact == 1) {
        frm.set_df_property('preferred_method_of_communication', 'read_only', 0);
        frm.set_df_property('phone', 'read_only', 0);
        frm.set_df_property('mobile_no', 'read_only', 0);
        frm.set_df_property('mobile_no_1', 'read_only', 0);
        frm.set_df_property('watsapp', 'read_only', 0);
        frm.set_df_property('telegram', 'read_only', 0);
    }
    if (frm.doc.modify_contact === 0) {
        frm.set_df_property('preferred_method_of_communication', 'read_only', 1);
        frm.set_df_property('phone', 'read_only', 1);
        frm.set_df_property('mobile_no', 'read_only', 1);
        frm.set_df_property('mobile_no_1', 'read_only', 1);
        frm.set_df_property('watsapp', 'read_only', 1);
        frm.set_df_property('telegram', 'read_only', 1);
    }
}