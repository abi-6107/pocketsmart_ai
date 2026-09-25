from fastapi.testclient import TestClient
from main import app
from app.services.database import init_db
init_db()
client=TestClient(app)

def test_home():
    r=client.get("/")
    assert r.status_code==200
    assert "PocketSmart" in r.text

def test_startup():
    r=client.get("/startup")
    assert r.status_code==200
    assert r.json()["status"]=="ok"

def test_register_login_flow():
    username="test_user_unique"
    r=client.post("/register",data={"username":username,"email":username+"@example.com","password":"secret123","confirm_password":"secret123"},follow_redirects=False)
    assert r.status_code==303
    r=client.post("/login",data={"username":username,"password":"secret123"},follow_redirects=False)
    assert r.status_code==303
