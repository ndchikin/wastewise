output "container_fqdn" {
  value = azurerm_container_group.server.fqdn
}

output "container_ip_address" {
  value = azurerm_container_group.server.ip_address
}
