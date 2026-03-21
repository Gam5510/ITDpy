# Formatting

`itdpy` умеет автоматически преобразовывать Markdown и HTML в `content + spans`.

## Markdown

```python
post = client.posts.create(
    content="**Жирный** и `код`",
    parse_md=True,
)
```

Поддерживаются:

- `**bold**`
- `*italic*`
- `~~strike~~`
- `__underline__`
- `` `code` ``
- `||spoiler||`
- `[text](url)`

## HTML

```python
post = client.posts.create(
    content="<b>Жирный</b> <spoiler>спойлер</spoiler>",
    parse_html=True,
)
```

Поддерживаются:

- `<b>`, `<strong>`
- `<i>`, `<em>`
- `<s>`
- `<u>`
- `<code>`
- `<spoiler>`
- `<a href="...">`

Также `||spoiler||` в HTML-режиме автоматически преобразуется в spoiler span.
