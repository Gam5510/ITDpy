"""Example: upload a file and attach it to a post."""
from itdpy import ITDClient

with ITDClient(refresh_token="YOUR_REFRESH_TOKEN") as client:
    file = client.files.upload("/path/to/image.jpg")
    print(f"Uploaded: {file.id} -> {file.url}")

    post = client.posts.create(
        content="Check this out!",
        attachment_ids=[file.id],
    )
    print(f"Post with attachment: {post.id}")
