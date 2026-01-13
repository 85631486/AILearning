"""
Test configuration and fixtures
"""

import pytest
import os
import tempfile
from flask import Flask
from app import create_app, db
from app.models import User, Exercise, Week


@pytest.fixture(scope='session')
def test_app():
    """Create and configure a test app instance."""
    # Create temporary database
    db_fd, db_path = tempfile.mkstemp()

    app = create_app('testing')

    # Override config for testing
    app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': f'sqlite:///{db_path}',
        'SECRET_KEY': 'test-secret-key',
        'WTF_CSRF_ENABLED': False,
        'QWEN_MOCK_MODE': True,
        'CODE_FORMAT_ENABLED': False,
    })

    with app.app_context():
        db.create_all()

        # Create test data
        _create_test_data()

    yield app

    # Cleanup
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture(scope='function')
def test_client(test_app):
    """A test client for the app."""
    return test_app.test_client()


@pytest.fixture(scope='function')
def authenticated_client(test_app):
    """A test client with an authenticated user."""
    client = test_app.test_client()

    with test_app.app_context():
        # Create test user
        user = User(
            username='testuser',
            email='test@example.com',
            password_hash='dummy_hash'  # In real tests, use proper hashing
        )
        db.session.add(user)
        db.session.commit()

        # Log in the user (this depends on your login implementation)
        with client:
            # This is a simplified login - adjust based on your auth system
            client.post('/login', data={
                'username': 'testuser',
                'password': 'password123'
            })

    return client


def _create_test_data():
    """Create test data for tests."""
    # Create a test week
    week = Week(week_number=1, title='Test Week')
    db.session.add(week)
    db.session.commit()

    # Create a test exercise
    exercise = Exercise(
        week_id=week.id,
        title='Test Exercise',
        description='A test exercise for automated testing',
        initial_code='print("Hello World!")',
        test_code='assert True',
        difficulty='beginner',
        points=10
    )
    db.session.add(exercise)
    db.session.commit()


# Playwright fixtures for E2E tests
@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """Configure browser context for E2E tests."""
    return {
        **browser_context_args,
        "viewport": {"width": 1280, "height": 720},
        "ignore_https_errors": True,
    }


@pytest.fixture
def authenticated_page(page, test_app):
    """Create an authenticated page for E2E testing."""
    # This fixture would need to be implemented based on your specific
    # authentication flow. For now, it returns the page.
    return page
