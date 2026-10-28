
---

```markdown
# 🚀 Proyecto 1: CI/CD con GitHub Actions + Terraform + Docker
**PIN (Proyecto Integral Final) — Diplomatura DevOps**

Repositorio oficial del proyecto integrador. Implementa un pipeline automatizado de integración y entrega continua (CI/CD) para una API REST de clientes desarrollada con Flask, contenerizada con Docker, gestionada mediante infraestructura como código (Terraform), validada con estrictos controles de seguridad y monitoreada con Prometheus y Grafana.

---

## 📌 Objetivo del proyecto

Construir un pipeline robusto en GitHub Actions que compile, testee, analice la seguridad y empaquete una aplicación generada con IA en un contenedor Docker. La infraestructura subyacente es gestionada de punta a punta con Terraform.

---

## 🧰 Herramientas utilizadas (Una por categoría)

| Categoría | Herramienta | Descripción |
| :--- | :--- | :--- |
| **CI/CD** | `GitHub Actions` | Automatización del pipeline de integración y entrega continua. |
| **IaC** | `Terraform` | Proveedor `kreuzwerker/docker` para gestionar imágenes y contenedores. |
| **Contenedores** | `Docker` | Empaquetado y aislamiento de la aplicación. |
| **Seguridad** | `SonarCloud` + `Snyk` | Análisis estático de código (SAST) y escaneo de vulnerabilidades en dependencias. |
| **Monitoreo** | `Prometheus` + `Grafana` | Recopilación de métricas y visualización en dashboards interactivos. |
| **Aplicación base** | `Flask` | API REST generada con IA (almacenamiento en memoria). |

---

## 🗂️ Estructura del Repositorio

```text
.
├── .github/
│   └── workflows/
│       └── pipeline.yml            # Pipeline CI/CD automatizado
├── terraform/
│   └── main.tf                     # IaC: gestión de imagen y contenedor Docker
├── app.py                          # Instancia Flask y configuración base
├── main.py                         # Endpoints del CRUD y métricas de Prometheus
├── requirements.txt                # Dependencias del proyecto Python
├── Dockerfile                      # Receta de construcción de la imagen Docker
├── docker-compose-monitoring.yml   # Stack local de Prometheus + Grafana
├── prometheus.yml                  # Configuración de scrapeo para Prometheus
└── README.md                       # Documentación del proyecto

```

---

## 🚀 Aplicación Base (API REST)

API REST de clientes con almacenamiento **en memoria**, que expone los siguientes endpoints:

| Método | Endpoint | Descripción |
| --- | --- | --- |
| `GET` | `/` | Health check del servicio |
| `GET` | `/clientes` | Lista todos los clientes almacenados |
| `GET` | `/clientes/<id>` | Obtiene un cliente específico por su ID |
| `POST` | `/clientes` | Crea un nuevo registro de cliente |
| `PUT` | `/clientes/<id>` | Actualiza los datos de un cliente existente |
| `DELETE` | `/clientes/<id>` | Elimina un cliente por su ID |
| `GET` | `/metrics` | Exposición automática de métricas para Prometheus |

### Ejemplo de uso local con cURL:

```bash
# Crear un cliente
curl -X POST http://localhost:8080/clientes \
  -H "Content-Type: application/json" \
  -d '{"nombre":"Ana","email":"ana@mail.com","dni":"12345678"}'

# Listar clientes
curl http://localhost:8080/clientes

```

---

## 🏗️ Infraestructura como Código (Terraform)

Terraform gestiona de manera declarativa el ciclo de vida completo de la aplicación:

* `docker_image`: Construye automáticamente la imagen utilizando el `Dockerfile` del proyecto.
* `docker_container`: Despliega el contenedor exponiendo el puerto `8080`.
* **Triggers:** Configurados para forzar la reconstrucción de la imagen ante cualquier modificación en `requirements.txt`, `main.py`, `app.py` o el propio `Dockerfile`.

### Comandos de uso:

```bash
cd terraform
terraform init
terraform plan
terraform apply -auto-approve

```

Para destruir y limpiar la infraestructura:

```bash
terraform destroy

