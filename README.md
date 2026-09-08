# CLI Automation Framework

An enterprise-grade Python CLI Automation Framework designed for keyword-driven, data-driven, and environment-driven testing of command-line interfaces, SSH operations, databases, and filesystem interactions.

## Features

- **Keyword-Driven Architecture**: Reusable automation keywords for common operations
- **Data-Driven Testing**: Support for YAML, JSON, CSV, and Excel test data
- **Environment-Driven**: Configure behavior for QA, Stage, and Production environments
- **SSH Operations**: Secure SSH client with host key verification and key authentication
- **Database Support**: PostgreSQL integration with parameterized queries
- **Comprehensive Logging**: Structured logging with detailed execution traces
- **Allure Reporting**: Beautiful HTML reports with command output and results
- **Parallel Execution**: Support for pytest-xdist parallel test execution
- **Schema Validation**: JSON Schema validation with detailed error reporting
- **Collection-Time Validation**: Validate all test data before test execution
- **Soft Assertions**: Collect multiple assertion failures per test
- **CI/CD Ready**: Azure Pipelines integration with artifact collection
- **Security First**: Encrypted secrets management, parameterized SQL, safe command construction

## Requirements

- Python 3.12+
- PostgreSQL (for database testing)
- SSH access to target servers
- Virtual environment support

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/ilakal/cli_automation_python.git
cd cli_automation_python
```

### 2. Create Virtual Environment

**Linux/macOS:**
```bash
python3.12 -m venv venv
source venv/bin/activate
```

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure Environment

Copy the example environment file and update with your credentials:

```bash
cp .env.example .env
```

Edit `.env` with your configuration:

```env
# SSH Configuration
SSH_USERNAME=your_username
SSH_KEY_PATH=/path/to/private/key
SSH_KNOWN_HOSTS_PATH=/home/user/.ssh/known_hosts

# Database Configuration
DB_HOST=localhost
DB_PORT=5432
DB_NAME=testdb
DB_USERNAME=postgres
DB_PASSWORD=your_password

# Logging
LOG_LEVEL=INFO
```

### 5. SSH Setup

**Generate SSH Key Pair:**

```bash
ssh-keygen -t ed25519 -C "your_email@example.com" -f ~/.ssh/id_ed25519 -N ""
```

**Add Public Key to Target Server:**

```bash
ssh-copy-id -i ~/.ssh/id_ed25519.pub user@target_host
```

**Setup Known Hosts:**

```bash
ssh-keyscan -H target_host >> ~/.ssh/known_hosts
```

**Verify Known Hosts Entry:**

```bash
cat ~/.ssh/known_hosts | grep target_host
```

## Configuration

### Environment Configuration Files

Environment-specific YAML configuration in `config/`:

**config/qa.yaml:**
```yaml
environment: qa
servers:
  server1:
    host: qa-server-01.example.com
    port: 22
    username: qa_user
database:
  host: qa-db.example.com
  port: 5432
  name: qa_testdb
```

**config/stage.yaml:**
```yaml
environment: stage
servers:
  server1:
    host: stage-server-01.example.com
    port: 22
    username: stage_user
database:
  host: stage-db.example.com
  port: 5432
  name: stage_testdb
```

**config/prod.yaml:**
```yaml
environment: prod
servers:
  server1:
    host: prod-server-01.example.com
    port: 22
    username: prod_user
database:
  host: prod-db.example.com
  port: 5432
  name: prod_testdb
```

### Schema Mapping

Map test data files to their schemas in `schemas/schema_map.yaml`:

```yaml
services.yaml: services_schema.yaml
commands.yaml: commands_schema.yaml
users.json: users_schema.yaml
processes.csv: processes_schema.yaml
servers.xlsx: servers_schema.yaml
```

## Test Data

### YAML Format

**testdata/yaml/services.yaml:**
```yaml
- name: nginx
  status: running
  enabled: true
- name: postgresql
  status: running
  enabled: true
