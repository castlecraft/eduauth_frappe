"""Setup and seed demo data for manual testing of Topaz ReBAC permissions on a fresh site."""

from __future__ import annotations

import frappe
from frappe.utils.password import update_password

DEMO_USERS = [
	{
		"email": "albus.dumbledore@hogwarts.edu",
		"first_name": "Albus",
		"last_name": "Dumbledore",
		"roles": ["System Manager"],
	},
	{
		"email": "minerva.mcgonagall@hogwarts.edu",
		"first_name": "Minerva",
		"last_name": "McGonagall",
		"roles": ["Desk User"],
	},
	{
		"email": "harry.potter@hogwarts.edu",
		"first_name": "Harry",
		"last_name": "Potter",
		"roles": ["Desk User"],
	},
	{
		"email": "severus.snape@hogwarts.edu",
		"first_name": "Severus",
		"last_name": "Snape",
		"roles": ["Desk User"],
	},
]


def setup_demo(password: str = "password123"):
	"""Create demo users, role permissions, and educational records."""
	print("--- 1. Creating Demo Users ---")
	for udata in DEMO_USERS:
		email = udata["email"]
		if not frappe.db.exists("User", email):
			user = frappe.get_doc(
				{
					"doctype": "User",
					"email": email,
					"first_name": udata["first_name"],
					"last_name": udata["last_name"],
					"send_welcome_email": 0,
					"user_type": "System User",
				}
			)
			user.insert(ignore_permissions=True)
			print(f"Created user: {email}")
		else:
			user = frappe.get_doc("User", email)
			user.user_type = "System User"
			user.enabled = 1
			user.save(ignore_permissions=True)

		# Set standard password
		update_password(email, password)

		# Assign roles
		for role in udata["roles"]:
			if not frappe.db.exists("Has Role", {"parent": email, "role": role}):
				user.add_roles(role)

	print("--- 2. Granting Desk Permissions on DocTypes ---")
	# Grant Desk User read & write permissions so Frappe allows the request through
	# to the Topaz ReBAC gate (custom_has_permission & query_conditions).
	for doctype in ["Eduauth Department", "Eduauth Committee", "Eduauth Institute", "Eduauth Project"]:
		if not frappe.db.exists("Custom DocPerm", {"parent": doctype, "role": "Desk User"}):
			frappe.get_doc(
				{
					"doctype": "Custom DocPerm",
					"parent": doctype,
					"parenttype": "DocType",
					"parentfield": "permissions",
					"role": "Desk User",
					"read": 1,
					"write": 1,
					"create": 1,
					"delete": 1,
				}
			).insert(ignore_permissions=True)
			print(f"Added Desk User permission for {doctype}")

	print("--- 3. Creating Educational Records ---")
	# Institute
	if not frappe.db.exists("Eduauth Institute", "Hogwarts"):
		frappe.get_doc(
			{
				"doctype": "Eduauth Institute",
				"name": "Hogwarts",
				"institute_name": "Hogwarts School of Witchcraft and Wizardry",
				"director": "albus.dumbledore@hogwarts.edu",
				"deputy_director": "minerva.mcgonagall@hogwarts.edu",
			}
		).insert(ignore_permissions=True)
		print("Created Institute: Hogwarts")

	# Department
	if not frappe.db.exists("Eduauth Department", "Gryffindor"):
		frappe.get_doc(
			{
				"doctype": "Eduauth Department",
				"name": "Gryffindor",
				"department_name": "House of Gryffindor",
				"parent_institute": "Hogwarts",
				"head": "minerva.mcgonagall@hogwarts.edu",
				"faculty_members": [{"user": "minerva.mcgonagall@hogwarts.edu"}],
				"students": [{"user": "harry.potter@hogwarts.edu"}],
			}
		).insert(ignore_permissions=True)
		print("Created Department: Gryffindor")

	# Committee
	if not frappe.db.exists("Eduauth Committee", "Order_Of_The_Phoenix"):
		frappe.get_doc(
			{
				"doctype": "Eduauth Committee",
				"name": "Order_Of_The_Phoenix",
				"committee_name": "Order of the Phoenix Advisory",
				"chair": "albus.dumbledore@hogwarts.edu",
				"members": [
					{"user": "minerva.mcgonagall@hogwarts.edu"},
					{"user": "severus.snape@hogwarts.edu"},
				],
			}
		).insert(ignore_permissions=True)
		print("Created Committee: Order_Of_The_Phoenix")

	frappe.db.commit()
	print(f"\nDemo setup complete! All demo user passwords are set to: {password}")
