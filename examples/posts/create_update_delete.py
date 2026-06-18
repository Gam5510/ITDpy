"""Example: create, update, and delete a post."""
from itdpy import ITDClient

with ITDClient(refresh_token="YOUR_REFRESH_TOKEN") as client:
    post = client.posts.create(content="Hello from ITDpy!")
    print(f"Created: {post.id}")

    updated = client.posts.update(post.id, content="Updated via ITDpy!")
    print(f"Updated at: {updated.updated_at}")

    client.posts.delete(post.id)
    print("Deleted.")
