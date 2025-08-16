# -*- coding: utf-8 -*-
# Copyright (c) 2020, Core Initiative and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import datetime
import frappe
import json
import random
import string
from frappe.model.document import Document, flt
from inn.inn_hotels.doctype.inn_channel.inn_channel import (
    check_channel_commission,
    PROFIT_SHARING_ENABLED,
    PROFIT_SHARING_TYPE_PERCENTAGE,
)
from inn.inn_hotels.doctype.inn_folio.inn_folio import (
    close_folio,
    get_balance_by_reservation,
    create_folio,
)


class InnReservation(Document):
    pass


@frappe.whitelist()
def check_in_reservation(reservation_id):
    doc = frappe.get_doc("Inn Reservation", reservation_id)

    channel = check_channel_commission(doc)
    if channel.profit_sharing == PROFIT_SHARING_ENABLED:
        if channel.sharing_type == PROFIT_SHARING_TYPE_PERCENTAGE:
            doc.comission = channel.breakfast_cashback + channel.room_cashback
            doc.save()

    room_doc = frappe.get_doc("Inn Room", doc.actual_room_id)
    if room_doc.room_status == "Vacant Ready":
        if doc.status == "Reserved":
            doc.status = "In House"
            doc.save()
            if doc.status == "In House":
                room_doc.room_status = "Occupied Clean"
                room_doc.save()

        return doc.status
    else:
        return (
            "Currently, Room " + room_doc.name + "status is not Vacant Ready. "
            "Please consult with Room Service or choose another Room to continue Checking In."
        )


@frappe.whitelist()
def start_check_in(source, reservation):
    if source == "list":
        reservation_id = json.loads(reservation)[0]
    elif source == "check_in_button":
        reservation_id = reservation

    if frappe.db.get_value("Inn Reservation", reservation_id, "status") == "Reserved":
        generate_wifi_password(reservation_id)
        return (
            frappe.utils.get_url_to_form("Inn Reservation", reservation_id)
            + "?is_check_in=true"
        )
    else:
        frappe.msgprint("Reservation Status must be Reserved in order to be Checked In")


@frappe.whitelist()
def cancel_reservation(source, reservation):
    reservation_to_cancel = []
    exist_status_not_reserved = []
    exist_cancellation_fail = []

    if source == "list":
        reservation = json.loads(reservation)
        for item in reservation:
            reservation_to_cancel.append(item)
    elif source == "cancel_button":
        reservation_to_cancel.append(reservation)

    for reservation_id in reservation_to_cancel:
        doc = frappe.get_doc("Inn Reservation", reservation_id)
        if doc.status != "Reserved":
            exist_status_not_reserved.append(reservation_id)

    if len(exist_status_not_reserved) > 0:
        return 1
    else:
        for reservation_id in reservation_to_cancel:
            cancellation_message = cancel_single_reservation(reservation_id)
            if cancellation_message == 1:
                exist_cancellation_fail.append(reservation_id)

        if len(exist_cancellation_fail) > 0:
            return 1
        else:
            return 0


def cancel_single_reservation(reservation_id):
    reservation = frappe.get_doc("Inn Reservation", reservation_id)
    folio = frappe.get_doc("Inn Folio", {"reservation_id": reservation_id})
    room_booking = frappe.get_doc(
        "Inn Room Booking",
        {"reference_type": "Inn Reservation", "reference_name": reservation_id},
    )

    if reservation.status != "Cancel":
        reservation.status = "Cancel"
        reservation.save()
    if folio.status != "Cancel":
        folio.status = "Cancel"
        folio.save()
    if room_booking.status != "Canceled":
        room_booking.status = "Canceled"
        room_booking.save()

    if (
        reservation.status == "Cancel"
        and folio.status == "Cancel"
        and room_booking.status == "Canceled"
    ):
        return 0
    else:
        return 1


@frappe.whitelist()
def cancel_single_reservation_in_house(reservation_id):
    # return 0 if cancel success
    # return 1 if cancel fail
    # return 2 if the folio balance of Folio not 0 yet

    if get_balance_by_reservation(reservation_id) == 0:
        reservation = frappe.get_doc("Inn Reservation", reservation_id)
        room_doc = frappe.get_doc("Inn Room", reservation.actual_room_id)
        folio = frappe.get_doc("Inn Folio", {"reservation_id": reservation_id})
        room_booking = frappe.get_doc(
            "Inn Room Booking",
            {"reference_type": "Inn Reservation", "reference_name": reservation_id},
        )

        if reservation.status != "Cancel":
            reservation.status = "Cancel"
            reservation.save()
        if room_doc.room_status != "Vacant Dirty":
            room_doc.room_status = "Vacant Dirty"
            room_doc.save()
        if folio.status != "Closed":
            folio.status = "Closed"
            folio.save()
        if room_booking.status != "Finished":
            room_booking.status = "Finished"
            room_booking.end = frappe.utils.today()
            room_booking.save()

        if (
            reservation.status == "Cancel"
            and room_doc.room_status == "Vacant Dirty"
            and folio.status == "Closed"
            and room_booking.status == "Finished"
        ):
            return 0
        else:
            return 1
    else:
        return 2


@frappe.whitelist()
def no_show_reservation(source, reservation):
    reservation_to_no_show = []
    exist_status_not_reserved = []
    exist_no_show_fail = []

    if source == "list":
        reservation = json.loads(reservation)
        for item in reservation:
            reservation_to_no_show.append(item)
    elif source == "no_show_button":
        reservation_to_no_show.append(reservation)

    for reservation_id in reservation_to_no_show:
        doc = frappe.get_doc("Inn Reservation", reservation_id)
        if doc.status != "Reserved":
            exist_status_not_reserved.append(reservation_id)

    if len(exist_status_not_reserved) > 0:
        return 1
    else:
        for reservation_id in reservation_to_no_show:
            no_show_message = no_show_single_reservation(reservation_id)
            if no_show_message == 1:
                exist_no_show_fail.append(reservation_id)

        if len(exist_no_show_fail) > 0:
            return 1
        else:
            return 0


