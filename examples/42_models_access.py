# 42_models_access.py
# Работа с моделями как object/dict/json

from itdpy import ITDClient

client = ITDClient(refresh_token="token")

post = client.posts.get("a90b001d-c7d3-497f-ba23-bb30b03d3891")

print(post.id) # может быть  pydamic модлью 
print(post["id"]) # json
print(post.get("createdAt")) # json
print(post.to_dict()) # переводить словарь в любом месте кода 
print(post.to_json()) # переводить json в любом месте

if post.poll:
    print(post.poll["question"])
    print(post.poll.to_dict()) 

client.close()