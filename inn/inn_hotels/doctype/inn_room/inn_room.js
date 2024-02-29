// Copyright (c) 2020, Core Initiative and contributors
// For license information, please see license.txt

frappe.ui.form.on('Inn Room', {
	refresh: function (frm, cdt, cdn) {

		set_option_floor_plan(frm)

		if (frappe.user.has_role('Housekeeping') ||
			frappe.user.has_role('Housekeeping Assistant') ||
			frappe.user.has_role('Housekeeping Supervisor') ||
			frappe.user.has_role('Administrator')) {
			if (frm.doc.room_status == 'Occupied Dirty' ||
				frm.doc.room_status == 'Vacant Dirty' ||
				frm.doc.room_status == 'Vacant Clean') {
				frm.page.add_menu_item(__('Clean Room'), function () {
					frappe.confirm(
						__('You are about to update status of Room ' + frm.doc.name + ', are you sure?'),
						() => {
							frappe.call({
								method: 'inn.inn_hotels.doctype.inn_room.inn_room.update_single_room_status',
								args: {
									room: frm.doc.name,
									mode: 'clean'
								},
								callback: (r) => {
									if (r.message) {
										frm.reload_doc();
										frappe.msgprint(r.message);
									}
								}
							});
						});
				})
			}
			else if (frm.doc.room_status == 'Vacant Clean' ||
				frm.doc.room_status == 'Vacant Ready' ||
				frm.doc.room_status == 'Occupied Clean') {
				frm.page.add_menu_item(__('Dirty Room'), function () {
					frappe.confirm(
						__('You are about to update status of Room ' + frm.doc.name + ', are you sure?'),
						() => {
							frappe.call({
								method: 'inn.inn_hotels.doctype.inn_room.inn_room.update_single_room_status',
								args: {
									room: frm.doc.name,
									mode: 'dirty'
								},
								callback: (r) => {
									if (r.message) {
										frm.reload_doc();
										frappe.msgprint(r.message);
									}
								}
							});
						});
				})
			}
		}
		frm.add_custom_button(__('Clear Door Status'), function () {
			frappe.db.set_value(cdt, cdn, 'door_status', 'No Status');
			frappe.show_alert('Door Status Cleared');
		});
		frm.add_custom_button(__('Do Not Disturb'), function () {
			if (frm.doc.room_status === 'Occupied Clean' || frm.doc.room_status === 'Occupied Dirty') {
				frappe.db.set_value(cdt, cdn, 'door_status', 'Do Not Disturb');
				frappe.show_alert('Door Status set to Do Not Disturb');
			}
			else {
				frappe.show_alert('Door Status cannot be changed in Vacant Room');
			}
		});
		frm.add_custom_button(__('Double Lock'), function () {
			if (frm.doc.room_status === 'Occupied Clean' || frm.doc.room_status === 'Occupied Dirty') {
				frappe.db.set_value(cdt, cdn, 'door_status', 'Double Lock');
				frappe.show_alert('Door Status set to Double Lock');
			}
			else {
				frappe.show_alert('Door Status cannot be changed in Vacant Room');
			}
		});
		frm.add_custom_button(__('Sleep Out'), function () {
			if (frm.doc.room_status === 'Occupied Clean' || frm.doc.room_status === 'Occupied Dirty') {
				frappe.db.set_value(cdt, cdn, 'door_status', 'Sleeping Out');
				frappe.show_alert('Door Status set to Sleep Out');
			}
			else {
				frappe.show_alert('Door Status cannot be changed in Vacant Room');
			}
		});
	},
	amenities_template: function (frm) {
		if (frm.doc.amenities_template) {
			frappe.call({
				method: "inn.inn_hotels.doctype.inn_room.inn_room.copy_amenities_template",
				args: {
					amenities_type_id: frm.doc.amenities_template
				},
				callback: (response) => {
					if (response.message) {
						frm.set_value('amenities', []);
						$.each(response.message, function (i, d) {
							var item = frm.add_child('amenities');
							item.item = d.item;
							item.item_name = d.item_name;
							item.qty = d.qty;
						});
					}
					frm.refresh_field('amenities');
				}
			})
		}
	},
});

let form_control_field;

async function set_option_floor_plan(frm) {
	wrapper = $(".layout-main-section").find('div[data-fieldname="room_detail"]').find('.section-body').find('div[data-fieldname="column_break"').find("form")
	if (!wrapper.find('[data-fieldname="floor_choice"]').length) {
		await create_choice_field_floor(frm, wrapper)
	}

	if (!frm.__islocal) {
		form_control_field.set_value(frm.doc.floor)
	}
}

async function create_choice_field_floor(frm, wrapper) {
	frm.set_df_property("floor", "hidden", true)
	let opt_floor = [""]

	await frappe.db.get_single_value("Inn Hotels Setting", "number_of_floor",)
		.then(num => {
			opt_floor = ([...Array(num).keys()].map(x => ++x))
			opt_floor.splice(0, 0, 0)
		})

	form_control_field = frappe.ui.form.make_control({
		parent: wrapper,
		df: {
			label: "Floor",
			fieldname: "floor_choice",
			fieldtype: "Select",
			options: opt_floor,
			onchange: function () {
				frm.set_value("floor", this.value)
			}
		},
		render_input: true
	})
}