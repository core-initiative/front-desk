frappe.require(["point-of-sale.bundle.js", "inn-pos.bundle.js"], function () {
    inn.PointOfSale.PosExtendItemCart = class PosExtendItemCart extends erpnext.PointOfSale.ItemCart {
        constructor({ wrapper, events, settings }) {
            super({ wrapper, events, settings });
        }
        init_child_components() {
            this.init_customer_selector();
            this.init_table_selector();
            this.init_cart_components();
        }

        init_table_selector() {
            this.$component.append(
                `<div class="table-section"></div>`
            )
            this.$table_section = this.$component.find('.table-section');
            this.make_table_selector();
        }


        make_table_selector() {
            this.$table_section.html(`<div class="table-field"></div>`)
            const me = this;
            this.table_field = frappe.ui.form.make_control({
                df: {
                    label: __('No Table'),
                    fieldtype: 'Link',
                    options: 'Inn Point Of Sale Table',
                    placeholder: __('Search table number'),
                    get_query: function () {
                        return {
                            filters: [
                                ["Inn Point Of Sale Table", "status", "=", "Empty"]
                            ]
                        }
                    },
                    onchange: function () {
                        me["table_number"] = this.get_value()
                        me.events.get_frm().dirty()
                    }
                },
                parent: this.$table_section.find('.table-field'),
                render_input: true,
            });
            this.table_field.toggle_label(false);
        }
        load_invoice() {
            super.load_invoice()

            const frm = this.events.get_frm()
            const me = this
            let table_number = undefined

            frappe.call({
                method: "inn.inn_hotels.page.pos_extended.pos_extended.get_table_number",
                args: {
                    invoice_name: frm.doc.name
                },
                async: false,
                callback: function (r) {
                    table_number = r.message
                    if (table_number) {
                        me.$table_section.find("input").val(table_number.table)
                        me.table_number = table_number
                    } else {
                        me.$table_section.find("input").val()
                        me.table_number = ""
                    }
                }
            })
        }

        make_cart_totals_section() {
            this.$totals_section = this.$component.find('.cart-totals-section');

            this.$totals_section.append(
                `<div class="add-discount-wrapper">
                ${this.get_discount_icon()} ${__('Add Discount')}
            </div>
            <div class="item-qty-total-container">
                <div class="item-qty-total-label">${__('Total Items')}</div>
                <div class="item-qty-total-value">0.00</div>
            </div>
            <div class="net-total-container">
                <div class="net-total-label">${__("Net Total")}</div>
                <div class="net-total-value">0.00</div>
            </div>
            <div class="taxes-container"></div>
            <div class="grand-total-container">
                <div>${__('Grand Total')}</div>
                <div>0.00</div>
            </div>
            <div class="print-order-section">
                <div class="caption-order-btn" data-button-value="captain-order">${__('Captain Order')}</div>
                <div class="table-order-btn" data-button-value="table-order">${__('Table Order')}</div>
            </div>
            <div class="transfer-btn">Transfer Charges</div> 
            <div class="checkout-btn">${__('Checkout')}</div>
            <div class="edit-cart-btn">${__('Edit Cart')}</div>`
            )

            this.$add_discount_elem = this.$component.find(".add-discount-wrapper");
        }

        highlight_checkout_btn(toggle) {
            super.highlight_checkout_btn(toggle)
            if (toggle) {
                this.$cart_container.find('.caption-order-btn').css({
                    'background-color': 'var(--gray-800)'
                });
                this.$cart_container.find('.table-order-btn').css({
                    'background-color': 'var(--gray-800)'
                });
                this.$cart_container.find('.transfer-btn').css({
                    'background-color': 'var(--gray-800)'
                });
            } else {
                this.$cart_container.find('.caption-order-btn').css({
                    'background-color': 'var(--gray-300)'
                });
                this.$cart_container.find('.table-order-btn').css({
                    'background-color': 'var(--gray-300)'
                });
                this.$cart_container.find('.transfer-btn').css({
                    'background-color': 'var(--gray-300)'
                });
            }
        }

        bind_events() {
            super.bind_events()

            const me = this;
            this.$component.on("click", ".caption-order-btn", async function () {
                if ($(this).attr('style').indexOf('--gray-800') == -1) return;

                await me.events.print_captain_order();
            })

            this.$component.on("click", ".table-order-btn", async function () {
                if ($(this).attr('style').indexOf('--gray-800') == -1) return;

                await me.events.print_table_order();
            })

            this.$component.on("click", ".transfer-btn", async function () {
                if ($(this).attr('style').indexOf('--gray-800') == -1) return;

                await me.events.transfer_folio();
            })
        }
    }
})

export default inn.PointOfSale.PosExtendItemCart