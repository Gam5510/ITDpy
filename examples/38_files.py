# 38_files.py
# Upload / get / delete file

from itdpy import ITDClient

client = ITDClient(refresh_token="токен")

uploaded = client.files.upload(file_path="test.png")
print(uploaded.id)
print(uploaded.url)

client.files.delete(uploaded.id)

client.close()
