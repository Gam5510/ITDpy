"""Example: create a comment, reply, then delete both."""
from itdpy import ITDClient

POST_ID = "REPLACE_WITH_POST_UUID"
with ITDClient(refresh_token="YOUR_REFRESH_TOKEN") as client:
    comment = client.comments.create(POST_ID, content="Great post!")
    print(f"Created comment: {comment.id}")

    reply = client.comments.reply(comment.id, content="Thanks!")
    print(f"Created reply: {reply.id}")

    client.comments.delete(reply.id)
    client.comments.delete(comment.id)
    print("Cleaned up.")
