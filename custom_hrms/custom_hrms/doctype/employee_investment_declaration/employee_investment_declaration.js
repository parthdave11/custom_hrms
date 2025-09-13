// Copyright (c) 2025, Parth Dave and contributors
// For license information, please see license.txt

frappe.ui.form.on("Employee Investment Declaration", {
	refresh(frm) {

	},
    section_80c(frm) { calculate_total(frm); },
    section_80d(frm) { calculate_total(frm); },
    other_exemptions(frm) { calculate_total(frm); }
});

function calculate_total(frm) {
    frm.set_value("total_investment", 
        (frm.doc.section_80c || 0) +
        (frm.doc.section_80d || 0) +
        (frm.doc.other_exemptions || 0)
    );
}