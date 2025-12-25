# tests/test_main.py
import pytest


def test_read_root(client):
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()


def test_health_check(client):
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_scan_valid_shopify_store(client, sample_store_url):
    """Test scanning a valid Shopify store"""
    response = client.post(
        "/scan",
        json={"store_url": sample_store_url}
    )
    assert response.status_code == 200
    data = response.json()
    assert "overall_score" in data
    assert "seo_score" in data
    assert isinstance(data["overall_score"], int)
    assert 0 <= data["overall_score"] <= 100


def test_scan_invalid_url(client, invalid_url):
    """Test scanning with invalid URL"""
    response = client.post(
        "/scan",
        json={"store_url": invalid_url}
    )
    assert response.status_code == 422


def test_scan_non_shopify_store(client, non_shopify_url):
    """Test scanning a non-Shopify store"""
    response = client.post(
        "/scan",
        json={"store_url": non_shopify_url}
    )
    assert response.status_code == 400