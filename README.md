# Blimp Boards Backend

![wercker status](https://app.wercker.com/status/24f70b41859e7084501e7e4bf4ad3c18 "wercker status")

## Install

```
$ git clone git@github.com:GetBlimp/boards-backend.git
$ cd boards-backend/
$ pip install -r requirements.txt
```

## First time setup

```
$ ./manage.py syncdb --noinput
$ ./manage.py migrate
$ ./manage.py loaddata blimp_boards/utils/fixtures/notification_types.json
$ ./manage.py loaddata blimp_boards/users/fixtures/users.json
```

## Running web server

```
$ ./manage.py runserver_plus
```

## Running websockets server

```
$ python ws.py --debug
```

## Running tests

```
$ ./manage.py test --settings=settings.testing
```

## Running tests with tox

```
$ pip install tox
$ tox
```

## Code coverage

```
$ pip install coverage
$ coverage run --source='.' manage.py test --settings=settings.testing
$ coverage report --show-missing --omit='*migrations*'
```
