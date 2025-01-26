# -*- coding: utf-8 -*-
# Copyright (c) 2020, Core Initiative and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

import frappe
import datetime
from frappe.model.document import Document
from inn.inn_hotels.doctype.inn_audit_log.inn_audit_log import get_last_audit_date
from inn.inn_hotels.doctype.inn_folio.inn_folio import check_void_request
from inn.inn_hotels.doctype.inn_dayend_close.inn_dayend_close_helper import (
    _fill_party_account,
)


class InnDayendClose(Document):
    pass


@frappe.whitelist()
def is_there_open_dayend_close():
    if frappe.get_all("Inn Dayend Close", {"status": "Open"}):
        return 1
    else:
        return 2


@frappe.whitelist()
def process_dayend_close(doc_id):
    need_resolve_flag = False

    # Fetch transaction types from Inn Hotels Setting
    hotel_settings = frappe.get_doc("Inn Hotels Setting")
    transaction_types = {
        "credit_card_administration_fee": hotel_settings.credit_card_administration_fee,
        "package": hotel_settings.package,
        "room_charge": hotel_settings.room_charge,
        "breakfast_charge": hotel_settings.breakfast_charge,
        "refund": hotel_settings.refund,
        "dp_kamar": hotel_settings.dp_kamar,
        "room_payment": hotel_settings.room_payment,
        "deposit": hotel_settings.deposit,
        "down_payment": hotel_settings.down_payment,
        "payment": hotel_settings.payment,
        "additional_charge": hotel_settings.additional_charge,
        "restaurant_food": hotel_settings.restaurant_food,
        "restaurant_beverages": hotel_settings.restaurant_beverages,
        "restaurant_other": hotel_settings.restaurant_other,
        "room_service_food": hotel_settings.room_service_food,
        "room_service_beverage": hotel_settings.room_service_beverage,
        "fbs_service_10": hotel_settings.fbs_service_10,
        "round_off": hotel_settings.round_off,
        "laundry": hotel_settings.laundry,
        "cancellation_fee": hotel_settings.cancellation_fee,
        "late_checkout": hotel_settings.late_checkout,
        "early_checkin": hotel_settings.early_checkin,
    }
    if hotel_settings.include_tax:
        transaction_types["room_charge_tax_service"] = (
            hotel_settings.room_charge_tax_service
        )

        transaction_types["breakfast_charge_tax_service"] = (
            hotel_settings.breakfast_charge_tax_service
        )

        transaction_types["fbs_tax_11"] = hotel_settings.fbs_tax_11

    COMMISSION_TRANSACTION_TYPE = hotel_settings.profit_sharing_transaction_type

    # Create Journal Entry Pairing for Every Eligible Inn Folio Transactions
    folio_list = frappe.get_all(
        "Inn Folio",
        filters={
            "status": ["in", ["Open", "Closed"]],
            "journal_entry_id_closed": ["=", ""],
        },
        fields=["name", "reservation_id"],
    )
    for item in folio_list:
        need_resolve_list = check_void_request(item.name)
        if len(need_resolve_list) > 0:
            need_resolve_flag = True
            break

    if need_resolve_flag:
        return "There are transaction requested to be voided not yet responded. Please resolve the request first."
    else:
        print("Folio List Size: ", len(folio_list))
        for item in folio_list:
            print(datetime.datetime.now(), ": Folio ", item.name)
            doc_folio = frappe.get_doc("Inn Folio", item.name)
            if doc_folio.reservation_id:
                reservation = frappe.get_doc(
                    "Inn Reservation", doc_folio.reservation_id
                )

                if reservation.status == "In House":
                    actual_room = frappe.get_doc("Inn Room", reservation.actual_room_id)
                    actual_room.room_status = "Occupied Dirty"
                    actual_room.save()

            trx_list: list[Document] = doc_folio.get("folio_transaction")
            for trx in trx_list:
                if trx.is_void == 0 and trx.journal_entry_id is None:
                    if trx.remark is None:
                        remark = trx.transaction_type + " " + trx.parent
                    elif trx.remark == "":
                        remark = trx.transaction_type + " " + trx.parent
                    else:
                        remark = trx.remark
                    customer_name = frappe.db.get_value(
                        "Inn Folio", trx.parent, "customer_id"
                    )
                    doc_je = frappe.new_doc("Journal Entry")
                    doc_je.title = doc_folio.name
                    doc_je.voucher_type = "Journal Entry"
                    doc_je.naming_series = "ACC-JV-.YYYY.-"
                    doc_je.posting_date = get_last_audit_date()
                    doc_je.company = frappe.get_doc("Global Defaults").default_company
                    doc_je.total_amount_currency = frappe.get_doc(
                        "Global Defaults"
                    ).default_currency
                    doc_je.remark = remark
                    doc_je.user_remark = remark

                    doc_jea_debit = frappe.new_doc("Journal Entry Account")
                    doc_jea_debit.account = trx.debit_account
                    doc_jea_debit.debit = trx.amount
                    doc_jea_debit.debit_in_account_currency = trx.amount
                    doc_jea_debit.party_type, doc_jea_debit.party = _fill_party_account(
                        doc_jea_debit.account, customer_name
                    )
                    doc_jea_debit.user_remark = remark

                    if (
                        trx.transaction_type == COMMISSION_TRANSACTION_TYPE
                        and doc_jea_debit.party_type == "Supplier"
                    ):
                        channel_id = frappe.db.get_value(
                            "Inn Reservation", item.reservation_id, fieldname="channel"
                        )
                        channel_vendor = frappe.db.get_value(
                            "Inn Channel", channel_id, channel_id
                        )
                        doc_jea_debit.party = channel_vendor

                    doc_jea_credit = frappe.new_doc("Journal Entry Account")
                    doc_jea_credit.account = trx.credit_account
                    doc_jea_credit.credit = trx.amount
                    doc_jea_credit.credit_in_account_currency = trx.amount
                    doc_jea_credit.party_type, doc_jea_credit.party = (
                        _fill_party_account(doc_jea_credit.account, customer_name)
                    )
                    doc_jea_credit.user_remark = remark

                    if (
                        trx.transaction_type == COMMISSION_TRANSACTION_TYPE
                        and doc_jea_credit.party_type == "Supplier"
                    ):
                        channel_id = frappe.db.get_value(
                            "Inn Reservation", item.reservation_id, fieldname="channel"
                        )
                        channel_vendor = frappe.db.get_value(
                            doctype="Inn Channel",
                            filters={"name": channel_id},
                            fieldname="supplier",
                        )
                        doc_jea_credit.party = channel_vendor

                    doc_je.append("accounts", doc_jea_debit)
                    doc_je.append("accounts", doc_jea_credit)

                    doc_je.save()
                    doc_je.submit()

                    trx.journal_entry_id = doc_je.name
                    trx.save()

        # Create Journal Entry Pairing for Every Eligible Inn Folio
        closed_folio_list = frappe.get_all(
            "Inn Folio",
            filters={
                "status": "Closed",
                "total_credit": ["!=", 0],
                "total_debit": ["!=", 0],
                "journal_entry_id_closed": ["=", ""],
            },
        )
        for item in closed_folio_list:
            doc_folio = frappe.get_doc("Inn Folio", item.name)
            cust_name = doc_folio.customer_id
            # Get all Closed folio with close date == last audit date
            if (
                doc_folio.journal_entry_id_closed is None
                and doc_folio.close == get_last_audit_date()
            ):
                closed_folio_remark = "Closed Folio Transaction"
                # Get all transactions that not void
                closed_trx_list = frappe.get_all(
                    "Inn Folio Transaction",
                    filters={"parent": item.name, "is_void": 0},
                    fields=["*"],
                )
                # Folio must not be empty, Because Journal Entry Table Account not allowed to be empty
                if len(closed_trx_list) > 0:
                    doc_je = frappe.new_doc("Journal Entry")
                    doc_je.title = doc_folio.name
                    doc_je.voucher_type = "Journal Entry"
                    doc_je.naming_series = "ACC-JV-.YYYY.-"
                    doc_je.posting_date = get_last_audit_date()
                    doc_je.company = frappe.get_doc("Global Defaults").default_company
                    doc_je.total_amount_currency = frappe.get_doc(
                        "Global Defaults"
                    ).default_currency
                    doc_je.remark = closed_folio_remark
                    doc_je.user_remark = closed_folio_remark

                    for trx in closed_trx_list:
                        if trx.flag == "Debit":
                            doc_jea_debit = frappe.new_doc("Journal Entry Account")
                            doc_jea_debit.account = trx.debit_account
                            doc_jea_debit.debit = trx.amount
                            doc_jea_debit.credit_in_account_currency = (
                                trx.amount
                            )  # amount flipped to credit
                            doc_jea_debit.party_type, doc_jea_debit.party = (
                                _fill_party_account(doc_jea_debit.account, cust_name)
                            )
                            doc_jea_debit.user_remark = closed_folio_remark
                            doc_je.append("accounts", doc_jea_debit)
                            print(
                                f"DEBIT {doc_jea_debit.debit} - {doc_jea_debit.credit_in_account_currency} {trx.remark}"
                            )
                        elif trx.flag == "Credit":
                            doc_jea_credit = frappe.new_doc("Journal Entry Account")
                            doc_jea_credit.account = trx.credit_account
                            doc_jea_credit.credit = trx.amount
                            doc_jea_credit.debit_in_account_currency = (
                                trx.amount
                            )  # amount flipped to debit
                            doc_jea_credit.party_type, doc_jea_credit.party = (
                                _fill_party_account(doc_jea_credit.account, cust_name)
                            )
                            doc_jea_credit.user_remark = closed_folio_remark
                            doc_je.append("accounts", doc_jea_credit)
                            print(
                                f"CREDIT {doc_jea_credit.credit} - {doc_jea_credit.debit_in_account_currency} {trx.remark}"
                            )

                    doc_je.save()
                    doc_je.submit()
                    doc_folio.journal_entry_id_closed = doc_je.name
                    doc_folio.save()

        # Create Journal Entry for Inn Restaurant Finished Order
        # Get all finished order that not transfered to folio and not paired with journal entry yet
        # create_je_for_inn_restaurant_finished_order(transaction_types)

        doc_audit_log = frappe.new_doc("Inn Audit Log")
        doc_audit_log.naming_series = "AL.DD.-.MM.-.YYYY.-"
        doc_audit_log.audit_date = get_last_audit_date() + datetime.timedelta(days=1)
        doc_audit_log.posting_date = datetime.datetime.now()
        doc_audit_log.posted_by = frappe.session.user
        doc_audit_log.insert()

        doc = frappe.get_doc("Inn Dayend Close", doc_id)
        doc.status = "Closed"
        doc.save()

        return doc.status


