# Coding Challenge: Secure Platform Engineering

## Context

You just joined **Acme Corp** as a Platform / Security Engineer. A colleague built the following project over a weekend to solve an urgent business need:

> A Python-based **Azure Function** runs once per hour, queries an external API (`https://my-cool-api.ch/results`), and stores the results as a CSV file in Azure Blob Storage.

The code works — data shows up in the storage account every hour — but it was shipped under time pressure with **no security review**.

Your manager has asked you to **review, harden, and professionalize** this project before it goes to production.

---

## Repository Structure

```
.
├── terraform/
│   ├── providers.tf        # Terraform provider configuration
│   ├── variables.tf        # Input variables
│   ├── main.tf             # Infrastructure definitions
│   └── outputs.tf          # Output values
├── function_app/
│   ├── function_app.py     # Azure Function code (Python v2 model)
│   ├── host.json           # Function host configuration
│   ├── requirements.txt    # Python dependencies
│   └── local.settings.json # Local development settings
├── deploy.sh               # Deployment script
└── README.md               # This file
```

---

## How to Deploy (current state)

1. Fill in the variables in `terraform/variables.tf`
2. Run `terraform init && terraform apply` from the `terraform/` directory
3. Run `./deploy.sh` to package and deploy the function code

## Local Deployment (no Azure account required)

This challenge can be run end-to-end on Linux without creating an Azure account.

### Quick Start (Linux)

From this folder (`SWE_platform_security/`), run:

```bash
chmod +x setup_linux.sh && ./setup_linux.sh
```

This installs:
- `just`
- `uv`
- Python 3 + pip
- Docker + Docker Compose plugin
- Python dependencies from `function_app/requirements.txt`

Then run one local ingestion cycle:

```bash
just run-once
```

### What `just run-once` does

1. Starts local services with Docker:
   - Azurite (Azure Blob emulator)
   - Mock API (`http://localhost:8081/results`)
2. Ensures blob container `api-results` exists
3. Fetches mock API data
4. Writes a CSV blob to local Azurite storage

### Optional Commands

Run local services only:

```bash
just local-up
```

Run Azure Functions host locally (requires Azure Functions Core Tools):

```bash
just run-func
```

Stop and clean local services:

```bash
just local-down
```

If Docker permission is denied after setup, run:

```bash
newgrp docker
```

---

## Your Tasks

Please spend **60–90 minutes** on this challenge. You do **not** need to produce a fully working deployment — we are more interested in your **thought process, priorities, and approach**.

### 1. Security Review
Identify as many security issues as you can across the entire codebase (Terraform, Python, deployment process). For each issue:
- Describe the **risk**
- Suggest a **remediation**
- Rate the **severity** (Critical / High / Medium / Low)

### 2. Code Improvements
Pick the **top 3–5 issues** you identified and actually fix them in code. Feel free to refactor, restructure, or rewrite as needed.

### 3. CI/CD Pipeline (Stretch Goal)
Propose or implement a CI/CD pipeline (GitHub Actions, Azure DevOps, GitLab CI, or similar) that:
- Automates deployment
- Includes security checks (linting, scanning, etc.)
- Follows best practices for infrastructure-as-code

### 4. Documentation
Briefly document your changes and reasoning. A few paragraphs or bullet points is fine.

---

## What We're Looking For

- **Security mindset**: Can you spot vulnerabilities across the stack?
- **Prioritization**: Do you focus on what matters most?
- **Practical skills**: Can you translate findings into working code?
- **Communication**: Can you explain risks clearly to a mixed audience?

Good luck! 🚀
