package simple_policy

# Default rule - deny by default
default allow := false

# Allow if user is admin
allow if {
	input.user == "admin"
}

# Allow if user is owner of the resource
allow if {
	input.user == input.resource.owner
}

# Allow read access to public resources
allow if {
	input.action == "read"
	input.resource.public == true
}

# Helper rule to check if user is authenticated
is_authenticated if {
	input.user != ""
	input.user != null
}

# Rule with multiple conditions
allow if {
	is_authenticated
	input.action == "read"
	input.resource.type == "document"
}
