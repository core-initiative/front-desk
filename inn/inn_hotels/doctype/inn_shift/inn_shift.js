// Copyright (c) 2020, Core Initiative and contributors
// For license information, please see license.txt
var total_cash_count = 0;
var total_cash_qty = 0;
var total_payment = 0;
var total_refund = 0;

frappe.ui.form.on('Inn Shift', {
	onload: function(frm) {
		frm.set_df_property('total_cash_qty', 'hidden', 0);
		frm.get_field('cc_detail').grid.cannot_add_rows = true;
		frm.get_field('payment_detail').grid.cannot_add_rows = true;
		frm.get_field('refund_detail').grid.cannot_add_rows = true;
		if (frm.doc.__islocal === 1) {
			frappe.call({
				method: 'inn.inn_hotels.doctype.inn_shift.inn_shift.is_there_open_shift',
				callback: (r) => {
					if (r.message === 1) {
						frappe.set_route('List', 'Inn Shift');
						frappe.msgprint('A Shift already Opened. Please close it first before creating new one.');
					}
					else{
						let cash_count = [100, 200, 500, 1000, 2000, 5000, 10000, 20000, 50000, 100000];
						frm.set_value('cc_detail', []);
						for (var i = 0; i < cash_count.length; i++) {
							var item = frm.add_child('cc_detail');
							item.nominal = cash_count[i];
							item.qty = 0;
							item.amount = 0;
						}
						frm.refresh_field('cc_detail');
					}
				}
			});
		}
	}
});
frappe.ui.form.on('Inn CC Detail',{
	qty: function (frm, cdt, cdn) {
		let child = locals[cdt][cdn];
		child.amount = child.nominal*child.qty;
		frm.refresh_field('cc_detail');

		let cc_detail_list = frm.doc.cc_detail;
		total_cash_count = 0;
		total_cash_qty = 0;
		for (var i = 0; i < cc_detail_list.length; i++) {
			total_cash_count += cc_detail_list[i].amount;
			total_cash_qty += parseInt(cc_detail_list[i].qty, 10);
		}
		frm.set_value('total_cash_count', total_cash_count);
		frm.set_value('total_cash_qty', total_cash_qty);
	}
});
