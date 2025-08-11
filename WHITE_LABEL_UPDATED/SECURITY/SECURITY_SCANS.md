# 🔍 Security Scans

Dependencies
```bash
# Python
pip install safety
safety check --full-report | cat

# Node
npm audit --production | cat
```

DAST
- OWASP ZAP baseline scan against staging

SAST
- Enable CodeQL/Semgrep in CI

Secrets
- git-secrets / trufflehog pre-commit checks
