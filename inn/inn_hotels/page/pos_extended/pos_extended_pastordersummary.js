frappe.require(["point-of-sale.bundle.js"], function () {

    inn.PointOfSale.PosExtendPastOrderSummary = class PosExtendPastOrderSummary extends erpnext.PointOfSale.PastOrderSummary {
        constructor({ wrapper, events }) {
            super({ wrapper, events })
        }

        async attach_document_info(doc) {
            await frappe.db.get_value('Customer', this.doc.customer, 'email_id').then(({ message }) => {
                doc.customer_email = message.email_id || '';
            });

            const upper_section_dom = this.get_upper_section_html(doc);
            this.$upper_section.html(upper_section_dom);
        }

        print_receipt() {
            const frm = this.events.get_frm();
            frappe.utils.print(
                this.doc.doctype,
                this.doc.name,
                "POS Extended Invoice",
                this.doc.letter_head,
                this.doc.language || frappe.boot.lang
            );
        }

        get_upper_section_html(doc) {
            const { status } = doc;
            let indicator_color = '';

            in_list(['Paid', 'Consolidated'], status) && (indicator_color = 'green');
            status === 'Draft' && (indicator_color = 'red');
            status === 'Return' && (indicator_color = 'grey');

            var table_number = undefined

            frappe.call({
                method: "inn.inn_hotels.page.pos_extended.pos_extended.get_table_number",
                args: {
                    invoice_name: doc.name
                },
                async: false,
                callback: function (r) {
                    table_number = r.message
                }
            })

            return `<div class="left-section">
                    <div class="customer-name">${doc.customer}</div>
                    <div class="customer-email">${doc.customer_email}</div>
                    <div class="table-number">${__('Table')}: ${table_number}</div>
                    <div class="cashier">${__('Sold by')}: ${doc.owner}</div>
                </div>
                <div class="right-section">
                    <div class="paid-amount">${format_currency(doc.paid_amount, doc.currency)}</div>
                    <div class="invoice-name">${doc.name}</div>
                    <span class="indicator-pill whitespace-nowrap ${indicator_color}"><span>${doc.status}</span></span>
                </div>`;
        }
    }

})