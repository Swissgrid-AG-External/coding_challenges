# Security Remediation Status and Prioritization

This document summarizes what has been fixed in this branch, prioritized per the assessment instructions in `README.md`.

## Prioritization Approach

- `P0` Critical security controls that reduce immediate compromise risk.
- `P1` High-impact hardening that reduces exploitability and abuse.
- `P2` Medium improvements and operational hygiene.
- `Deferred` Items intentionally out of scope for this branch (to be handled later).

## Completed in This Branch

### P0 Completed

1. Removed secret defaults from function code and required env-based configuration.
   - Related findings: `PY-001`
2. Enforced HTTPS-only access for the Function App in Terraform.
   - Related findings: `TF-001`
3. Removed sensitive Terraform outputs that could expose storage secrets.
   - Related findings: `TF-M1`

### P1 Completed

1. Added API URL validation (absolute URL, no embedded credentials).
   - Related findings: `PY-003`
2. Hardened Azure Storage configuration:
   - Blob container access set to private
   - Nested public access disabled
   - HTTPS-only storage traffic
   - Related findings: `TF-003`, `TF-005`, partially `TF-010`
3. Added managed identity path for blob access and Terraform role assignment for blob write.
   - Related findings: `PY-009`
4. Added CI/CD workflow (`.github/workflows/cicd.yml`) with automated linting, formatting, Terraform validate, Checkov, and Trivy checks on PRs.
   - Related findings: `DEP-001` (partially)

### P2 Completed

1. Added startup/runtime config validation for required settings.
   - Related findings: `PY-005`
2. Reduced secret leakage risk in logs (no API key logging).
   - Related findings: `PY-007`
3. Improved exception handling behavior (generic error logging + re-raise).
   - Related findings: `PY-006`
4. Enabled additional storage hardening controls:
   - Infrastructure encryption enabled
   - Minimum TLS set to `TLS1_2`
   - Shared access key disabled
   - Blob/container soft-delete retention enabled
   - Related findings: `TF-009`, `TF-011`, `TF-014`, `TF-013`
5. Removed legacy `deploy.sh` script to avoid uncontrolled `terraform apply -auto-approve` usage.
   - Related findings: `DEP-001` (partially)
6. Refactored function data processing to a DataFrame-first pipeline:
   - `fetch_data()` now parses API JSON directly into a pandas DataFrame using `pd.json_normalize(...)`
   - Column names are sanitized (`.`, `-` -> `_`, lowercase), missing values are normalized (`fillna("")`), and columns are deterministically ordered
   - CSV-injection protection remains enforced before export via `_safe_cell` in `convert_to_csv()`
   - Related findings: supports hardening posture for `PY-006` and `PY-008` by keeping transformation logic centralized and explicit

## Open / Deferred

### Still Open

- `PY-002`, `TF-M2`: Upstream API is still `http://` (external dependency and challenge constraint).
- `PY-008`: Explicit API response size limiting is not yet implemented.
- `TF-007`, `TF-004`, `TF-006`, `TF-012`, `TF-016`, `TF-017`, `TF-018`, and remaining policy checks currently skipped or de-scoped.
- Azure Storage monitoring/observability controls (storage account and container read/write logging, diagnostics, and related monitoring policies) are explicitly out of scope


## Finding Status Snapshot

| Finding ID | Status |
|---|---|
| PY-001 | Fixed |
| PY-002 | Open (External dependency) |
| PY-003 | Fixed |
| PY-004 | Partially addressed (still contains contact identifier) |
| PY-005 | Fixed |
| PY-006 | Fixed |
| PY-007 | Fixed |
| PY-008 | Open |
| PY-009 | Fixed |
| TF-M1 | Fixed |
| TF-M2 | Open (External dependency / policy choice) |
| TF-001 | Fixed |
| TF-002 | Open / Deferred |
| TF-003 | Fixed |
| TF-004 | Deferred |
| TF-005 | Fixed |
| TF-006 | Deferred |
| TF-007 | Deferred |
| TF-008 | Open / Deferred |
| TF-009 | Fixed |
| TF-010 | Partially fixed |
| TF-011 | Fixed |
| TF-012 | Deferred |
| TF-013 | Fixed |
| TF-014 | Fixed |
| TF-015 | Open / Deferred |
| TF-016 | Deferred |
| TF-017 | Deferred |
| TF-018 | Deferred |
| DEP-001 | Partially fixed (legacy script removed; CI/CD introduced; apply remains demo) |
