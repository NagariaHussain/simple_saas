# Copyright (c) 2023, Build With Hussain and contributors
# For license information, please see license.txt

import frappe
import stripe
from frappe.model.document import Document
from frappe.utils.password import get_decrypted_password


api_key = get_decrypted_password("SaaS Settings", "SaaS Settings", "stripe_secret_key")
stripe.api_key = api_key	

class StripeCustomer(Document):
	def before_insert(self):
		full_name = frappe.db.get_value("User", self.user, "full_name")
		customer = stripe.Customer.create(email=self.user, name=full_name)
		self.customer_id = customer.id
