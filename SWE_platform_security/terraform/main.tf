resource "azurerm_resource_group" "rg" {
  name     = var.resource_group_name
  location = var.location
}

# ---------- Storage Account ----------

resource "azurerm_storage_account" "storage" {
  name                     = var.storage_account_name
  resource_group_name      = azurerm_resource_group.rg.name
  location                 = azurerm_resource_group.rg.location
  account_tier             = "Standard"
  account_replication_type = "LRS"

  allow_nested_items_to_be_public = true

  https_traffic_only_enabled = false

  shared_access_key_enabled = true
}

resource "azurerm_storage_container" "data" {
  name                  = "api-results"
  storage_account_id    = azurerm_storage_account.storage.id

  container_access_type = "blob"
}

# ---------- App Service Plan ----------

resource "azurerm_service_plan" "plan" {
  name                = "asp-data-collector"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  os_type             = "Linux"
  sku_name            = "Y1"

}

# ---------- Function App ----------

resource "azurerm_linux_function_app" "func" {
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

    ftps_state = "AllAllowed"
    cors {
      allowed_origins = ["*"]
    }
  }

  https_only = false

  app_settings = {
    "API_KEY"                        = var.api_key
    "API_URL"                        = "http://my-cool-api.ch/results"

    "STORAGE_CONNECTION_STRING"      = azurerm_storage_account.storage.primary_connection_string

    "FUNCTIONS_WORKER_RUNTIME"       = "python"
    "AzureWebJobsFeatureFlags"       = "EnableWorkerIndexing"

    "SCM_DO_BUILD_DURING_DEPLOYMENT" = "false"
  }

}
