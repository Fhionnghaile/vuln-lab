# Derry-Vuln-Lab + pentest report — manual

*One page, eight blocks. Every figure here comes from this repository's own tests and README.*

## 1. Claim
Six OWASP Top 10:2025 flaws each have an exploit that works on the vulnerable build and is blocked on the fixed build, written up in a CVSS v4.0 report.

## 2. What it is
A deliberately vulnerable web app, a professional penetration-test report on it, and a fixed version. The same tests that break the vulnerable app fail against the fixed one, which proves the fixes work.

## 3. Demo
The report itself: `report/report.md` (rendered to `report/report.pdf`). Capture to record: the test run.

## 4. Run it yourself
**Prerequisites:** Docker and Python 3.

```bash
docker compose up
pip install -r app/requirements.txt && pytest -q
```

## 5. What you will see
7 tests pass: each exploit succeeds on the vulnerable build and is blocked on the fixed one. The report renders.

## 6. 30-second talking point
> Finding a flaw is half the job. The other half is the report an auditor or client can act on. This lab does both and proves the remediation with the same tests that proved the flaws.

## 7. Scope and limits
- A teaching and demonstration app, not a test of a real production system.
- Proofs of concept are hard-wired to this app's own routes and seed data. No general-purpose tooling ships.

## 8. Links
[Repository](https://github.com/fhionnghaile/vuln-lab) · [Write-up](https://padraigfhionnghaile.com/work/vuln-lab/) · [README](README.md)
