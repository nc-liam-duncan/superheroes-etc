import pytest
import json
from src.main import app
from src.db.seed import seed
from fastapi.testclient import TestClient


@pytest.fixture(autouse=True)
def reseed_db():
    with open("src/data/test/teams.json", "r", encoding="utf-8") as file:
        teams_data = json.load(file)

    with open("src/data/test/superheroes.json", "r", encoding="utf-8") as file:
        superheroes_data = json.load(file)

    seed(teams_data, superheroes_data)


@pytest.fixture
def test_client():
    return TestClient(app)


class TestHealthCheck():
    def test_health_check_response(self, test_client):
        response = test_client.get("/healthcheck")
        assert response.status_code == 200
        assert response.json() == {"msg": "server up and running!"}


class TestGetSuperheroes():
    def test_200_responds_with_list_of_superheroes(self, test_client):
        response = test_client.get("/api/superheroes")
        assert response.status_code == 200
        superheroes = response.json()["superheroes"]
        assert len(superheroes) == 4
        for hero in superheroes:
            assert isinstance(hero["superhero_id"], int)
            assert isinstance(hero["alias"], str)
            assert isinstance(hero["real_name"], str)
            assert isinstance(hero["is_identity_secret"], bool)
            assert isinstance(hero["image_url"], str)
            assert isinstance(hero["team_id"], int)

    def test_secret_identity_query_filters_superheroes(self, test_client):
        response = test_client.get("/api/superheroes?is_identity_secret=false")
        superheroes = response.json()["superheroes"]
        assert len(superheroes) == 3
        for hero in superheroes:
            assert hero["is_identity_secret"] is False

    def test_400_secret_identity_query_given_non_bool_value(self, test_client):
        response = test_client.get("/api/superheroes?is_identity_secret=YEET")
        error_response = response.json()
        assert response.status_code == 400
        assert error_response \
            == {"detail": "invalid type for is_identity_secret query"}


class TestPostSuperhero():
    def test_201_responds_with_posted_superhero(self, test_client):
        request_body = {
            "alias": "Bolin",
            "real_name": "Bolin",
            "is_identity_secret": False,
            "image_url": "bolin.com/bolin.png",
            "team_id": 1
        }
        response = test_client.post("/api/superheroes", json=request_body)
        superhero = response.json()["new_superhero"]
        assert response.status_code == 201
        assert len(superhero) >= 5
        for key in superhero:
            if key == "superhero_id":
                assert isinstance(superhero[key], int)
            else:
                assert superhero[key] == request_body[key]
