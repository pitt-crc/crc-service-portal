FROM python:3.11.4-slim

EXPOSE 80

# Disable Python byte code caching and output buffering
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install --no-install-recommends -y \
    # Required for LDAP support
    build-essential \
    libsasl2-dev \
    libldap2-dev \
    # Required for running Celery
    redis \
    # Required for Docker HEALTHCHECK
    curl \
    # Required for static file serving
    nginx \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

# Create an unprivliged user for running background services
RUN groupadd --gid 900 keystone && useradd -m -u 900 -g keystone keystone

# Install the application
WORKDIR /app
COPY . src
RUN pip install ./src[all] && rm -rf src

# Configure media file storage
ENV CONFIG_UPLOAD_DIR=/app/media
RUN mkdir $CONFIG_UPLOAD_DIR

# Configure the NGINX proxy
RUN groupadd nginx && useradd -m -g nginx nginx
COPY conf/nginx.conf /etc/nginx/nginx.conf

# Use the API health checks to report container health
HEALTHCHECK CMD curl --fail --location localhost/health/ || exit 1

# Setup the container to launch the application
COPY --chmod=755 conf/entrypoint.sh /app/entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["quickstart", "--all"]
