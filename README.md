# Blimp Boards Backend

![wercker status](https://app.wercker.com/status/eee8e64a497f80d5367f9012fd2aff4a "wercker status")

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
$ ./manage.py loaddata blimp/users/fixtures/users.json
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
