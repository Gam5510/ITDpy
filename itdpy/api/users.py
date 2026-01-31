from ..models import User, Me, Users

def get_me(client):
    r = client.get("/api/users/me")
    return Me(r.json())

def get_user(client, username):
    r = client.get(f"/api/users/{username}")
    return User(r.json())

def follow_user(client, username: str):
    r = client.post(f"/api/users/{username}/follow")
    r.raise_for_status()
    return True

def unfollow_user(client, username: str):
    r = client.delete(f"/api/users/{username}/follow")
    r.raise_for_status()
    return True

def get_followers(client, username: str, page: int = 1, limit: int = 30):
    r = client.get(
        f"/api/users/{username}/followers?page={page}&limit={limit}"
    )
    r.raise_for_status()
    return Users(r.json())

def get_following(client, username: str, page: int = 1, limit: int = 30):
    r = client.get(
        f"/api/users/{username}/following?page={page}&limit={limit}"
    )
    r.raise_for_status()
    return Users(r.json())