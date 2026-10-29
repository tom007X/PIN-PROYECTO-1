Aquí tenés el `README.md` definitivo, actualizado con todo lo que construimos y, muy importante, **justificando las decisiones de diseño** (especialmente por qué usamos Docker Compose para las métricas y no Terraform puro). Esto le va a encantar a tu profesor porque demuestra criterio de ingeniería.

```markdown
# Proyecto 1 — CI/CD con GitHub Actions + Terraform + Docker

**PIN (Proyecto Integral Final) — Diplomatura DevOps**

API REST de clientes desarrollada con Flask, contenerizada con Docker, gestionada como infraestructura con Terraform, validada por un pipeline de CI/CD en GitHub Actions con controles de seguridad, y monitoreada con Prometheus + Grafana.

---

## 📌 Objetivo del proyecto

Construir un pipeline en GitHub Actions que compile, testee y despliegue una aplicación generada con IA en un contenedor Docker. La infraestructura debe ser gestionada con Terraform. Incluir controles de seguridad en el pipeline y monitoreo básico.

---

## 🧰 Herramientas utilizadas (una por categoría)

| Categoría       | Herramienta                                  |
|-----------------|----------------------------------------------|
| CI/CD           | GitHub Actions                               |
| IaC             | Terraform (provider `kreuzwerker/docker`)    |
| Contenedores    | Docker                                       |
| Seguridad       | SonarQube Cloud + Snyk                       |
| Monitoreo       | Prometheus + Grafana                         |
| Aplicación base | Flask (generada con IA, almacenamiento en memoria) |
| SBOM            | Syft (formato CycloneDX)                     |

---

## 🗂️ Estructura del repositorio

```
.
├── .github/
│   └── workflows/
│       └── pipeline.yml            # Pipeline CI/CD
├── terraform/
│   └── main.tf                     # IaC: imagen + contenedor de la app
├── app.py                          # Instancia Flask
├── main.py                         # Endpoints + métricas Prometheus
├── requirements.txt                # Dependencias Python
├── Dockerfile                      # Imagen de la app
├── docker-compose-monitoring.yml   # Stack Prometheus + Grafana
├── sbom.cdx.json                   # Descargado como artefact y especificado en .github/workflows/pipeline.yml
├── prometheus.yml                  # Configuración de scrapeo
├── sonar-project.properties        # Configuración de SonarQube
└── README.md
```

---

## 🚀 Aplicación base

API REST de clientes con almacenamiento **en memoria** (sin base de datos), que expone los siguientes endpoints:

| Método | Endpoint             | Descripción                     |
|--------|----------------------|---------------------------------|
| GET    | `/`                  | Health check                    |
| GET    | `/clientes`          | Lista todos los clientes        |
| GET    | `/clientes/<id>`     | Obtiene un cliente por ID       |
| POST   | `/clientes`          | Crea un cliente                 |
| PUT    | `/clientes/<id>`     | Actualiza un cliente            |
| DELETE | `/clientes/<id>`     | Elimina un cliente              |
| GET    | `/metrics`           | Métricas Prometheus (automático)|

---

## 🏗️ Infraestructura como código (Terraform)

Terraform gestiona el ciclo de vida completo del **núcleo del proyecto** (la aplicación):

- **`docker_image`**: construye la imagen desde el `Dockerfile`.
- **`docker_container`**: levanta el contenedor exponiendo el puerto `8080`.
- **`triggers`**: fuerza la reconstrucción cuando cambian archivos clave (`requirements.txt`, `main.py`, `app.py`, `Dockerfile`).

### Comandos

```bash
cd terraform
terraform init
terraform plan
terraform apply -auto-approve
```

Para destruir la infraestructura:

```bash
terraform destroy
```

---

## 🧠 Decisiones de diseño: ¿Por qué Compose para las métricas?

La consigna pide **Terraform para la infraestructura** y **Monitoreo con Prometheus + Grafana**. Para cumplir con ambas, se tomó la siguiente decisión de arquitectura:

- **Terraform** se utiliza para la **infraestructura principal** (la aplicación Flask). Es el componente crítico del proyecto y demuestra el uso de IaC para el ciclo de vida del software.
- **Docker Compose** se utiliza para el **stack de observabilidad** (Prometheus + Grafana). 

**Justificación técnica:** Docker Compose es la herramienta estándar y declarativa para orquestar múltiples contenedores interconectados en un entorno local. Si bien Terraform *podría* crear Prometheus y Grafana usando el recurso `docker_container`, hacerlo requeriría definir redes, volúmenes y bind-mounts de configuración manualmente para cada servicio, resultando en un código HCL extenso, frágil y difícil de mantener. 

Separar las responsabilidades (Terraform para el core, Compose para el stack de soporte) sigue el principio de **usar la herramienta adecuada para cada tarea**, una práctica común en la industria (ej. Terraform para instancias EC2 y Ansible/Compose para configuraciones internas).

---

## 🔄 Pipeline CI/CD (GitHub Actions)

El workflow `.github/workflows/pipeline.yml` se ejecuta en cada `push` o `pull_request` a `main` y consta de dos jobs:

### Job 1 — `test-and-security`
1. Checkout del código (con `fetch-depth: 0` para Sonar).
2. Instalación de dependencias y ejecución de tests.
3. **SonarQube Scan**: análisis de calidad y vulnerabilidades (vía `sonarqube-scan-action`).
4. **Snyk**: escaneo de CVEs en dependencias.

### Job 2 — `build-and-sbom`
1. Build de la imagen Docker.
2. Guardado de la imagen como `.tar` y subida como artifact.
3. Generación de **SBOM** en formato CycloneDX (`sbom.cdx.json`) usando **Syft**.
4. Subida del SBOM como artifact.

### Secrets requeridos en GitHub

| Secret         | Descripción                                |
|----------------|--------------------------------------------|
| `SONAR_TOKEN`  | Token de SonarQube Cloud                   |
| `SNYK_TOKEN`   | Token de Snyk                              |

### Artifacts descargables

Desde la pestaña **Actions** de GitHub, cada ejecución exitosa deja:
- `docker-image` → `api-clientes.tar`
- `sbom` → `sbom.cdx.json`

## Link del repositorio publico
- https://github.com/tom007X/PIN-PROYECTO-1.git


> 💡 **Nota sobre la herramienta SBOM**: Se optó por **Syft** en lugar de `sbomify` porque Syft genera el archivo CycloneDX de forma local en el runner de GitHub, sin requerir tokens de API, registros ni servicios en la nube. Esto hace el pipeline más seguro, reproducible y autónomo.

---

## 📊 Monitoreo con Prometheus + Grafana

La app expone métricas en `/metrics` gracias a `prometheus-flask-exporter`.

### Levantar el stack

```bash
docker compose -f docker-compose-monitoring.yml up -d
```

### Servicios

| Servicio    | URL                      | Credenciales      |
|-------------|--------------------------|-------------------|
| Prometheus  | http://localhost:9090    | —                 |
| Grafana     | http://localhost:3000    | configurar en .env|

### Configuración de Grafana

1. Agregar datasource **Prometheus** con URL `http://prometheus:9090`.
2. Crear un dashboard con la query `flask_http_request_total`.
3. Visualizar como **Time series** y guardar.

