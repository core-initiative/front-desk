import frappe
from datetime import date

FILTER_FIELD_DATE = "expected_arrival"
FILTER_FIELD_STATUS = "status"
STATUS_RESERVED = "Reserved"
TRANSACTION_TYPE_ROOM_REVENUE = ""
TRANSACTION_TYPE_COMISSION = ""
TRANSACTION_TYPE_BREAKFAST_REVENUE = ""
TRANSACTION_TYPE_PAYMENT = ""
TRANSACTION_TYPE_ROOM_PAYMENT = ""
BREAKFAST_REVENUE_ACCOUNT = ""
ROOM_REVENUE_ACCOUNT = ""


def execute(filters=None):
    columns = [
        {
            'fieldname': 'rsv',
            'label': 'RSV',
            'fieldtype': 'Data',
            'width': 150,
        },
        {
            'fieldname': 'customer',
            'label': 'Customer',
            'fieldtype': 'Data',
            'width': 150,
        },
        {
            'fieldname': 'room_type',
            'label': 'Room Type',
            'fieldtype': 'Data',
            'width': 150,
        },
        {
            'fieldname': 'actual_room',
            'label': 'Actual Room',
            'fieldtype': 'Data',
            'width': 150,
        },
        {
            'fieldname': 'actual_room_rate',
            'label': 'Actual Room Rate',
            'fieldtype': 'Currency',
            'width': 150,
        },
        {
            'fieldname': 'actual_room_nett',
            'label': 'Actual Room Nett',
            'fieldtype': 'Currency',
            'width': 150,
        },
        {
            'fieldname': 'bf_revenue',
            'label': 'BF Revenue',
            'fieldtype': 'Currency',
            'width': 150,
        },
        {
            'fieldname': "comission",
            'fieldtype': "Currency",
            'label': "Comission",
            'width': 150
        },
        {
            'fieldname': 'payment_by',
            'label': 'Payment By',
            'fieldtype': 'Data',
            'width': 150,
        },
        {
            'fieldname': 'status',
            'label': 'Status',
            'fieldtype': 'Data',
            'width': 150,
        },
        {
            'fieldname': 'mode_of_payment',
            'label': 'Mode of Payment',
            'fieldtype': 'Data',
            'width': 150,
        },
        {
            'fieldname': 'total_amount',
            'label': 'Total Amount',
            'fieldtype': 'Currency',
            'width': 150,
        },
        {
            'fieldname': "posting_date",
            "label": "Posting date",
            'fieldtype': 'Date',
            'width': 150
        },
        {
            'fieldname': 'paid_date',
            'label': 'Paid Date',
            'fieldtype': 'Date',
            'width': 150,
        },
        {
            'fieldname': 'remark',
            'label': 'Remark',
            'fieldtype': 'Data',
            'width': 150,
        }
    ]

    data = get_data(filters)

    return columns, data


def get_data(filters):
    if filters.date == None:
        filters.date = date.today().isoformat()

    return get_data_detail(filters.date, filters.fill_mode_payment)


def get_data_detail(start_date, is_show_mode_payment):

    query = f"""
        select ir.name, ir.status, ir.customer_id, ir.room_type, ir.actual_room_id, ir.channel, ir.actual_room_rate, if.name as folio, if.bill_instructions
        from `tabInn Reservation` as ir
        left join `tabInn Folio` as `if`
        on if.reservation_id = ir.name
        where {FILTER_FIELD_DATE} = '{start_date}' and ir.{FILTER_FIELD_STATUS} != '{STATUS_RESERVED}'
    """

    reservation = frappe.db.sql(query=query, as_dict=1)
    if len(reservation) == 0:
        return []

    folio_name = tuple([x.folio for x in reservation])
    folio_detail = get_folio_detail(folio_name)

    if is_show_mode_payment:
        res = [
            [x.name,
             x.customer_id,
             x.room_type,
             x.actual_room_id,
             x.actual_room_rate,
             folio_detail[x.folio]["actual_room_nett"],
             folio_detail[x.folio]["breakfast_revenue"],
             folio_detail[x.folio]["comission"],  # comission
             x.channel,
             "",
             # mode of payment
             folio_detail[x.folio]["mode_of_payment"][:-2],
             folio_detail[x.folio]["payment_date"],  # paid date
             folio_detail[x.folio]["total_amount"],
             "",
             x.bill_instructions
             ]
            for x in reservation]
    else:
        res = [
            [x.name,
             x.customer_id,
             x.room_type,
             x.actual_room_id,
             x.actual_room_rate,
             folio_detail[x.folio]["actual_room_nett"],
             folio_detail[x.folio]["breakfast_revenue"],
             folio_detail[x.folio]["comission"],  # comission
             x.channel,
             "",
             "",  # mode of payment
             folio_detail[x.folio]["payment_date"],  # paid date
             folio_detail[x.folio]["total_amount"],
             "",
             x.bill_instructions
             ]
            for x in reservation]

    return res


