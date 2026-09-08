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

## Quick Start

```bash
# Clone repository
git clone https://github.com/ilakal/cli_automation_python.git
cd cli_automation_python

# Create virtual environment
python3.12 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your credentials

# Run tests
pytest --env=qa
```

## Running Tests

```bash
# Run all tests
pytest

# Run specific environment
pytest --env=qa
pytest --env=stage
pytest --env=prod

# Run with Allure reports
pytest --allure-dir=reports/allure-results
allure serve reports/allure-results

# Parallel execution
pytest -n auto
```

See [README.md](README.md) for complete documentation.
