app_name = "eduauth_frappe"
app_title = "Eduauth Frappe"
app_publisher = "Castlecraft Ecommerce Pvt. Ltd."
app_description = "Topaz Frappe used for Education Institute"
app_email = "support@castlecraft.in"
app_license = "apache-2.0"

# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "eduauth_frappe",
# 		"logo": "/assets/eduauth_frappe/logo.png",
# 		"title": "Eduauth Frappe",
# 		"route": "/eduauth_frappe",
# 		"has_permission": "eduauth_frappe.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/eduauth_frappe/css/eduauth_frappe.css"
# app_include_js = "/assets/eduauth_frappe/js/eduauth_frappe.js"

# include js, css files in header of web template
# web_include_css = "/assets/eduauth_frappe/css/eduauth_frappe.css"
# web_include_js = "/assets/eduauth_frappe/js/eduauth_frappe.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "eduauth_frappe/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "eduauth_frappe/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# automatically load and sync documents of this doctype from downstream apps
# importable_doctypes = [doctype_1]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "eduauth_frappe.utils.jinja_methods",
# 	"filters": "eduauth_frappe.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "eduauth_frappe.install.before_install"
# after_install = "eduauth_frappe.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "eduauth_frappe.uninstall.before_uninstall"
# after_uninstall = "eduauth_frappe.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "eduauth_frappe.utils.before_app_install"
# after_app_install = "eduauth_frappe.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "eduauth_frappe.utils.before_app_uninstall"
# after_app_uninstall = "eduauth_frappe.utils.after_app_uninstall"

# Build
# ------------------
# To hook into the build process

# after_build = "eduauth_frappe.build.after_build"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "eduauth_frappe.notifications.get_notification_config"

# Awesome Bar
# -----------
# Extra search results: list of dicts with label, description, route, index.
# route: ["List", "ToDo"], "/desk/docs/some/page", or "https://example.com"
# awesomebar_search = ["eduauth_frappe.search.awesomebar_results"]

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"eduauth_frappe.tasks.all"
# 	],
# 	"daily": [
# 		"eduauth_frappe.tasks.daily"
# 	],
# 	"hourly": [
# 		"eduauth_frappe.tasks.hourly"
# 	],
# 	"weekly": [
# 		"eduauth_frappe.tasks.weekly"
# 	],
# 	"monthly": [
# 		"eduauth_frappe.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "eduauth_frappe.install.before_tests"

# Extend DocType Class
# ------------------------------
#
# Specify custom mixins to extend the standard doctype controller.
# extend_doctype_class = {
# 	"Task": "eduauth_frappe.custom.task.CustomTaskMixin"
# }

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "eduauth_frappe.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "eduauth_frappe.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["eduauth_frappe.utils.before_request"]
# after_request = ["eduauth_frappe.utils.after_request"]

# Job Events
# ----------
# before_job = ["eduauth_frappe.utils.before_job"]
# after_job = ["eduauth_frappe.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"eduauth_frappe.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

# Translation
# ------------
# List of apps whose translatable strings should be excluded from this app's translations.
# ignore_translatable_strings_from = []

# Topaz Registry Mapping
# ----------------------
topaz_registry = {
	"Eduauth Institute": {
		"object": {"type": "institution", "id_field": "name"},
		"relations": [
			{"kind": "link", "relation": "director", "target_type": "user", "field": "director"},
			{
				"kind": "link",
				"relation": "deputy_director",
				"target_type": "user",
				"field": "deputy_director",
			},
			{"kind": "link", "relation": "dean_rnd", "target_type": "user", "field": "dean_rnd"},
			{"kind": "link", "relation": "dean_ap", "target_type": "user", "field": "dean_ap"},
			{"kind": "link", "relation": "dean_admin", "target_type": "user", "field": "dean_admin"},
			{"kind": "link", "relation": "registrar", "target_type": "user", "field": "registrar"},
		],
	},
	"Eduauth Department": {
		"object": {"type": "department", "id_field": "name"},
		"relations": [
			{
				"kind": "link",
				"relation": "parent_institute",
				"target_type": "institution",
				"field": "parent_institute",
			},
			{"kind": "link", "relation": "head", "target_type": "user", "field": "head"},
			{"kind": "link", "relation": "acting_head", "target_type": "user", "field": "acting_head"},
			{
				"kind": "link",
				"relation": "store_keeper",
				"target_type": "role",
				"field": "store_keeper_role",
				"subject_relation": "assignee",
			},
			{
				"kind": "child",
				"table": "faculty_members",
				"subject_field": "user",
				"static_relation": "faculty",
			},
			{"kind": "child", "table": "students", "subject_field": "user", "static_relation": "student"},
			{"kind": "child", "table": "staff_members", "subject_field": "user", "static_relation": "staff"},
			{"kind": "child", "table": "candidates", "subject_field": "user", "static_relation": "candidate"},
		],
		"permissions": {
			"read": "is_member",
			"write": "lead",
		},
	},
	"Eduauth Committee": {
		"object": {"type": "committee", "id_field": "name"},
		"relations": [
			{"kind": "link", "relation": "chair", "target_type": "user", "field": "chair"},
			{"kind": "child", "table": "members", "subject_field": "user", "static_relation": "member"},
			{
				"kind": "child",
				"table": "external_experts",
				"subject_field": "user",
				"static_relation": "external_expert",
			},
		],
		"permissions": {
			# Array/list of Topaz relations: user with either relation gets read access
			"read": ["is_member", "can_access"],
			"write": "can_sign",
		},
	},
	"Eduauth Project": {
		"object": {"type": "project", "id_field": "name"},
		"relations": [
			{
				"kind": "link",
				"relation": "host_department",
				"target_type": "department",
				"field": "host_department",
			},
			{
				"kind": "link",
				"relation": "lead_investigator",
				"target_type": "user",
				"field": "lead_investigator",
			},
			{
				"kind": "link",
				"relation": "co_investigator",
				"target_type": "user",
				"field": "co_investigator",
			},
			{
				"kind": "link",
				"relation": "research_fellow",
				"target_type": "user",
				"field": "research_fellow",
			},
			{
				"kind": "link",
				"relation": "delegate_signatory",
				"target_type": "user",
				"field": "delegate_signatory",
			},
		],
	},
	"Eduauth Group": {
		"object": {"type": "group", "id_field": "name"},
		"relations": [
			{"kind": "child", "table": "members", "subject_field": "user", "static_relation": "member"},
		],
	},
	"Eduauth Role": {
		"object": {"type": "role", "id_field": "name"},
		"relations": [
			{"kind": "child", "table": "assignees", "subject_field": "user", "static_relation": "assignee"},
		],
	},
	"Eduauth Identity": {
		"object": {"type": "identity", "id_field": "name"},
		"relations": [
			{"kind": "link", "relation": "identifier", "target_type": "user", "field": "user"},
		],
	},
	"User": {
		"object": {"type": "user", "id_field": "name"},
		"relations": [],
	},
}
