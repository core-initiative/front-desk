frappe.ui.form.on("POS Closing Entry", {
    async refresh(frm) {
        frm.draft_invoice = await frappe.call({
            method: "inn.overrides.erpnext.accounts.pos_closing_entry.pos_closing_entry.get_draft_pos_invoice",
            args: {
                start: frappe.datetime.get_datetime_as_string(frm.doc.period_start_date),
                end: frappe.datetime.get_datetime_as_string(frm.doc.period_end_date),
                pos_profile: frm.doc.pos_profile,
                user: frm.doc.user,
            }
        })
        frm.draft_invoice = frm.draft_invoice.message
        if (frm.draft_invoice.length > 0) {
            frm.disable_save()
            frm.dashboard.set_headline(
                __(
                    "There are POS Invoice that not paid yet, please overhandle at Create Overhandle"
                )
            )
        }


        frm.add_custom_button(__("Create Overhandle"), async function () {
            await create_overhandle(frm)
        }, "Overhandle")

        frm.add_custom_button(__("Get Overhandle"), function () {
            get_overhandle(frm)
        }, "Overhandle")
    }
})

async function get_overhandle(frm) {
    frm.new_invoice = await frappe.call({
        method: "inn.overrides.erpnext.accounts.pos_closing_entry.pos_closing_entry.get_overhandled_pos_invoice",
        args: {
            pos_profile: frm.doc.pos_profile
        }
    })

    frm.new_invoice = frm.new_invoice.message
    frappe.msgprint({
        title: __("POS Invoice not Consolidated"),
        message: __(`
        <div>
            <p>These POS Invoice will be taken:</p> <ul>` +
            frm.new_invoice.map((invoice) => `<li><a href='/app/pos-invoice/${invoice.name}'>${invoice.name}</a> (${invoice.customer})</li>`).join("")
            + `</ul><p>Do you want to take these invoice(s)?</p>
        </div>
    `),
        primary_action_label: "Overhandle",
        primary_action: {
            async action() {

                await take_overhandle_pos_invoice(frm)

                frappe.show_alert({
                    message: `All POS Invoice has been overhandled`,
                    indicator: "green"
                })
                frappe.msg_dialog.hide()
            }
        },
        secondary_action: {
            action() {
                frappe.msg_dialog.hide()
            },
            label: "No"
        }
    })
}

async function take_overhandle_pos_invoice(frm) {
    frappe.require("/app/erpnext/erpnext/accounts/doctype/pos_closing_entry/pos_closing_entry.js")
    let overhandled_pos = await frappe.call({
        method: "inn.overrides.erpnext.accounts.pos_closing_entry.pos_closing_entry.take_overhandle_pos_invoice",
        args: {
            pos_invoice: frm.new_invoice,
            user: frm.doc.user
        }
    })

    overhandled_pos = overhandled_pos.message

    set_form_data(overhandled_pos, frm)
    refresh_fields(frm)
    set_html_data(frm)
}

async function create_overhandle(frm) {
    frappe.msgprint({
        title: __("POS Invoice not Consolidated"),
        message: __(`
        <div>
            <p>These POS Invoice is not consolidated yet:</p> <ul>` +
            frm.draft_invoice.map((invoice) => `<li><a href='/app/pos-invoice/${invoice.name}'>${invoice.name}</a> (${invoice.customer})</li>`).join("")
            + `</ul><p>Do you want to overhandle these?</p>
        </div>
    `),
        primary_action_label: "Overhandle",
        primary_action: {
            async action() {
                frm.enable_save()
                let overhandled_number = await frappe.call({
                    method: "inn.overrides.erpnext.accounts.pos_closing_entry.pos_closing_entry.overhandle_draft_pos_invoice",
                    args: {
                        pos_invoice: frm.draft_invoice,
                        user: frm.doc.user
                    }
                })
                overhandled_number = overhandled_number.message

                frappe.show_alert({
                    message: `${overhandled_number} POS Invoice has been overhandled`,
                    indicator: "green"
                })
                frappe.msg_dialog.hide()
            }
        },
        secondary_action: {
            action() {
                frappe.msg_dialog.hide()
            },
            label: "No"
        }
    })

}


// startcopy this is copied from pos_closing_entry erpnext

function set_form_data(data, frm) {
    data.forEach((d) => {
        add_to_pos_transaction(d, frm);
        frm.doc.grand_total += flt(d.grand_total);
        frm.doc.net_total += flt(d.net_total);
        frm.doc.total_quantity += flt(d.total_qty);
        refresh_payments(d, frm);
        refresh_taxes(d, frm);
    });
}


function add_to_pos_transaction(d, frm) {
    frm.add_child("pos_transactions", {
        pos_invoice: d.name,
        posting_date: d.posting_date,
        grand_total: d.grand_total,
        customer: d.customer,
    });
}

function refresh_payments(d, frm) {
    d.payments.forEach((p) => {
        const payment = frm.doc.payment_reconciliation.find(
            (pay) => pay.mode_of_payment === p.mode_of_payment
        );
        if (p.account == d.account_for_change_amount) {
            p.amount -= flt(d.change_amount);
        }
        if (payment) {
            payment.expected_amount += flt(p.amount);
            payment.closing_amount = payment.expected_amount;
            payment.difference = payment.closing_amount - payment.expected_amount;
        } else {
            frm.add_child("payment_reconciliation", {
                mode_of_payment: p.mode_of_payment,
                opening_amount: 0,
                expected_amount: p.amount,
                closing_amount: 0,
            });
        }
    });
}


function refresh_taxes(d, frm) {
    d.taxes.forEach((t) => {
        const tax = frm.doc.taxes.find((tx) => tx.account_head === t.account_head && tx.rate === t.rate);
        if (tax) {
            tax.amount += flt(t.tax_amount);
        } else {
            frm.add_child("taxes", {
                account_head: t.account_head,
                rate: t.rate,
                amount: t.tax_amount,
            });
        }
    });
}

function refresh_fields(frm) {
    frm.refresh_field("pos_transactions");
    frm.refresh_field("payment_reconciliation");
    frm.refresh_field("taxes");
    frm.refresh_field("grand_total");
    frm.refresh_field("net_total");
    frm.refresh_field("total_quantity");
}

function set_html_data(frm) {
    if (frm.doc.docstatus === 1 && frm.doc.status == "Submitted") {
        frappe.call({
            method: "get_payment_reconciliation_details",
            doc: frm.doc,
            callback: (r) => {
                frm.get_field("payment_reconciliation_details").$wrapper.html(r.message);
            },
        });
    }
}

// endcopy