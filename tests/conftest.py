import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

# This fixture creates an in-memory SQLite engine and rebinds the project's DB to it.
@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    # create a fresh in-memory engine
    test_engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
    )

    # Import the project's db module and swap the engine & SessionLocal
    import db
    db.engine = test_engine
    db.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

    # Create all tables on the test engine
    try:
        db.Base.metadata.create_all(bind=test_engine)
    except Exception:
        # If db.Base isn't available for any reason, let the error surface in tests
        raise

    yield

    # Tear down
    db.Base.metadata.drop_all(bind=test_engine)


# Provide a TestClient that will use the patched DB above.
@pytest.fixture
def client():
    from main import app
    with TestClient(app) as c:
        yield c
