# Rego Basics - Open Policy Agent (OPA)

## Table of Contents
1. [Introduction](#introduction)
2. [Basic Syntax](#basic-syntax)
3. [Data Types](#data-types)
4. [Rules and Queries](#rules-and-queries)
5. [Variables and Unification](#variables-and-unification)
6. [Built-in Functions](#built-in-functions)
7. [Arrays and Objects](#arrays-and-objects)
8. [Iteration and Comprehensions](#iteration-and-comprehensions)
9. [Conditionals](#conditionals)
10. [Practical Examples](#practical-examples)

## Introduction

**Open Policy Agent (OPA)** is an open-source, general-purpose policy engine that enables unified policy enforcement across different services and applications. **Rego** is the high-level declarative language used to write policies in OPA.

### Key Concepts:
- **Declarative**: You describe what you want, not how to achieve it
- **Immutable**: Data cannot be modified once created
- **Query-based**: Policies are evaluated through queries
- **JSON-compatible**: Works seamlessly with JSON data structures

## Basic Syntax

### Package Declaration
Every Rego policy starts with a package declaration:

```rego
package example

## This is a comment
```

### Basic Rules
Rules in Rego have the following structure:

```rego
rule_name if {
## rule body
}

## Or with assignment
rule_name := value if {
## rule body
}
```

## Data Types

### Scalars
```rego
## Boolean
allow := true
deny := false

## String
message := "Hello, World!"
name := "Alice"

## Number
age := 25
pi := 3.14

## Null
empty := null
```

### Collections
```rego
## Array
numbers := [1, 2, 3, 4, 5]
mixed := [1, "hello", true, null]

## Object
person := {
    "name": "John",
    "age": 30,
    "active": true
}

## Set
permissions := {"read", "write", "execute"}
```

## Rules and Queries

### Simple Rules
```rego
package example

## A rule that always evaluates to true
allow if {
    true
}

## A rule with conditions
allow if {
    input.user == "admin"
}

## Multiple conditions (AND)
allow if {
    input.user == "admin"
    input.action == "read"
}

## Rule with assignment
user_type := "admin" if {
    input.user == "root"
}

user_type := "regular" if {
    input.user != "root"
}
```

### Default Values
```rego
## Default rule (fallback)
default allow := false

## This means allow is false unless explicitly set to true
allow if {
    input.user == "admin"
}
```

## Variables and Unification

### Variable Binding
```rego
## Variable binding through unification
user_name := input.user

## Using variables in conditions
allow if {
    user := input.user
    user == "admin"
}
```

### Pattern Matching
```rego
## Array pattern matching
first_item := arr[0] if {
    arr := [1, 2, 3]
}

## Object pattern matching
user_age := person.age if {
    person := {"name": "John", "age": 30}
}
```

## Built-in Functions

### String Functions
```rego
## String operations
starts_with_hello if {
    startswith(input.message, "Hello")
}

contains_world if {
    contains(input.message, "World")
}

## String formatting
greeting := sprintf("Hello, %s!", [input.name])
```

### Array Functions
```rego
## Array length
array_length := count(input.items)

## Check if array contains element
has_admin if {
    "admin" in input.roles
}
```

### Math Functions
```rego
## Mathematical operations
sum := x + y if {
    x := 10
    y := 20
}

## Using built-in math functions
max_value := max(input.numbers)
min_value := min(input.numbers)
```

## Arrays and Objects

### Working with Arrays
```rego
## Access array elements
first_user := input.users[0]

## Iterate over array indices
user_exists if {
    input.users[i].name == "Alice"
}

## Array comprehension
admin_users := [user | user := input.users[_]; user.role == "admin"]
```

### Working with Objects
```rego
## Access object properties
user_name := input.user.name

## Check if key exists
has_email if {
    input.user.email
}

## Object comprehension
user_names := {name | name := input.users[_].name}
```

## Iteration and Comprehensions

### Array Comprehensions
```rego
## Simple array comprehension
numbers := [x | x := input.items[_]; x > 10]

## Complex array comprehension
admin_emails := [email | 
    user := input.users[_]
    user.role == "admin"
    email := user.email
]
```

### Object Comprehensions
```rego
## Create object from array
user_lookup := {user.id: user.name | user := input.users[_]}

## Conditional object comprehension
active_users := {user.id: user | 
    user := input.users[_]
    user.active == true
}
```

### Set Comprehensions
```rego
## Create set of unique values
unique_roles := {role | role := input.users[_].role}

## Filtered set
admin_names := {name | 
    user := input.users[_]
    user.role == "admin"
    name := user.name
}
```

## Conditionals

### Basic Conditionals
```rego
## Simple condition
allow if {
    input.user == "admin"
}

## Multiple conditions (AND)
allow if {
    input.user == "admin"
    input.action == "read"
}

## OR conditions (separate rules)
allow if {
    input.user == "admin"
}

allow if {
    input.user == "owner"
    input.resource.owner == input.user
}
```

### Negation
```rego
## Using not
deny if {
    not allow
}

## Checking non-existence
no_admin if {
    not input.users[_].role == "admin"
}
```

## Practical Examples

### Example 1: User Authorization
```rego
package authz

## Default deny
default allow := false

## Allow admins to do anything
allow if {
    input.user.role == "admin"
}

## Allow users to read their own data
allow if {
    input.action == "read"
    input.user.id == input.resource.owner
}

## Allow users to write their own data
allow if {
    input.action == "write"
    input.user.id == input.resource.owner
    input.user.active == true
}
```

### Example 2: Resource Access Control
```rego
package resources

## Default values
default allow := false
default reason := "Access denied"

## Allow access to public resources
allow if {
    input.resource.public == true
}

## Allow access to resources owned by user
allow if {
    input.resource.owner == input.user.id
}

## Allow access based on permissions
allow if {
    permission := input.user.permissions[_]
    permission.resource == input.resource.id
    permission.action == input.action
}

## Provide reason for denial
reason := "Resource is private" if {
    input.resource.public == false
    input.resource.owner != input.user.id
}

reason := "Insufficient permissions" if {
    input.resource.public == false
    input.resource.owner != input.user.id
    not user_has_permission
}

user_has_permission if {
    permission := input.user.permissions[_]
    permission.resource == input.resource.id
    permission.action == input.action
}
```

### Example 3: Time-based Access
```rego
package time_based

import future.keywords.in

## Allow access during business hours
allow if {
    current_hour := time.now_ns() / 1000000000 / 3600 % 24
    current_hour >= 9
    current_hour <= 17
}

## Allow access on weekdays
allow if {
    weekday := time.weekday(time.now_ns())
    weekday in [1, 2, 3, 4, 5]  # Monday to Friday
}

## Emergency access
allow if {
    input.emergency == true
    input.user.role in ["admin", "operator"]
}
```

Remember: Rego is all about expressing policies declaratively. Focus on describing the conditions under which something should be allowed or denied, rather than the step-by-step process to determine it.