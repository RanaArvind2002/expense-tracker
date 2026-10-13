import pytest
from app import app as flask_app
from database.db import init_db, seed_db


@pytest.fixture
def app():
    flask_app.config.update({
        'TESTING': True,
        'DATABASE': ':memory:',
        'SECRET_KEY': 'test-secret',
        'WTF_CSRF_ENABLED': False,
    })
    with flask_app.app_context():
        init_db()
        seed_db()
        yield flask_app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def auth_client(client):
    client.post('/register', data={
        'name': 'Demo User',
        'email': 'demo@spendly.com',
        'password': 'demo123',
        'confirm_password': 'demo123',
    })
    client.post('/login', data={
        'email': 'demo@spendly.com',
        'password': 'demo123',
    })
    return client


class TestProfileDateFilter:
    def test_unauthenticated_profile_redirects_to_login(self, client):
        response = client.get('/profile', follow_redirects=False)
        assert response.status_code == 302
        assert '/login' in response.headers.get('Location', '')

    def test_logged_in_profile_loads_user_info(self, auth_client):
        response = auth_client.get('/profile')
        assert response.status_code == 200
        assert b'Demo User' in response.data
        assert b'demo@spendly.com' in response.data

    def test_no_filter_shows_all_transactions_and_stats(self, auth_client):
        response = auth_client.get('/profile')
        assert response.status_code == 200
        assert b'Lunch' in response.data
        assert b'Dinner' in response.data
        assert b'Food' in response.data

    def test_start_date_only_filters_correctly(self, auth_client):
        response = auth_client.get('/profile?start_date=2026-10-05')
        assert response.status_code == 200
        assert b'Electricity' in response.data
        assert b'Lunch' not in response.data

    def test_end_date_only_filters_correctly(self, auth_client):
        response = auth_client.get('/profile?end_date=2026-10-03')
        assert response.status_code == 200
        assert b'Bus ticket' in response.data
        assert b'Electricity' not in response.data

    def test_both_dates_filter_range(self, auth_client):
        response = auth_client.get('/profile?start_date=2026-10-05&end_date=2026-10-07')
        assert response.status_code == 200
        assert b'Electricity' in response.data
        assert b'Pharmacy' in response.data
        assert b'Movie' not in response.data

    def test_filter_form_retains_start_date(self, auth_client):
        response = auth_client.get('/profile?start_date=2026-10-11')
        assert response.status_code == 200
        assert b'value="2026-10-11"' in response.data

    def test_filter_form_retains_end_date(self, auth_client):
        response = auth_client.get('/profile?end_date=2026-10-07')
        assert response.status_code == 200
        assert b'value="2026-10-07"' in response.data

    def test_filter_form_retains_both_dates(self, auth_client):
        response = auth_client.get('/profile?start_date=2026-10-01&end_date=2026-10-15')
        assert response.status_code == 200
        assert b'value="2026-10-01"' in response.data
        assert b'value="2026-10-15"' in response.data

    def test_neither_date_shows_empty_form_values(self, auth_client):
        response = auth_client.get('/profile')
        assert response.status_code == 200
        assert b'name="start_date"' in response.data
        assert b'name="end_date"' in response.data

    def test_sql_injection_attempt_does_not_crash(self, auth_client):
        response = auth_client.get("/profile?start_date=' OR '1'='1")
        assert response.status_code == 200

    def test_stats_respond_to_date_filter(self, auth_client):
        full = auth_client.get('/profile')
        filtered = auth_client.get('/profile?start_date=2026-10-11')
        assert full.status_code == 200
        assert filtered.status_code == 200
        assert b'Total spent' in full.data
        assert b'Total spent' in filtered.data

    def test_transactions_table_present_with_filter(self, auth_client):
        response = auth_client.get('/profile?start_date=2026-10-13')
        assert response.status_code == 200
        assert b'Gift' in response.data
        assert b'New shoes' not in response.data
