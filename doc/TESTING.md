# Testing Guide for CredMarket

This guide explains how to write, run, and maintain tests for the CredMarket project.

## Table of Contents

1. [Overview](#overview)
2. [Test Setup](#test-setup)
3. [Running Tests](#running-tests)
4. [Writing Tests](#writing-tests)
5. [Pre-Push Hook](#pre-push-hook)
6. [Coverage Reports](#coverage-reports)
7. [Best Practices](#best-practices)

## Overview

CredMarket uses **pytest** and **pytest-django** for testing. We aim for:
- **Minimum 50% code coverage** before pushing to production
- Tests for all critical features (authentication, listings, messaging, admin)
- Automated testing via Git pre-push hooks

## Test Setup

### Install Testing Dependencies

```bash
# Install from requirements.txt
pip install -r requirements.txt
```

Testing packages included:
- `pytest` - Modern Python testing framework
- `pytest-django` - Django integration for pytest
- `pytest-cov` - Coverage reporting
- `coverage` - Code coverage measurement
- `factory-boy` - Test data factories (optional)
- `faker` - Fake data generation (optional)

### Configuration Files

- **pytest.ini** - Pytest configuration and settings
- **.coveragerc** - Coverage reporting configuration
- **conftest.py** - Shared fixtures and test setup

## Running Tests

### Run All Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run with coverage report
pytest --cov
```

### Run Specific Tests

```bash
# Run tests for a specific app
pytest accounts/tests.py

# Run a specific test class
pytest accounts/tests.py::UserAuthenticationTests

# Run a specific test method
pytest accounts/tests.py::UserAuthenticationTests::test_login_with_valid_credentials

# Run tests matching a pattern
pytest -k "login"
```

### Run Tests with Options

```bash
# Stop on first failure
pytest -x

# Show local variables in tracebacks
pytest -l

# Run without coverage (faster)
pytest --no-cov

# Run only failed tests from last run
pytest --lf

# Run tests in parallel (requires pytest-xdist)
pytest -n auto
```

## Writing Tests

### Test File Structure

Each Django app has a `tests.py` file:
```
accounts/
  tests.py          # All tests for accounts app
companies/
  tests.py          # All tests for companies app
listings/
  tests.py          # All tests for listings app
messaging/
  tests.py          # All tests for messaging app
```

### Test Classes

Organize tests into classes by functionality:

```python
from django.test import TestCase

class UserAuthenticationTests(TestCase):
    """Tests for user authentication."""
    
    def setUp(self):
        """Set up test data."""
        # Create test data here
        pass
    
    def test_login_with_valid_credentials(self):
        """Test login with valid credentials."""
        # Test implementation
        pass
    
    def test_login_with_invalid_credentials(self):
        """Test login with invalid credentials."""
        # Test implementation
        pass
```

### Common Test Patterns

#### Testing Views

```python
from django.test import Client
from django.urls import reverse

def test_view_loads(self):
    """Test that a view loads successfully."""
    response = self.client.get(reverse('app:view_name'))
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, 'Expected Text')
```

#### Testing Authentication

```python
def test_requires_authentication(self):
    """Test that view requires authentication."""
    response = self.client.get(reverse('app:protected_view'))
    # Should redirect to login
    self.assertEqual(response.status_code, 302)

def test_authenticated_access(self):
    """Test authenticated user can access view."""
    self.client.login(email='test@example.com', password='password')
    response = self.client.get(reverse('app:protected_view'))
    self.assertEqual(response.status_code, 200)
```

#### Testing Models

```python
def test_create_model(self):
    """Test creating a model instance."""
    obj = MyModel.objects.create(
        field1='value1',
        field2='value2'
    )
    self.assertEqual(obj.field1, 'value1')
    self.assertTrue(obj.is_active)
```

#### Testing Forms

```python
def test_valid_form(self):
    """Test form with valid data."""
    form = MyForm(data={
        'field1': 'valid_value',
        'field2': 'valid_value'
    })
    self.assertTrue(form.is_valid())

def test_invalid_form(self):
    """Test form with invalid data."""
    form = MyForm(data={})
    self.assertFalse(form.is_valid())
```

### Using Fixtures

Fixtures in `conftest.py` can be used in tests:

```python
def test_with_user(test_user):
    """Test using the test_user fixture."""
    assert test_user.email == 'testuser@testcorp.com'

def test_with_authenticated_client(authenticated_client):
    """Test using authenticated client fixture."""
    response = authenticated_client.get('/profile/')
    assert response.status_code == 200
```

## Pre-Push Hook

### What is it?

The pre-push hook automatically runs tests before allowing a push to the repository. This ensures:
- No broken code is pushed to production
- Tests are run consistently
- Code quality is maintained

### Installation

On **Windows (PowerShell)**:
```powershell
.\install_hooks.ps1
```

On **Linux/Mac**:
```bash
chmod +x install_hooks.sh
./install_hooks.sh
```

### How it Works

When you run `git push`:
1. Git triggers the pre-push hook
2. Hook runs: `pytest --no-cov-on-fail --cov-fail-under=50 -x`
3. If tests **pass** (and coverage ≥ 50%): Push proceeds
4. If tests **fail**: Push is aborted with error message

### Bypassing the Hook (Emergency Only)

```bash
# Not recommended for production!
git push --no-verify
```

⚠️ **Warning**: Only bypass the hook in emergencies. Pushing failing tests to production can break the application.

## Coverage Reports

### Viewing Coverage

After running tests with coverage:

```bash
# Terminal coverage report
pytest --cov

# HTML coverage report (more detailed)
pytest --cov --cov-report=html
```

Open `htmlcov/index.html` in a browser to see detailed coverage.

### Coverage Configuration

Configured in `.coveragerc`:
- Excludes: migrations, tests, utility scripts, settings
- Minimum coverage: 50% (enforced by pre-push hook)

### Improving Coverage

1. Identify uncovered code:
   ```bash
   pytest --cov --cov-report=term-missing
   ```

2. Write tests for uncovered areas

3. Focus on:
   - Critical business logic
   - Authentication/authorization
   - Data validation
   - Error handling

## Best Practices

### Test Naming

- Use descriptive names: `test_login_with_valid_credentials`
- Start with `test_` prefix
- Describe what is being tested and expected outcome

### Test Organization

- One test file per Django app
- Group related tests in classes
- Use `setUp()` for common test data
- Keep tests independent (don't rely on test order)

### Test Data

- Create minimal data needed for each test
- Use fixtures for common test data
- Consider using factory-boy for complex objects
- Clean up after tests (Django handles this automatically)

### What to Test

✅ **Do Test:**
- View responses and redirects
- User authentication and permissions
- Model creation and validation
- Form validation
- Business logic
- API endpoints
- Error handling

❌ **Don't Test:**
- Django's built-in functionality
- Third-party packages
- Database operations (unless custom)

### Test Performance

- Keep tests fast (use SQLite for testing)
- Mock external services (email, APIs)
- Use `pytest -x` to stop on first failure
- Run specific tests during development
- Run full suite before pushing

### Continuous Improvement

- Write tests for new features
- Write tests when fixing bugs
- Update tests when requirements change
- Review and refactor old tests
- Increase coverage gradually

## Troubleshooting

### Tests Fail to Run

```bash
# Check Django settings
python manage.py check

# Ensure test database can be created
pytest --create-db

# Clear pytest cache
pytest --cache-clear
```

### Import Errors

```bash
# Ensure all dependencies installed
pip install -r requirements.txt

# Check PYTHONPATH
echo $PYTHONPATH  # Linux/Mac
echo $env:PYTHONPATH  # PowerShell
```

### Coverage Not Working

```bash
# Reinstall coverage
pip install --upgrade coverage pytest-cov

# Check .coveragerc configuration
cat .coveragerc
```

## Quick Reference

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov

# Run specific app
pytest accounts/tests.py

# Run and stop on first failure
pytest -x

# Run with verbose output
pytest -v

# Generate HTML coverage report
pytest --cov --cov-report=html

# Install pre-push hook
./install_hooks.ps1  # Windows
./install_hooks.sh   # Linux/Mac
```

## Next Steps

1. **Install the pre-push hook**: `./install_hooks.ps1`
2. **Run the test suite**: `pytest --cov`
3. **Review coverage**: Open `htmlcov/index.html`
4. **Write missing tests**: Focus on uncovered critical areas
5. **Push with confidence**: Let the hook validate your code

---

**Remember**: Tests are your safety net. Write them, run them, and trust them!
