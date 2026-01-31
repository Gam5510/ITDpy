from ..models import Comment

def create_comment(client, post_id: str, content: str, attachment_ids: list[str] | str | None = None):
    if attachment_ids is None:
        attachment_ids = []
    elif isinstance(attachment_ids, str):
        attachment_ids = [attachment_ids]

    payload = {
        "content": content,
        "attachmentIds": attachment_ids
    }

    r = client.post(
        f"/api/posts/{post_id}/comments",
        json=payload
    )

    r.raise_for_status()
    return Comment(r.json())

def reply_to_comment(client, comment_id: str, content: str, attachment_ids: list[str] | str | None = None):
    
    if attachment_ids is None:
        attachment_ids = []
    elif isinstance(attachment_ids, str):
        attachment_ids = [attachment_ids]

    payload = {
        "content": content,
        "attachmentIds": attachment_ids
    }

    r = client.post(
        f"/api/comments/{comment_id}/replies",
        json=payload
    )

    r.raise_for_status()
    return Comment(r.json())

def delete_comment(client, comment_id: str) -> bool:
    r = client.delete(f"/api/comments/{comment_id}")

    if r.status_code == 204:
        return True

    r.raise_for_status()
    return False

def like_comment(client, comment_id: str):
    r = client.post(f"/api/comments/{comment_id}/like")
    r.raise_for_status()
    if r.status_code == 200:
        return True
    return False


def unlike_comment(client, comment_id: str):
    r = client.delete(f"/api/comments/{comment_id}/like")
    r.raise_for_status()
    if r.status_code == 200:
        return True
    return False
