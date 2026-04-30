import swing.error.migrations as migrations


def test_migrations_module_imports() -> None:
    assert migrations is not None
