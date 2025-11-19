# Security Policy

## Supported Versions

We release security updates for the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

We take security vulnerabilities seriously. If you discover a security issue in GitSage, please report it responsibly.

### How to Report

**Please do NOT create a public GitHub issue for security vulnerabilities.**

Instead, please report security issues via:

1. **Preferred**: Open a [security advisory](https://github.com/shadowdevnotreal/gitsage/security/advisories/new)
2. **Alternative**: Email the maintainers directly (check repository for contact info)

### What to Include

Please include as much information as possible:

- **Description** of the vulnerability
- **Steps to reproduce** the issue
- **Potential impact** of the vulnerability
- **Suggested fix** (if you have one)
- **Your contact information** for follow-up

### What to Expect

- **Acknowledgment**: We'll acknowledge receipt within 48 hours
- **Assessment**: We'll assess the vulnerability within 7 days
- **Updates**: We'll keep you informed of progress
- **Credit**: We'll credit you in the security advisory (unless you prefer to remain anonymous)
- **Fix Timeline**: We aim to release fixes within 30 days for critical issues

## Security Best Practices

When using GitSage, please follow these security best practices:

### Repository Deletion
- **Verify** which repository you're deleting before confirming
- **Backup** important data before deletion operations
- **Understand** that deletion is permanent and irreversible
- **Test** on non-critical repositories first

### GitHub CLI Authentication
- **Use** GitHub's official authentication methods (`gh auth login`)
- **Never** share your authentication tokens
- **Revoke** old tokens when no longer needed
- **Use** fine-grained personal access tokens when possible

### Git Operations
- **Review** all changes before force pushing
- **Understand** that history resets are irreversible
- **Backup** repositories before history operations
- **Verify** remote URLs before pushing

### Script Execution
- **Review** scripts before running them
- **Understand** what permissions scripts require
- **Run** in a safe environment (not on production servers)
- **Keep** GitSage updated to the latest version

## Known Security Considerations

### Repository Deletion
- **Permanent**: Deleted repositories cannot be recovered
- **Immediate**: Deletion happens immediately upon confirmation
- **Irreversible**: No undo or rollback capability

### Git History Reset
- **Data Loss**: All commit history is permanently deleted
- **Force Push**: Requires force push to update remote
- **Team Impact**: Affects all users of the repository

### GitHub CLI Permissions
- GitSage requires GitHub CLI to be authenticated
- GitHub CLI has access to all your repositories
- Ensure `gh` is properly secured on your system

## Scope

This security policy applies to:

- ✅ GitSage core scripts (Bash and Python)
- ✅ Wiki generator components
- ✅ Cross-platform launcher
- ✅ Git reset utilities

Out of scope:
- ❌ Third-party dependencies (report to their maintainers)
- ❌ GitHub CLI itself (report to GitHub)
- ❌ Git itself (report to Git project)
- ❌ User's local environment configuration

## Security Update Process

When security issues are identified:

1. **Fix Development**: Develop and test fix privately
2. **Version Release**: Release new version with fix
3. **Security Advisory**: Publish security advisory
4. **User Notification**: Notify users to update
5. **CVE Assignment**: Request CVE if applicable

## Responsible Disclosure

We believe in coordinated vulnerability disclosure:

- We'll work with you to understand and address the issue
- We won't publicly disclose until a fix is available
- We'll credit researchers who report responsibly
- We ask for reasonable time to fix before public disclosure

## Questions?

If you have questions about this security policy, please open a discussion or contact the maintainers.

---

**Last Updated**: November 19, 2025
**Version**: 1.0.0
