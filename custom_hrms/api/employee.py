# custom_hrms/hrms/employee.py
import frappe

def on_employee_before_save(doc, method):
    # Safely handle status before saving
    stage = getattr(doc, "custom_employment_stage", "")

    # Joining → Inactive
    if stage == "Joining":
        doc.status = "Inactive"

    # Confirmation → Active
    elif stage == "Confirmation":
        doc.status = "Active"

    # Exit → Left
    elif stage == "Exit":
        if not doc.relieving_date:
            frappe.throw("Please Fill The Employee Relieving Date in Employee Exit Tab")
        else:
            doc.status = "Left"
            attach_experience_letter(doc)


def attach_experience_letter(doc):
    """Generate Experience Letter PDF and attach to Employee if status is Left."""
    try:
        if doc.status != "Left":
            return

        # Generate PDF from print format
        pdf_content = frappe.get_print(doc.doctype, doc.name, print_format="Experience Letter", as_pdf=True)
        file_name = f"Experience_Letter_{doc.employee_name}.pdf"

        # Delete old file if exists
        existing_files = frappe.get_all("File", filters={
            "attached_to_doctype": doc.doctype,
            "attached_to_name": doc.name,
            "file_name": file_name
        }, pluck="name")
        for f in existing_files:
            frappe.delete_doc("File", f, force=True)

        # Create new file
        file_doc = frappe.get_doc({
            "doctype": "File",
            "file_name": file_name,
            "attached_to_doctype": doc.doctype,
            "attached_to_name": doc.name,
            "content": pdf_content,
            "is_private": 0,  # set to 1 if you want private file
        })
        file_doc.insert(ignore_permissions=True)
        frappe.db.commit()

    except Exception:
        frappe.log_error(frappe.get_traceback(), "Failed to attach Experience Letter")





@frappe.whitelist()
def get_experience_letter(employee):
    """Return experience letter file URL if status is Left, otherwise a message."""
    emp = frappe.get_doc("Employee", employee)
    if emp.status != "Left":
        return {"allowed": False, "message": "You are still part of the organization. You cannot view the Experience Letter."}

    # Find attached file
    file_doc = frappe.get_all("File", filters={
        "attached_to_doctype": "Employee",
        "attached_to_name": employee,
        "file_name": ["like", "Experience_Letter%"]
    }, fields=["file_url"], limit=1)

    if not file_doc:
        return {"allowed": False, "message": "Experience Letter not found. Please contact HR."}

    return {"allowed": True, "file_url": file_doc[0].file_url}
