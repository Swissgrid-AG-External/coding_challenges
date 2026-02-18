
output "storage_account_key" {
  value = azurerm_storage_account.storage.primary_access_key
}

output "storage_connection_string" {
  value     = azurerm_storage_account.storage.primary_connection_string
  sensitive = true
}

output "function_app_url" {
  value = azurerm_linux_function_app.func.default_hostname
}

output "function_app_name" {
  value = azurerm_linux_function_app.func.name
}
