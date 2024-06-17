variable "client_id" {
  type = string
  sensitive = true
}

variable "client_secret" {
  type = string
  sensitive = true
}

variable "tenant_id" {
  type = string
  sensitive = true
}

variable "subscription_id" {
  type = string
  sensitive = true
}

variable "server_image" {
  type = string
}

variable "gateway_image" {
  type = string
}
