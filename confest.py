import pytest
import os
from ypostirizoclient import settings


@pytest.fixture(scope='session')
def django_db_setup():
    """Configs the database for running the tests"""
    settings.DATABASES['default']['NAME'] = os.path.join(settings.BASE_DIR, 'test_db.sqlite3')
