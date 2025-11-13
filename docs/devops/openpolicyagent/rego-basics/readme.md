# Learning Path and Examples

## 📚 Learning Materials

- **[Basics.md](./Basics.md)** - Complete theoretical guide to Rego fundamentals
- **[Understanding-OPA-Eval-Results.md](./Understanding-OPA-Eval-Results.md)** - Guide to interpreting `opa eval` command results

## Getting Started

This directory contains practical examples to help you learn Rego step by step:

### 1. Basic Policy (`01-simple-policy.rego`)
- Basic allow/deny rules
- Simple conditions
- Default values
- Helper rules

**Test with:**
```bash
opa eval -d 01-simple-policy.rego -i input1.json "data.simple_policy.allow"
opa eval -d 01-simple-policy.rego -i input2.json "data.simple_policy.allow"
```

### 2. RBAC Policy (`02-rbac-policy.rego`)
- Role-based access control
- Time-based restrictions
- Violation messages
- Complex conditions

**Test with:**
```bash
opa eval -d 02-rbac-policy.rego -i rbac-input.json "data.rbac_policy"
```

### 3. Arrays and Objects (`03-arrays-objects.rego`)
- Array comprehensions
- Object comprehensions
- Set comprehensions
- Complex data structures

**Test with:**
```bash
opa eval -d 03-arrays-objects.rego "data.array_object_examples.active_users"
```

## Practice Exercises

1. **Modify the simple policy** to add a new rule for "editor" role
2. **Create a new input file** with different user roles and test the RBAC policy
3. **Experiment with array comprehensions** in the arrays-objects example
4. **Write a new policy** for file system permissions


## Useful OPA Commands

```bash
# Install OPA (if not installed)
curl -L -o opa https://github.com/open-policy-agent/opa/releases/latest/download/opa_linux_amd64
chmod +x opa
sudo mv opa /usr/local/bin/

# Format Rego files
opa fmt --diff *.rego

# Interactive REPL
opa run policy.rego

# Test policies (requires _test.rego files)
opa test .
```

## Next Steps

1. Try the [OPA Playground](https://play.openpolicyagent.org/)
2. Write test files for your policies
3. Explore OPA integration with applications
4. Learn about OPA performance optimization
5. Study real-world policy examples