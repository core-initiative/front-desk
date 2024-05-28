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

        update_table_section() {
            const me = this;
            if (me.table_number) {
                this.$table_section.html(`
                <div style="
                    display: flex;
                    align-items: center;
                    font-weight: 700;
                    font-size: var(--text-lg);    
                ">
                    <div style="
                    width: 3rem;
                    margin-right: var(--margin-md);
                    ">
                    </div>

                    <div style="
                        flex: auto;
                    ">
                        <div>
                            <span>Table ${me.table_number}</span>
                        </div>
                    </div>

                    <div class="reset-table-btn" style="cursor: pointer;">
                        <svg width="32" height="32" viewBox="0 0 14 14" fill="none">
                            <path d="M4.93764 4.93759L7.00003 6.99998M9.06243 9.06238L7.00003 6.99998M7.00003 6.99998L4.93764 9.06238L9.06243 4.93759" stroke="#8D99A6"/>
                        </svg>
                    </div>
                </div>
                `)
            } else {
                this.make_table_selector()
            }
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
                        me.update_table_section()
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
                        me.table_number = table_number.table
                        me.update_table_section()
                    } else {
                        me.$table_section.find("input").val()
                        me.table_number = ""
                        me.update_table_section()
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

        reset_table_section() {
            this["table_number"] = undefined
            this.make_table_selector()
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

            this.$component.on("click", ".reset-table-btn", async function () {
                me.reset_table_section()
            })
        }
    }
})

export default inn.PointOfSale.PosExtendItemCart