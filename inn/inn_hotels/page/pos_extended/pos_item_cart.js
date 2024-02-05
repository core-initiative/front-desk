frappe.provide('erpnext.PointOfSale');

erpnext.PointOfSale.ItemCart = class PosExtendItemCart extends erpnext.PointOfSale.ItemCart {
    constructor(wrapper) {
        super(wrapper);
    }
}