import vk_api
import getpass
import pickle

def get():
    user = vk_api.VkApi(login=input("login: "), password=getpass.getpass("password: "))

    user.auth()

    api = user.get_api()

    print("Авторизация успешна. Получение данных о подписках... ", end='')

    getted = api.users.getSubscriptions(user_id=api.users.get()[0]["id"], extended=0)

    print("Готово")

    return (getted, api)


if __name__ == "__main__":
    getted, api = get()
    users_count = getted["users"]["count"]
    groups_count = getted["groups"]["count"]

    print("Подписок на группы: %i\nПодписок на пользователей: %i" % (groups_count, users_count))

    print("Сохранение данных о подписках... ", end='')

    file = open(".data.pkl", 'wb')

    pickle.dump({
        'groups':getted["groups"]["items"],
        'users':getted["users"]["items"]
        },
        file
    )

    print("Готово")

    file.close()