@frappe.whitelist()
def load_child(date):
    audit_date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
    # return get_arrived_today(audit_date), get_departed_today(audit_date), get_closed_today(audit_date), get_ongoing_order_need_to_be_finished()
    return (
        get_arrived_today(audit_date),
        get_departed_today(audit_date),
        get_closed_today(audit_date),
    )


def get_arrived_today(date):
    return_list = []
    list = frappe.get_all(
        "Inn Reservation", filters={"status": "Reserved"}, fields=["*"]
    )
    for item in list:
        if item.expected_arrival == date:
            new_arrived = frappe.new_doc("Inn Expected Arrived Today")
            new_arrived.reservation_id = item.name
            new_arrived.folio_id = frappe.get_doc(
                "Inn Folio", {"reservation_id": item.name}
            ).name
            new_arrived.customer_id = item.customer_id
            new_arrived.description = "Must Check In Today"
            return_list.append(new_arrived)
    return return_list


def get_departed_today(date):
    return_list = []
    list = frappe.get_all(
        "Inn Reservation", filters={"status": "In House"}, fields=["*"]
    )
    for item in list:
        if item.departure.date() == date:
            new_departed = frappe.new_doc("Inn Expected Departed Today")
            new_departed.reservation_id = item.name
            new_departed.folio_id = frappe.get_doc(
                "Inn Folio", {"reservation_id": item.name}
            ).name
            new_departed.customer_id = item.customer_id
            new_departed.description = "Must Check Out Today"
            return_list.append(new_departed)
    return return_list


