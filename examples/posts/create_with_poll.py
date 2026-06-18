"""Example: create a post with a poll."""
from itdpy import ITDClient, PollBuilder

with ITDClient(refresh_token="YOUR_REFRESH_TOKEN") as client:
    poll = (
        PollBuilder("Favourite language?")
        .add("Python")
        .add("JavaScript")
        .add("Rust")
        .build()
    )
    post = client.posts.create(content="Vote!", poll=poll)
    print(f"Created post {post.id} with poll: {post.poll.question if post.poll else 'N/A'}")
