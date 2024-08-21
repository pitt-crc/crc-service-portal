# Application Settings

Keystone API reads application settings from environmental variables.
Individual settings are listed below by category and use case.

## Security Settings

Security settings are used to configure application networking and request signing.
These values should be chosen with care.
Improperly configured settings can introduce dangerous vulnerabilities and may damage your production deployment.

| Setting Name                    | Default Value         | Description                                                   |
|---------------------------------|-----------------------|---------------------------------------------------------------|
| `SECURE_SECRET_KEY`             | Randomly generated    | Key value used to enforce cryptographic signing.              |
| `SECURE_ALLOWED_HOSTS`          | `localhost,127.0.0.1` | Comma-separated list of accepted host/domain names.           |
| `SECURE_SSL_REDIRECT`           | `False`               | Automatically redirect all HTTP traffic to HTTPS.             |
| `SECURE_SESSION_TOKENS`         | `False`               | Only issue session/CSRF tokens over secure connections.       |
| `SECURE_CSRF_ORIGINS`           | `[]`                  | Domains (with protocol) to accept CSRF headers from.          |
| `SECURE_HSTS_SECONDS`           | `0` (Disabled)        | HSTS cache duration in seconds.                               |
| `SECURE_HSTS_SUBDOMAINS`        | `False`               | Enable HSTS for subdomains.                                   |
| `SECURE_HSTS_PRELOAD`           | `False`               | Enable HSTS preload functionality.                            |
| `SECURE_ACCESS_TOKEN_LIFETIME`  | `300` (5 Minutes)     | JWT Access token lifetime in seconds.                         |
| `SECURE_REFRESH_TOKEN_LIFETIME` | `86400` (1 Day)       | JWT Refresh token lifetime in seconds.                        |

## General Configuration

Keystone uses various static files and user content to facilitate operation.
By default, these files are stored in subdirectories of the installed application directory (`<app>`).

| Setting Name              | Default Value            | Description                                                                                       |
|---------------------------|--------------------------|---------------------------------------------------------------------------------------------------|
| `CONFIG_TIMEZONE`         | `UTC`                    | The application timezone.                                                                         |
| `CONFIG_STATIC_DIR`       | `<app>/static_files`     | Where to store internal static files required by the application.                                 |
| `CONFIG_UPLOAD_DIR`       | `<app>/upload_files`     | Where to store file data uploaded by users.                                                       |
| `CONFIG_LOG_RETENTION`    | 30 days                  | How long to store log records in seconds. Set to 0 to keep all records.                           |
| `CONFIG_LOG_LEVEL`        | `WARNING`                | Only record logs above this level (`CRITICAL`, `ERROR`, `WARNING`, `INFO`, `DEBUG`, or `NOTSET`). |

## API Throttling

API settings are used to throttle incoming API requests against a maximum limit.
Limits are specified as the maximum number of requests per `day`, `minute`, `hour`, or `second`.

| Setting Name              | Default Value            | Description                                                   |
|---------------------------|--------------------------|---------------------------------------------------------------|
| `API_THROTTLE_ANON`       | `1000/day`               | Rate limiting for anonymous (unauthenticated) users.          |
| `API_THROTTLE_USER`       | `10000/day`              | Rate limiting for authenticated users.                        |

## Database Connection

Official support is included for both SQLite and PostgreSQL database backends.
Using SQLite is intended for development and demonstrative use-cases only.
The PostgreSQL backend should always be used in production settings.

| Setting Name              | Default Value            | Description                                                   |
|---------------------------|--------------------------|---------------------------------------------------------------|
| `DB_POSTGRES_ENABLE`      | `False`                  | Use PostgreSQL instead of the default Sqlite driver.          |
| `DB_NAME`                 | `keystone`               | The name of the application database.                         |
| `DB_USER`                 |                          | Username for database authentication (PostgreSQL only).       |
| `DB_PASSWORD`             |                          | Password for database authentication (PostgreSQL only).       |
| `DB_HOST`                 | `localhost`              | Database host address (PostgreSQL only).                      |
| `DB_PORT`                 | `5432`                   | Database host port (PostgreSQL only).                         |

