resource "azurerm_resource_group" "rg" {
  name     = var.resource_group_name
  location = var.location
}

# ---------- Storage Account ----------
# AZU-0057 excluded: detailed storage logging is de-scoped for this challenge
# AZU-0012 excluded: Network default action is not denied for this storage account - assumption; design decision
resource "azurerm_storage_account" "storage" {
  #checkov:skip=CKV2_AZURE_1: Ensure storage for critical data are encrypted with Customer Managed Key - assumption; design decision
  #checkov:skip=CKV2_AZURE_33: Ensure storage account is configured with private endpoint - assumption; design decision
  #checkov:skip=CKV_AZURE_59: Ensure that Storage accounts disallow public access - assumption; design decision
  #checkov:skip=CKV_AZURE_33: "Ensure Storage logging is enabled for Queue service for read, write and delete requests - no queue in use
  name                              = var.storage_account_name
  resource_group_name               = azurerm_resource_group.rg.name
  location                          = azurerm_resource_group.rg.location
  account_tier                      = "Standard"
  account_replication_type          = "GRS"
  infrastructure_encryption_enabled = true

  allow_nested_items_to_be_public = false

  https_traffic_only_enabled = true
  min_tls_version            = "TLS1_2"

  shared_access_key_enabled = false

  blob_properties {
    delete_retention_policy {
      days = 7
    }
    container_delete_retention_policy {
      days = 7
    }
  }
}

resource "azurerm_storage_container" "data" {
  #checkov:skip=CKV2_AZURE_21: Blob read logging is de-scoped for this challenge
  name               = "api-results"
  storage_account_id = azurerm_storage_account.storage.id

  container_access_type = "private"
}

# ---------- App Service Plan ----------

resource "azurerm_service_plan" "plan" {
  #checkov:skip=CKV_AZURE_225: Ensure the App Service Plan is zone redundant - assumption; design decision
  #checkov:skip=CKV_AZURE_212: "Ensure App Service has a minimum number of instances for failover - assumption; design decision
  name                = "asp-data-collector"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  os_type             = "Linux"
  sku_name            = "Y1"

}

# ---------- Function App ----------

resource "azurerm_linux_function_app" "func" {
  #checkov:skip=CKV_AZURE_221: Ensure that Azure Function App public network access is disabled - assumption; design decision
  name                = var.function_app_name
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  service_plan_id     = azurerm_service_plan.plan.id

  storage_account_name       = azurerm_storage_account.storage.name
  storage_account_access_key = azurerm_storage_account.storage.primary_access_key

  site_config {
    application_stack {
      python_version = "3.12"
    }

    ftps_state = "FtpsOnly"
    #cors {
    #  allowed_origins = ["*"]
    #}
  }

  identity {
    type = "SystemAssigned"
  }

  https_only = true

  app_settings = {
    "API_KEY" = "@Microsoft.KeyVault(SecretUri=${var.api_key_secret_uri})"
    "API_URL" = var.api_url

    #"STORAGE_CONNECTION_STRING" = azurerm_storage_account.storage.primary_connection_string
    "STORAGE_ACCOUNT_URL" = "https://${azurerm_storage_account.storage.name}.blob.core.windows.net"
    "CONTAINER_NAME"      = "api-results"

    "FUNCTIONS_WORKER_RUNTIME" = "python"
    "AzureWebJobsFeatureFlags" = "EnableWorkerIndexing"

    "SCM_DO_BUILD_DURING_DEPLOYMENT" = "false"
  }

}

resource "azurerm_role_assignment" "func_blob_write" {
  scope                = azurerm_storage_account.storage.id
  role_definition_name = "Storage Blob Data Contributor"
  principal_id         = azurerm_linux_function_app.func.identity[0].principal_id
}
