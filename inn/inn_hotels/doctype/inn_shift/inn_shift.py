# -*- coding: utf-8 -*-
# Copyright (c) 2020, Core Initiative and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

from datetime import datetime, timedelta

import frappe
from frappe.utils import now
from frappe.model.document import Document

class InnShift(Document):
    def before_insert(self):
        self.status = "Open"

@frappe.whitelist()
def is_there_open_shift():
    if frappe.get_all('Inn Shift', {'status': 'Open'}):
        return 1
    else:
        return 2

def get_last_closed_shift():
    d = frappe.get_all('Inn Shift', filters={'status': 'Closed'}, order_by='creation desc', limit_page_length=1)
    if d:
        return frappe.get_doc('Inn Shift', d[0].name)
    else:
        return None

@frappe.whitelist()
def populate_cr_payment(shift_id):
    returned_cr_payment_detail_list = []
    cr_payment_detail_list = []
    transaction_list = []

    # Fetch transaction types from Inn Hotels Setting
    hotel_settings = frappe.get_doc("Inn Hotels Setting")
    list_of_payment_type = [
        hotel_settings.room_charge_tax_service,
        hotel_settings.breakfast_charge_tax_service,
        hotel_settings.credit_card_administration_fee,
        hotel_settings.package,
        hotel_settings.room_charge,
        hotel_settings.breakfast_charge,
        hotel_settings.refund,
        hotel_settings.dp_kamar,
        hotel_settings.room_payment,
        hotel_settings.deposit,
        hotel_settings.down_payment,
        hotel_settings.payment,
        hotel_settings.additional_charge,
        hotel_settings.restaurant_food,
        hotel_settings.restaurant_beverages,
        hotel_settings.restaurant_other,
        hotel_settings.room_service_food,
        hotel_settings.room_service_beverage,
        hotel_settings.fbs_service_10,
        hotel_settings.fbs_tax_11,
        hotel_settings.round_off,
        hotel_settings.laundry,
        hotel_settings.cancellation_fee,
        hotel_settings.late_checkout,
        hotel_settings.early_checkin,
    ]

    mode_of_payment = frappe.get_all('Mode of Payment')
    reservation_list = frappe.get_all('Inn Reservation', filters={'status': ['in', ['Reserved', 'In House', 'Finish', 'Cancel']]}, fields=['*'])

    if shift_id:
        last_shift = get_last_closed_shift()
        if last_shift is None:
            # Get Guest Folio Transaction type Payment that appear from the beginning
            for reservation_item in reservation_list:
                folio_name = frappe.db.get_value('Inn Folio', {'reservation_id': reservation_item.name}, ['name'])
                folio_transaction_list = frappe.get_all('Inn Folio Transaction',
                                                        filters={'parent': folio_name,
                                                                 'transaction_type': ['in', list_of_payment_type],
                                                                 'is_void': 0},
                                                        fields=['*'])
                for folio_trx_item in folio_transaction_list:
                    payment_detail_doc = frappe.new_doc('Inn CR Payment Detail')
                    payment_detail_doc.mode_of_payment = folio_trx_item.mode_of_payment
                    payment_detail_doc.amount = folio_trx_item.amount
                    cr_payment_detail_list.append(payment_detail_doc)

                    payment_transaction_doc = frappe.new_doc('Inn CR Payment Transaction')
                    payment_transaction_doc.type = folio_trx_item.transaction_type
                    payment_transaction_doc.transaction_id = folio_trx_item.name
                    payment_transaction_doc.reservation_id = reservation_item.name
                    payment_transaction_doc.folio_id = folio_name
                    payment_transaction_doc.customer_id = reservation_item.customer_id
                    payment_transaction_doc.account = folio_trx_item.debit_account
                    payment_transaction_doc.amount = folio_trx_item.amount
                    payment_transaction_doc.user = payment_transaction_doc.owner
                    transaction_list.append(payment_transaction_doc)

            # Get Master/Desk Folio transactions type Payment that appear from the beginning
            master_desk_folio_list = frappe.get_all('Inn Folio',
                                                    filters={'type': ['in', ['Master', 'Desk']],
                                                             'status': ['in', ['Open', 'Closed']]},
                                                    fields=['*'])
            for item in master_desk_folio_list:
                folio_transaction_list = frappe.get_all('Inn Folio Transaction',
                                                        filters={'parent': item.name,
                                                                 'transaction_type': ['in', list_of_payment_type],
                                                                 'is_void': 0},
                                                        fields=['*'])
                for folio_trx_item in folio_transaction_list:
                    payment_detail_doc = frappe.new_doc('Inn CR Payment Detail')
                    payment_detail_doc.mode_of_payment = folio_trx_item.mode_of_payment
                    payment_detail_doc.amount = folio_trx_item.amount
                    cr_payment_detail_list.append(payment_detail_doc)

                    payment_transaction_doc = frappe.new_doc('Inn CR Payment Transaction')
                    payment_transaction_doc.type = folio_trx_item.transaction_type
                    payment_transaction_doc.transaction_id = folio_trx_item.name
                    payment_transaction_doc.folio_id = item.name
                    payment_transaction_doc.customer_id = item.customer_id
                    payment_transaction_doc.account = folio_trx_item.debit_account
                    payment_transaction_doc.amount = folio_trx_item.amount
                    payment_transaction_doc.user = payment_transaction_doc.owner
                    transaction_list.append(payment_transaction_doc)

        else:
            # Get Guest Folio Transactions type Payment that appear since last shift
            for reservation_item in reservation_list:
                folio_name = frappe.db.get_value('Inn Folio', {'reservation_id': reservation_item.name}, ['name'])
                folio_transaction_list = frappe.get_all('Inn Folio Transaction',
                                                        filters={'creation': ['>=', last_shift.time_out],
                                                                 'parent': folio_name,
                                                                 'transaction_type': ['in', list_of_payment_type],
                                                                 'is_void': 0},
                                                        fields=['*'])
                for folio_trx_item in folio_transaction_list:
                    payment_detail_doc = frappe.new_doc('Inn CR Payment Detail')
                    payment_detail_doc.mode_of_payment = folio_trx_item.mode_of_payment
                    payment_detail_doc.amount = folio_trx_item.amount
                    cr_payment_detail_list.append(payment_detail_doc)

                    payment_transaction_doc = frappe.new_doc('Inn CR Payment Transaction')
                    payment_transaction_doc.type = folio_trx_item.transaction_type
                    payment_transaction_doc.transaction_id = folio_trx_item.name
                    payment_transaction_doc.reservation_id = reservation_item.name
                    payment_transaction_doc.folio_id = folio_name
                    payment_transaction_doc.customer_id = reservation_item.customer_id
                    payment_transaction_doc.account = folio_trx_item.debit_account
                    payment_transaction_doc.amount = folio_trx_item.amount
                    payment_transaction_doc.user = payment_transaction_doc.owner
                    transaction_list.append(payment_transaction_doc)

            # Get Master/Desk Folio transactions type Payment that appear since last shift
            master_desk_folio_list = frappe.get_all('Inn Folio',
                                                    filters={'type': ['in', ['Master', 'Desk']],
                                                             'status': ['in', ['Open', 'Closed']]},
                                                    fields=['*'])
            for item in master_desk_folio_list:
                folio_transaction_list = frappe.get_all('Inn Folio Transaction',
                                                        filters={'creation': ['>=', last_shift.time_out],
                                                                 'parent': item.name,
                                                                 'transaction_type': ['in', list_of_payment_type],
                                                                 'is_void': 0},
                                                        fields=['*'])
                for folio_trx_item in folio_transaction_list:
                    payment_detail_doc = frappe.new_doc('Inn CR Payment Detail')
                    payment_detail_doc.mode_of_payment = folio_trx_item.mode_of_payment
                    payment_detail_doc.amount = folio_trx_item.amount
                    cr_payment_detail_list.append(payment_detail_doc)

                    payment_transaction_doc = frappe.new_doc('Inn CR Payment Transaction')
                    payment_transaction_doc.type = folio_trx_item.transaction_type
                    payment_transaction_doc.transaction_id = folio_trx_item.name
                    payment_transaction_doc.folio_id = item.name
                    payment_transaction_doc.customer_id = item.customer_id
                    payment_transaction_doc.account = folio_trx_item.debit_account
                    payment_transaction_doc.amount = folio_trx_item.amount
                    payment_transaction_doc.user = payment_transaction_doc.owner
                    transaction_list.append(payment_transaction_doc)
    else:
        if len(frappe.get_all('Inn Shift')) > 0:
            last_shift = get_last_closed_shift()
            # Get Guest Folio Transactions type Payment that appear since last shift
            for reservation_item in reservation_list:
                folio_name = frappe.db.get_value('Inn Folio', {'reservation_id': reservation_item.name}, ['name'])
                folio_transaction_list = frappe.get_all('Inn Folio Transaction',
                                                        filters={'creation': ['>=', last_shift.time_out],
                                                                 'parent': folio_name,
                                                                 'transaction_type': ['in', list_of_payment_type],
                                                                 'is_void': 0},
                                                        fields=['*'])
                for folio_trx_item in folio_transaction_list:
                    payment_detail_doc = frappe.new_doc('Inn CR Payment Detail')
                    payment_detail_doc.mode_of_payment = folio_trx_item.mode_of_payment
                    payment_detail_doc.amount = folio_trx_item.amount
                    cr_payment_detail_list.append(payment_detail_doc)

                    payment_transaction_doc = frappe.new_doc('Inn CR Payment Transaction')
                    payment_transaction_doc.type = folio_trx_item.transaction_type
                    payment_transaction_doc.transaction_id = folio_trx_item.name
                    payment_transaction_doc.reservation_id = reservation_item.name
                    payment_transaction_doc.folio_id = folio_name
                    payment_transaction_doc.customer_id = reservation_item.customer_id
                    payment_transaction_doc.account = folio_trx_item.debit_account
                    payment_transaction_doc.amount = folio_trx_item.amount
                    payment_transaction_doc.user = payment_transaction_doc.owner
                    transaction_list.append(payment_transaction_doc)

            # Get Master/Desk Folio transactions type Payment that appear since last shift
            master_desk_folio_list = frappe.get_all('Inn Folio',
                                                    filters={'type': ['in', ['Master', 'Desk']],
                                                             'status': ['in', ['Open', 'Closed']]},
                                                    fields=['*'])
            for item in master_desk_folio_list:
                folio_transaction_list = frappe.get_all('Inn Folio Transaction',
                                                        filters={'creation': ['>=', last_shift.time_out],
                                                                 'parent': item.name,
                                                                 'transaction_type': ['in', list_of_payment_type],
                                                                 'is_void': 0},
                                                        fields=['*'])
                for folio_trx_item in folio_transaction_list:
                    payment_detail_doc = frappe.new_doc('Inn CR Payment Detail')
                    payment_detail_doc.mode_of_payment = folio_trx_item.mode_of_payment
                    payment_detail_doc.amount = folio_trx_item.amount
                    cr_payment_detail_list.append(payment_detail_doc)

                    payment_transaction_doc = frappe.new_doc('Inn CR Payment Transaction')
                    payment_transaction_doc.type = folio_trx_item.transaction_type
                    payment_transaction_doc.transaction_id = folio_trx_item.name
                    payment_transaction_doc.folio_id = item.name
                    payment_transaction_doc.customer_id = item.customer_id
                    payment_transaction_doc.account = folio_trx_item.debit_account
                    payment_transaction_doc.amount = folio_trx_item.amount
                    payment_transaction_doc.user = payment_transaction_doc.owner
                    transaction_list.append(payment_transaction_doc)

        else:
            # Get Guest Folio Transaction type Payment that appear from the beginning
            for reservation_item in reservation_list:
                folio_name = frappe.db.get_value('Inn Folio', {'reservation_id': reservation_item.name}, ['name'])
                folio_transaction_list = frappe.get_all('Inn Folio Transaction',
                                                        filters={'parent': folio_name,
                                                                 'transaction_type': ['in', list_of_payment_type],
                                                                 'is_void': 0},
                                                        fields=['*'])
                for folio_trx_item in folio_transaction_list:
                    payment_detail_doc = frappe.new_doc('Inn CR Payment Detail')
                    payment_detail_doc.mode_of_payment = folio_trx_item.mode_of_payment
                    payment_detail_doc.amount = folio_trx_item.amount
                    cr_payment_detail_list.append(payment_detail_doc)

                    payment_transaction_doc = frappe.new_doc('Inn CR Payment Transaction')
                    payment_transaction_doc.type = folio_trx_item.transaction_type
                    payment_transaction_doc.transaction_id = folio_trx_item.name
                    payment_transaction_doc.reservation_id = reservation_item.name
                    payment_transaction_doc.folio_id = folio_name
                    payment_transaction_doc.customer_id = reservation_item.customer_id
                    payment_transaction_doc.account = folio_trx_item.debit_account
                    payment_transaction_doc.amount = folio_trx_item.amount
                    payment_transaction_doc.user = payment_transaction_doc.owner
                    transaction_list.append(payment_transaction_doc)

            # Get Master/Desk Folio transactions type Payment that appear from the beginning
            master_desk_folio_list = frappe.get_all('Inn Folio',
                                                    filters={'type': ['in', ['Master', 'Desk']],
                                                             'status': ['in', ['Open', 'Closed']]},
                                                    fields=['*'])
            for item in master_desk_folio_list:
                folio_transaction_list = frappe.get_all('Inn Folio Transaction',
                                                        filters={'parent': item.name,
                                                                 'transaction_type': ['in', list_of_payment_type],
                                                                 'is_void': 0},
                                                        fields=['*'])
                for folio_trx_item in folio_transaction_list:
                    payment_detail_doc = frappe.new_doc('Inn CR Payment Detail')
                    payment_detail_doc.mode_of_payment = folio_trx_item.mode_of_payment
                    payment_detail_doc.amount = folio_trx_item.amount
                    cr_payment_detail_list.append(payment_detail_doc)

                    payment_transaction_doc = frappe.new_doc('Inn CR Payment Transaction')
                    payment_transaction_doc.type = folio_trx_item.transaction_type
                    payment_transaction_doc.transaction_id = folio_trx_item.name
                    payment_transaction_doc.folio_id = item.name
                    payment_transaction_doc.customer_id = item.customer_id
                    payment_transaction_doc.account = folio_trx_item.debit_account
                    payment_transaction_doc.amount = folio_trx_item.amount
                    payment_transaction_doc.user = payment_transaction_doc.owner
                    transaction_list.append(payment_transaction_doc)

    for mode_of_payment_item in mode_of_payment:
        new_payment_detail = frappe.new_doc('Inn CR Payment Detail')
        new_payment_detail.mode_of_payment = mode_of_payment_item.name
        new_payment_detail.amount = 0
        for cr_payment_detail_item in cr_payment_detail_list:
            if cr_payment_detail_item.mode_of_payment == new_payment_detail.mode_of_payment:
                new_payment_detail.amount += float(cr_payment_detail_item.amount)
        if new_payment_detail.amount > 0:
            returned_cr_payment_detail_list.append(new_payment_detail)

    return transaction_list, returned_cr_payment_detail_list

