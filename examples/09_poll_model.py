# 09_poll_model.py
# Работа с моделью Poll

from itdpy.models import Poll

poll = Poll(
    question="Как ваши дела?",
    options=["классно", "хорошо", "нормально", "плохо"],
    multipleChoice=False,
)

print(poll.question)
print(poll.options[0].text)
print(poll.to_dict())         # полная модель
print(poll.to_request_dict()) # payload для API