def get_folio_detail(folio_id: list):
    # folio detail
    # need data:
    # actual room nett, breakfast revenue, mode of payment, total_amount (payment_amount?), payment_date

    fill_setting_data()
    transaction_type_list = (TRANSACTION_TYPE_COMISSION, TRANSACTION_TYPE_ROOM_REVENUE,
                             TRANSACTION_TYPE_BREAKFAST_REVENUE, TRANSACTION_TYPE_PAYMENT, TRANSACTION_TYPE_ROOM_PAYMENT)

    if (len(folio_id) == 1):
        folio_id_query = f"= '{folio_id[0]}'"
    else:
        folio_id_query = f'in {folio_id}'

    query = f"""
        select parent, transaction_type, amount, mode_of_payment, creation
        from `tabInn Folio Transaction` as ift
        where ift.parent {folio_id_query}
        and
        ift.transaction_type in {transaction_type_list}
    """
    folio_detail = frappe.db.sql(query=query, as_dict=1)
    res = {folio: {
        "actual_room_nett": 0,
        "breakfast_revenue": 0,
        "mode_of_payment": "",
        "total_amount": 0,
        "payment_date": "",
        "comission": 0
    } for folio in folio_id}

    for data in folio_detail:
        # populate aggrate folio data detail, grouped by folio number
        if data.transaction_type == TRANSACTION_TYPE_ROOM_REVENUE:
            res[data.parent]["actual_room_nett"] += data.amount
        elif data.transaction_type == TRANSACTION_TYPE_PAYMENT or data.transaction_type == TRANSACTION_TYPE_ROOM_PAYMENT:
            res[data.parent]["mode_of_payment"] += f"BY {data.mode_of_payment} {data.amount:,}".replace(
                ",", ".") + ", "
            res[data.parent]["total_amount"] += data.amount
            res[data.parent]["payment_date"] += f"{data.creation}, "
        elif data.transaction_type == TRANSACTION_TYPE_BREAKFAST_REVENUE:
            res[data.parent]["breakfast_revenue"] += data.amount
        elif data.transaction_type == TRANSACTION_TYPE_COMISSION:
            res[data.parent]["comission"] += data.amount

    return res


def fill_setting_data():
    # get data setting
    global TRANSACTION_TYPE_COMISSION, TRANSACTION_TYPE_ROOM_REVENUE, TRANSACTION_TYPE_BREAKFAST_REVENUE, TRANSACTION_TYPE_PAYMENT, TRANSACTION_TYPE_ROOM_PAYMENT, BREAKFAST_REVENUE_ACCOUNT, ROOM_REVENUE_ACCOUNT
    transaction_type = frappe.db.get_values_from_single(fields=["profit_sharing_transaction_type", "room_revenue_transaction_type", "breakfast_revenue_transaction_type", "customer_payment_transaction_type",
                                                        "customer_room_payment_transaction_type", "breakfast_revenue_account", "room_revenue_account"], filters="", doctype="Inn Hotels Setting", as_dict=True)[0]
    if transaction_type.profit_sharing_transaction_type == None:
        TRANSACTION_TYPE_COMISSION = "Comission Channel"
    else:
        TRANSACTION_TYPE_COMISSION = transaction_type.profit_sharing_transaction_type

    if transaction_type.room_revenue_transaction_type == None:
        TRANSACTION_TYPE_ROOM_REVENUE = "Room Charge"
    else:
        TRANSACTION_TYPE_ROOM_REVENUE = transaction_type.room_revenue_transaction_type

    if transaction_type.breakfast_revenue_transaction_type == None:
        TRANSACTION_TYPE_BREAKFAST_REVENUE = "Breakfast Charge"
    else:
        TRANSACTION_TYPE_BREAKFAST_REVENUE = transaction_type.breakfast_revenue_transaction_type

    if transaction_type.customer_payment_transaction_type == None:
        TRANSACTION_TYPE_PAYMENT = "Payment"
    else:
        TRANSACTION_TYPE_PAYMENT = transaction_type.customer_payment_transaction_type

    if transaction_type.customer_room_payment_transaction_type == None:
        TRANSACTION_TYPE_ROOM_PAYMENT = "Room Payment"
    else:
        TRANSACTION_TYPE_ROOM_PAYMENT = transaction_type.customer_room_payment_transaction_type

    if transaction_type.breakfast_revenue_account == None:
        raise ImportError(
            "Breakfast Revenue Account in Inn Hotels Setting not set yet")
    else:
        BREAKFAST_REVENUE_ACCOUNT = transaction_type.breakfast_revenue_account

    if transaction_type.room_revenue_account == None:
        raise ImportError(
            "Room Revenue Account in Inn Hotels Setting not set yet")
    else:
        ROOM_REVENUE_ACCOUNT = transaction_type.room_revenue_account
