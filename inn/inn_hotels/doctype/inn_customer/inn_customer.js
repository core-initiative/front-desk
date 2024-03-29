// Copyright (c) 2024, Core Initiative and contributors
// For license information, please see license.txt

frappe.ui.form.on("Inn Customer", {
    refresh(frm) {
        fieldToggle(frm)
    },
    after_save(frm) {
        let path = "/app/inn-reservation/new"
        window.location.href = window.location.protocol + "//" + window.location.host + path
    }
});

function fieldToggle(frm) {
    console.log(frm.doc.__islocal)
    if (frm.doc.__islocal === 1) {
        frm.set_df_property('supplier_name', 'hidden', 1);
        frm.set_df_property('customer', 'hidden', 1);
    } else {
        frm.set_df_property('supplier_name', 'read_only', 1);
        frm.set_df_property('customer_name', 'read_only', 1);
    }
}
