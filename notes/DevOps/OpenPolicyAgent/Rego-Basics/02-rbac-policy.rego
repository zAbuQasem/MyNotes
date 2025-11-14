package rbac_policy

# Default values
default allow := false

default user_role := "guest"

# Define user roles based on input
user_role := "admin" if {
	input.user.name in ["admin", "root", "superuser"]
}

user_role := "manager" if {
	input.user.department == "management"
	input.user.level >= 5
}

user_role := "employee" if {
	input.user.department != ""
	input.user.level > 0
}

# Permission rules based on roles
allow if {
	user_role == "admin"
	# Admins can do anything
}

allow if {
	user_role == "manager"
	input.action in ["read", "write", "delete"]
	input.resource.department == input.user.department
}

allow if {
	user_role == "employee"
	input.action in ["read", "write"]
	input.resource.owner == input.user.id
}

allow if {
	user_role == "employee"
	input.action == "read"
	input.resource.public == true
}

# Helper rules
is_business_hours if {
	hour := ((time.now_ns() / 1000000000) / 3600) % 24
	hour >= 9
	hour <= 17
}

is_weekday if {
	weekday := time.weekday(time.now_ns())
	weekday >= 1 # Monday
	weekday <= 5 # Friday
}

# Time-based restrictions
allow if {
	user_role == "employee"
	input.action == "read"
	is_business_hours
	is_weekday
}

# Violation messages
violation[msg] if {
	not allow
	msg := sprintf("Access denied for user %s to %s resource %s", [
		input.user.name,
		input.action,
		input.resource.id,
	])
}

violation[msg] if {
	not allow
	user_role == "employee"
	not is_business_hours
	msg := "Access denied: Outside business hours"
}

violation[msg] if {
	not allow
	user_role == "employee"
	not is_weekday
	msg := "Access denied: Weekend access not allowed"
}
