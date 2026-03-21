# 47_Poll.py
# Работа с Poll и Poll Builder

from itdpy import ITDClient
from itdpy.models import PollBuilder, Poll

client = ITDClient(refresh_token="токен")

post_poll = client.posts.create(
    content="Демо пост с моделью Poll",
    poll=Poll(
        question="Выбери вариант",
        options=["A", "B", "C", "D"],
        multipleChoice=True
    ),
)

print(post_poll.id)
print(post_poll.poll.question)
print(post_poll.poll.options.to_json())

poll_builder = (
    PollBuilder("Как подавать котлеты?") # Poll Builder нужен, чтобы легко добавлять и менять и постепенно строить Poll
    .add("С пюрешкой")
    .add("Без пюрешки")
    .multiple_choice(True)
    .build()
)
# poll = PollBuilder("Как подавать котлеты?").add("С пюрешкой").add("Без пюрешки").multiple_choice(True).build() можно так 

print(poll_builder)
print(poll_builder.to_dict())
print(poll_builder.to_request_dict())

post = client.posts.create(
    content="Голосуем",
    poll=poll_builder,
)

print(post.id)
print(post.poll.question)
print(post.poll.options.to_json())

list = [1, 2, 3, 4, 5, 6, 7, 8, 9]

poll_by_list = PollBuilder("Какая цыфтра лучше всего вам подходит")

for number in list:
    poll_by_list.add(number)

poll_by_list.build() # Нужно обезательно писать чтобы построить Poll

print(poll_by_list) 
print(poll_by_list.to_dict())
print(poll_by_list.to_request_dict())

post_by_list = client.posts.create(
    content="Пример создание опроса с помощью **Poll builder**",
    poll=poll_by_list,
    parse_md=True
)
print(post_by_list.id)
print(post_by_list.poll.question)
print(client.posts.vote(post_id=post_by_list.id, option_ids=post_by_list.poll.options[0].id))

print(post_by_list.poll.options.to_json())

client.close()