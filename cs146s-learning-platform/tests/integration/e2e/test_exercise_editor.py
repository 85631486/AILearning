"""
E2E tests for exercise editor functionality
Tests autosave, lint, format, and execution workflows
"""

import pytest
import time
import json
from playwright.sync_api import Page, expect


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """Configure browser context for tests"""
    return {
        **browser_context_args,
        "viewport": {"width": 1280, "height": 720},
        "ignore_https_errors": True,
    }


@pytest.fixture
def authenticated_page(page: Page, test_app):
    """Create an authenticated page for testing"""
    # Start the test server
    with test_app.test_client() as client:
        # Create a test user and login
        from app.models import User, db
        from werkzeug.security import generate_password_hash

        with test_app.app_context():
            # Create test user if not exists
            test_user = User.query.filter_by(username='testuser').first()
            if not test_user:
                test_user = User(
                    username='testuser',
                    email='test@example.com',
                    password_hash=generate_password_hash('password123')
                )
                db.session.add(test_user)
                db.session.commit()

            # Create a test exercise
            from app.models import Exercise, Week
            test_week = Week.query.filter_by(week_number=1).first()
            if not test_week:
                test_week = Week(week_number=1, title='Test Week')
                db.session.add(test_week)
                db.session.commit()

            test_exercise = Exercise.query.filter_by(title='Test Exercise').first()
            if not test_exercise:
                test_exercise = Exercise(
                    week_id=test_week.id,
                    title='Test Exercise',
                    description='Test exercise for E2E testing',
                    initial_code='print("Hello World!")',
                    test_code='assert True',
                    difficulty='beginner',
                    points=10
                )
                db.session.add(test_exercise)
                db.session.commit()

            exercise_id = test_exercise.id

    # Navigate to login page and login
    page.goto("http://localhost:5000/login")
    page.fill('input[name="username"]', 'testuser')
    page.fill('input[name="password"]', 'password123')
    page.click('button[type="submit"]')

    # Wait for login to complete
    page.wait_for_url("**/weeks")

    # Navigate to the test exercise
    page.goto(f"http://localhost:5000/exercises/{exercise_id}")

    # Wait for editor to load
    page.wait_for_selector('#editor-container', timeout=10000)

    return page, exercise_id