def no_show_single_reservation(reservation_id):
    reservation = frappe.get_doc("Inn Reservation", reservation_id)
    folio = frappe.get_doc("Inn Folio", {"reservation_id": reservation_id})
    room_booking = frappe.get_doc(
        "Inn Room Booking",
        {"reference_type": "Inn Reservation", "reference_name": reservation_id},
    )

    if reservation.status != "No Show":
        reservation.status = "No Show"
        reservation.save()
    if folio.status != "Cancel":
        folio.status = "Cancel"
        folio.save()
    if room_booking.status != "Canceled":
        room_booking.status = "Canceled"
        room_booking.save()

    if (
        reservation.status == "No Show"
        and folio.status == "Cancel"
        and room_booking.status == "Canceled"
    ):
        return 0
    else:
        return 1


@frappe.whitelist()
def check_out_reservation(reservation_id):
    doc = frappe.get_doc("Inn Reservation", reservation_id)
    room_doc = frappe.get_doc("Inn Room", doc.actual_room_id)
    folio_doc = frappe.get_doc("Inn Folio", {"reservation_id": reservation_id})
    # Change folio status
    folio_status = close_folio(folio_doc.name)
    if folio_status == "Closed":
        if doc.status == "In House":
            doc.departure = datetime.datetime.now()
            doc.status = "Finish"
            doc.save()
            if doc.status == "Finish":
                # Change room status
                room_doc.room_status = "Vacant Dirty"
                room_doc.save()
        return doc.status
    else:
        return folio_status


def generate_wifi_password(reservation_id):
    reservation = frappe.get_doc("Inn Reservation", reservation_id)
    mode = frappe.db.get_single_value("Inn Hotels Setting", "hotspot_api_mode")

    if mode == "First Name":
        guest_name = reservation.guest_name
        if guest_name:
            password = guest_name.partition(" ")[0]
        else:
            name = reservation.customer_id
            password = name.partition(" ")[0].lower()
    elif mode == "Random Number":
        digits = string.digits
        password = "".join(random.choice(digits) for i in range(6))
    else:
        digits = string.digits
        password = "".join(random.choice(digits) for i in range(6))

    if reservation.wifi_password is None or reservation.wifi_password == "":
        frappe.db.set_value(
            "Inn Reservation", reservation_id, "wifi_password", password
        )


@frappe.whitelist()
def calculate_room_bill(arrival, departure, actual_rate):
    start = datetime.datetime.strptime(arrival, "%Y-%m-%d %H:%M:%S")
    end = datetime.datetime.strptime(departure, "%Y-%m-%d %H:%M:%S")
    total_day = (end - start).days
    return float(total_day) * float(actual_rate)


@frappe.whitelist()
def get_folio_url(reservation_id):

    folio_name = frappe.db.get_value(
        "Inn Folio", {"reservation_id": reservation_id}, ["name"]
    )
    if folio_name == None:
        create_folio(reservation_id)
        folio_name = frappe.db.get_value(
            "Inn Folio", {"reservation_id": reservation_id}, ["name"]
        )

    return frappe.utils.get_url_to_form("Inn Folio", folio_name)


@frappe.whitelist()
def allowed_to_in_house(reservation_id):
    deposit = False
    if frappe.db.exists(
        "Inn Folio Transaction",
        {
            "parent": frappe.get_doc(
                "Inn Folio", {"reservation_id": reservation_id}
            ).name,
            "transaction_type": "Deposit",
        },
    ):
        deposit = True
    return deposit


@frappe.whitelist()
def get_total_deposit(doc):
    """
    Get the total deposit for a reservation or group.
    The transaction type (e.g., 'Down Payment') is dynamically fetched from Inn Hotels Setting.
    """
    # Fetch the transaction type from Inn Hotels Setting
    transaction_type = frappe.db.get_single_value("Inn Hotels Setting", "down_payment")

    if not transaction_type:
        frappe.throw("Transaction type for deposit is not set in Inn Hotels Setting.")

    if doc.group_id:
        return frappe.db.sql(
            """
      SELECT SUM(amount) AS amount 
      FROM `tabInn Folio Transaction` ft
      LEFT JOIN `tabInn Folio` f ON f.name=ft.parent
      LEFT JOIN `tabInn Reservation` r ON r.name=f.reservation_id
      WHERE r.group_id=%s AND ft.transaction_type=%s
    """,
            (doc.group_id, transaction_type),
            as_dict=True,
        )
    else:
        return frappe.db.sql(
            """
      SELECT SUM(amount) AS amount 
      FROM `tabInn Folio Transaction` ft
      LEFT JOIN `tabInn Folio` f ON f.name=ft.parent
      LEFT JOIN `tabInn Reservation` r ON r.name=f.reservation_id
      WHERE r.name=%s AND ft.transaction_type=%s
    """,
            (doc.name, transaction_type),
            as_dict=True,
        )


@frappe.whitelist()
def get_date():
    return datetime.datetime.now().strftime("%d/%m/%Y")


@frappe.whitelist()
def check_discount(room_type, discount):
    maximum_discount = frappe.db.get_value(
        "Inn Room Type", room_type, "maximum_discount_percentage"
    )
    return flt(discount, 3) <= flt(maximum_discount, 3)
