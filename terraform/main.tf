resource "azurerm_resource_group" "sil" {
  name     = "sil"
  location = "westeurope"
}

resource "azurerm_container_group" "server" {
  name                = "server"
  resource_group_name = azurerm_resource_group.sil.name
  location            = azurerm_resource_group.sil.location
  os_type             = "Linux"
  dns_name_label      = "sil2024"

  container {
    name   = "server"
    image  = var.server_image
    cpu    = 3.5
    memory = 8
  }

  container {
    name   = "gateway"
    image  = var.gateway_image
    cpu    = 0.5
    memory = 0.5

    ports {
      port = 80
    }

    ports {
      port = 443
    }
  }
}
