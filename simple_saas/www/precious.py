import frappe

def get_context(context):
	if frappe.session.user == "Guest":
		context.is_subscribed = False
		return context

	plan = "price_1NY4ntSAUHwwQiieYmQmhCRL"
	current_user = frappe.session.user
	customer_name = frappe.db.get_value("Stripe Customer", {"user": current_user}, "name")

	status = frappe.db.get_value(
		"Subscription Record",
		{"stripe_customer": customer_name, "plan": plan},
		"status",
	)

	context.is_subscribed = status == "Active"
