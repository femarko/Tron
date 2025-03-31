import pytest
from fastapi.testclient import TestClient

from src.entrypoints import web


@pytest.fixture
def test_client():
    return TestClient(web.app)
