# Understanding OPA Eval Results

## What is `opa eval`?

`opa eval` is the command-line tool to evaluate Rego policies and queries. It takes your policy files, optional input data, and a query, then returns the evaluation result.

## Basic Command Structure

```bash
opa eval [flags] <query>

# Common flags:
# -d, --data <file>     Load policy or data from file
# -i, --input <file>    Load input document from file
# --format <format>     Set output format (default: json)
```

## Types of Results

### 1. Boolean Results (true/false)

When you query a rule that returns a boolean:

```bash
opa eval -d 01-simple-policy.rego -i input1.json "data.simple_policy.allow"
```

**Possible outputs:**

#### ✅ True Result
```json
{
  "result": [
    {
      "expressions": [
        {
          "value": true,
          "text": "data.simple_policy.allow",
          "location": {
            "row": 1,
            "col": 1
          }
        }
      ]
    }
  ]
}
```
**Meaning**: The policy allows the action (rule evaluated to `true`)

#### ❌ False/Undefined Result
```json
{
  "result": [
    {
      "expressions": [
        {
          "value": false,
          "text": "data.simple_policy.allow",
          "location": {
            "row": 1,
            "col": 1
          }
        }
      ]
    }
  ]
}
```
**Meaning**: The policy denies the action (rule evaluated to `false` or `undefined`)

### 2. String/Value Results

When you query a rule that returns a specific value:

```bash
opa eval -d 02-rbac-policy.rego -i rbac-input.json "data.rbac_policy.user_role"
```

**Output:**
```json
{
  "result": [
    {
      "expressions": [
        {
          "value": "admin",
          "text": "data.rbac_policy.user_role",
          "location": {
            "row": 1,
            "col": 1
          }
        }
      ]
    }
  ]
}
```
**Meaning**: The user's role is "admin"

### 3. Array/Set Results

When you query a rule that returns multiple values:

```bash
opa eval -d 02-rbac-policy.rego -i rbac-input.json "data.rbac_policy.violation"
```

**Output (when there are violations):**
```json
{
  "result": [
    {
      "expressions": [
        {
          "value": [
            "Access denied for user john to read resource doc123",
            "Access denied: Outside business hours"
          ],
          "text": "data.rbac_policy.violation",
          "location": {
            "row": 1,
            "col": 1
          }
        }
      ]
    }
  ]
}
```

**Output (when no violations):**
```json
{
  "result": [
    {
      "expressions": [
        {
          "value": [],
          "text": "data.rbac_policy.violation",
          "location": {
            "row": 1,
            "col": 1
          }
        }
      ]
    }
  ]
}
```

### 4. Object Results

When you query for complete data structures:

```bash
opa eval -d 02-rbac-policy.rego -i rbac-input.json "data.rbac_policy"
```

**Output:**
```json
{
  "result": [
    {
      "expressions": [
        {
          "value": {
            "allow": false,
            "user_role": "guest",
            "violation": [
              "Access denied for user john to read resource doc123"
            ]
          },
          "text": "data.rbac_policy",
          "location": {
            "row": 1,
            "col": 1
          }
        }
      ]
    }
  ]
}
```

## Understanding the JSON Structure

### Main Components:

```json
{
  "result": [              // Array of results (usually one item)
    {
      "expressions": [      // Array of evaluated expressions
        {
          "value": true,    // The actual result value
          "text": "query",  // The query that was evaluated
          "location": {     // Where the query was in your command
            "row": 1,
            "col": 1
          }
        }
      ]
    }
  ]
}
```

## Simplified Output Formats

### Raw Format (just the value)
```bash
opa eval -d policy.rego --format raw "data.example.allow"
```
**Output:** `true` or `false` (just the value, no JSON wrapper)

### Pretty Format (formatted JSON)
```bash
opa eval -d policy.rego --format pretty "data.example.allow"
```
**Output:** Pretty-printed JSON with indentation

## Common Query Patterns

### 1. Check Single Rule
```bash
# Query: Does the policy allow this action?
opa eval -d policy.rego -i input.json "data.package_name.allow"
```

### 2. Get All Rules from Package
```bash
# Query: Show me all evaluated rules
opa eval -d policy.rego -i input.json "data.package_name"
```