class TestExerciseEditor:
    """Test exercise editor functionality"""

    def test_autosave_functionality(self, authenticated_page):
        """Test that code is automatically saved"""
        page, exercise_id = authenticated_page

        # Type some code
        page.click('#editor-container')
        page.keyboard.type('def test_function():\n    return "autosave test"')

        # Wait for autosave (should happen within 2 seconds)
        time.sleep(2)

        # Check that autosave indicator shows saved
        autosave_indicator = page.locator('#autosave-indicator')
        expect(autosave_indicator).to_contain_text('已保存')

        # Refresh page and check if code is restored
        page.reload()
        page.wait_for_selector('#editor-container', timeout=5000)

        # The editor should contain our code (this would require more complex checks)
        # For now, just verify the page loads without errors

    def test_code_execution(self, authenticated_page):
        """Test code execution functionality"""
        page, exercise_id = authenticated_page

        # Type executable code
        page.click('#editor-container')
        page.keyboard.press('Control+a')  # Select all
        page.keyboard.press('Delete')  # Clear
        page.keyboard.type('print("Hello, E2E Test!")\nprint(42)')

        # Click run button
        page.click('#runCodeBtn')

        # Wait for execution to complete
        page.wait_for_selector('.output-content', timeout=10000)

        # Check that output contains expected results
        output_content = page.locator('.output-content')
        expect(output_content).to_contain_text('Hello, E2E Test!')
        expect(output_content).to_contain_text('42')

    def test_lint_functionality(self, authenticated_page):
        """Test code linting and error highlighting"""
        page, exercise_id = authenticated_page

        # Type code with syntax error
        page.click('#editor-container')
        page.keyboard.press('Control+a')
        page.keyboard.press('Delete')
        page.keyboard.type('def broken_function(\nprint("missing closing paren")')

        # Wait for lint check
        time.sleep(2)

        # Check that lint panel shows errors
        lint_panel = page.locator('#lint-panel')
        expect(lint_panel).to_be_visible()

        lint_count = page.locator('#lint-count')
        expect(lint_count).to_have_text('1')

        # Check that error message is displayed
        lint_content = page.locator('#lint-content')
        expect(lint_content).to_contain_text('语法错误')

    def test_keyboard_shortcuts(self, authenticated_page):
        """Test keyboard shortcuts functionality"""
        page, exercise_id = authenticated_page

        # Focus editor
        page.click('#editor-container')

        # Test Ctrl+Enter (run code)
        page.keyboard.press('Control+Enter')

        # Should trigger run (we can check if run button gets disabled temporarily)
        run_btn = page.locator('#runCodeBtn')
        # Note: This might be tricky to test precisely due to timing

        # Test Ctrl+/ (comment toggle)
        page.keyboard.press('Control+/')
        # This would require checking if a comment was added

    def test_format_functionality(self, authenticated_page):
        """Test code formatting functionality"""
        page, exercise_id = authenticated_page

        # Type unformatted code
        page.click('#editor-container')
        page.keyboard.press('Control+a')
        page.keyboard.press('Delete')
        page.keyboard.type('def   test():\n  print("bad formatting")')

        # Click format button
        page.click('#formatCodeBtn')

        # Wait for formatting to complete
        time.sleep(2)

        # Check that code was formatted (this might use fallback formatting)
        # The exact behavior depends on whether black is installed

    def test_theme_toggle(self, authenticated_page):
        """Test theme switching functionality"""
        page, exercise_id = authenticated_page

        # Click settings button
        page.click('#editorSettingsBtn')

        # Click theme toggle
        page.click('text=切换到深色主题')

        # Check that theme indicator changes
        theme_indicator = page.locator('#theme-indicator')
        expect(theme_indicator).to_have_text('🌙')

    def test_line_numbers_toggle(self, authenticated_page):
        """Test line numbers toggle functionality"""
        page, exercise_id = authenticated_page

        # Click settings button
        page.click('#editorSettingsBtn')

        # Click line numbers toggle
        page.click('text=隐藏行号')

        # Check that indicator changes
        line_numbers_indicator = page.locator('#line-numbers-indicator')
        expect(line_numbers_indicator).to_have_text('📄')

    def test_error_recovery(self, authenticated_page):
        """Test error recovery and offline functionality"""
        page, exercise_id = authenticated_page

        # Type some code
        page.click('#editor-container')
        page.keyboard.type('print("test recovery")')

        # Simulate going offline (this is hard to test with playwright)
        # Instead, we can test that localStorage is used

        # Check that code is saved to localStorage (would require page.evaluate)
        local_storage_code = page.evaluate("""
            localStorage.getItem('exercise_{exercise_id}_draft');
        """.format(exercise_id=exercise_id))

        assert local_storage_code is not None
        data = json.loads(local_storage_code)
        assert 'code' in data
        assert 'print("test recovery")' in data['code']


class TestExerciseEditorIntegration:
    """Integration tests combining multiple features"""

    def test_complete_workflow(self, authenticated_page):
        """Test a complete exercise workflow"""
        page, exercise_id = authenticated_page

        # 1. Load exercise and verify editor loads
        expect(page.locator('#editor-container')).to_be_visible()

        # 2. Type some code
        page.click('#editor-container')
        page.keyboard.type('def fibonacci(n):\n    if n <= 1:\n        return n\n    return fibonacci(n-1) + fibonacci(n-2)\n\nprint(fibonacci(10))')

        # 3. Wait for autosave
        time.sleep(2)
        autosave_indicator = page.locator('#autosave-indicator')
        expect(autosave_indicator).to_contain_text('已保存')

        # 4. Run the code
        page.click('#runCodeBtn')
        page.wait_for_selector('.output-content', timeout=10000)
        output_content = page.locator('.output-content')
        expect(output_content).to_contain_text('55')  # fibonacci(10) = 55

        # 5. Test linting on good code
        lint_count = page.locator('#lint-count')
        # Should have 0 issues for correct code

        # 6. Submit the solution
        page.click('#submitBtn')

        # Handle confirmation dialog
        page.on('dialog', lambda dialog: dialog.accept())

        # Wait for submission result
        page.wait_for_selector('.alert', timeout=5000)

        # Should show success or appropriate result
        alert = page.locator('.alert')
        expect(alert).to_be_visible()


if __name__ == '__main__':
    # Allow running tests directly
    pytest.main([__file__, '-v'])