```

### JSON Format

**testdata/json/users.json:**
```json
[
  {
    "username": "admin",
    "role": "administrator",
    "active": true
  },
  {
    "username": "user1",
    "role": "viewer",
    "active": true
  }
]
```

### CSV Format

**testdata/csv/processes.csv:**
```
process_name,pid,status
sshd,1234,running
systemd,1,running
```

CSV loaders automatically add `_row` metadata with row number.

### Excel Format

**testdata/excel/servers.xlsx:**
Supports multiple sheets. Each row includes `_row` metadata.

## Running Tests

### Run All Tests

```bash
pytest
```

### Run Tests for Specific Environment

```bash
pytest --env=qa
pytest --env=stage
pytest --env=prod
```

### Run Specific Test Suite

```bash
pytest tests/smoke/
pytest tests/regression/
pytest tests/framework/
```

### Run with Verbose Output

```bash
pytest -v
```

### Run with Markers

```bash
pytest -m smoke
pytest -m regression
```

### Generate Allure Report

```bash
pytest --allure-dir=reports/allure-results
allure serve reports/allure-results
```

### Generate JUnit XML Report

```bash
pytest --junit-xml=reports/junit/results.xml
```

### Parallel Execution

Run tests in parallel with auto-detection of CPU count:

```bash
pytest -n auto
```

Run tests with specific number of workers:

```bash
pytest -n 4
```

## Framework Architecture

```
Tests
  ↓
Test Data (YAML, JSON, CSV, Excel)
  ↓
Data Loaders + Schema Validation
  ↓
Keywords (ServerKeywords, DatabaseKeywords, FilesystemKeywords)
  ↓
Assertions (Hard & Soft)
  ↓
Core Services
  ├── SSH Client (with host key verification)
  ├── Command Executor (timeout, retry, logging)
  ├── Database Client (parameterized queries)
  └── Config Manager (environment-specific)
```

## Framework Components

### ConfigManager

Loads environment-specific configuration:

```python
from framework.core.config_manager import ConfigManager

config = ConfigManager("qa")
server_host = config.get("servers.server1.host")
db_host = config.get("database.host")
```

### SecretsManager

Loads secrets from `.env` file:

```python
from framework.core.secrets_manager import SecretsManager

secrets = SecretsManager()
ssh_key_path = secrets.get("SSH_KEY_PATH")
db_password = secrets.get("DB_PASSWORD")
```

### SSHClient

Secure SSH client with host key verification:

```python
from framework.core.ssh_client import SSHClient

client = SSHClient(
    hostname="server.example.com",
    username="user",
    key_filename="/path/to/key",
    known_hosts_file="/path/to/known_hosts"
)

stdout, stderr = client.execute_command("whoami")
client.close()
```

### CommandExecutor

Execute commands with timeout and retry:

```python
from framework.core.command_executor import CommandExecutor

executor = CommandExecutor(ssh_client=client)

result = executor.execute(
    command="ls -la /tmp",
    timeout=30,
    retries=3
)
```

### DatabaseClient

PostgreSQL operations with parameterized queries:

```python
from framework.core.database import DatabaseClient

db = DatabaseClient(
    host="localhost",
    port=5432,
    database="testdb",
    user="postgres",
    password="password"
)

# Query with parameters
rows = db.query("SELECT * FROM users WHERE id = %s", (1,))

# Execute with parameters
db.execute("INSERT INTO users (name) VALUES (%s)", ("John",))

db.close()
```

### Keywords

Reusable automation keywords:

```python
# Server Operations
server_keywords.hostname(server_name)
server_keywords.service_status(server_name, service_name)
server_keywords.process_exists(server_name, process_name)

# Database Operations
database_keywords.record_count(query)
database_keywords.record_exists(query)

# Filesystem Operations
filesystem_keywords.file_exists(server_name, file_path)
filesystem_keywords.directory_exists(server_name, dir_path)
```

### Assertions

Hard and soft assertions:

```python
from framework.assertions.assertions import Assertions
from framework.assertions.soft_assertions import SoftAssertions

# Hard assertions
assertions = Assertions()
assertions.equals("actual", "expected", "Values should match")
assertions.contains("haystack", "needle", "Should contain substring")

# Soft assertions (collect failures)
soft = SoftAssertions()
soft.equals("actual", "expected")
soft.equals("another", "value")
soft.assert_all()  # Fails if any assertion failed
```

### Data Loaders

Load test data from various formats:

```python
from framework.dataloaders.loader_factory import LoaderFactory

loader_factory = LoaderFactory()