@frappe.whitelist()
def populate_cr_refund(shift_id):
    returned_cr_refund_detail_list = []
    transaction_list = []
    cr_refund = frappe.new_doc('Inn CR Refund Detail')
    cr_refund.type = 'Refund'
    cr_refund.amount = 0
    reservation_list = frappe.get_all('Inn Reservation', filters={'status': ['in', ['In House', 'Finish', 'Cancel']]},
                                      fields=['*'])

    if shift_id:
        last_shift = get_last_closed_shift()
        if last_shift is None:
            # Get all Guest Folio Transactions Refund that appear from beginning
            for reservation_item in reservation_list:
                folio_name = frappe.db.get_value('Inn Folio', {'reservation_id': reservation_item.name}, ['name'])
                folio_transaction_list = frappe.get_all('Inn Folio Transaction',
                                                        filters={'transaction_type': 'Refund',
                                                                 'parent': folio_name,
                                                                 'is_void': 0},
                                                        fields=['*'])
                for folio_trx_item in folio_transaction_list:
                    cr_refund.amount += folio_trx_item.amount

                    refund_detail_doc = frappe.new_doc('Inn CR Refund Transaction')
                    refund_detail_doc.type = folio_trx_item.transaction_type
                    refund_detail_doc.transaction_id = folio_trx_item.name
                    refund_detail_doc.reservation_id = reservation_item.name
                    refund_detail_doc.folio_id = folio_name
                    refund_detail_doc.customer_id = reservation_item.customer_id
                    refund_detail_doc.account = folio_trx_item.credit_account
                    refund_detail_doc.amount = folio_trx_item.amount
                    refund_detail_doc.user = refund_detail_doc.owner
                    transaction_list.append(refund_detail_doc)

            # Get all Master/Desk Folio Transactions Refund that appear from beginning
            master_desk_folio_list = frappe.get_all('Inn Folio',
                                                    filters={'type': ['in', ['Master', 'Desk']],
                                                             'status': ['in', ['Open', 'Closed']]},
                                                    fields=['*'])
            for item in master_desk_folio_list:
                folio_transaction_list = frappe.get_all('Inn Folio Transaction',
                                                        filters={'transaction_type': 'Refund',
                                                                 'parent': item.name,
                                                                 'is_void': 0},
                                                        fields=['*'])
                for folio_trx_item in folio_transaction_list:
                    cr_refund.amount += folio_trx_item.amount

                    refund_detail_doc = frappe.new_doc('Inn CR Refund Transaction')
                    refund_detail_doc.type = folio_trx_item.transaction_type
                    refund_detail_doc.transaction_id = folio_trx_item.name
                    refund_detail_doc.folio_id = item.name
                    refund_detail_doc.customer_id = item.customer_id
                    refund_detail_doc.account = folio_trx_item.credit_account
                    refund_detail_doc.amount = folio_trx_item.amount
                    refund_detail_doc.user = refund_detail_doc.owner
                    transaction_list.append(refund_detail_doc)

        else:
            # Get all Guest Folio Transactions Refund that appear since last shift
            for reservation_item in reservation_list:
                folio_name = frappe.db.get_value('Inn Folio', {'reservation_id': reservation_item.name}, ['name'])
                folio_transaction_list = frappe.get_all('Inn Folio Transaction',
                                                        filters={'transaction_type': 'Refund',
                                                                 'creation': ['>=', last_shift.time_out],
                                                                 'parent': folio_name,
                                                                 'flag': 'Debit',
                                                                 'is_void': 0},
                                                        fields=['*'])
                for folio_trx_item in folio_transaction_list:
                    cr_refund.amount += folio_trx_item.amount

                    refund_detail_doc = frappe.new_doc('Inn CR Refund Transaction')
                    refund_detail_doc.type = folio_trx_item.transaction_type
                    refund_detail_doc.transaction_id = folio_trx_item.name
                    refund_detail_doc.reservation_id = reservation_item.name
                    refund_detail_doc.folio_id = folio_name
                    refund_detail_doc.customer_id = reservation_item.customer_id
                    refund_detail_doc.account = folio_trx_item.credit_account
                    refund_detail_doc.amount = folio_trx_item.amount
                    refund_detail_doc.user = refund_detail_doc.owner
                    transaction_list.append(refund_detail_doc)

            # Get all Master/Desk Folio Transactions Refund that appear since last shift
            master_desk_folio_list = frappe.get_all('Inn Folio',
                                                    filters={'type': ['in', ['Master', 'Desk']],
                                                             'status': ['in', ['Open', 'Closed']]},
                                                    fields=['*'])
            for item in master_desk_folio_list:
                folio_transaction_list = frappe.get_all('Inn Folio Transaction',
                                                        filters={'transaction_type': 'Refund',
                                                                 'creation': ['>=', last_shift.time_out],
                                                                 'parent': item.name,
                                                                 'is_void': 0},
                                                        fields=['*'])
                for folio_trx_item in folio_transaction_list:
                    cr_refund.amount += folio_trx_item.amount

                    refund_detail_doc = frappe.new_doc('Inn CR Refund Transaction')
                    refund_detail_doc.type = folio_trx_item.transaction_type
                    refund_detail_doc.transaction_id = folio_trx_item.name
                    refund_detail_doc.folio_id = item.name
                    refund_detail_doc.customer_id = item.customer_id
                    refund_detail_doc.account = folio_trx_item.credit_account
                    refund_detail_doc.amount = folio_trx_item.amount
                    refund_detail_doc.user = refund_detail_doc.owner
                    transaction_list.append(refund_detail_doc)
    else:
        if len(frappe.get_all('Inn Shift')) > 0:
            last_shift = get_last_closed_shift()
            # Get all Guest Folio Transactions Refund that appear since last shift
            for reservation_item in reservation_list:
                folio_name = frappe.db.get_value('Inn Folio', {'reservation_id': reservation_item.name}, ['name'])
                folio_transaction_list = frappe.get_all('Inn Folio Transaction',
                                                        filters={'transaction_type': 'Refund',
                                                                 'creation': ['>=', last_shift.time_out],
                                                                 'parent': folio_name,
                                                                 'is_void': 0},
                                                        fields=['*'])
                for folio_trx_item in folio_transaction_list:
                    cr_refund.amount += folio_trx_item.amount

                    refund_detail_doc = frappe.new_doc('Inn CR Refund Transaction')
                    refund_detail_doc.type = folio_trx_item.transaction_type
                    refund_detail_doc.transaction_id = folio_trx_item.name
                    refund_detail_doc.reservation_id = reservation_item.name
                    refund_detail_doc.folio_id = folio_name
                    refund_detail_doc.customer_id = reservation_item.customer_id
                    refund_detail_doc.account = folio_trx_item.credit_account
                    refund_detail_doc.amount = folio_trx_item.amount
                    refund_detail_doc.user = refund_detail_doc.owner
                    transaction_list.append(refund_detail_doc)

            # Get all Master/Desk Folio Transactions Refund that appear since last shift
            master_desk_folio_list = frappe.get_all('Inn Folio',
                                                    filters={'type': ['in', ['Master', 'Desk']],
                                                             'status': ['in', ['Open', 'Closed']]},
                                                    fields=['*'])
            for item in master_desk_folio_list:
                folio_transaction_list = frappe.get_all('Inn Folio Transaction',
                                                        filters={'transaction_type': 'Refund',
                                                                 'creation': ['>=', last_shift.time_out],
                                                                 'parent': item.name,
                                                                 'is_void': 0},
                                                        fields=['*'])
                for folio_trx_item in folio_transaction_list:
                    cr_refund.amount += folio_trx_item.amount

                    refund_detail_doc = frappe.new_doc('Inn CR Refund Transaction')
                    refund_detail_doc.type = folio_trx_item.transaction_type
                    refund_detail_doc.transaction_id = folio_trx_item.name
                    refund_detail_doc.folio_id = item.name
                    refund_detail_doc.customer_id = item.customer_id
                    refund_detail_doc.account = folio_trx_item.credit_account
                    refund_detail_doc.amount = folio_trx_item.amount
                    refund_detail_doc.user = refund_detail_doc.owner
                    transaction_list.append(refund_detail_doc)
        else:
            # Get all Guest Folio Transactions Refund that appear from beginning
            for reservation_item in reservation_list:
                folio_name = frappe.db.get_value('Inn Folio', {'reservation_id': reservation_item.name}, ['name'])
                folio_transaction_list = frappe.get_all('Inn Folio Transaction',
                                                        filters={'transaction_type': 'Refund',
                                                                 'parent': folio_name,
                                                                 'is_void': 0},
                                                        fields=['*'])
                for folio_trx_item in folio_transaction_list:
                    cr_refund.amount += folio_trx_item.amount

                    refund_detail_doc = frappe.new_doc('Inn CR Refund Transaction')
                    refund_detail_doc.type = folio_trx_item.transaction_type
                    refund_detail_doc.transaction_id = folio_trx_item.name
                    refund_detail_doc.reservation_id = reservation_item.name
                    refund_detail_doc.folio_id = folio_name
                    refund_detail_doc.customer_id = reservation_item.customer_id
                    refund_detail_doc.account = folio_trx_item.credit_account
                    refund_detail_doc.amount = folio_trx_item.amount
                    refund_detail_doc.user = refund_detail_doc.owner
                    transaction_list.append(refund_detail_doc)

            # Get all Master/Desk Folio Transactions Refund that appear from beginning
            master_desk_folio_list = frappe.get_all('Inn Folio',
                                                    filters={'type': ['in', ['Master', 'Desk']],
                                                             'status': ['in', ['Open', 'Closed']]},
                                                    fields=['*'])
            for item in master_desk_folio_list:
                folio_transaction_list = frappe.get_all('Inn Folio Transaction',
                                                        filters={'transaction_type': 'Refund',
                                                                 'parent': item.name,
                                                                 'is_void': 0},
                                                        fields=['*'])
                for folio_trx_item in folio_transaction_list:
                    cr_refund.amount += folio_trx_item.amount

                    refund_detail_doc = frappe.new_doc('Inn CR Refund Transaction')
                    refund_detail_doc.type = folio_trx_item.transaction_type
                    refund_detail_doc.transaction_id = folio_trx_item.name
                    refund_detail_doc.folio_id = item.name
                    refund_detail_doc.customer_id = item.customer_id
                    refund_detail_doc.account = folio_trx_item.credit_account
                    refund_detail_doc.amount = folio_trx_item.amount
                    refund_detail_doc.user = refund_detail_doc.owner
                    transaction_list.append(refund_detail_doc)

    returned_cr_refund_detail_list.append(cr_refund)

    return transaction_list, returned_cr_refund_detail_list

@frappe.whitelist()
def close_shift(shift_id):
    doc = frappe.get_doc('Inn Shift', shift_id)
    doc.time_out = now()
    doc.username = frappe.session.user
    doc.status = 'Closed'
    doc.save()

    if frappe.db.get_value('Inn Shift', {'name': shift_id}, ['status']) == 'Closed':
        return True
    else:
        return False

@frappe.whitelist()
def get_max_opening_cash():
    return frappe.db.get_single_value('Inn Hotels Setting', 'max_opening')