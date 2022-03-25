# Укорачиватель ссылок с помощь API сервиса bit.ly

Скрипт позволяет представить любой URL как короткую ссылки вида:

```
https://bit.ly/xxxxxxx
```
А также посчитать количество переходов по такой ссылке, если в качестве URL использовать короткую ссылку.

Скрипт поддерживате ссылки вида "site.domen", автоматически добавляя "http://" в начало.


## Как установить

Python3 должен быть уже установлен. Затем используйте pip (или pip3, есть конфликт с Python2) для установки зависимостей:

```
pip install -r requirements.txt
```
Не забудьте создать необходимый файл ``settings.py`` для правильной работы dotenv, документация по ссылке:
``https://pypi.org/project/python-dotenv/``

### Получите токен для работы API:

Зарегистрируйтесь на сервисе ``https://bitly.com/``
В разделе Settings вашего аккаунта перейдите на вкладку Developer settings -> API

В поле Access token введите пароль от вашей учетной записи bitly.com и нажмите Generate token

Вы получите токен вида

```
7e3396221d62eacd6704628b042a6cd726c370bf
```
Создайте файл .env в корневой папке и положите туда переменную с полученным токеном

```
BITLINK_ACCESS_TOKEN = 7e3396221d62eacd6704628b042a6cd726c370bf

```

### Свой домен (custom_domen)

При использовании своего домена custom_domain для генерация коротких ссылок (платная опция ``bit.ly``) в файл .evn нужно добавить следующие переменные:

```
CUSTOM DOMAIN = example.ru
GROUP_ID = example_group
```

``GPOUP_ID`` соответствует группе в настройках ``bit.ly`` (Account setting -> Groups) в которой подключен свой домен. Если используется только одна группа, ``GROUP_ID`` можно оставить пустым.

Подробная документация по ссылке:

https://support.bitly.com/hc/en-us/articles/4408507361165-How-do-I-change-my-default-domain-for-creating-links-

Ограничения по использованию custom_domen:

```
Keep these things in mind as you choose and set up a custom domain:
The domain for your short links must be different than your website domain.
It can't be more than 32 characters long, including the dot.
If you haven't added one yet, Bitly offers a complimentary domain. However, if you add your own domain, you won't be able to redeem this offer later.
```


### Запуск скрипта

Запуск скрипта производится командой

```
python3 main.py http://longurl.domen/xxx
```

где "http://longurl.domen/xxx" - ссылка, которую надо укоротить

## Пример использования

```
$ python3 main.py http://ya.ru
Битлинк https://bit.ly/3icwVzX

$ python3 main.py http://ya.ru
Количество кликов: 3
```

## Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков dvmn.org.

## Лицензия

Код распространяется свободно согласно MIT License
