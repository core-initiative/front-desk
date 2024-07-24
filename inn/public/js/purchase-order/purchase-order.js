frappe.ui.form.on("Purchase Order Item", {

    item_code: async function (frm, cdt, cdn) {
        var row = locals[cdt][cdn]
        console.log("called")

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
        refresh_field("items")
    }
})