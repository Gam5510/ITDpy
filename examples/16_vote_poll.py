# 16_vote_poll.py
# Проголосовать в poll

from itdpy import ITDClient

client = ITDClient(refresh_token="токен")

poll = client.posts.vote(
    post_id="a7f92746-8fa0-4c89-b376-2e8e7fe3b868",
    option_ids="7c68de15-a42a-4b98-a944-6b877dd1fbce",
)

print(poll)
print(poll.get("question"))
print(poll.total_votes)
print(poll["has_voted"])
print(poll.voted_option_ids)

for option in poll.options:
    print(option.id, option.text, option.votes_count)

client.close()
