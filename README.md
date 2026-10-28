# 🚀 Proyecto 1: CI/CD con GitHub Actions, Terraform y Docker

Repositorio correspondiente al **Proyecto Integral Final (PIN)** de la diplomatura. Este proyecto implementa un pipeline automatizado de integración y entrega continua (CI/CD) para una aplicación base generada con IA, integrando infraestructura como código (IaC), contenedorización, escaneo de seguridad avanzado y observabilidad.

---

## 🏗️ Arquitectura y Stack Tecnológico

El proyecto cumple con la restricción de utilizar una sola herramienta por categoría según el programa:

| Categoría | Herramienta | Descripción |
| :--- | :--- | :--- |
| **CI/CD** | `GitHub Actions` | Automatización de compilación, testing, análisis de seguridad y despliegue. |
| **IaC** | `Terraform` | Aprovisionamiento y gestión declarativa de la infraestructura. |
| **Contenedores** | `Docker` | Empaquetado y ejecución de la aplicación en entornos aislados. |
| **Seguridad** | `SonarQube / ESLint` + `Snyk` | Análisis estático de código (SAST), detección de vulnerabilidades y generación de SBOM. |
| **Monitoreo** | `Prometheus` + `Grafana` | Recopilación de métricas del sistema/aplicación y visualización en dashboards. |

---

## 📂 Estructura del Repositorio

```text
├── .github/
│   └── workflows/
│       └── pipeline.yml       # Pipeline principal de CI/CD en GitHub Actions
├── terraform/
│   ├── main.tf                # Recursos de infraestructura
│   ├── variables.tf           # Definición de variables
│   └── outputs.tf             # Outputs de Terraform
├── main                       # Código fuente de la aplicación generada con IA
├── Dockerfile                 # Receta para la construcción de la imagen de contenedor
├── docker-compose.yml         # Orquestación local (Prometheus, Grafana, App)
└── README.md
```
---

## api-clientes (Python / Flask)



## Endpoints
| Método | Ruta            | Descripción          |
|--------|-----------------|-----------------------|
| GET    | `/`             | Health check          |
| GET    | `/clientes`     | Listar todos          |
| GET    | `/clientes/:id` | Obtener uno           |
| POST   | `/clientes`     | Crear (alta)          |
| PUT    | `/clientes/:id` | Modificar             |
| DELETE | `/clientes/:id` | Borrar (baja)         |

Body de ejemplo (`POST` / `PUT`):
```json
{ "nombre": "Ana Torres", "email": "ana@example.com", "dni": "30111222" }
```

.
