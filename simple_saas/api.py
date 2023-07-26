import frappe
import stripe

from frappe.utils.password import get_decrypted_password

api_key = get_decrypted_password("SaaS Settings", "SaaS Settings", "stripe_secret_key")
stripe.api_key = api_key


@frappe.whitelist()
def mark_subscription_active():
	plan = "price_1NY4ntSAUHwwQiieYmQmhCRL"
	current_user = frappe.session.user
	customer = frappe.get_doc("Stripe Customer", {"user": current_user})

	frappe.db.set_value(
		"Subscription Record",
		{"stripe_customer": customer.name, "plan": plan},
		"status",
		"Active"
	)


@frappe.whitelist()
def subscribe():
	plan = "price_1NY4ntSAUHwwQiieYmQmhCRL"
	current_user = frappe.session.user
	customer = frappe.get_doc("Stripe Customer", {"user": current_user})

	subscription_exists = frappe.db.exists(
		"Subscription Record", {"stripe_customer": customer.name, "plan": plan}
	)

	# if subscription_exists:
	# 	return {
	# 		"secret_key": frappe.db.get_value(
	# 			"Subscription Record",
	# 			{"stripe_customer": customer.name, "plan": plan},
	# 			"pi_secret_key",
	# 		)
	# 	}

	s = stripe.Subscription.create(
		customer=customer.customer_id,
		items=[{"price": plan}],
		payment_behavior="default_incomplete",
		payment_settings={"save_default_payment_method": "on_subscription"},
		expand=["latest_invoice.payment_intent"],
	)

	subscription_record = frappe.new_doc("Subscription Record")
	subscription_record.stripe_customer = customer.name
	subscription_record.plan = plan
	subscription_record.pi_secret_key = s.latest_invoice.payment_intent.client_secret
	subscription_record.save(ignore_permissions=True)

	return {"secret_key": s.latest_invoice.payment_intent.client_secret}