def get_closed_today(date):
    return_list = []
    list = frappe.get_all(
        "Inn Folio",
        filters={"status": "Open", "type": ["in", ["Master", "Desk"]]},
        fields=["*"],
    )
    for item in list:
        if item.close == date:
            new_closed = frappe.new_doc("Inn Expected Closed Today")
            new_closed.type = item.type
            new_closed.folio_id = item.name
            new_closed.customer_id = item.customer_id
            new_closed.description = "Must Close Today"
            return_list.append(new_closed)
    return return_list


def get_ongoing_order_need_to_be_finished():
    return_list = []
    list = frappe.get_all("Inn Restaurant Ongoing Order", fields=["*"])
    for item in list:
        new_order_need_to_finish = frappe.new_doc(
            "Inn Restaurant Order Expected to be Finished"
        )
        new_order_need_to_finish.ongoing_order_id = item.name
        new_order_need_to_finish.restaurant = item.restaurant
        new_order_need_to_finish.customer = item.customer
        new_order_need_to_finish.description = (
            "Restaurant Order need to be finished today"
        )
        return_list.append(new_order_need_to_finish)
    return return_list


def create_journal_entry(title, remark, debit_account, credit_account, amount):
    print("Journal Entry Title: " + title)
    customer_name = "Customer Restaurant"
    doc_je = frappe.new_doc("Journal Entry")
    doc_je.title = title
    doc_je.voucher_type = "Journal Entry"
    doc_je.naming_series = "ACC-JV-.YYYY.-"
    doc_je.posting_date = get_last_audit_date()
    doc_je.company = frappe.get_doc("Global Defaults").default_company
    doc_je.total_amount_currency = frappe.get_doc("Global Defaults").default_currency
    doc_je.remark = remark
    doc_je.user_remark = remark

    doc_jea_debit = frappe.new_doc("Journal Entry Account")
    doc_jea_debit.account = debit_account
    doc_jea_debit.debit = amount
    doc_jea_debit.debit_in_account_currency = amount
    doc_jea_debit.party_type, doc_jea_debit.party = _fill_party_account(
        doc_jea_debit.account, customer_name
    )
    doc_jea_debit.user_remark = remark

    doc_jea_credit = frappe.new_doc("Journal Entry Account")
    doc_jea_credit.account = credit_account
    doc_jea_credit.credit = amount
    doc_jea_credit.credit_in_account_currency = amount
    doc_jea_credit.party_type, doc_jea_credit.party = _fill_party_account(
        doc_jea_credit.account, customer_name
    )
    doc_jea_credit.user_remark = remark

    doc_je.append("accounts", doc_jea_debit)
    doc_je.append("accounts", doc_jea_credit)

    doc_je.save()
    doc_je.submit()


