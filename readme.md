# MyNotes

A comprehensive collection of cybersecurity, development, and system administration knowledge compiled from various courses, certifications, books, and hands-on experience. This repository serves as both a personal knowledge base and a resource for the security community.

## 📖 About This Repository

This repository is organized as a GitBook-compatible knowledge base with properly structured markdown files. Each topic is carefully documented with practical examples, commands, techniques, and references.

**What you'll find here:**
- Detailed penetration testing methodologies and techniques
- Step-by-step guides for various attack vectors and defenses
- Command references and cheatsheets
- Programming guides and best practices
- Infrastructure and DevOps knowledge

## 🗺️ Navigation Guide

### 🔐 Security & Penetration Testing

#### **[Active Directory](notes/active-directory/)**
Complete guide to Active Directory security, covering enumeration, privilege escalation, lateral movement, persistence, and defensive measures.

**Key Topics:** Domain Enumeration • Local/Domain PrivEsc • Lateral Movement • Persistence • Kerberos Attacks • Certificate Services • Detection & Defense

#### **[Web Pentesting](notes/web-pentesting/)**
Comprehensive web application security testing guide covering modern vulnerabilities and attack techniques.

**Key Topics:** SQL Injection • XSS • CSRF • SSRF • SSTI • Authentication/Authorization Testing • JWT • API Security

#### **[Red Teaming](notes/red-teaming/)**
Advanced offensive security operations including credential harvesting, tunneling, and automation techniques.

**Key Topics:** Credential Harvesting (Windows/Linux/macOS) • Network Tunneling • Post-Exploitation

#### **[AWS Pentesting](notes/aws-pentesting/)**
Cloud security testing focused on Amazon Web Services infrastructure and services.

**Key Topics:** Cloud Enumeration • IAM Exploitation • S3 Security • Service-Specific Attacks

#### **[Metasploit](notes/metasploit/)**
Comprehensive exploitation framework guide with commands, modules, and practical usage examples.

### 💻 Development & Operations

#### **[DevOps](notes/devops/)**
Modern DevOps practices including container orchestration, CI/CD, and infrastructure as code.

**Key Topics:** Kubernetes Security • GitHub Actions • Terraform • Ansible • Container Security • Monitoring • OPA/Rego

#### **[Golang](notes/golang/)**
Go programming language guide from fundamentals to advanced concepts like concurrency and channels.

**Key Topics:** Variables & Types • Control Flow • Functions • Concurrency • Channels • Best Practices

### 🔧 Reverse Engineering

#### **[Reverse Engineering](notes/reverse-engineering/)**
Binary analysis, debugging techniques, and reverse engineering fundamentals.

**Key Topics:** Binary Analysis • GDB Debugging • Assembly • Exploitation Development

---

## 🚀 Quick Start

---

## 🚀 Quick Start

### Browse Online
This repository is published as a GitBook. Navigate through the topics using the sidebar on [the GitBook site](https://github.com/zAbuQasem/MyNotes) or browse directly on GitHub.

### Local Reading

**Option 1: GitHub/Web Browser**
Simply browse the `notes/` directory on GitHub. Each section has a README with organized navigation.

**Option 2: Using Obsidian** (Recommended for local use)

Obsidian provides a rich markdown editing and viewing experience with graph views and backlinks:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/zAbuQasem/MyNotes.git
   cd MyNotes
   ```

2. **Install Obsidian**:
   Download from the [official website](https://obsidian.md/) if you haven't already.

3. **Open as Vault**:
   - Launch Obsidian
   - Click "Open folder as vault"
   - Select the `notes/` directory from this repository

4. **Start Exploring**:
   Use the file explorer, search, or graph view to navigate the knowledge base.

## 📚 Repository Structure

```
MyNotes/
├── notes/                          # Main content directory
│   ├── active-directory/          # AD security and pentesting
│   ├── web-pentesting/            # Web application security
│   ├── red-teaming/               # Red team operations
│   ├── aws-pentesting/            # Cloud security (AWS)
│   ├── metasploit/                # Metasploit framework
│   ├── devops/                    # DevOps and infrastructure
│   ├── golang/                    # Go programming
│   └── reverse-engineering/       # Binary analysis
├── scripts/                        # Utility scripts
└── readme.md                       # This file
```

## 🎯 How to Use These Notes

- **For Learning**: Start with a topic's README file for an overview, then dive into specific subtopics
- **As Reference**: Use the search function (GitHub or Obsidian) to find specific commands or techniques
- **For Certifications**: Many notes are structured around certification exam objectives (CRTP, OSCP, CKA, etc.)
- **In Practice**: Copy and adapt commands for real-world engagements (ensure you have proper authorization)

## 📝 Note Format

Each note typically includes:
- Clear headings and table of contents
- Practical examples and command syntax
- Step-by-step procedures
- References and further reading
- Detection/defense considerations where applicable

## 🤝 Contributing

While these are personal notes, I welcome:
- **Issues**: Report broken links, errors, or outdated information
- **Suggestions**: Recommend improvements or additional topics
- **Pull Requests**: Fix typos, improve clarity, or add missing details

Feel free to fork this repository and customize it for your own learning journey!

## ⚖️ Disclaimer

These notes are for **educational and authorized security testing purposes only**. Always:
- Obtain proper written authorization before testing
- Respect scope limitations and rules of engagement
- Follow responsible disclosure practices
- Comply with applicable laws and regulations

Unauthorized access to computer systems is illegal.

## 📄 License

This repository is shared for educational purposes. Please use responsibly and give credit when using or sharing these materials.

---

**Happy Learning! 🚀**

*Last Updated: 2025*