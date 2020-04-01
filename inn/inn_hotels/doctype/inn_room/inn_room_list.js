frappe.listview_settings['Inn Room'] = {
    onload: function (listview) {
        if (frappe.user.has_role('Housekeeping') ||
            frappe.user.has_role('Housekeeping Assistant') ||
            frappe.user.has_role('Housekeeping Supervisor') ||
            frappe.user.has_role('Administrator')) {
            listview.page.add_menu_item(__('Clean Room'), function () {
                if (listview.get_checked_items(true).length > 0) {
                    frappe.confirm(
                        __('You are about to update status of Room(s) ' + listview.get_checked_items(true) + ', are you sure?'),
                        () => {
                        frappe.call({
                            method: 'inn.inn_hotels.doctype.inn_room.inn_room.update_room_status',
                            args: {
                                rooms: listview.get_checked_items(true),
                                mode: 'clean'
                            },
                            callback: (r) => {
                                if (r.message) {
                                    listview.refresh();
                                    frappe.msgprint(r.message);
                                }
                            }
                        });
                    });
                }
                else {
                    frappe.msgprint("Please select at least one Room to be cleaned.");
                }
            });

            listview.page.add_menu_item(__('Dirty Room'), function () {
                if (listview.get_checked_items(true).length > 0) {
                    frappe.confirm(
                        __('You are about to update status of Room(s) ' + listview.get_checked_items(true) + ', are you sure?'),
                        () => {
                        frappe.call({
                            method: 'inn.inn_hotels.doctype.inn_room.inn_room.update_room_status',
                            args: {
                                rooms: listview.get_checked_items(true),
                                mode: 'dirty'
                            },
                            callback: (r) => {
                                if (r.message) {
                                    listview.refresh();
                                    frappe.msgprint(r.message);
                                }
                            }
                        });
                    });
                }
                else {
                    frappe.msgprint("Please select at least one Room to be set to Dirty.");
                }
            });
        }

    }
};