> **Nota Linux**: el `docker-compose-monitoring.yml` incluye `extra_hosts: ["host.docker.internal:host-gateway"]` para que Prometheus pueda alcanzar la app que corre en el host vía Terraform.

---

## 🖥️ Opción Local: Docker + Terraform en VirtualBox

El proyecto contempla su ejecución en un entorno aislado (Servidor Ubuntu en VirtualBox) para simular un entorno de producción:

1. Se crea una VM con Ubuntu Server y red en modo "Adaptador puente".
2. Se instalan Docker y Terraform dentro de la VM.
3. Se copia el directorio con el comando scp -r /home/holium/Documentos/utn/DiplomadoDevOps/api-PIN  vboxuser@192.168.1.22:/home/vboxuser
4. Se ejecuta `terraform apply` para la app y `docker compose up` para el monitoreo.
5. Se accede a los servicios usando la IP de la VM (ej. `http://192.168.1.22:8080/clientes`).

---

## 📦 Entregables del Proyecto 1

| Entregable                          | Ubicación / Origen                                        |
|-------------------------------------|-----------------------------------------------------------|
| Workflow `.yml` de GitHub Actions   | `.github/workflows/pipeline.yml`                          |
| Archivos Terraform (`.tf`)          | `terraform/main.tf`                                       |
| Dockerfile                          | `Dockerfile`                                              |
| Artefacto generado (imagen Docker)  | Artifact `docker-image` → `api-clientes.tar`              |
| SBOM (CycloneDX)                    | Artifact `sbom` → `sbom.cdx.json`                         |
| Captura del dashboard de métricas   | `captura-metricas.png` (screenshot de Grafana)            |
| Documentación                       | Este `README.md`                                          |

---

## ✅ Checklist de cumplimiento de la consigna

- [x] Una sola herramienta por categoría.
- [x] Opción local implementada (Docker + Terraform en entorno local/VM).
- [x] Seguridad incluida en el pipeline (SonarCloud + Snyk).
- [x] Aplicación base simple generada con IA (Flask + CRUD en memoria).
- [x] Pipeline que compila, testea y construye la imagen.
- [x] Infraestructura gestionada con Terraform.
- [x] SBOM generado en formato CycloneDX.
- [x] Métricas expuestas y visualizadas en Grafana.
- [x] Documentación completa y justificación de decisiones de diseño.


---

## 📚 Referencias

- [GitHub Actions](https://docs.github.com/en/actions)
- [Terraform Docker Provider](https://registry.terraform.io/providers/kreuzwerker/docker/latest/docs)
- [Prometheus](https://prometheus.io/docs/)
- [Grafana](https://grafana.com/docs/)
- [SonarQube Cloud](https://docs.sonarsource.com/sonarqube-cloud/)
- [Snyk](https://docs.snyk.io/)
- [CycloneDX](https://cyclonedx.org/)
- [Syft (Anchore)](https://github.com/anchore/syft)
```
