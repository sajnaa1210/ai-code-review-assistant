from server import app


def test_health_endpoint():
    with app.test_client() as client:
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json == {"status": "ok"}


def test_review_endpoint_mock_mode():
    with app.test_client() as client:
        response = client.post(
            "/review",
            json={"code": "def f():\n    return 1", "use_mock": True},
        )
        assert response.status_code == 200
        assert isinstance(response.json.get("score"), int)
        assert isinstance(response.json.get("issues"), list)


def test_review_endpoint_without_code():
    with app.test_client() as client:
        response = client.post("/review", json={})
        assert response.status_code == 400
        assert "error" in response.json
