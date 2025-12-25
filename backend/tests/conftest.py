# tests/conftest.py
import sys
from pathlib import Path

# Add parent directory to Python path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

import pytest


@pytest.fixture
def client():
    """Create test client for FastAPI app"""
    from fastapi.testclient import TestClient
    from main import app
    
    return TestClient(app)


@pytest.fixture
def sample_store_url():
    """Sample Shopify store URL for testing"""
    return "https://gymshark.com"


@pytest.fixture
def invalid_url():
    """Invalid URL for testing validation"""
    return "not-a-valid-url"


@pytest.fixture
def non_shopify_url():
    """Non-Shopify URL for testing"""
    return "https://google.com"