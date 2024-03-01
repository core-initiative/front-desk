import frappe


def _fill_party_account(doc_id: str, party_in: str) -> tuple[str, str]:
    """Return party type is Customer or Supplier 
    by querying to Account database and check its account type if its 
    Receiveable (return Customer) or Payable (return Supplier)

    Parameters
    ----
    doc_id : str, account id
        Account identifier
    
    party : str, party name
        Party name will be echoed if account type is Receiveable or Payable 

    """
    party_type = ""
    party = ""
    doc_jea_type_account = frappe.get_doc("Account", doc_id)
    match doc_jea_type_account.account_type:
        case "Receivable":
            party_type = 'Customer'
            party = party_in
        case "Payable":
            party_type = 'Supplier'
            party = party_in
    # print('--from _fill_party_account')
    # print('account: '+ doc_id)
    # print('account type: ' + doc_jea_type_account.account_type)
    # print("party type: " + party_type)
    # print("party: " + party)
    # print('--endfrom')

    return party_type, party