
import frappe
import json
from pathlib import Path

@frappe.whitelist()
def insert_role():
    path = Path(__file__).with_name("role.json")
    with path.open("r") as file:
        data = json.load(file)
        file.close()
 
    create_role(data["role"])
    create_role_profile(data["role_profile"]) 
    frappe.msgprint("Generating Role and Role Profile Success")
    return 

def create_role(roles):

    for group in roles:
        group_name = group["group"]
        print(f"FROM GROUP: {group_name}")
        for role in group["roles"]:
            role_name = role["name"]

            if not frappe.db.exists("Role", role_name):
                print(f"----CREATING ROLE: {role_name}")

                doc_role = frappe.new_doc("Role")
                doc_role.search_bar = True
                doc_role.desk_access = True
                doc_role.list_sidebar = True
                doc_role.dashboard = True
                doc_role.role_name = role_name

                doc_role.insert()
            else:
                print(f"----ROLE {role_name} already exists!")

def create_role_profile(profiles):
    
    for profile in profiles:
        profile_name = profile["name"]

        if not frappe.db.exists("Role Profile", profile_name):
            print(f"CREATING ROLE PROFILE: {profile_name}")

            profile_doc = frappe.new_doc("Role Profile")
            profile_doc.role_profile = profile_name

            for role in profile["roles_assigned"]:
                role_name = role["name"]
                print(f"----APPEND ROLE: {role_name}")
                role_doc = frappe.new_doc("Has Role")
                role_doc.role = role_name
                role_doc.parentfield = "roles"
                role_doc.parent = profile_doc.name
                role_doc.parenttype = "Role Profile"
                profile_doc.roles.append(role_doc)
            
            profile_doc.save()