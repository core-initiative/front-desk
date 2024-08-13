frappe.ui.form.on("Purchase Order", {
    refresh: function (frm) {
        if (frm.doc.docstatus === 0) {
            frm.add_custom_button(
                __("Check Last Purchase"),
                async function () {
                    for (const row of frm.doc.items) {
                        await get_last_purchase(frm, row)
                    }
                    refresh_field("items")
                }
            )
        }
    },
    before_save: async function (frm) {
        for (const row of frm.doc.items) {
            await get_last_purchase(frm, row)
        }
    }
})

frappe.ui.form.on("Purchase Order Item", {
    item_code: async function (frm, cdt, cdn) {
        var row = locals[cdt][cdn]

        await get_last_purchase(frm, row)
        refresh_field("items")
    }
})


async function get_last_purchase(frm, row) {
    let result = await frappe.call({
        method: "inn.overrides.erpnext.accounts.purchase_order.purchase_order.get_last_purchase_request",
        args: {
            item_code: row.item_code
        }
    })
    result = result.message
    row.custom_last_purchased_quantity = result.last_purchased_quantity
    row.custom_last_purchase_order = result.last_purchase_order
    row.custom_last_purchase_date = result.transaction_date
}