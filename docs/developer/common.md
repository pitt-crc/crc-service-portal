# Common Developer Tasks

The following sections outline common tasks for application developers and contributors.

## Python Environment Setup

Start by cloning the project repository from GitHub.

```bash
git clone https://github.com/pitt-crc/keystone-api
```

Keystone-API uses [Poetry](https://python-poetry.org/docs/) to manage application dependencies.
Certain dependencies, such as those required for building documentation, are optional.
To install the project dependencies, execute the following command from the root of the cloned repository:

```bash
poetry install --all-extras
```

The API package itself is installed using the `pip` command.
The use of editable mode (`-e`) is recommended:

```bash
pip install -e .
```

If the installation was successful, the packaged CLI tool will be available in your working environment.
Use the `enable_autocomplete` command to enable autocomplete for the Bash shell.

```bash
keystone-api enable_autocomplete
```

## CLI Utilities

Keystone-API comes bundled with the `keystone-api` utility which wraps the standard Django management script.
Use the `runserver` command to launch a development API server:

```bash
keystone-api runserver
```

In addition to the standard Django commands, `keystone-api` includes the following custom commands for automating development tasks.
Use the `keystone-api <command> --help` option for specific usage information.

| Command                   | Description                                                                              |
|---------------------------|------------------------------------------------------------------------------------------|
| `clean`                   | Clean up files generated when launching a new application instance.                      |
| `quickstart`              | A helper utility for quickly migrating/deploying an application instance.                |

## Running In Debug Mode

The Django framework provides a debug mode which enables detailed error tracebacks directly in the browser.
To enable debug mode, specify the `DEBUG=true` setting.

!!! danger

    The `DEBUG` option is inherently insecure and should **never** be enabled in production settings.

```bash
DEBUG=True keystone-api runserver
```

## Tests and System Checks

Application tests are executed using the `test` command:

```bash
keystone-api test
```

Subsets of tests are run by specifying the desired application module(s) relative to the package root.
For example, tests under the `apps/users` and `apps/allocations` directories are executed as:

```bash
keystone-api test apps.users apps.allocations
```

Higher level system checks are available using the standard Django commands:

```bash
keystone-api check #(1)! 
keystone-api makemigrations --check #(2)! 
keystone-api health_check #(3)! 
```

1. Check for system configuration errors
2. Check for missing database migrations
3. Check the status of backend services

## OpenAPI Generation

The `spectacular` command will dynamically generate an OpenAPI schema in YAML format.
Rendering the specification into HTML is left to the developer and the documentation tool of their choice.

```bash
keystone-api spectacular --file api.yml
```
