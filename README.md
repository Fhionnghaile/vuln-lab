# Derry-Vuln-Lab + pentest report

<!-- at-a-glance -->
> **Six classic web flaws shown broken and fixed, with the professional report to match.**  
> **Result:** 7 tests — each exploit works on the vulnerable build and is blocked on the fixed build; the CVSS v4.0 report renders to PDF.  
> **Reproduce:** `pytest -q`  
> ![CI](https://github.com/fhionnghaile/vuln-lab/actions/workflows/ci.yml/badge.svg)
>
> **What this is worth:** Proves you can both find the flaw and communicate it in the artifact an auditor or client expects.


A deliberately vulnerable app with planted **OWASP Top-10:2025** flaws, a professional **pentest
report** (CVSS v4.0), and a remediation that closes every finding.

> **Safety:** only minimal, lab-specific proofs-of-concept live here - each hard-wired to this app's
> own routes and seed data. No scanners, payload generators, or post-exploitation tooling.

## Run
```bash
docker compose up            # vulnerable app on :5000
pip install -r app/requirements.txt && pytest -q   # PoC per flaw: exploit on vuln, blocked on fixed
```

## The flaws (and the differentiator: the report)
SQLi auth-bypass - IDOR - reflected XSS - SSRF - unverified JWT - MD5 password hashing. Each is
demonstrated, rated with a valid **CVSS v4.0** vector, and remediated. The real deliverable is
[`report/report.md`](report/report.md) (rendered to `report/report.pdf`): exec summary, scope,
methodology, evidence, business impact, remediation, and a status appendix.

The same test suite that **exploits** `main` **fails to exploit** the fixed app (`secure=True` /
the `fixed` branch) - remediation proven, not claimed.

## License
MIT (lab + report).

## Key decisions

- One app, two builds (vulnerable/secure), so exploit and fix are tested together.
- Real OWASP 2025 classes (SQLi, IDOR, XSS, SSRF, JWT, weak hashing), not toy bugs.
- Machine-linted CVSS v4.0 vectors, so the report is defensible.

## Scope & limits

- A teaching/demonstration app, not a pentest of a real production system.