## Redis Connection

Redis settings define the network location and connection information for the application Redis cache.
Enabling password authentication is recommended.

| Setting Name              | Default Value            | Description                                                   |
|---------------------------|--------------------------|---------------------------------------------------------------|
| `REDIS_HOST`              | `127.0.0.1`              | URL for the Redis message cache.                              |
| `REDIS_PORT`              | `6379`                   | Port number for the Redis message cache.                      |
| `REDIS_DB`                | `0`                      | The Redis database number to use.                             |
| `REDIS_PASSWORD`          |                          | Optionally connect using the given password.                  |

## Email Server

Keystone will default to using the local server when issuing email notifications.
Securing your production email server with a username/password is recommended, but not required.

| Setting Name              | Default Value            | Description                                                   |
|---------------------------|--------------------------|---------------------------------------------------------------|
| `EMAIL_HOST`              | `localhost`              | The host server to use for sending email.                     |
| `EMAIL_PORT`              | `25`                     | Port to use for the SMTP server.                              |
| `EMAIL_HOST_USER`         |                          | Username to use for the SMTP server.                          |
| `EMAIL_HOST_PASSWORD`     |                          | Password to use for the SMTP server.                          |
| `EMAIL_USE_TLS`           | `False`                  | Use a TLS connection to the SMTP server.                      |
| `EMAIL_FROM_ADDRESS`      | `noreply@keystone.bot`   | Use a TLS connection to the SMTP server.                      |

## LDAP Authentication

Enabling LDAP authentication is optional and disabled by default.
To enable LDAP, set the `AUTH_LDAP_SERVER_URI` value to the desired LDAP endpoint.

Application user fields are mapped to LDAP attributes by specifying the `AUTH_LDAP_ATTR_MAP` setting.
The following example maps the `first_name` and `last_name` fields used by Keystone to the LDAP attributes `givenName` and `sn`:

```bash
AUTH_LDAP_ATTR_MAP="first_name=givenName,last_name=sn"
```

See the `apps.users.models.User` class for a full list of available Keystone fields.

| Setting Name              | Default Value            | Description                                                       |
|---------------------------|--------------------------|-------------------------------------------------------------------|
| `AUTH_LDAP_SERVER_URI`    |                          | The URI of the LDAP server.                                       |
| `AUTH_LDAP_START_TLS`     | `True`                   | Whether to use TLS when connecting to the LDAP server.            |
| `AUTH_LDAP_BIND_DN`       |                          | Optionally bind LDAP queries to the given DN.                     |
| `AUTH_LDAP_BIND_PASSWORD` |                          | The password to use when binding to the LDAP server.              |
| `AUTH_LDAP_USER_SEARCH`   | `(uid=%(user)s)`         | The search query for finding a user in the LDAP server.           |
| `AUTH_LDAP_REQUIRE_CERT`  | `False`                  | Whether to require certificate verification.                      |
| `AUTH_LDAP_ATTR_MAP`      |                          | A mapping of user fields to LDAP attribute names.                 |
| `AUTH_LDAP_PURGE_REMOVED` | `False`                  | Delete users when removed from LDAP instead of deactivating them. |

## Developer Settings

The following settings are intended exclusively for use in development.

!!! danger

    The `DEBUG` option is inherently insecure and should **never** be enabled in production settings.

| Setting Name              | Default Value            | Description                                                   |
|---------------------------|--------------------------|---------------------------------------------------------------|
| `DEBUG`                   | `False`                  | Enable or disable in browser error tracebacks.                |
| `DEBUG_EMAIL_DIR`         | ``                       | Write emails to disk instead of using the SMTP server.        |
