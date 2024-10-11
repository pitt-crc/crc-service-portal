# Deploying with Docker

The Keystone API can be deployed as a single container using Docker, or as several containers using Docker Compose.
Single container deployments are best suited for those looking to test-drive Keystone's capabilities.
Multi-container deployments are strongly recommended for teams operating at scale.

## Using Docker Standalone

The following command will automatically pull and launch the latest application image from the GitHub container registry.
In this example the image is launched as a container called `keystone` and the API is mapped to port 8000 on the local machine.

```bash
docker run --detach --publish 8000:8000 --name keystone ghcr.io/better-hpc/keystone-api
```

The health of the running API instance can be checked by querying the API `health` endpoint.

```bash
curl -L http://localhost:8000/health | jq .
```

The default container command executes the `quickstart` utility, which automatically spins up system dependencies (Postgres, Redis, etc.) within the container.
The command also checks for any existing user accounts and, if no accounts are found, creates an admin account with username `admin` password `quickstart`.
This behavior can be overwritten by manually specifying the docker deployment command.
New administrator accounts can also be created manually by running the `keystone-api` utility from within the container.

```bash
docker exec -i -t keystone keystone-api createsuperuser
```

You can test the new credentials by authenticating against the API and generating a pair of JWT tokens.

```bash
curl \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"username": "[USERNAME]", "password": "[PASSWORD]"}' \
  http://localhost:80/api/token/
```

If successful, you will receive a response similar to the following:

```json
{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX3BrIjoxLCJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiY29sZF9zdHVmZiI6IuKYgyIsImV4cCI6MTIzNDU2LCJqdGkiOiJmZDJmOWQ1ZTFhN2M0MmU4OTQ5MzVlMzYyYmNhOGJjYSJ9.NHlztMGER7UADHZJlxNG0WSi22a2KaYSfd1S-AuT7lU",
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX3BrIjoxLCJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImNvbGRfc3R1ZmYiOiLimIMiLCJleHAiOjIzNDU2NywianRpIjoiZGUxMmY0ZTY3MDY4NDI3ODg5ZjE1YWMyNzcwZGEwNTEifQ.aEoAYkSJjoWH1boshQAaTkf8G3yn0kapko6HFRt7Rh4"
}
```

!!! important

    The default container instance is **not** suitable for production out of the box.
    Supporting services will not save data between container restarts and should be deployed separately to ensure data persistence. 
    See the [Settings](settings.md) page for a complete overview of configurable options and recommended settings.

## Using Docker Compose

The following compose recipe provides a functional starting point for building a scalable API deployment.
Application dependencies are defined as separate services and settings values are configured using environmental
variables in various `.env` files.

```yaml
version: "3.7"

services:
  cache: # (1)!
    image: redis
    container_name: keystone-cache
    command: redis-server
    restart: always
    volumes:
      - cache_data:/data

  db: # (2)!
    image: postgres
    container_name: keystone-db
    restart: always
    env_file:
      - db.env
    volumes:
      - postgres_data:/var/lib/postgresql/data/

  api: # (3)!
    image: ghcr.io/better-hpc/keystone-api
    container_name: keystone-api
    entrypoint: sh
    command: |
      -c '
        keystone-api migrate --no-input
        keystone-api collectstatic --no-input
        gunicorn --bind 0.0.0.0:8000 keystone_api.main.wsgi:application'
    restart: always
    depends_on:
      - cache
      - db
    ports:
      - "8000:8000"
    env_file:
      - api.env
    volumes:
      - static_files:/app/static
      - uploaded_files:/app/upload_files

  celery-worker: # (4)!
    image: ghcr.io/better-hpc/keystone-api
    container_name: keystone-celery-worker
    entrypoint: celery -A keystone_api.apps.scheduler worker --uid 900
    restart: always
    depends_on:
      - cache
      - db
      - api
    env_file:
      - api.env

  celery-beat: # (5)!
    image: ghcr.io/better-hpc/keystone-api
    container_name: keystone-celery-beat
    entrypoint: celery -A keystone_api.apps.scheduler beat --scheduler django_celery_beat.schedulers:DatabaseScheduler --uid 900
    restart: always
    depends_on:
      - cache
      - db
      - api
      - celery-worker
    env_file:
      - api.env

volumes:
  static_files:
  uploaded_files:
  postgres_data:
  cache_data:

```

1. The `cache` service acts as a job queue for background tasks. Note the mounting of cache data onto the host machine to ensure data persistence between container restarts.
2. The `db` service defines the application database. User credentials are defined as environmental variables in the `db.env` file. Note the mounting of database data onto the host machine to ensure data persistence between container restarts.
3. The `api` service defines the Keystone API application. It migrates the database schema, configures static file hosting, and launches the API behind a production quality web server.
4. The `celery-worker` service executes background tasks for the API application. It uses the same base image as the `api` service.
5. The `celery-beat` service handles task scheduling for the `celery-worker` service. It uses the same base image as the `api` service.

The following examples define the minimal required settings for deploying the recipe.
The `DJANGO_SETTINGS_MODULE="keystone_api.main.settings"` setting is required by the application.

!!! important

    The settings provided below are intended for demonstrative purposes only.
    These values are not iherintly secure and should be customized to meet the needs at hand.

=== "api.env"

    ```bash
    # General Settings
    DJANGO_SETTINGS_MODULE="keystone_api.main.settings"
    STORAGE_STATIC_DIR="/app/static"
    STORAGE_UPLOAD_DIR="/app/upload_files"
    
    # Security Settings
    SECURE_ALLOWED_HOSTS="*"
    
    # Redis settings
    REDIS_HOST="cache" # (1)!
    
    # Database settings
    DB_POSTGRES_ENABLE="true"
    DB_NAME="keystone"
    DB_USER="db_user"
    DB_PASSWORD="foobar123"
    DB_HOST="db" # (2)!
    ```

    1. This value should match the service name defined in the compose file.
    2. This value should match the service name defined in the compose file.

=== "db.env"

    ```bash
    # Credential values must match api.env
    POSTGRES_DB="keystone"
    POSTGRES_USER="db_user" # (1)!
    POSTGRES_PASSWORD="foobar123"
    ```

    1. Database credentials must match those defined in `api.env`.
