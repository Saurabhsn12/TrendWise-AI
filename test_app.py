from main import app

def test_signup():
  tester = app.test_client()
  data = {
    "Username": "Steve",
    "Email": "stevemichael681@gmail.com",
    "Password": "steve"
  }
  response = tester.get("/home", json = data)
  assert response.status_code == 405

def test_login():
  tester = app.test_client()
  data = {