### 3. Check Specific Value
```bash
# Query: What role does this user have?
opa eval -d policy.rego -i input.json "data.package_name.user_role"
```

### 4. Get Violation Messages
```bash
# Query: Why was access denied?
opa eval -d policy.rego -i input.json "data.package_name.violation"
```

## Practical Examples with Your Policies

### Example 1: Testing Simple Policy
```bash
# Test if admin user is allowed
opa eval -d 01-simple-policy.rego -i input1.json "data.simple_policy.allow"

# Expected result for admin: {"result": [{"expressions": [{"value": true, ...}]}]}
# Expected result for regular user: {"result": [{"expressions": [{"value": false, ...}]}]}
```

### Example 2: Testing RBAC Policy
```bash
# Check user role
opa eval -d 02-rbac-policy.rego -i rbac-input.json "data.rbac_policy.user_role"

# Check if allowed
opa eval -d 02-rbac-policy.rego -i rbac-input.json "data.rbac_policy.allow"

# Get violation messages
opa eval -d 02-rbac-policy.rego -i rbac-input.json "data.rbac_policy.violation"

# Get everything
opa eval -d 02-rbac-policy.rego -i rbac-input.json "data.rbac_policy"
```

## Debugging Tips

### 1. Use Raw Format for Quick Checks
```bash
opa eval -d policy.rego -i input.json --format raw "data.example.allow"
# Output: just "true" or "false"
```

### 2. Query Intermediate Values
```bash
# Debug: What role was assigned?
opa eval -d policy.rego -i input.json "data.example.user_role"

# Debug: What are the business hours?
opa eval -d policy.rego -i input.json "data.example.is_business_hours"
```

### 3. Query Input Data
```bash
# See what input was loaded
opa eval -i input.json "input"

# Check specific input fields
opa eval -i input.json "input.user.name"
```

## Error Cases

### Policy File Not Found
```bash
opa eval -d nonexistent.rego "data.example.allow"
```
**Output:** Error message about file not found

### Query Path Doesn't Exist
```bash
opa eval -d policy.rego "data.nonexistent.rule"
```
**Output:** `undefined` result or empty result set

### Syntax Error in Policy
**Output:** Compilation error with line numbers and descriptions

## Quick Reference

| Query Type | Command | Expected Result |
|------------|---------|-----------------|
| Boolean rule | `"data.pkg.allow"` | `true`/`false` |
| String value | `"data.pkg.user_role"` | `"admin"` |
| Array/Set | `"data.pkg.violations"` | `[...]` |
| All rules | `"data.pkg"` | `{...}` |
| Input data | `"input"` | `{...}` |

## Understanding Common Results

### ✅ Access Allowed
```json
{"result": [{"expressions": [{"value": true, ...}]}]}
```

### ❌ Access Denied
```json
{"result": [{"expressions": [{"value": false, ...}]}]}
```

### 🔍 Getting Details
```bash
# Get the user role
opa eval -d policy.rego -i input.json "data.pkg.user_role"

# Get violation reasons
opa eval -d policy.rego -i input.json "data.pkg.violation"

# Get all policy results
opa eval -d policy.rego -i input.json "data.pkg"
```

### 🐛 Debugging Undefined Results
If you get `undefined` or empty results:
1. Check if the package name matches your query
2. Verify the rule name exists
3. Ensure the rule conditions can be satisfied
4. Check if there are syntax errors in your policy

## Practice Commands

Try these commands with your existing policies:

```bash
# Test your simple policy
opa eval -d 01-simple-policy.rego -i input1.json "data.simple_policy.allow"

# Test your RBAC policy  
opa eval -d 02-rbac-policy.rego -i rbac-input.json "data.rbac_policy"

# Get just the user role
opa eval -d 02-rbac-policy.rego -i rbac-input.json --format raw "data.rbac_policy.user_role"

# Debug: Check what input was loaded
opa eval -i rbac-input.json "input"

# Debug: Check if business hours rule works
opa eval -d 02-rbac-policy.rego "data.rbac_policy.is_business_hours"
```

## Remember

- In Rego, `false` and `undefined` are treated the same way - both mean "not allowed" or "rule doesn't apply"
- Use `--format raw` for simple true/false results
- Use `--format pretty` for readable JSON output
- Query intermediate values for debugging
- Always check your package names and rule names match your queries
