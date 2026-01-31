from ..models import Posts, Post

def get_posts(client, limit: int = 20, tab: str = "popular"):
    r = client.get(f"/api/posts?limit={limit}&tab={tab}")
    r.raise_for_status()

    return Posts(r.json())

def get_post(client, post_id: str):
    r = client.get(f"/api/posts/{post_id}")
    return Post(r.json())

def create_post(client,content: str = "",attachment_ids: list[str] | str | None = None,wall_recipient_id: str | None = None):

    if attachment_ids is None:
        attachment_ids = []
    elif isinstance(attachment_ids, str):
        attachment_ids = [attachment_ids]

    payload = {
        "content": content,
        "attachmentIds": attachment_ids
    }

    if wall_recipient_id is not None:
        payload["wallRecipientId"] = wall_recipient_id

    r = client.post(
        "/api/posts",
        json=payload
    )

    r.raise_for_status()
    return Post(r.json())

def update_post(client, post_id: str, content: str):
    payload = {
        "content": content
    }

    r = client.put(
        f"/api/posts/{post_id}",
        json=payload
    )

    r.raise_for_status()
    return r.json()

def delete_post(client, post_id: str) -> bool:
    r = client.delete(f"/api/posts/{post_id}")

    if r.status_code == 204:
        return True

    r.raise_for_status()
    return False

def like_post(client, post_id: str):
    r = client.post(f"/api/posts/{post_id}/like")
    r.raise_for_status()
    if r.status_code == 200:
        return True
    return False

def unlike_post(client, post_id: str):
    r = client.delete(f"/api/posts/{post_id}/like")
    r.raise_for_status()
    if r.status_code == 200:
        return True
    return False

def repost_post(client, post_id: str):
    r = client.post(f"/api/posts/{post_id}/repost")
    r.raise_for_status()
    return True

def get_user_posts(client, username: str, limit: int = 20, sort: str = "new"):# new | popular
    r = client.get(
        f"/api/posts/user/{username}?limit={limit}&sort={sort}"
    )
    r.raise_for_status()

    return Posts(r.json())
