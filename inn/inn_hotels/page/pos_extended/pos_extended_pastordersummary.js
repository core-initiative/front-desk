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

        bind_events() {
            super.bind_events();

            this.$summary_container.on('click', '.show-btn', () => {
                console.log(this.doc)
                this.events.print_bill(this.doc)
            });
        }

        get_condition_btn_map(after_submission) {
            if (after_submission)
                return [{ condition: true, visible_btns: ['Print Receipt', 'Email Receipt', 'New Order'] }];

            return [
                { condition: this.doc.docstatus === 0, visible_btns: ['Show Bill', 'Edit Order', 'Delete Order'] },
                { condition: !this.doc.is_return && this.doc.docstatus === 1, visible_btns: ['Print Receipt', 'Email Receipt', 'Return'] },
                { condition: this.doc.is_return && this.doc.docstatus === 1, visible_btns: ['Print Receipt', 'Email Receipt'] }
            ];
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
            var me = this

            frappe.call({
                method: "inn.inn_hotels.page.pos_extended.pos_extended.get_table_number",
                args: {
                    invoice_name: doc.name
                },
                async: false,
                callback: function (r) {
                    table_number = r.message.table
                    me.transfer_to_folio = r.message.transfer_to_folio
                }
            })

            if (this.transfer_to_folio != null) {
                this.$payment_container.append(`
                <div class="summary-row-wrapper payments">
					<div>Transferred to</div>
					<div>${this.transfer_to_folio}</div>
				</div>`);
            }

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