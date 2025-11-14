package array_object_examples

# Working with arrays
users := [
	{"name": "alice", "role": "admin", "active": true},
	{"name": "bob", "role": "user", "active": true},
	{"name": "charlie", "role": "user", "active": false},
]

# Array comprehensions
active_users := [user | user := users[_]; user.active == true]
admin_users := [user | user := users[_]; user.role == "admin"]
user_names := [name | name := users[_].name]

# Object comprehensions
user_by_name := {user.name: user | user := users[_]}
active_user_names := {user.name: user.role | user := users[_]; user.active == true}

# Set comprehensions
unique_roles := {role | role := users[_].role}
active_user_set := {user.name | user := users[_]; user.active == true}

# Rules using arrays and objects
allow if {
	# Check if user exists in our user list
	user := users[_]
	user.name == input.user
	user.active == true
}

allow if {
	# Check if user has required role
	user := users[_]
	user.name == input.user
	user.role in input.required_roles
}

# Find user by name
find_user[user] if {
	user := users[_]
	user.name == input.user
}

# Check permissions
has_permission if {
	user := find_user[_]
	user.role == "admin"
}

has_permission if {
	user := find_user[_]
	user.role == "user"
	input.action in ["read", "write"]
}

# Complex array operations
count_active_users := count([user | user := users[_]; user.active == true])
count_admins := count([user | user := users[_]; user.role == "admin"])

# Check if all users are active
all_users_active if {
	count(users) == count_active_users
}

# Check if any user is admin
has_admin if {
	users[_].role == "admin"
}

# Nested object access
resource_permissions := {
	"doc1": {"read": ["alice", "bob"], "write": ["alice"]},
	"doc2": {"read": ["alice", "charlie"], "write": ["alice"]},
}

can_access_resource if {
	permissions := resource_permissions[input.resource]
	input.user in permissions[input.action]
}

# Working with complex nested structures
departments := {
	"engineering": {
		"budget": 1000000,
		"employees": ["alice", "bob"],
		"projects": ["project1", "project2"],
	},
	"marketing": {
		"budget": 500000,
		"employees": ["charlie"],
		"projects": ["campaign1"],
	},
}

can_access_department if {
	dept := departments[input.department]
	input.user in dept.employees
}

department_budget[dept] := budget if {
	dept := input.department
	budget := departments[dept].budget
}
