# Derry-Vuln-Lab — Penetration Test Report

**Client:** Derry Training (lab) · **Engagement:** Grey-box web application assessment
**Date:** 2026-11-14 · **Tester:** P · **Classification:** Public (lab)

## 1. Executive summary
Testing identified **six findings** — two **Critical**, three **High**, one **Medium**. An
unauthenticated attacker can bypass authentication (SQL injection), read any user's PII (IDOR), reach
the cloud metadata endpoint (SSRF), and reach the admin area with a forged token (JWT verification
disabled). All findings were remediated on the `fixed` branch and re-tested closed.

## 2. Scope & methodology
In scope: the lab web app and its six routes. Methodology followed OSCP/PTES phases mapped to
**OWASP Top 10:2025**. Risk is rated with **CVSS v4.0** (FIRST).

## 3. Findings

### 3.1 SQL injection → authentication bypass — Critical
- CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N
- **Evidence:** `POST /login {"username":"admin' -- ","password":"x"}` returns `{"ok":true,"role":"admin"}`.
- **Impact:** full authentication bypass as any user, including admin.
- **Remediation:** parameterised queries; never concatenate SQL.

### 3.2 Unverified JWT → admin access — Critical
- CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N
- **Evidence:** a token signed with an attacker key is accepted by `/admin`.
- **Remediation:** verify signature; pin `algorithms=["HS256"]`; reject `alg:none`.

### 3.3 IDOR → PII disclosure — High
- CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N
- **Evidence:** `GET /api/user/3` as user 1 returns admin's SSN.
- **Remediation:** enforce object-level authorisation.

### 3.4 SSRF → cloud metadata — High
- CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:L/VA:N/SC:L/SI:N/SA:N
- **Evidence:** `GET /fetch?url=http://169.254.169.254/...` is accepted.
- **Remediation:** allowlist hosts; block link-local/private ranges.

### 3.5 Reflected XSS — High
- CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:L/VI:L/VA:N/SC:L/SI:L/SA:N
- **Evidence:** `/greet?name=<script>alert(1)</script>` reflects unescaped.
- **Remediation:** context-aware output encoding; strict CSP in depth.

### 3.6 MD5 password hashing — Medium
- CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N
- **Evidence:** `/register` stores unsalted `md5(password)`.
- **Remediation:** bcrypt/argon2 with per-password salt.

## 4. Remediation status
| # | finding | severity | status |
|---|---|---|---|
| 3.1 | SQLi auth bypass | Critical | Fixed |
| 3.2 | Unverified JWT | Critical | Fixed |
| 3.3 | IDOR | High | Fixed |
| 3.4 | SSRF | High | Fixed |
| 3.5 | Reflected XSS | High | Fixed |
| 3.6 | MD5 hashing | Medium | Fixed |

All six re-tested: exploit requests return 401/403/sanitised on the remediated app.