```

---

## 🔄 Pipeline CI/CD (GitHub Actions)

El workflow definido en `.github/workflows/pipeline.yml` se dispara automáticamente ante eventos de `push` o `pull_request` sobre la rama principal, estructurándose en dos jobs paralelos/secuenciales:

### Job 1 — `test-and-security`

1. Checkout del código fuente.
2. Configuración del entorno e instalación de dependencias de Python.
3. Ejecución de pruebas unitarias con `pytest` y generación de reporte de cobertura.
4. **SonarCloud:** Análisis estático de calidad de código y detección de code smells/vulnerabilidades.
5. **Snyk:** Escaneo exhaustivo de CVEs en las dependencias del proyecto.

### Job 2 — `build-and-sbom`

1. Construcción de la imagen Docker de la aplicación.
2. Exportación de la imagen como archivo `.tar` y subida como **Artifact** (`docker-image`).
3. Generación del reporte **SBOM** (Software Bill of Materials) en formato CycloneDX (`sbom.cdx.json`).
4. Subida del SBOM como **Artifact** de la ejecución.

### 🔐 Secrets requeridos en GitHub

Para el correcto funcionamiento de los análisis de seguridad, configura los siguientes secretos en tu repositorio (`Settings > Secrets and variables > Actions`):

| Secret | Descripción |
| --- | --- |
| `SONAR_TOKEN` | Token de acceso de SonarCloud |
| `SNYK_TOKEN` | Token de autenticación de Snyk |

*(Nota: Si no se configuran, los pasos de seguridad cuentan con `continue-on-error: true` para evitar bloqueos académicos, pero se recomienda activarlos).*

### 📦 Artifacts descargables

Al finalizar con éxito una ejecución en la pestaña **Actions** de GitHub, podrás descargar:

* `docker-image` → Contiene el archivo empaquetado `api-clientes.tar`.
* `sbom` → Contiene el reporte de componentes en formato CycloneDX (`sbom.cdx.json`).

---

## 📊 Monitoreo con Prometheus + Grafana

La aplicación expone métricas en tiempo real gracias a la librería `prometheus-flask-exporter`.

### Levantar el stack local de observabilidad:

```bash
docker compose -f docker-compose-monitoring.yml up -d

```

### Servicios disponibles:

| Servicio | URL de Acceso | Credenciales |
| --- | --- | --- |
| **Prometheus** | [http://localhost:9090](http://localhost:9090) | Sin credenciales |
| **Grafana** | [http://localhost:3000](http://localhost:3000) | `admin` / `admin` |

### Configuración rápida en Grafana:

1. Agregar una nueva fuente de datos (**Data Source**) de tipo **Prometheus** con la URL `http://prometheus:9090`.
2. Crear un nuevo panel (*Dashboard*) utilizando la query de métricas: `flask_http_request_total`.
3. Seleccionar el tipo de visualización **Time series** y guardar el dashboard.

> 💡 **Nota para entornos Linux:** El archivo `docker-compose-monitoring.yml` incluye la directiva `extra_hosts: ["host.docker.internal:host-gateway"]` para permitir que Prometheus scrapee correctamente la aplicación que corre en el host vía Terraform.

Verifica que el target esté activo ingresando a [http://localhost:9090/targets](http://localhost:9090/targets).

---

## 📦 Resumen de Entregables del Proyecto 1

| Entregable | Ruta / Ubicación en el Repositorio |
| --- | --- |
| **Workflow de GitHub Actions** | `.github/workflows/pipeline.yml` |
| **Archivos de Terraform (.tf)** | `terraform/main.tf` |
| **Dockerfile** | `Dockerfile` |
| **Artefacto de imagen Docker** | Artifact en GitHub Actions (`api-clientes.tar`) |
| **Reporte SBOM (CycloneDX)** | Artifact en GitHub Actions (`sbom.cdx.json`) |
| **Captura de métricas** | `captura-metricas.png` (Dashboard de Grafana) |
| **Documentación técnica** | Este archivo `README.md` |

---

## ✅ Checklist de Cumplimiento de la Consigna

* [x] Una sola herramienta por categoría (GitHub Actions, Terraform, Docker, SonarCloud/Snyk, Prometheus/Grafana).
* [x] Opción local implementada (Docker + Terraform).
* [x] Controles de seguridad integrados en el pipeline (SonarCloud + Snyk).
* [x] Aplicación base simple generada con IA (Flask + CRUD en memoria).
* [x] Pipeline automatizado que compila, testea y construye la imagen.
* [x] Infraestructura provisionada y gestionada con Terraform.
* [x] SBOM generado formalmente en formato CycloneDX.
* [x] Métricas expuestas y visualizadas mediante un dashboard en Grafana.
* [x] Documentación completa y detallada en el repositorio.

---

## 👥 Equipo

* **Equipo:** EquipoX
* **Integrantes:** *(Completar con los nombres de los integrantes)*
* **Fecha de entrega:** *(Completar con la fecha)*

---

## 📚 Referencias y Documentación Oficial

* [Documentación Oficial de Git](https://git-scm.com/doc)
* [GitHub Actions Documentation](https://docs.github.com/en/actions)
* [Terraform Docker Provider](https://registry.terraform.io/providers/kreuzwerker/docker/latest/docs)
* [Prometheus Documentation](https://prometheus.io/docs/)
* [Grafana Documentation](https://grafana.com/docs/)
* [SonarCloud](https://sonarcloud.io/)
* [Snyk Documentation](https://docs.snyk.io/)
* [CycloneDX SBOM Standard](https://cyclonedx.org/)

```

```

