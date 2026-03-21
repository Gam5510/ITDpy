# 07_create_post_markdown.py
# Создать пост с markdown

from itdpy import ITDClient

client = ITDClient(refresh_token="токен")

post = client.posts.create(
    content="**Жирный** *текст* __и__ [ссылка](https://github.com/Gam5510/ITDpy) ||на|| `ITDpy`. Это тест ",
    parse_md=True,
)

print(post.id)
print(post.content)
print(post.spans)

client.close()