def create_je_for_inn_restaurant_finished_order(transaction_types):
    order_list = frappe.get_all(
        "Inn Restaurant Finished Order",
        filters={
            "transfer_charges_folio": ("=", ""),
            "is_journaled": 0,
        },
        fields=["*"],
    )
    for order in order_list:
        restaurant_food = 0
        restaurant_beverage = 0
        restaurant_other = 0

        # 1. ORDER ITEM IN RESTAURANT FINISHED ORDER
        order_item_list = frappe.get_all(
            "Inn Restaurant Order Item", filters={"parent": order.name}, fields=["*"]
        )

        print("order item list of " + order.name + " is " + str(len(order_item_list)))
        if order_item_list is not None and len(order_item_list) > 0:
            print("masuk if order list exist")
            # Calculate Total Amount of Food, Beverages and Other Charges in Restaurant Order
            for item in order_item_list:
                print("item now = " + item.name)
                menu_type = frappe.db.get_value(
                    "Inn Restaurant Menu Item", item.item, "item_type"
                )
                print("menu type = " + menu_type)
                if menu_type == "Food":
                    restaurant_food += float(item.rate)
                    print("restaurant_food now = " + str(restaurant_food))
                elif menu_type == "Beverage":
                    restaurant_beverage += float(item.rate)
                    print("restaurant_beverage now = " + str(restaurant_beverage))
                elif menu_type == "Other":
                    restaurant_other += float(item.rate)
                    print("restaurant_other now = " + str(restaurant_other))
        else:
            print("order list not exist")
        # Create Journal Entry for Total Amount of Orders for Food, Beverages, and Other Restaurant charges
        if restaurant_food > 0:
            print("entry restaurant food")
            food_title = "Restaurant Food of " + order.name
            food_remark = "Restaurant Food Charges from Restaurant Order: " + order.name
            food_debit_account = frappe.get_doc(
                "Inn Folio Transaction Type", transaction_types["restaurant_food"]
            ).debit_account
            food_credit_account = frappe.get_doc(
                "Inn Folio Transaction Type", transaction_types["restaurant_food"]
            ).credit_account
            create_journal_entry(
                food_title,
                food_remark,
                food_debit_account,
                food_credit_account,
                restaurant_food,
            )

        if restaurant_beverage > 0:
            print("entry restaurant beverage")
            bev_title = "Restaurant Beverages of " + order.name
            bev_remark = (
                "Restaurant Beverage Charges from Restaurant Order: " + order.name
            )
            bev_debit_account = frappe.get_doc(
                "Inn Folio Transaction Type", transaction_types["restaurant_beverages"]
            ).debit_account
            bev_credit_account = frappe.get_doc(
                "Inn Folio Transaction Type", transaction_types["restaurant_beverages"]
            ).credit_account
            create_journal_entry(
                bev_title,
                bev_remark,
                bev_debit_account,
                bev_credit_account,
                restaurant_beverage,
            )
        if restaurant_other > 0:
            print("entry Other Restaurant")
            other_title = "Other Restaurant of " + order.name
            other_remark = (
                "Other Restaurant Charges from Restaurant Order: " + order.name
            )
            other_debit_account = frappe.get_doc(
                "Inn Folio Transaction Type", transaction_types["restaurant_other"]
            ).debit_account
            other_credit_account = frappe.get_doc(
                "Inn Folio Transaction Type", transaction_types["restaurant_other"]
            ).credit_account
            create_journal_entry(
                other_title,
                other_remark,
                other_debit_account,
                other_credit_account,
                restaurant_other,
            )

        # Create Journal Entry for Round Off Charges
        if float(order.rounding_amount) > 0:
            ro_title = "Round Off of " + order.name
            ro_remark = (
                "Rounding off Amount of Restaurant Charges from Restaurant Order: "
                + order.name
            )
            ro_debit_account = frappe.get_doc(
                "Inn Folio Transaction Type", transaction_types["round_off"]
            ).debit_account
            ro_credit_account = frappe.get_doc(
                "Inn Folio Transaction Type", transaction_types["round_off"]
            ).credit_account
            create_journal_entry(
                ro_title,
                ro_remark,
                ro_debit_account,
                ro_credit_account,
                order.rounding_amount,
            )

        # Create Journal Entry for Service
        service_title = "FBS -- Service 10 % of " + order.name
        service_remark = (
            "Service of Restaurant Charges from Restaurant Order: " + order.name
        )
        srv_debit_account = frappe.get_doc(
            "Inn Folio Transaction Type", transaction_types["fbs_service_10"]
        ).debit_account
        srv_credit_account = frappe.get_doc(
            "Inn Folio Transaction Type", transaction_types["fbs_service_10"]
        ).credit_account
        create_journal_entry(
            service_title,
            service_remark,
            srv_debit_account,
            srv_credit_account,
            order.service_amount,
        )
        # Create Journal Entry for Tax
        tax_title = "FBS -- Tax 11 %" + order.name
        tax_remark = "Tax of Restaurant Charges from Restaurant Order: " + order.name
        tax_debit_account = frappe.get_doc(
            "Inn Folio Transaction Type", transaction_types["fbs_tax_11"]
        ).debit_account
        tax_credit_account = frappe.get_doc(
            "Inn Folio Transaction Type", transaction_types["fbs_tax_11"]
        ).credit_account
        create_journal_entry(
            tax_title,
            tax_remark,
            tax_debit_account,
            tax_credit_account,
            order.tax_amount,
        )

        # 2. ORDER PAYMENT IN RESTAURANT FINISHED ORDER
        order_payment_list = order.get("order_payment")
        if order_payment_list is not None and len(order_payment_list) > 0:
            for payment in order_payment_list:
                payment_title = payment.mode_of_payment + " Payment for " + order.name
                payment_remark = (
                    "Payment with "
                    + payment.mode_of_payment
                    + "from Restaurant Order: "
                    + order.name
                )
                payment_debit_account = frappe.db.get_value(
                    "Mode of Payment Account",
                    {
                        "parent": payment.mode_of_payment,
                        "company": frappe.get_doc("Global Defaults").default_company,
                    },
                    "default_account",
                )
                payment_credit_account = frappe.db.get_list(
                    "Account", filters={"account_number": "2110.005"}
                )[0].name
                create_journal_entry(
                    payment_title,
                    payment_remark,
                    payment_debit_account,
                    payment_credit_account,
                    payment.amount,
                )

        # 3. SET VALUE IS_JOURNALED IN FINISHED ORDER TO TRUE, MARKING THAT THE ORDER ALREADY PAIRED WITH JOURNAL ENTRIES
        frappe.db.set_value(
            "Inn Restaurant Finished Order", order.name, "is_journaled", 1
        )
