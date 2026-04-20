import pytest
from fastapi.testclient import TestClient
from app.main import app, is_valid_title, is_valid_priority

client = TestClient(app)

# ==========================================
# 1. UNIT TESTING (Minimal 15 Case)
# ==========================================

# Mengetes logika validasi judul (7 Skenario)
@pytest.mark.parametrize("title,expected", [
    ("Study", True),           # Valid
    ("Fix Bug", True),         # Valid
    ("A", False),              # Terlalu pendek
    ("Ab", False),             # Terlalu pendek
    ("", False),               # Kosong
    ("Judul yang sangat panjang sekali lebih dari lima puluh karakter", False), # Terlalu panjang
    ("Makan", True)            # Valid
])
def test_title_validation(title, expected):
    assert is_valid_title(title) == expected

# Mengetes logika validasi prioritas (8 Skenario)
@pytest.mark.parametrize("priority,expected", [
    (1, True), (2, True), (3, True),   # Valid
    (0, False),                        # Di bawah batas
    (4, False),                        # Di atas batas
    (-1, False),                       # Angka negatif
    (100, False),                      # Angka terlalu besar
    (2, True)                          # Valid lagi (pelengkap kuota 15)
])
def test_priority_validation(priority, expected):
    assert is_valid_priority(priority) == expected

# ==========================================
# 2. INTEGRATION TESTING (Minimal 5 Case)
# ==========================================

def test_api_create_task_success():
    response = client.post("/tasks", json={"id": 1, "title": "UAS Testing", "priority": 1})
    assert response.status_code == 201

def test_api_get_all_tasks():
    response = client.get("/tasks")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_api_create_invalid_task():
    # Mengetes apakah API menolak input yang salah (judul terlalu pendek)
    response = client.post("/tasks", json={"id": 2, "title": "X", "priority": 1})
    assert response.status_code == 400

def test_api_delete_existing_task():
    # Buat dulu tasknya, lalu hapus
    client.post("/tasks", json={"id": 10, "title": "Delete Me", "priority": 1})
    response = client.delete("/tasks/10")
    assert response.status_code == 200

def test_api_delete_non_existent_task():
    # Mencoba hapus ID yang tidak ada
    response = client.delete("/tasks/999")
    assert response.status_code == 404