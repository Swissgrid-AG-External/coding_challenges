#!/bin/bash
# deploy.sh — Quick and dirty deployment script
# Usage: ./deploy.sh

# ============================================================
# CONFIGURATION
# ============================================================

RESOURCE_GROUP="rg-data-collector"
FUNCTION_APP_NAME="func-data-collector-prod"

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

echo ""
echo ">>> Deployment complete!"