# Load YAML
services = loader_factory.load("testdata/yaml/services.yaml")

# Load JSON
users = loader_factory.load("testdata/json/users.json")

# Load CSV (includes _row metadata)
processes = loader_factory.load("testdata/csv/processes.csv")

# Load Excel (includes _row metadata)
servers = loader_factory.load("testdata/excel/servers.xlsx")
```

### Schema Validation

Validate test data against schemas:

```python
from framework.validators.schema_validator import SchemaValidator

validator = SchemaValidator()

# Validate single file
errors = validator.validate_file(
    "testdata/yaml/services.yaml",
    "schemas/services_schema.yaml"
)

# Validate all files (runs at pytest startup)
all_errors = validator.validate_all("schemas/schema_map.yaml")
```

## Writing Tests

### Smoke Test Example

**tests/smoke/test_hostname.py:**
```python
import pytest

@pytest.mark.smoke
def test_server_hostname(server_keywords):
    """Verify server hostname is accessible."""
    hostname = server_keywords.hostname("server1")
    assert hostname is not None
    assert len(hostname) > 0
```

### Data-Driven Test Example

**tests/regression/test_services.py:**
```python
import pytest
from framework.dataloaders.loader_factory import LoaderFactory

@pytest.fixture
def services_data():
    loader = LoaderFactory()
    return loader.load("testdata/yaml/services.yaml")

@pytest.mark.parametrize("service_data", 
    LoaderFactory().load("testdata/yaml/services.yaml"),
    ids=lambda x: x.get("name", "unknown")
)
def test_service_running(server_keywords, service_data):
    """Verify service is running."""
    status = server_keywords.service_status("server1", service_data["name"])
    assert status == "running"
```

### Database Test Example

**tests/regression/test_database.py:**
```python
@pytest.mark.regression
def test_user_count(database_keywords):
    """Verify user count is greater than zero."""
    count = database_keywords.record_count("SELECT COUNT(*) FROM users")
    assert count > 0
```

### Soft Assertions Example

**tests/regression/test_collection.py:**
```python
@pytest.mark.regression
def test_multiple_conditions(server_keywords, soft_assertions):
    """Verify multiple conditions with soft assertions."""
    soft_assertions.equals(server_keywords.hostname("server1"), "qa-server-01")
    soft_assertions.contains(
        server_keywords.service_status("server1", "nginx"),
        "running"
    )
    soft_assertions.assert_all()
```

## Security Model

### Secrets Management

- All secrets are loaded from `.env` file (never commit to git)
- `.env` is listed in `.gitignore`
- Use `SecretsManager` to access secrets at runtime
- Never hardcode passwords, tokens, or keys

### SSH Security

1. **Key Authentication**: Use SSH private keys, never passwords
2. **Host Key Verification**: Strict verification using `known_hosts` file
3. **No Auto-Add Policy**: Prevents MITM attacks
4. **Known Hosts Setup**:
   ```bash
   ssh-keyscan -H host.example.com >> ~/.ssh/known_hosts
   ```

### Command Execution Safety

- All command arguments are escaped using `shlex.quote()`
- Safe command construction via `SafeCommandBuilder`
- No shell injection vulnerabilities
- Timeout protection (default 30 seconds)

### Database Security

- All database queries use parameterized SQL
- No string concatenation in queries
- Connection credentials from `.env`
- Automatic connection cleanup

### CI/CD Security

- Secrets injected via Azure Pipelines secrets
- Never exposed in logs
- Test artifacts collected securely

## Adding New Test Data

1. Create data file in appropriate format:
   ```
   testdata/yaml/new_data.yaml
   testdata/json/new_data.json
   testdata/csv/new_data.csv
   testdata/excel/new_data.xlsx
   ```

2. Create schema file:
   ```
   schemas/new_data_schema.yaml
   ```

3. Add mapping to `schemas/schema_map.yaml`:
   ```yaml
   new_data.yaml: new_data_schema.yaml
   ```

4. Reference in tests via LoaderFactory

## Adding New Keywords

1. Create keyword class in `framework/keywords/`:
   ```python
   from framework.core.ssh_client import SSHClient
   
   class NewKeywords:
       def __init__(self, ssh_client: SSHClient):
           self.ssh_client = ssh_client
       
       def new_operation(self, arg1, arg2):
           """Perform new operation."""
           pass
   ```

2. Add fixture in `conftest.py`

3. Use in tests as fixture

## Best Practices

1. **Use Keywords, Not Direct Commands**: Always prefer keywords over direct command execution
2. **Parameterize Tests**: Use pytest parametrize for multiple test cases
3. **Meaningful Assertions**: Use descriptive assertion messages
4. **Soft Assertions for Multiple Checks**: Use soft assertions to collect all failures
5. **Logging**: All framework operations are logged automatically
6. **Cleanup**: Use database cleanup fixture for teardown
7. **Environment Awareness**: Use config fixture to get environment-specific values
8. **Type Hints**: Use type hints in all function signatures
9. **Docstrings**: Document complex operations
10. **Error Handling**: Let framework handle errors with proper logging

## Fixtures

### config
Provides environment-specific configuration:
```python
def test_something(config):
    host = config.get("servers.server1.host")
