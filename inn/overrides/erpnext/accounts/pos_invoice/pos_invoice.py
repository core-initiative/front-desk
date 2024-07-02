import frappe


def before_submit(doc, method=None):
    doc.payments = [payment for payment in doc.payments if payment.amount != 0]
