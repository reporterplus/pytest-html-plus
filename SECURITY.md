# Security Policy

## Supported Versions

As a stable release, we provide security fixes for the **latest release only**.

| Version | Supported |
|---------|-----------|
| Latest  | ✅        |
| Older   | ❌        |

## Reporting a Vulnerability

**Please do not open a public GitHub issue for security vulnerabilities.**

Report vulnerabilities privately using GitHub's built-in vulnerability reporting:

👉 [Report a vulnerability](https://github.com/reporterplus/pytest-html-plus/security/advisories/new)

This keeps the disclosure private until a fix is released.

### What to include

To help us resolve the issue as quickly as possible, please provide:

- A clear description of the vulnerability
- Steps to reproduce the issue
- The affected version(s)
- Potential impact or attack scenario

## Response Timeline

| Stage | Target |
|-------|--------|
| Acknowledgement | Within 48 hours |
| Status update | Within 7 days |
| Fix release | Within 14 days where possible |

## Scope

Given the nature of a pytest reporting plugin, the realistic attack surface includes:

- Path traversal in report output paths
- HTML injection in generated reports
- Unsafe handling of test data or metadata in reports

Issues in upstream dependencies (`pytest`, `playwright`, `selenium`, etc.) should be reported directly to those projects.

## Disclosure Policy

Once a fix is released, we will publish a GitHub Security Advisory detailing the vulnerability, its impact, and the fix. We credit reporters by name unless they prefer to remain anonymous.
