#!/bin/bash
# deploy.sh — Quick and dirty deployment script
# Usage: ./deploy.sh

# ============================================================
# CONFIGURATION
# ============================================================

RESOURCE_GROUP="rg-data-collector"
FUNCTION_APP_NAME="func-data-collector-prod"
STORAGE_ACCOUNT="acmedatacollector01"

AZURE_STORAGE_KEY="bXktc3VwZXItc2VjcmV0LXN0b3JhZ2Uta2V5LXRoYXQtc2hvdWxkLW5vdC1iZS1oZXJl"
API_KEY="sk-proj-8a3b2f1e9d4c7a6b5e8f2d1c4a7b3e9f"

# ============================================================
# STEP 1: Terraform
# ============================================================

echo ">>> Running Terraform..."
cd terraform

terraform init
terraform apply -auto-approve

cd ..

# ============================================================
# STEP 2: Package Function App
# ============================================================

echo ">>> Packaging function app..."
cd function_app

pip install -r requirements.txt

zip -r ../functionapp.zip . 

cd ..

# ============================================================
# STEP 3: Deploy Function App
# ============================================================

echo ">>> Deploying function app..."

az functionapp deployment source config-zip \
  --resource-group "$RESOURCE_GROUP" \
  --name "$FUNCTION_APP_NAME" \
  --src functionapp.zip

# ============================================================
# STEP 4: Quick smoke test
# ============================================================

echo ">>> Running smoke test..."

curl http://${FUNCTION_APP_NAME}.azurewebsites.net/api/trigger

echo ""
echo ">>> Deployment complete!"