```

### ssh_client
Provides connected SSH client:
```python
def test_ssh(ssh_client):
    stdout, stderr = ssh_client.execute_command("whoami")
```

### executor
Provides command executor with retry logic:
```python
def test_command(executor):
    result = executor.execute("ls -la", timeout=30, retries=3)
```

### database
Provides database client:
```python
def test_db(database):
    rows = database.query("SELECT * FROM users WHERE id = %s", (1,))
```

### server_keywords
Provides server operations:
```python
def test_service(server_keywords):
    status = server_keywords.service_status("server1", "nginx")
```

### database_keywords
Provides database operations:
```python
def test_count(database_keywords):
    count = database_keywords.record_count("SELECT COUNT(*) FROM users")
```

### filesystem_keywords
Provides filesystem operations:
```python
def test_file(filesystem_keywords):
    exists = filesystem_keywords.file_exists("server1", "/tmp/test.txt")
```

## Reporting

### Allure Reports

Generate and serve Allure reports:

```bash
pytest --allure-dir=reports/allure-results
allure serve reports/allure-results
```

Reports automatically include:
- Command output
- Database query results
- Parsed operation results
- Execution timeline
- Test duration
- Pass/fail status

### JUnit XML Reports

Generate XML reports for CI/CD integration:

```bash
pytest --junit-xml=reports/junit/results.xml
```

## CI/CD Integration

### Azure Pipelines

The `azure-pipelines.yml` is configured for:

1. **Test Execution**: Runs tests across QA, Stage, and Prod
2. **Parallel Execution**: Uses pytest-xdist for parallel runs
3. **Allure Reports**: Generates and publishes Allure reports
4. **Artifacts**: Collects logs and reports
5. **Secrets**: Secure injection of SSH keys and credentials

### Running in Azure Pipelines

```yaml
- script: |
    pytest --env=qa -n auto --allure-dir=reports/allure-results
  displayName: 'Run Tests'
```

## Troubleshooting

### SSH Connection Issues

1. Verify SSH key permissions:
   ```bash
   chmod 600 ~/.ssh/id_ed25519
   ```

2. Verify known_hosts contains target host:
   ```bash
   ssh-keyscan -H target.example.com >> ~/.ssh/known_hosts
   ```

3. Test SSH connection manually:
   ```bash
   ssh -i ~/.ssh/id_ed25519 user@target.example.com whoami
   ```

### Database Connection Issues

1. Verify credentials in `.env`
2. Check PostgreSQL is running and accessible
3. Verify database exists and user has permissions
4. Test connection manually:
   ```bash
   psql -h localhost -U postgres -d testdb
   ```

### Schema Validation Failures

1. Check `schemas/schema_map.yaml` for correct mappings
2. Verify schema files exist in `schemas/` directory
3. Validate test data files match schema definitions
4. Check error messages in pytest output for specific failures

### Timeout Issues

1. Increase timeout in CommandExecutor calls:
   ```python
   executor.execute(command, timeout=60)
   ```

2. Check network connectivity to target servers
3. Review SSH key performance (ed25519 is faster than RSA)

## Contributing

1. Follow PEP8 style guide
2. Use type hints
3. Add docstrings to public methods
4. Write unit tests for new features
5. Update README with new capabilities

## License

Proprietary - Internal Use Only

## Support

For issues or questions, contact the automation team.
