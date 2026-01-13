# CS146S Learning Platform - Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Architecture Improvements

#### Models Package Refactoring
- **BREAKING**: Split monolithic `app/models.py` into package structure
- **NEW**: `app/models/` package with individual model modules:
  - `user.py` - User model and authentication methods
  - `week.py` - Learning week/course structure
  - `exercise.py` - Exercise and assignment definitions
  - `submission.py` - User code submissions
  - `user_progress.py` - Learning progress tracking
  - `ai_conversation.py` - AI assistant conversation logs
  - `system_config.py` - System configuration settings
  - `autosave.py` - User code auto-save functionality
  - `assignment_file.py` - Assignment file management
- **COMPATIBILITY**: Backward compatibility maintained via `app/models.py` shim
- **FIXED**: Renamed `metadata` field to `metadata_json` in AutoSave model (SQLAlchemy reserved word conflict)

#### Services Package Refactoring
- **BREAKING**: Reorganized `app/services/` into package-per-service structure
- **NEW**: Service packages with modular organization:
  - `auth_service/` - User authentication and authorization
  - `ai_assistant/` - AI-powered learning assistance
  - `assignment_manager/` - Assignment file management
  - `code_executor/` - Secure code execution
  - `exercise_service/` - Exercise management and validation
  - `progress_tracker/` - Learning progress analytics
- **COMPATIBILITY**: Original single-file imports remain functional via shim files

#### Testing Infrastructure Overhaul
- **NEW**: Reorganized test structure for better maintainability:
  - `tests/unit/` - Unit tests for individual components
  - `tests/integration/` - Integration tests for component interactions
  - `tests/integration/e2e/` - End-to-end user journey tests
- **IMPROVED**: Added pytest markers for selective test execution:
  - `@pytest.mark.unit` - Unit tests
  - `@pytest.mark.integration` - Integration tests
  - `@pytest.mark.service` - Service layer tests
- **CONFIG**: Updated `pytest.ini` with test type filtering and E2E test exclusion by default

#### Configuration Management
- **NEW**: `env.example` - Comprehensive environment variable documentation
- **DOCUMENTED**: All configuration options with defaults and descriptions
- **GUIDANCE**: Setup instructions for different environments (dev/test/prod)

#### Application Context Fixes
- **FIXED**: Delayed service initialization to avoid Flask application context errors
- **IMPROVED**: Routes now use lazy service instantiation via helper functions
- **STABILITY**: Eliminated runtime errors during app initialization

### Developer Experience

#### Import Path Updates
- **UPDATED**: All internal imports to use new package structure
- **MAINTAINED**: Backward compatibility for existing code
- **CLEANED**: Removed duplicate `db` imports from service files

#### Code Quality
- **FIXED**: Syntax errors in code executor (duplicate `delete` parameter)
- **FIXED**: Missing `ast` import in exercise service
- **IMPROVED**: Consistent import organization across modules

## Migration Guide

### For Existing Code

1. **No immediate action required** - backward compatibility shims maintain functionality
2. **Gradually migrate imports** to new package structure:
   ```python
   # Old (still works)
   from app.models import User
   from app.services.auth_service import AuthService

   # New (recommended)
   from app.models.user import User
   from app.services.auth_service import AuthService
   ```

3. **Update environment variables** - copy `env.example` to `.env` and configure

### For New Development

1. **Use package imports** for better organization and IDE support
2. **Follow service package pattern** for new services
3. **Add appropriate test markers** (`@pytest.mark.unit`, `@pytest.mark.integration`)
4. **Reference `env.example`** for configuration options

### Testing

```bash
# Run all unit tests
pytest tests/unit/ -m unit

# Run integration tests
pytest tests/integration/ -m integration

# Run service-specific tests
pytest tests/unit/ -m service

# Run with coverage
pytest --cov=app --cov-report=html
```

## Previous Versions

- No previous versioned releases. This is the first major architectural refactor.
