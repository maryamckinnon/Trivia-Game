from fastapi.testclient import TestClient
from main import app
from postgres.db import CategoryQueries

client = TestClient(app)


class EmptyCategoryQueries:
    def get_category(self, id):
        return None


class NormalCategoryQueries:
    def get_category(self, id):
        return [id, "OUR CATEGORY", True]


# class CreateCategoryQueries:
#     def create_category(self, title):
#         return [id, title, canon]


class DeleteCategoryQueries:
    def delete_category(self, id):
        return {"result": True}


class UpdateCategoryQueries:
    def update_category(self, id, title):
        return [id, title, False]


def test_get_category_returns_404():
    app.dependency_overrides[CategoryQueries] = EmptyCategoryQueries
    response = client.get("api/postgres/categories/1")
    assert response.status_code == 404
    app.dependency_overrides = {}


def test_get_category_returns_200():
    app.dependency_overrides[CategoryQueries] = NormalCategoryQueries
    response = client.get("/api/postgres/categories/1")
    d = response.json()
    assert response.status_code == 200
    assert d["id"] == 1
    assert d["title"] == "OUR CATEGORY"
    assert d["canon"] == True
    app.dependency_overrides = {}


# def test_update_category_returns_200():
#     app.dependency_overrides[CategoryQueries] = UpdateCategoryQueries
#     response = client.put("/api/postgres/categories/1")
#     assert response.status_code == 200
#     app.dependency_overrides = {}


# def test_update_category_returns_404():
#     app.dependency_overrides[CategoryQueries] = UpdateCategoryQueries
#     response = client.put("/api/postgres/categories/1")
#     assert response.status_code == 404
#     app.dependency_overrides = {}
    

def test_delete_category_returns_true():
    app.dependency_overrides[CategoryQueries] = DeleteCategoryQueries
    response = client.delete("/api/postgres/categories/1")
    d = response.json()
    assert response.status_code == 200
    assert d["result"] == True
    app.dependency_overrides = {}


def test_delete_category_returns_false():
    app.dependency_overrides[CategoryQueries] = EmptyCategoryQueries
    response = client.delete("/api/postgres/categories/1")
    d = response.json()
    assert response.status_code == 200
    assert d["result"] == False
    app.dependency_overrides = {}