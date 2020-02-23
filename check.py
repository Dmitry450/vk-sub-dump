from main import get
import pickle
import json

getted, api = get()

try:
    file = open(".data.pkl", 'rb')
except FileNotFoundError:
    print("Ошибка: файл дампа подписок не найден")
    raise SystemExit(1)

dumped_data = pickle.load(file)

users_count = getted["users"]["count"]
groups_count = getted["groups"]["count"]

print("Полученные данные:")
print("Подписок на группы: %i\nПодписок на пользователей: %i\n" % (groups_count, users_count))

users_count = len(dumped_data["users"])
groups_count = len(dumped_data["groups"])

print("Данные, сохраненные в файле:")
print("Подписок на группы: %i\nПодписок на пользователей: %i\n" % (groups_count, users_count))

print("Поиск различий... ", end='')

users_subscribed = []
users_unsubscribed = []
groups_subscribed = []
groups_unsubscribed = []

for el in dumped_data["users"]:
    if not el in getted["users"]["items"]:
        users_unsubscribed.append(el)

for el in dumped_data["groups"]:
    if not el in getted["groups"]["items"]:
        groups_unsubscribed.append(el)

for el in getted["users"]["items"]:
    if not el in dumped_data["users"]:
        users_subscribed.append(el)

for el in getted["groups"]["items"]:
    if not el in dumped_data["groups"]:
        groups_subscribed.append(el)

if not users_subscribed + users_unsubscribed + groups_subscribed + groups_unsubscribed:
    print("Различий не найдено")
    raise SystemExit(0)
else:
    print("Обнаружены различия")

if users_subscribed:
    print("Новых подписок на пользователей: ")
    for el in users_subscribed:
        _tmp = api.users.get(user_id=el)
        if isinstance(_tmp, list):
            _tmp = _tmp[0]
            print("\tid - %i, имя - %s %s" % (el, _tmp["first_name"], _tmp["last_name"]))
        else:
            print("\tid - %i, имя - DELETED" % el)

if users_unsubscribed:
    print("Отписок от пользователей: ")
    for el in users_unsubscribed:
        _tmp = api.users.get(user_id=el)
        if isinstance(_tmp, list):
            _tmp = _tmp[0]
            print("\tid - %i, имя - %s %s" % (el, _tmp["first_name"], _tmp["last_name"]))
        else:
            print("\tid - %i, имя - DELETED" % el)
    
if groups_subscribed:
    print("Новых подписок на сообщества: ")
    for el in groups_subscribed:
        _tmp = api.groups.getById(group_id=el)
        if isinstance(_tmp, list):
            _tmp = _tmp[0]
            print("\tid - %i, название - %s" % (el, _tmp["name"]))
        else:
            print("\tid - %i, название - DELETED" % el)

if groups_unsubscribed:
    print("Отписок от сообществ: ")
    for el in groups_unsubscribed:
        _tmp = api.groups.getById(group_id=el)
        if isinstance(_tmp, list):
            _tmp = _tmp[0]
            print("\tid - %i, название - %s" % (el, _tmp["name"]))
        else:
            print("\tid - %i, название - DELETED" % el)

print("Если среди изменений есть подозрительные, убедитесь, что ваша страница не взломана")