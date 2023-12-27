from fastapi.testclient import TestClient
from task3 import app

client = TestClient(app)
"""
Running these test requires that table Todo does not exist on current PostgreSQL server.
During testing, it will be created. After all tests, all recordings will be deleted (in case if all tests pass).
"""


def test_get_tasks():
    response = client.get("/tasks")
    assert response.status_code == 200
    assert response.json() == []


def test_add_tasks():
    response = client.put("/tasks", json=[{"task": "Do the homework", "status": True}])
    assert response.status_code == 200
    assert response.json() == [{"task_id": 1, "task": "Do the homework", "status": True}]

    response = client.put("/tasks", json=[{'task': "Go to gym", 'status': True}])
    assert response.status_code == 200
    assert response.json() == [{'task_id': 2, 'task': "Go to gym", 'status': True}]

    response = client.put("/tasks", json=[{'task': "Buy new clothes", 'status': True},
                                          {'task': "Wash the dishes", 'status': True}])
    assert response.status_code == 200
    assert response.json() == [{'task_id': 3, 'task': "Buy new clothes", 'status': True},
                               {'task_id': 4, 'task': "Wash the dishes", 'status': True}]

    response = client.put("/tasks", json=[{'task': "Go to gym", 'status': "Not done"}])
    assert response.status_code == 422

    response = client.put("/tasks", json=[{'status': "Not done"}])
    assert response.status_code == 422


def test_update_task():
    response = client.post("/tasks/1", json={"task": "Do the homework", "status": False})
    assert response.status_code == 200
    assert response.json() == {"task_id": 1, "task": "Do the homework", "status": False}

    response = client.post("/tasks/2", json={'task': "Go to gym twice", 'status': True})
    assert response.status_code == 200
    assert response.json() == {"task_id": 2, 'task': "Go to gym twice", 'status': True}

    response = client.post("/tasks/2", json={'task': "Go to gym", 'status': "Not done"})
    assert response.status_code == 422

    response = client.post("/tasks/5", json={'task': "Find Old Zealand", 'status': True})
    assert response.status_code == 404


def test_delete_task():
    response = client.delete("/tasks/1")
    assert response.status_code == 200
    assert response.json() is None

    response = client.delete("/tasks/2")
    assert response.status_code == 200
    assert response.json() is None

    response = client.delete("/tasks/3")
    assert response.status_code == 200
    assert response.json() is None

    response = client.delete("/tasks/4")
    assert response.status_code == 200
    assert response.json() is None

    response = client.delete("/tasks/5")
    assert response.status_code == 404


def test_int_to_roman():
    response = client.post("/int_to_roman/32")
    assert response.status_code == 200
    assert response.json() == "XXXII"

    response = client.post("/int_to_roman/54")
    assert response.status_code == 200
    assert response.json() == "LIV"

    response = client.post("/int_to_roman/1984")
    assert response.status_code == 200
    assert response.json() == "MCMLXXXIV"

    response = client.post("/int_to_roman/516")
    assert response.status_code == 200
    assert response.json() == "DXVI"

    response = client.post("/int_to_roman/2001")
    assert response.status_code == 200
    assert response.json() == "MMI"
