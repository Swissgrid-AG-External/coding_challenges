# Security Findings

## Scope Summary
- Function app findings: 9
- Terraform findings: 20 (18 scanner-grouped + 2 manual)
- Deployment findings: 1
- Total findings: 30

## Critical Findings
| ID | Area | Finding | Status |
|---|---|---|---|
| PY-001 | Function | Hardcoded API keys / sensitive info risk | Open |
| PY-002 | Function | API transport can be plaintext HTTP | Open (external dependency) |
| TF-M1 | Terraform | Terraform outputs exposed storage secrets | Open |
| TF-M2 | Terraform | `api_url` transport not enforced as HTTPS at input layer | Open  (external dependency) |
| TF-001 | Terraform | Function App HTTPS not enforced | Open |


## High Findings
| ID | Area | Finding | Status |
|---|---|---|---|
| PY-003 | Function | API URL validation missing/insufficient | Open |

| TF-003 | Terraform | Storage container public access | Open |
| TF-005 | Terraform | Storage secure transfer / HTTPS not enforced | Open |
| TF-006 | Terraform | Storage network rules default action not deny (`AZU-0012`) | Open |
| TF-011 | Terraform | Storage TLS minimum version | Open |
| DEP-001 | Deploy Script | `terraform apply -auto-approve` bypasses change control | Open |

## Medium Findings
| ID | Area | Finding | Status |
|---|---|---|---|
| PY-004 | Function | User-Agent information disclosure (contact/internal details) | Open |
| PY-005 | Function | Missing startup config validation | Open |
| PY-007 | Function | Secret logging risk | Open |
| TF-007 | Terraform | Storage logging not enabled (`AZU-0057`, `CKV_AZURE_33`) | Open|
| TF-009 | Terraform | Storage infrastructure encryption not enabled | Open |
| TF-015 | Terraform | SAS expiration policy | Open |

## Low Findings
| ID | Area | Finding | Status |
|---|---|---|---|
| PY-006 | Function | Broad exception logging hygiene | Open |
| PY-008 | Function | API response size limiting absent | Open |
| TF-008 | Terraform | Geo-redundancy/replication policy | Open |
| TF-013 | Terraform | Storage soft delete policy | Open |
| TF-014 | Terraform | Shared key authorization enabled | Open |
| TF-017 | Terraform | App Service Plan not zone redundant | Open |
| TF-018 | Terraform | App Service Plan min instances/failover | Open |

## Policy/Best-Practice Findings (No explicit severity in source)
| ID | Area | Finding | Status |
|---|---|---|---|
| PY-009 | Function | Prefer managed identity over connection strings | Recommended |
| TF-002 | Terraform | Function App public network access not disabled (`CKV_AZURE_221`) | Open |
| TF-004 | Terraform | Blob read logging control (`CKV2_AZURE_21`) | Open |
| TF-010 | Terraform | Public/anonymous access policy cluster (`CKV_AZURE_59`, `CKV_AZURE_190`, `CKV2_AZURE_47`) | Open |
| TF-012 | Terraform | Private endpoint not configured (`CKV2_AZURE_33`) | Open |
| TF-016 | Terraform | Customer-managed key not configured (`CKV2_AZURE_1`) | Open |
