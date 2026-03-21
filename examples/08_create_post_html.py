# 08_create_post_html.py
# Создать пост с html
from itdpy import ITDClient


client = ITDClient(refresh_token="токен")

post = client.posts.create(
    content="<b>Жирный</b> и <i>курсив</i> <u>и</u> <a href='https://github.com/Gam5510/ITDpy'>ссылка</a> <spoiler>на</spoiler> <code>ITDpy</code>. Это тест html.",
    parse_html=True,
)

print(post.id)
print(post.content)
print(post.spans)

client.close()
