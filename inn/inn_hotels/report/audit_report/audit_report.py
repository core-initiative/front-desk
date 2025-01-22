import frappe
from datetime import date
from dateutil.parser import parse

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

'''goals:

i want to see all reservation that have in house status in specified date
from all those reservation i want all transaction from that specified date on those reservation

question:

- apa yang menandakan bahwa reservasi sedang berstatus in house pada tanggal tsb?
jawab:
opt1:  
    - cek apakah reservasi sekarang berstatus in house memiliki expected date dibawah tanggal tersebut? 
        => tandanya pada tanggal tersebut terdapat transaksi pada reservasi tersebut
    - untuk reservasi status Reserved, Canceled, No Show berarti belum inhouse pada tanggal tersebut
    - untuk reservasi status finished, check apakah actual arrival dan actual 
        departure berada diantara tanggal tersebut 
        => tandanya pada tanggal tersebut terdapat transaksi pada reservasi
    - untuk seluruh transaksi pada reservasi, ambil transaksi yang terjadi pada tanggal tersebut


'''

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
    if filters.date is None:
        filters.date = date.today().isoformat()

    return get_data_detail(filters.date, filters.fill_mode_payment)

def get_data_detail(start_date, is_show_mode_payment):
    query = f"""
        select ir.name, ir.status, ir.customer_id, ir.room_type, ir.actual_room_id, ir.channel, ir.actual_room_rate, if.name as folio, if.bill_instructions
        from `tabInn Reservation` as ir
        left join `tabInn Folio` as `if`
        on if.reservation_id = ir.name
        where 
        (ir.status = 'In House' and ir.expected_arrival <= '{start_date}') or
        (ir.status = 'Finish' and ir.expected_arrival <= '{start_date}' and ir.expected_departure > '{start_date}')
    """

    reservation = frappe.db.sql(query=query, as_dict=1)
    if len(reservation) == 0:
        return []

    folio_name = tuple([x.folio for x in reservation])
    folio_detail = get_folio_detail(folio_name, start_date)

    if is_show_mode_payment:
        res = [
            [x.name,
             x.customer_id,
             x.room_type,
             x.actual_room_id,
             folio_detail[x.folio]["actual_room_rate"],
             folio_detail[x.folio]["actual_room_nett"],
             folio_detail[x.folio]["breakfast_revenue"],
             folio_detail[x.folio]["comission"],  # comission
             x.channel,
             "",
             # mode of payment
             folio_detail[x.folio]["mode_of_payment"][:-2],
             folio_detail[x.folio]["total_amount"],
             folio_detail[x.folio]["payment_date"],  # paid date
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
             folio_detail[x.folio]["actual_room_rate"],
             folio_detail[x.folio]["actual_room_nett"],
             folio_detail[x.folio]["breakfast_revenue"],
             folio_detail[x.folio]["comission"],  # comission
             x.channel,
             "",
             "",  # mode of payment
             folio_detail[x.folio]["total_amount"],
             folio_detail[x.folio]["payment_date"],  # paid date
             "",
             x.bill_instructions
             ]
            for x in reservation]

    return res
def get_folio_detail(folio_ids, start_date):
# folio detail
    # need data:
    # actual room nett, breakfast revenue, mode of payment, total_amount (payment_amount?), payment_date

    fill_setting_data()
    transaction_type_list = (TRANSACTION_TYPE_COMISSION, TRANSACTION_TYPE_ROOM_REVENUE,
                             TRANSACTION_TYPE_BREAKFAST_REVENUE, TRANSACTION_TYPE_PAYMENT, TRANSACTION_TYPE_ROOM_PAYMENT)

    if len(folio_ids) == 1:
        folio_id_query = "= %(folio_id)s"
        params = {'folio_id': folio_ids[0], 'start_date': start_date}
    else:
        folio_id_query = "IN %(folio_ids)s"
        params = {'folio_ids': folio_ids, 'start_date': start_date}

    query = f"""
        SELECT parent, transaction_type, amount, mode_of_payment, creation, actual_room_rate
        FROM `tabInn Folio Transaction` AS ift
        WHERE ift.parent {folio_id_query}
        AND ift.transaction_type IN %(transaction_types)s
        AND ift.audit_date = %(start_date)s
    """

    folio_detail = frappe.db.sql(query, {**params, 'transaction_types': transaction_type_list}, as_dict=True)
    res = {folio: {
        "actual_room_rate": 0,
        "actual_room_nett": 0,
        "breakfast_revenue": 0,
        "mode_of_payment": "",
        "total_amount": 0,
        "payment_date": "",
        "comission": 0
    } for folio in folio_ids}

    for data in folio_detail:
        if data.transaction_type == TRANSACTION_TYPE_ROOM_REVENUE:
            res[data.parent]["actual_room_nett"] += data.amount
            res[data.parent]["actual_room_rate"] = data.actual_room_rate
        elif data.transaction_type in (TRANSACTION_TYPE_PAYMENT, TRANSACTION_TYPE_ROOM_PAYMENT):
            res[data.parent]["mode_of_payment"] += f"BY {data.mode_of_payment} {data.amount:,}, ".replace(",", ".")
            res[data.parent]["total_amount"] += data.amount
            res[data.parent]["payment_date"] += f"{data.creation}, "
        elif data.transaction_type == TRANSACTION_TYPE_BREAKFAST_REVENUE:
            res[data.parent]["breakfast_revenue"] += data.amount
        elif data.transaction_type == TRANSACTION_TYPE_COMISSION:
            res[data.parent]["comission"] += data.amount

    return res

def fill_setting_data():
    global TRANSACTION_TYPE_COMISSION, TRANSACTION_TYPE_ROOM_REVENUE, TRANSACTION_TYPE_BREAKFAST_REVENUE, TRANSACTION_TYPE_PAYMENT, TRANSACTION_TYPE_ROOM_PAYMENT, BREAKFAST_REVENUE_ACCOUNT, ROOM_REVENUE_ACCOUNT

    setting = frappe.get_single("Inn Hotels Setting")
    TRANSACTION_TYPE_COMISSION = setting.comission_channel or "Comission Channel"
    TRANSACTION_TYPE_ROOM_REVENUE = setting.room_charge or "Room Charge"
    TRANSACTION_TYPE_BREAKFAST_REVENUE = setting.breakfast_charge or "Breakfast Charge"
    TRANSACTION_TYPE_PAYMENT = setting.payment or "Payment"
    TRANSACTION_TYPE_ROOM_PAYMENT = setting.room_payment or "Room Payment"

    if not setting.breakfast_revenue_account:
        frappe.throw("Breakfast Revenue Account in Inn Hotels Setting not set yet")
    BREAKFAST_REVENUE_ACCOUNT = setting.breakfast_revenue_account

    if not setting.room_revenue_account:
        frappe.throw("Room Revenue Account in Inn Hotels Setting not set yet")
    ROOM_REVENUE_ACCOUNT = setting.room_revenue_account