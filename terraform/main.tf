terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0"
    }
  }
}

provider "docker" {}

# Construye la imagen desde tu Dockerfile
resource "docker_image" "api_clientes" {
  name = "api-clientes:latest"
  build {
    context = ".."  # apunta al directorio del proyecto
  }

  triggers = {
    dir_sha1 = sha1(join("", [
      filesha1("../requirements.txt"),
      filesha1("../main.py"),
      filesha1("../Dockerfile"),
      filesha1("../app.py")
    ]))
  }
  
  keep_locally = true
}

# Levanta el contenedor
resource "docker_container" "api" {
  name  = "api-clientes"
  image = docker_image.api_clientes.image_id

  ports {
    internal = 8080
    external = 8080
  }

  # Healthcheck opcional
  healthcheck {
    test     = ["CMD", "curl", "-f", "http://localhost:8080/"]
    interval = "30s"
    timeout  = "10s"
    retries  = 3
  }
}