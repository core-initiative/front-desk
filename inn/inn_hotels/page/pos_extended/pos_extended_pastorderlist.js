frappe.require(["point-of-sale.bundle.js", "inn-pos.bundle.js"], function () {

    inn.PointOfSale.PosExtendedPastOrderList = class PosExtendedPastOrderList extends erpnext.PointOfSale.PastOrderList {
        constructor({ wrapper, events }) {
            super({ wrapper, events });
        }

        make_filter_section() {
            const me = this;
            this.search_field = frappe.ui.form.make_control({
                df: {
                    label: __('Search'),
                    fieldtype: 'Data',
                    placeholder: __('Search by invoice id or customer name')
                },
                parent: this.$component.find('.search-field'),
                render_input: true,
            });
            this.status_field = frappe.ui.form.make_control({
                df: {
                    label: __('Invoice Status'),
                    fieldtype: 'Select',
                    options: `Draft\nPaid\nTransferred\nConsolidated\nReturn`,
                    placeholder: __('Filter by invoice status'),
                    onchange: function () {
                        if (me.$component.is(':visible')) me.refresh_list();
                    }
                },
                parent: this.$component.find('.status-field'),
                render_input: true,
            });
            this.search_field.toggle_label(false);
            this.status_field.toggle_label(false);
            this.status_field.set_value('Draft');
        }
    }
});