from backend.app.core.config import Settings


def test_settings_defaults(monkeypatch):
    monkeypatch.setenv(
        "DATABASE_URL",
        "postgresql+psycopg://test:test@localhost:5432/test",
    )

    settings = Settings(_env_file=None)

    assert settings.app_name == "Rijeka Transit API"
    assert settings.app_version == "0.1.0"
    assert settings.autotrolej_username == ""
    assert settings.autotrolej_password == ""
    assert settings.database_url == "postgresql+psycopg://test:test@localhost:5432/test"


def test_settings_can_be_overridden_by_environment(monkeypatch):
    monkeypatch.setenv("APP_NAME", "Test Transit API")
    monkeypatch.setenv("AUTOTROLEJ_USERNAME", "test-user")
    monkeypatch.setenv("AUTOTROLEJ_PASSWORD", "test-password")
    monkeypatch.setenv(
        "DATABASE_URL",
        "postgresql+psycopg://test:test@localhost:5432/test",
    )

    settings = Settings(_env_file=None)

    assert settings.app_name == "Test Transit API"
    assert settings.autotrolej_username == "test-user"
    assert settings.autotrolej_password == "test-password"
    assert settings.database_url == "postgresql+psycopg://test:test@localhost:5432/test"
