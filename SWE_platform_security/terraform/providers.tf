
terraform {
  required_providers {
    azurerm = {
      source = "hashicorp/azurerm"
    }
  }
}

provider "azurerm" {
  features {}

  subscription_id = "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
}
