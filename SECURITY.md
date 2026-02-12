# Security Policy

## Supported Versions

| Version | Supported |
| ------- | --------- |
| 0.9.0   | ✅ Yes    |
| < 0.9.0 | ❌ No     |

## Reporting a Vulnerability

**Do NOT create a public issue for security vulnerabilities.**

Instead, send an email to: **bixing_support@chinamobile.com**

### What to Include

1. Description of the vulnerability
2. Potential impact
3. Steps to reproduce
4. Affected versions
5. Proposed fix (if available)

### Response Timeline

- Acknowledgment: Within 48 hours
- Fix: Within 7 days (depending on severity)

### Process

1. You'll receive an acknowledgment
2. We assess the vulnerability
3. We work with you to understand and fix it
4. We develop and test a fix
5. We coordinate public disclosure with you
6. You'll be credited (if desired)

## Security Best Practices

### For Users

- Keep BiXFlow updated to the latest version
- Regularly update dependencies
- Use HTTPS for MCP server connections
- Implement proper authentication for MCP servers
- Use environment variables for sensitive data
- Validate all workflow inputs
- Run with minimal necessary permissions

### MCP Server Security

When deploying MCP servers:

- Implement proper authentication
- Use HTTPS/TLS in production
- Implement rate limiting
- Validate and sanitize all inputs
- Avoid exposing sensitive information in error messages
- Implement proper logging for security auditing
- Use firewalls and network segmentation

### Workflow Security

- Always validate workflow input schemas
- Sanitize data before processing
- Implement proper error handling
- Set appropriate timeouts and resource limits
- Maintain audit logs of workflow executions

## Known Security Considerations

- Workflows execute with the permissions of the MCP servers they call
- Jinja2 templates are used for variable substitution - validate user-provided content
- Be cautious when executing workflows from untrusted sources

## Dependency Security

Regularly check and update dependencies:

```bash
pip check
pip install pip-audit
pip-audit
pip install --upgrade -r requirements.txt
```

## Current Security Features

- Input validation with JSON Schema
- Comprehensive error handling without exposing sensitive data
- Configurable timeouts for MCP server operations
- Full HTTPS support for MCP connections

## Disclosure Policy

We follow responsible disclosure:

1. Report vulnerabilities privately
2. Assess and develop a fix
3. Coordinate public disclosure with you
4. Credit reporters in security advisories

Security advisories will be published via:

- GitHub Security Advisories
- Release notes
- Project changelog

## License

BiXFlow is licensed under the MIT License. This license does not include warranties. Users are responsible for evaluating security and suitability for their use cases.

## Contact

For security questions or concerns:

- **Email**: bixing_support@chinamobile.com
- **Subject**: [SECURITY] BiXFlow Security Inquiry

---

Thank you for helping keep BiXFlow secure! 🛡️
