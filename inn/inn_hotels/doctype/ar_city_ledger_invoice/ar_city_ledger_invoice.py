# -*- coding: utf-8 -*-
# Copyright (c) 2020, Core Initiative and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document


class ARCityLedgerInvoice(Document):
    pass


@frappe.whitelist()
def get_payments_accounts(mode_of_payment):
    hotel_settings = frappe.get_single("Inn Hotels Setting")
    account = frappe.db.get_value(
        "Mode of Payment Account",
        {
            "parent": mode_of_payment,
            "company": frappe.get_doc("Global Defaults").default_company,
        },
        "default_account",
    )
    against = frappe.db.get_list(
        "Account",
        filters={"name": hotel_settings.ar_city_ledger_invoice_payment_account},
    )[0].name
    return account, against


@frappe.whitelist()
def make_payment(id):
    doc = frappe.get_doc("AR City Ledger Invoice", id)
    arc_id = []
    folio_list = doc.folio
    if len(folio_list) == 0:
        frappe.msgprint(
            "Please add the Folio to be Collected first before making payment"
        )
    else:
        for folio in folio_list:
            arc_id.append(folio.ar_city_ledger_id)
    payments = doc.get("payments")
    return_status = 1

    for payment in payments:
        remark = "AR City Ledger Invoice Payments: " + payment.name
        doc_je = frappe.new_doc("Journal Entry")
        doc_je.title = payment.name
        doc_je.voucher_type = "Journal Entry"
        doc_je.naming_series = "ACC-JV-.YYYY.-"
        doc_je.posting_date = payment.payment_reference_date
        doc_je.company = frappe.get_doc("Global Defaults").default_company
        doc_je.total_amount_currency = frappe.get_doc(
            "Global Defaults"
        ).default_currency
        doc_je.remark = remark
        doc_je.user_remark = remark

        doc_jea_debit = frappe.new_doc("Journal Entry Account")
        doc_jea_debit.account = payment.account
        doc_jea_debit.debit = payment.payment_amount
        doc_jea_debit.debit_in_account_currency = payment.payment_amount
        doc_jea_debit.party_type = "Customer"
        doc_jea_debit.party = doc.customer_id
        doc_jea_debit.user_remark = remark

        doc_jea_credit = frappe.new_doc("Journal Entry Account")
        doc_jea_credit.account = payment.account_against
        doc_jea_credit.credit = payment.payment_amount
        doc_jea_credit.credit_in_account_currency = payment.payment_amount
        doc_jea_credit.party_type = "Customer"
        doc_jea_credit.party = doc.customer_id
        doc_jea_credit.user_remark = remark

        doc_je.append("accounts", doc_jea_debit)
        doc_je.append("accounts", doc_jea_credit)

        doc_je.save()
        doc_je.submit()

        if (
            frappe.db.get_value("Journal Entry", {"title": payment.name}, "remark")
            == remark
        ):
            return_status = 2

        if return_status == 1:
            doc.status = "Paid"
            doc.save()
            for arc in arc_id:
                doc_arc_ledger = frappe.get_doc("AR City Ledger", arc)
                doc_arc_ledger.is_paid = 1
                doc_arc_ledger.save()

    return return_status
