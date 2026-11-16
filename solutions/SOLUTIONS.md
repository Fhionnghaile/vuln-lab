# Solutions - flaw -> fix

| # | OWASP 2025 | flaw | fix (on the `fixed` branch / `secure=True`) |
|---|---|---|---|
| 1 | A03 Injection | SQLi auth bypass (string-built query) | parameterised query (`?` placeholders) |
| 2 | A01 Broken Access Control | IDOR on `/api/user/<id>` | enforce caller == resource owner -> 403 |
| 3 | A03 Injection | reflected XSS on `/greet` | `html.escape()` the reflected value |
| 4 | A01 Broken Access Control | SSRF on `/fetch` | host allowlist -> 403 on anything else |
| 5 | A07 Auth Failures | JWT accepted unverified | verify signature + pin `algorithms=["HS256"]` |
| 6 | A02 Cryptographic Failures | MD5 password hashing | bcrypt with per-password salt |
