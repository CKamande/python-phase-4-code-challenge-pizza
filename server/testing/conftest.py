#!/usr/bin/env python3
import pytest
from server import create_app, db  # Adjust this if needed

def pytest_itemcollected(item):
    par = item.parent.obj
    node = item.obj
    pref = par.__doc__.strip() if par.__doc__ else par.__class__.__name__
    suf = node.__doc__.strip() if node.__doc__ else node.__name__
    if pref or suf:
        item._nodeid = ' '.join((pref, suf))


@pytest.fixture(scope='session')
def test_app():
    """Create and configure a new app instance once per test session."""
    app = create_app({
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'TESTING': True,
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
    })

    with app.app_context():
        yield app


@pytest.fixture(scope='function')
def init_database(test_app):
    """Set up and tear down the database for each test function."""
    db.create_all()
    yield db
    db.session.remove()
    db.drop_all()


@pytest.fixture(scope='function')
def client(test_app):
    """A test client for the app (clean per test)."""
    return test_app.test_client()
